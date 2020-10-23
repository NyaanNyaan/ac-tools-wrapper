# STL
import subprocess
import os
import time
import argparse
import collections
import json
import sys
import io
import threading

import config as cnfg
from stream import exec_cmd, Exec
from compiling import compile_problem
import bundle

# escape sequence
from ctypes import windll, wintypes, byref

STD_OUTPUT_HANDLE = -11
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

kernel32 = windll.kernel32
hOut = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
dwMode = wintypes.DWORD()
kernel32.GetConsoleMode(hOut, byref(dwMode))
dwMode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
kernel32.SetConsoleMode(hOut, dwMode)

# filename
workspace = "C:\\Users\\denjo\\Documents\\kpr"
tmpl_path = os.path.join(workspace, 'script', 'cpp-template')
config_path = os.path.join(workspace, 'script', 'config.json')
ac_tools_config = os.path.join(workspace, 'script', 'ac-tools-config.toml')

# setting parser
parser = argparse.ArgumentParser(description='test')
parser.add_argument('cmd')
parser.add_argument('-c', '--contest', default=None, help='set contest name')
parser.add_argument('-p', '--problem', default=None, help='set problem')
parser.add_argument('-u', '--unlock-safety', action='store_true')
parser.add_argument('-d', '--debug', action='store_true')
args = parser.parse_args()

# set config
config = cnfg.set_config(workspace, config_path, args)

# set encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# prepare
if args.cmd in ['dl', 'download']:
  # set contest
  contest_id = config['contest']
  cmd = ['atcoder-tools', 'gen',
         '--workspace', workspace,
         '--template', tmpl_path,
         '--config', ac_tools_config,
         contest_id]
  exec_cmd(cmd)

# debug
elif args.cmd in ['d', 'debug']:
  if args.problem == None:
    cnfg.set_problem_id(workspace, config, config_path)
  compile_problem(config, workspace,
                  exe_path=os.path.join(workspace, 'a.exe'),
                  debug=True)

# execute
elif args.cmd in ['e', 'exec']:
  exe_path = os.path.join(workspace, 'a.exe')
  exe = Exec(exe_path)

  def read_input():
    while exe.is_running():
      s = input()
      exe.send(s)
  thread = threading.Thread(target=read_input)
  thread.daemon = True
  thread.start()

  while exe.is_running():
    for l in exe.receive_lines():
      print(l, end='', flush=True)
    time.sleep(0.05)
  time.sleep(0.05)
  for l in exe.receive_lines():
    print(l, end='', flush=True)
  print('return code : ' + str(exe.returncode()), flush=True)

# test
elif args.cmd in ['t', 'test']:
  if args.problem == None:
    cnfg.set_problem_id(workspace, config, config_path)
  # compile
  compile_problem(config, workspace, debug=args.debug)
  # test
  contest_id = config['contest']
  problem_id = config['problem']
  problem_dir = os.path.join(workspace, contest_id, problem_id)
  cmd = ['atcoder-tools', 'test', '--dir', problem_dir]
  exec_cmd(cmd)

elif args.cmd in ['b', 'bundle']:
  if args.problem == None:
    cnfg.set_problem_id(workspace, config, config_path)
  contest_id = config['contest']
  problem_id = config['problem']
  problem_dir = os.path.join(workspace, contest_id, problem_id)
  bundle.bundle(problem_dir)

elif args.cmd in ['s', 'submit']:
  if args.problem == None:
    cnfg.set_problem_id(workspace, config, config_path)
  contest_id = config['contest']
  problem_id = config['problem']
  problem_dir = os.path.join(workspace, contest_id, problem_id)
  submit_path = os.path.join(problem_dir, 'submit.cpp')
  bundle.bundle(problem_dir)
  problem_dir = os.path.join(workspace, contest_id, problem_id)
  cmd = ['atcoder-tools', 'submit', '--code', submit_path,
         '--dir', problem_dir, '--force']
  if args.unlock_safety == True:
    cmd.append('-u')
  exec_cmd(cmd)

# generate naive.cpp and gen.cpp
elif args.cmd in ['n', 'naive']:
  if args.problem == None:
    cnfg.set_problem_id(workspace, config, config_path)
  contest_id = config['contest']
  problem_id = config['problem']
  problem_dir = os.path.join(workspace, contest_id, problem_id)
  problem_url = '/'.join([
      'https://atcoder.jp/contests',
      contest_id,
      'tasks',
      contest_id + '_' + problem_id.lower()
  ])
  cmd = ['atcoder-tools', 'codegen',
         '--template', tmpl_path,
         '--config', ac_tools_config,
         problem_url]
  src = subprocess.check_output(cmd).decode('utf-8')

  # naive.cpp
  with open(os.path.join(problem_dir, 'naive.cpp'), 'w', newline="") as f:
    f.write(src)

  # gen.cpp
  src = src.replace('cin >>', 'cout << " " <<')
  with open(os.path.join(problem_dir, 'gen.cpp'), 'w', newline="") as f:
    f.write('#include "misc/rng.hpp"\r\n')
    f.write(src)

# compare
elif args.cmd in ['cmp', 'compare']:
  if args.problem == None:
    cnfg.set_problem_id(workspace, config, config_path)
  contest_id = config['contest']
  problem_id = config['problem']
  problem_dir = os.path.join(workspace, contest_id, problem_id)

  compile_problem(config,
                  workspace,
                  main_path=os.path.join(problem_dir, 'main.cpp'),
                  exe_path=os.path.join(problem_dir, 'a.exe'),
                  debug=args.debug
                  )

  compile_problem(config,
                  workspace,
                  main_path=os.path.join(problem_dir, 'naive.cpp'),
                  exe_path=os.path.join(problem_dir, 'naive.exe'),
                  debug=args.debug
                  )

  compile_problem(config,
                  workspace,
                  main_path=os.path.join(problem_dir, 'gen.cpp'),
                  exe_path=os.path.join(problem_dir, 'gen.exe'),
                  debug=args.debug
                  )
  cmd = ['oj', 'g/i',
         '-c', os.path.join(problem_dir, 'naive.exe'),
         '--hack', os.path.join(problem_dir, 'a.exe'),
         '-t', '3',
         os.path.join(problem_dir, 'gen.exe')
         ]
  exec_cmd(cmd)

else:
  parser.print_help()
