
import tempfile
import os.path
import os
import sys
from contextlib import contextmanager

def make_stdout_unbuffered():
  sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

def delete_file(path):
  try:
    os.remove(path)
  except OSError as e:
    if e.errno != errno.ENOENT:
      raise

def read_file(path):
  with open (path) as f:
    contents = f.read()
    return contents

def read_file_or_none(path):
  """Read contents of a file. Return None if file does not exist."""
  try:
    with open (path) as f:
      contents = f.read()
      return contents
  except IOError as e:
    if e.errno != errno.ENOENT:
      raise
    return None 

def write_file(path, contents):
  with open(path, "w") as f:
    f.write(contents)

# from http://stackoverflow.com/a/25586245/866915
@contextmanager
def atomic_replace(filepath, binary=False, fsync=False):
    """ Writeable file object that atomically updates a file (using a temporary file).

    :param filepath: the file path to be opened
    :param binary: whether to open the file in a binary mode instead of textual
    :param fsync: whether to force write the file to disk
    """

    folder = os.path.dirname(filepath)
    fd, tmppath = tempfile.mkstemp(dir = folder)
    os.close(fd)
    try:
        with open(tmppath, 'wb' if binary else 'w') as file:
            yield file
            if fsync:
                file.flush()
                os.fsync(file.fileno())
        os.rename(tmppath, filepath)
    finally:
        try:
            os.remove(tmppath)
        except (IOError, OSError):
            pass

def atomic_write(path, content, binary=False, fsync=False):
  """Atomically update the contents of a file."""
  with atomic_replace(path, binary=binary, fsync=fsync) as f:
    f.write(content)



