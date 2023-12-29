from pathlib import Path
import jinja2

from jinja2.nodes import CallBlock
from jinja2.ext import Extension

from textwrap import dedent
import re
from .helpers import resolve, log

def makeExtension( meta, md ):
  setattr( makeExtension, 'meta',  meta )
  setattr( makeExtension, 'md',  md )
  return MarkdownExtension

def convert( md, txt ):
  if issubclass( type(txt), jinja2.Undefined ):
    return ''
  else:
    md.reset()
    return md.convert(txt)

class MarkdownExtension(Extension):
  tags = set(['markdown'])

  def __init__(self, environment):
    super(MarkdownExtension, self).__init__(environment)
    self.meta = getattr( makeExtension, 'meta' )
    self.md = getattr( makeExtension, 'md' )
    delattr( makeExtension, 'meta' )
    delattr( makeExtension, 'md' )

  def parse(self, parser):
    lineno = next(parser.stream).lineno
    body = parser.parse_statements(
      ('name:endmarkdown',),
      drop_needle=True
    )
    return CallBlock(
      self.call_method('convert_markdown'),
      [],
      [],
      body
    ).set_lineno(lineno)

  def build_url( self, text ):
    '''Returns a URL and label given text of a wiki link'''
    sep = text.find('|')
    if( sep >= 0 ):
      link = text[:sep]
      label = text[sep+1:]
    else:
      link = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', text)
      label = Path( text ).name
    if link[0] == '/':
      src_path = self.meta.base_dir / link[1:]
      link = self.meta.base_url + link[1:]
    else:
      src_path = self.meta.base_dir / self.meta.rel_src_dir / link
      if self.meta.absolute_links:
        resolve( 'base_dir', self.meta )
        link = self.meta.base_url + str(
            src_path.resolve().relative_to( self.meta.abs_base_dir ) )

    if not src_path.exists() or ( src_path.suffix == '.html' 
            and not src_path.with_suffix( '.md' ).exists() ):
      log.warning( f'{self.meta.src_file}: link {src_path} not found' )

    return ( link, label)


  def convert_markdown(self, caller):
    self.md.reset()
    block = self.md.convert( dedent( caller() ) )

    # Updates to meta probably won't affect template variables, so no need to
    # do them here
    #self.meta.toc = getattr( self.md, 'toc' )
    #self.meta.uses_math = getattr( self.md, 'uses_math', False )
    #self.meta.uses_codehilite = ( self.meta.content.find(
    #       'class="codehilite"' ) >= 0 )

    return block



# vim: set sw=2 :
