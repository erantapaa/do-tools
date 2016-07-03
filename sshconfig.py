
import sys
import os.path
import re
from subprocess import call , Popen, PIPE
import collections

Droplet = collections.namedtuple("Droplet", ["host", "ip_addr", "entry" ])

class Prelude():
  def __init__(self, lines):
    self.lines = lines

  def is_droplet(self):
    return False

  def host(self):
    return None

  def ip_addr(self):
    return None

  def __str__(self):
    return "-- Prelude:\n" + "\n".join(self.lines)

class HostEntry():
  def __init__(self, lines):
    self.lines = lines

  def is_droplet(self):
    for x in self.lines:
      if re.match("^\s*# droplet", x): return True
    return False

  def host(self):
    for x in self.lines:
      m = re.match("^\s*Host\s+(\S+)", x, re.I)
      if m: return m.group(1)
    return None

  def ip_addr(self):
    for x in self.lines:
      m = re.match("^\s*HostName\s+(\S+)", x, re.I)
      if m: return m.group(1)
    return None

  def __str__(self):
    return "-- HostEntry:\n" + "\n".join(self.lines)

def find_host_by_ip(hentries, ip_addr):
  try:
    y = (i for i,h in enumerate(hentries) if h.ip_addr() == ip_addr)
    return next(y)
  except StopIteration, e:
    return -1

def add_entries(hentries, new_entries):
  for i in xrange(0, len(hentries)):
    if hentries[i].host() == "*":
      break
  else:
    i = len(hentries)
  hentries[i:0] = new_entries

# each droplet has the fields:  .ip_addr, .entry
def update_droplets(hentries, droplets):
  wanted_ips = set( [ d.ip_addr for d in droplets ] )

  # remove droplet entries not found in droplet_ips

  remove = []
  add = []
  hs = []

  for h in hentries:
    if h.is_droplet() and h.ip_addr() not in wanted_ips:
      remove.append(h)
    else:
      hs.append(h)

  for d in droplets:
    if find_host_by_ip(hs, d.ip_addr) < 0:
      add.append(d)

  # return: surviving entries, entried removed, droplets to add
  return (hs, remove, add)

def collect_stdout(cmd):
  return Popen(cmd, stdout=PIPE).communicate()[0]

def tugboat_droplets():
  """Returns an Iterable of host, ip pairs."""
  output = collect_stdout(['tugboat', 'droplets'])
  for x in output.split("\n"):
    m = re.match("([\w-]+)\s*\(ip:\s*(\d+\.\d+\.\d+\.\d+)", x)
    if m:
      host = m.group(1)
      ip = m.group(2)
      yield (host, ip)

def read_file(path):
  with open (path) as f:
    contents = f.read()
    return contents

def write_file(path, contents):
  with open(path, "w") as f:
    f.write(contents)

def read_ssh_config(path):
  lines = read_file(path).split('\n')
  c = parse_ssh_config(lines)
  return c

def parse_ssh_config(lines):
  first = True
  prelude = []
  hentries = []
  h = []
  for x in lines:
    m = re.match('\s*Host\s+(.*)', x)
    if m:
      hentries.append( h )
      h = []
    h.append(x)
  if h:
    hentries.append( h )
  if hentries:
    hentries[0] = Prelude( hentries[0] )
  for i in xrange(1, len(hentries)):
    hentries[i] = HostEntry( hentries[i] )
  return hentries

def to_config(hentries):
  return "".join( [ "".join( [ x + "\n" for x in h.lines ] ) for h in hentries ] )

def write_ssh_config(path, hentries):
  write_file(path, to_config(hentries))

