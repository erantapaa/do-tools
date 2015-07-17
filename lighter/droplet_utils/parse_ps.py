#
# library to parse ps tabular output
#

import re

# which columns are left justified:

LEFTIES = set(['USER', 'RUSER', 'UCOMM', 'COMMAND'])

class Column():
  def __init__(self, start, end, title, rjust=True):
    self.start = start
    self.end = end
    self.title = title
    self.rjust = rjust    # is this column right-justified

  def __str__(self):
    return "Column(start={}, end={}, rjust={}, title=\"{}\")".format(self.start, self.end, str(self.rjust), self.title)

  def extract_values(self, line, d):
    val = line[ self.start : self.end ].strip()
    d[ self.title ] = val

class ColumnPair():
  def __init__(self, col1, col2):
    self.col1 = col1
    self.col2 = col2

  def __str__(self):
    return "ColumnPair(col1={}, col2={})".format( str(self.col1), str(self.col2) )

  def extract_values(self, line, d):
    x = line.rfind(' ', self.col1.end, self.col2.start)
    if x < 0:
      x = self.col2.start
    val1 = line[ self.col1.start : x ].strip()
    val2 = line[ x : self.col2.end ].strip()
    d[ self.col1.title ] = val1
    d[ self.col2.title ] = val2

def compile_ps_line_parser(columns):
  """Returns a list of Single/DoubleValues."""
  vals = []
  start = 0
  i = 0
  while i < len(columns):
    col = columns[i]
    if col.rjust:
      vals.append( Column(start, col.end, col.title) )
      # add a Single
      start = col.end
    elif i+1 >= len(columns):
      vals.append( Column(start, -1, col.title) )
      # at end - no need to set start
    else:
      ncol = columns[i+1]
      if not ncol.rjust:
        vals.append( Column(start, ncol.start, col.title) )
        start = ncol.start
      else:
        vals.append( ColumnPair(col, ncol) )
        start = ncol.end
        i += 1
    i += 1
  return vals

def parse_ps_header(header):
  """Return a list of Columns from the first header of ps output."""
  cols = []
  for m in re.finditer('\S+', header):
    title = m.group(0)
    rjust = not (title in LEFTIES)
    cols.append( Column( start = m.start(), end = m.end(), title = title, rjust = rjust) )
  return cols

def parse_ps_line(actions, line):
  d = {}
  for a in actions:
    a.extract_values(line, d)
  return d

def parse_ps_output(columns, lines):
  """Parse ps output to a list of dictionaries."""
  actions = compile_ps_line_parser(columns)
  rows = []
  for line in lines:
    if re.search('\S', line):
      d = parse_ps_line(actions, line)
      rows.append(d)
  return rows

if __name__ == '__main__':
  from _file_util import read_file

  def test1():
    contents = read_file("ps-output-1")
    lines = contents.split('\n')
    header = lines[0]
    cols = parse_ps_header(header)
    # print "columns:"
    # for c in cols: print c
    # actions = compile_ps_line_parser(cols)
    # for a in actions: print a
    rows = parse_ps_output(cols, lines[1:])
    for r in rows: print r
    # for r in rows: print r['USER']

  test1()

