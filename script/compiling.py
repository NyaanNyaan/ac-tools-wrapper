
import os
from stream import Exec
import time

CXX = 'g++'
CXXFLAGS = ['-I', 'C:\\Users\\denjo\\Desktop\\ABC\\library',
            '-fconstexpr-loop-limit=1048576',
            '-Wall', '-Wextra', '-Wno-unknown-pragmas', '-Wno-attributes',
            '-Wl,-stack,1073741824', '-DNyaan', '-O2']

# function for compiling
def compile_problem(config, workspace, main_path=None, exe_path=None, debug=False):
  contest_id = config['contest']
  problem_id = config['problem']
  problem_dir = os.path.join(workspace, contest_id, problem_id)
  # path of source
  if main_path == None:
    main_path = os.path.join(problem_dir, 'main.cpp')
  # .exe file
  if exe_path == None:
    exe_path = os.path.join(problem_dir, 'a.exe')
  compile_cmd = [CXX, *CXXFLAGS, main_path, '-o', exe_path]
  # debug
  if debug == True:
    compile_cmd.extend(['-DNyaanDebug', '-D_GLIBCXX_DEBUG'])
  print(' '.join(compile_cmd), flush=True)
  import subprocess
  exe = subprocess.Popen(compile_cmd)
  assert exe.wait() == 0, "compiling falied."
