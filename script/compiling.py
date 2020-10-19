
import os
from stream import Exec
import time

CXX = 'g++'
CXXFLAGS = ['-I', 'C:\\Users\\denjo\\Desktop\\ABC\\library',
            '-fconstexpr-loop-limit=1048576',
            '-Wall', '-Wextra', '-Wno-unknown-pragmas', '-Wno-attributes',
            '-Wl,-stack,1073741824', '-DNyaan', '-O2']

# function for compiling
def compile_problem(config, workspace, exe_path=None, debug=False):
  contest_id = config['contest']
  problem_id = config['problem']
  problem_dir = os.path.join(workspace, contest_id, problem_id)
  main_path = os.path.join(problem_dir, 'main.cpp')
  # .exe file
  if exe_path == None:
    exe_path = os.path.join(problem_dir, 'a.exe')
  compile_cmd = [CXX, *CXXFLAGS, main_path, '-o', exe_path]
  # debug
  if debug == True:
    compile_cmd.extend(['-DNyaanDebug', '-D_GLIBCXX_DEBUG'])
  print(' '.join(compile_cmd), flush=True)
  exe = Exec(compile_cmd)
  while exe.is_running():
    time.sleep(0.1)
    for line in exe.receive_lines():
      print(line, end='', flush=True)
  assert exe.returncode() == 0, "compiling falied."
