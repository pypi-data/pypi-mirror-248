import sys, logging, re
from pathlib import Path
from types import SimpleNamespace
from copy import deepcopy

# {{{ Logging
class CallCounted:
    """Decorator to determine number of calls for a method"""

    def __init__(self,method):
        self.method=method
        self.counter=0

    def __call__(self,*args,**kwargs):
        self.counter+=1
        return self.method(*args,**kwargs)

class CustomFormatter(logging.Formatter):
  """Logging Formatter to add colors and count warning / errors"""

  if sys.stdout.isatty():
    RE='\033[0m'
    ER='\033[0;31m'
    BD='\033[0;36m'
    UL='\033[0;32m'
    IT='\033[0;33m'
  else:
    (RE, ER, BD, UL, IT) = ['']*5

  fmt = "{levelname:.1s}: {message}"
  formatters = {
    logging.INFO: logging.Formatter(UL+fmt+RE, style='{' ),
    logging.WARNING: logging.Formatter(IT+fmt+RE, style='{' ),
    logging.ERROR: logging.Formatter(ER+fmt+RE, style='{' )
  }
  default_formatter = logging.Formatter( fmt, style='{' )

  def format(self, record):
    formatter = self.formatters.get( record.levelno, self.default_formatter )
    return formatter.format(record)

# Setup logging
def init_log():
  log = logging.getLogger("md-to-html")
  log.setLevel(logging.INFO)
  ch = logging.StreamHandler()
  ch.setFormatter(CustomFormatter() )
  log.addHandler( ch )
  log.error = CallCounted( log.error )

  return log

log = init_log()
#}}}

def merge_meta( old, new ):
  '''Merge new meta data (dict or namespace) with current (namespace)'''
  d = vars( deepcopy(old) )
  new_dict = vars(new) if type(new) == SimpleNamespace else new

  # Make lists extend old value, unless first element is '__reset__'
  for k, v in new_dict.items():
    if type(v) == list:
      if len(v) >= 1  and v[0] == '__reset__':
        # Clear old value
        del v[0]
      elif k in d and type(d[k]) == list and d[k] != v:
        # Extend old value
        #print( f'k={k}, new_dict[k]={v}, d[k] = {d[k]} (len={len(d[k])})' )
        d[k].extend( [x for x in v if x not in d[k]] ) 
        new_dict[k] = d[k]

  d.update( new_dict )
  return SimpleNamespace( **d )

def resolve( attr, meta):
  '''Adds abs_{attr} to meta, pointing to resolved location of meta.{attr}'''
  if not hasattr( meta, f'abs_{attr}' ):
    setattr( meta, f'abs_{attr}', getattr( meta, attr ).resolve() )

# Helper functions
def normalize_dirs( opts, cwd ):
  '''make directories relative to cwd'''
  if 'base_dir' in opts:
    opts['base_dir'] = cwd / opts['base_dir']
  if 'dst_dir' in opts:
    opts['dst_dir'] = cwd / opts['dst_dir']


def needs_rendering( meta, src, dst ):
  return not meta.update or not dst.exists() \
      or src.stat().st_mtime > dst.stat().st_mtime

def build_url( meta, text ):
  '''Returns a URL and label given text of a wiki link'''
  sep = text.find('|')
  if( sep >= 0 ):
    link = text[:sep]
    label = text[sep+1:]
  else:
    link = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', text)
    label = Path( text ).name
  if link[0] == '/':
    src_path = meta.base_dir / link[1:]
    link = meta.base_url + link[1:]
  else:
    src_path = meta.base_dir / meta.rel_src_dir / link
    if meta.absolute_links:
      resolve( 'base_dir', meta )
      link = meta.base_url + str(
          src_path.resolve().relative_to( meta.abs_base_dir ) )

  if not src_path.exists() or ( src_path.suffix == '.html' 
          and not src_path.with_suffix( '.md' ).exists() ):
    log.warning( f'{meta.src_file}: link {src_path} not found' )

  return ( link, label)


# vim: set sw=2 :
