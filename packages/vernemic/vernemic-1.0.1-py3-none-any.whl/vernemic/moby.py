from contextlib import contextmanager
import os
import logging as lg


URL = 'https://web.archive.org/web/20170930060409/http://www.dcs.shef.ac.uk/research/ilash/Moby/moby.tar.Z'

def show_transfer_status(total) :
  # import sys
  from tqdm import tqdm

  with tqdm(total, unit='B') as pbar :
  
    def status (dt, dd, ut, uu) :
      pbar.update(dd - pbar.n)

    yield status

def download_at(path) :
  import pycurl

  filename = sanitize_path_dot_Z(path)
  ensure_parent_path(filename)

  lg.debug(f'download_at: filename:{filename}')

  with open(filename, 'wb') as Z :
    c = pycurl.Curl()
    c.setopt(c.URL, URL)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.WRITEDATA, Z)
    c.setopt(c.NOPROGRESS, False)

    c.perform()
    c.close()

  return filename

def ensure_parent_path(filename) :
  from pathlib import Path

  Path(filename).parent.mkdir(
    parents=True, exist_ok=True
  )

def sanitize_path_dot_Z(path) :
  from pathlib import Path

  _name = URL.rsplit("/", 1)[-1]

  path = Path(path)
  if path.suffixes != Path(_name).suffixes :
    path /= _name

  return str(path)

@contextmanager
def cd(dirname) :
  saved = os.getcwd()
  os.chdir(os.path.expanduser(dirname))
  try : yield
  finally: os.chdir(saved)

def decompress(filename) :
  from pathlib import Path

  dirname = Path(filename).parent
  basename = Path(filename).name
  cmd = f'tar -xzf {basename}'

  lg.debug(f'dirname: {dirname}')
  lg.debug(f'cmd: {cmd}')

  with cd(dirname) :
    with os.popen(cmd) as F :
      pass

  if not (dirname / 'Moby').is_dir() :
    raise RuntimeError('Error decompressing Moby.')

  return str(dirname / 'Moby')

def get(location='~/.moby') :
  from pathlib import Path
  location = Path(location).expanduser().resolve()
  mobydir = location / 'Moby'

  if not mobydir.is_dir() :
    mobydir = decompress(download_at(location))

  return Moby(mobydir)

class Moby :
  def __init__(self, root) :
    self.root = root

  @property
  def names(self) :
    from pathlib import Path

    names = Path(self.root) / 'mwords/21986na.mes'

    with names.open('rb') as F :
      data = F.read()

    # filter nonascii
    # map to lowercase ascii
    nonempty = lambda x: not not x
    def lcascii (bs):
      s = None
      try :
        s = bs.decode('ascii').lower()
      except UnicodeError :
        pass

      return s

    words = filter(
      nonempty, map(lcascii, data.split(b'\r\n'))
    )

    return list(words)

if __name__ == '__main__' :
  from tempfile import mkdtemp

  lg.basicConfig(
    level=lg.DEBUG,
    format='%(levelname)-8s: %(message)s'
  )

  moby = get()
  # moby = Moby(decompress('/tmp/tmp7mx3pbxw/moby.tar.Z'))
  lg.info('#moby.names: %s', len(moby.names))
  lg.info('john in moby.names: %s',
          'john' in moby.names)

