import subprocess
import sys
import re
import io
import os

def bundle(dir):
  library_path = 'C:\\Users\\denjo\\Desktop\\ABC\\library'
  main_path = os.path.join(dir, 'main.cpp')
  buffer = os.path.join(dir, 'buf.cpp')
  submit_path = os.path.join(dir, 'submit.cpp')

  buf = open(buffer, mode='w', encoding='utf-8')
  with open(main_path, mode='r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
      buf.write(line)
      if len(line) > 8 and line[:8] == '#include':
        buf.write('\n')
  buf.close()

  with open(submit_path, 'w') as f:
    import datetime
    nw = datetime.datetime.now()
    f.write('/**\n')
    f.write(' *  date : ' + nw.strftime('%Y-%m-%d %H:%M:%S') + '\n')
    f.write(' */' + '\n')
    f.write('\n')
    cmd = ['oj-bundle', '-I', library_path, buffer]
    src = subprocess.check_output(cmd).decode('utf-8')
    lines = src.split('\n')
    for line in lines:
      if not re.match('^#line', line):
        f.write(line)
