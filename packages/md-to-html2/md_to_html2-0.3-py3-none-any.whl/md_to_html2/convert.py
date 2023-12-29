# Copyright 2023, Gautam Iyer. MIT Licence

import time, re
from html import escape
from pathlib import Path
from types import SimpleNamespace
from markupsafe import Markup

# May need installation
import markdown, frontmatter, yaml
import markdown.extensions.toc as toc
import jinja2

from .helpers import *
from . import mdx, j2x

class Converter:
  globals = SimpleNamespace()

  def __init__( self, globals={}, config_dirs=[] ):
    self.globals = merge_meta( self.globals, globals )

    config_dirs.insert( 0, Path(__file__).parent )
    self.template_dirs = [ d / 'templates'  for d in config_dirs]

    for d in config_dirs:
      cfgfile =  d / 'config.yaml'
      self.globals = self.read_config_file( cfgfile, self.globals )

  def read_config_file( self, cfgfile:Path, meta=None, allow_exec=False,
      ignore_errors=True ):
    '''
    Merges new values from the config and meta, and returns the result
    '''
    if meta == None: meta = self.globals
    try:
      with cfgfile.open() as f:
        opts = yaml.load( f, Loader=yaml.CLoader )
        if allow_exec == False and 'exec' in opts:
          del opts['exec']

      normalize_dirs( opts, cfgfile.parent )
      return merge_meta( meta, opts )
    except FileNotFoundError:
      if ignore_errors==False:
        log.warning( f"Couldn't find {cfgfile}" )
      return meta


  def read_frontmatter( self, src:Path, dir_config=None ):
    """
    Read frontmatter from src, and return the metadata.
    Content is in meta.content
    """
    fm = frontmatter.load( src )

    src_dir = src.parent
    normalize_dirs( fm, src_dir )

    meta = self.read_config_file( src_dir / 'config.yaml' ) \
        if dir_config is None else dir_config
    meta = merge_meta( meta, fm.metadata )
    meta.content = fm.content

    # Put the destination file name in dst_filename
    meta.src_file = src
    if not hasattr( meta, 'base_dir' ): meta.base_dir = src_dir
    if meta.absolute_links: resolve( 'base_dir', meta )

    if not hasattr( meta, 'dst_dir' ): meta.dst_dir = meta.base_dir
    try:
      meta.rel_src_dir = src_dir.relative_to( meta.base_dir )
    except ValueError:
      # Normalize and try again
      resolve( 'base_dir', meta )
      meta.rel_src_dir = src_dir.resolve().relative_to( meta.abs_base_dir )

    if hasattr( meta, 'dst_file' ):
      meta.rel_dst_file = Path(meta.dst_file)
    else:
      meta.rel_dst_file = meta.rel_src_dir / src.with_suffix( '.html' ).name
    meta.dst_file = meta.dst_dir / meta.rel_dst_file

    if not meta.standalone and not hasattr( meta, 'shared_prefix' ):
      if meta.base_url != '':
        meta.shared_prefix = meta.base_url + meta.shared_dir
      else:
        meta.shared_prefix = Path( meta.shared_dir )
        p = meta.rel_dst_file.parent
        while p != Path('.'):
          meta.shared_prefix = '..' / meta.shared_prefix
          p = p.parent

    return merge_meta( self.globals, meta )

  def convert( self, src:Path, meta=None, dir_config=None ):
    '''
    Convert src into html by applying a Jinja2 template. All metadata in meta
    is passed to the Jinja2 environment. If meta is not provided, it is got
    from read_frontmatter().

    Returns name of the file rendered, and the directory for shared files (if
    it is not standalone)
    '''

    start = time.monotonic()
    #log.debug( f'Rendering {str(src)}...' )

    if meta is None: meta=self.read_frontmatter( src, dir_config )
    if not needs_rendering( meta, meta.src_file, meta.dst_file ):
      #log.debug( f'{src} newer than '
      #    f'{meta.dst_dir.name / meta.rel_dst_file}, skipping. '
      #    f'({(time.monotonic() - start)*1000:.0f}ms)' )
      return meta.dst_file, None if meta.standalone else meta.dst_dir 

    # Initialize markdown converter
    extensions = [
        'extra',
        'sane_lists',
        'smarty',
        toc.makeExtension(toc_depth=meta.toc_depth),
        mdx.LinkExtension(html_class=None,
            build_url=lambda text, *_: build_url( meta, text ) ),
        mdx.DelExtension(),
      ]
    if meta.enable_codehilite:
      extensions.append( 'codehilite' )
    if meta.enable_mathjax:
      extensions.append( mdx.MathExtension(enable_dollar_delimiter=True) )

    md = markdown.Markdown( extensions=extensions )
    #self.md.reset()

    # Initialize Jinja2 environment.
    env = jinja2.Environment(
      autoescape=jinja2.select_autoescape(),
      extensions=[j2x.makeExtension(meta, md) ],
      loader = jinja2.FileSystemLoader(
        [src.parent, src.parent/'templates', *self.template_dirs],
        followlinks=True )
    )
    env.filters['markdown'] = lambda txt: Markup( j2x.convert( md, txt ) )

    # Run metadata through Jinja2 if enabled.
    if meta.enable_jinja and meta.jinja_prefix != '':
      # Handle meta.content specially.
      meta.content = meta.jinja_prefix + meta.jinja_header + meta.content

      vm = vars(meta)
      for k, v in vm.items():
        if type(v) == str and k != 'jinja_prefix' \
            and v.startswith(meta.jinja_prefix):
          v = env.from_string(
              v.removeprefix(meta.jinja_prefix)).render( vm )
          setattr( meta, k, v )

    # Get title if needed
    if not hasattr( meta, 'title' ):
      m = re.search( r'^#\s+(.+?)\s+$', meta.content, re.M )
      if m is not None:
        meta.title = escape( m[1] )

    # Convert content to markdown, and update template variables
    meta.content = md.convert( meta.content )
    meta.toc = getattr( md, 'toc' )

    meta.uses_math = getattr( md, 'uses_math', False )
    meta.uses_codehilite = (meta.content.find( 'class="codehilite"' ) >= 0 )

    # Render the HTML
    tn = Path(meta.template).with_suffix('.j2')
    template = env.get_template( str(tn) )

    meta.dst_file.parent.mkdir( parents=True, exist_ok=True )
    template.stream( vars(meta) ).dump( str(meta.dst_file), meta.encoding )


    #log.debug( f'dst_file={meta.dst_file.resolve()}' )
    log.info( f'{src} → {meta.dst_dir.name / meta.rel_dst_file} '
        f'({(time.monotonic() - start)*1000:.0f}ms)' )
    return meta.dst_file, None if meta.standalone else meta.dst_dir 

  def create_shared_files(self, dirname ):
    # No markdown processed in shared files
    env = jinja2.Environment(
      autoescape=jinja2.select_autoescape(),
      loader = jinja2.FileSystemLoader(
          [self.globals.base_dir, *self.template_dirs]
            if hasattr( self.globals, 'base_dir' ) else self.template_dirs,
          followlinks=True )
    )
    shared_dir = dirname / self.globals.shared_dir
    shared_dir.mkdir( parents=True, exist_ok=True )

    for f in ['themeswitch.js', 'mathjax-config.js', 'styles.css']:
      dst = shared_dir / f
      template = env.get_template( 'shared/' + f )
      #log.debug( f'{vars(template)}' )
      if needs_rendering( self.globals, Path(str(template.filename)), dst ):
        template.stream( vars(self.globals) ).dump(
            str(dst), self.globals.encoding )
        log.info( f'Created shared file {dst}' )

# vim: set sw=2 :
