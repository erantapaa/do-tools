#
# return information from lsof
#

from subprocess import PIPE, Popen

def grep_pids(cmd):
  """Return only process ids from an lsof call."""
  p = Popen(cmd, stdout=PIPE, close_fds=True)
  output, err = p.communicate()

  pids = []
  for line in output.split('\n'):
    if line.startswith('p'):
      pids.append( int(line[1:]) )
  return pids

def pids_listening_on(port):
  """Return a list of pids which are listening on a port."""
  return grep_pids(['lsof', '-F', '-nP', '-iTCP:{}'.format(port), '-sTCP:LISTEN' ])

def listening_pids(ports):
  """Determine which pids are listening on a list or set of ports.
     Returns a list of (port,pids) pairs."""
  if not ports:
    return []
  cmd = ['lsof', '-F', '-nP', '-sTCP:LISTEN'] + [ '-iTCP:{}'.format(p) for p in ports ]
  p = Popen(cmd, stdout=PIPE, close_fds=True)
  output, err = p.communicate()
  results = []
  pid = None
  for line in output.split('\n'):
    if line.startswith('p'):
      pid = int(line[1:])
    elif line.startswith('n'):
      x = line.rindex(':')
      port = line[ x+1: ]
      results.append( (port, pid) )
  return results

