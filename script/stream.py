from subprocess import Popen, PIPE, STDOUT
from time import sleep
from nonblocking import NonBlockingStreamReader as NBSR
import shlex
import time

# executing chlid processes with non-blocking stream
# initialize : exe = Exec(cmd,cwd)
#   cmd ... command cwd ... directory
# input      : exe.send(massage)
# read       : exe.receive()
# readlines  : exe.receive_lines()
# kill       : exe.kill()


class Exec:
  def __init__(self, cmd, cwd=None):
    self.p = Popen(
        cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=cwd, shell=True,
        bufsize=0
    )
    self.nbsr = NBSR(self.p.stdout)

  def send(self, massage):
    self.update()
    if not self.is_running():
      print("Exec is not running", flush=True)
      return
    self.p.stdin.write((massage + '\n').encode())
    self.p.stdin.flush()

  def receive(self):
    self.update()
    output = self.nbsr.readline()
    if not output:
      return None
    else:
      return output.decode()

  def receive_lines(self):
    self.update()
    while True:
      output = self.nbsr.readline()
      if output:
        yield output.decode()
      else:
        break

  def kill(self):
    self.nbsr.is_running = False
    self.p.kill()

  def returncode(self):
    return self.p.poll()

  def is_running(self):
    self.update()
    return self.p.poll() == None

  def update(self):
    if self.returncode() != None:
      self.nbsr.is_running = False

def exec_cmd(cmd, cwd=None):
  print(' '.join(cmd), flush=True)
  import subprocess
  exe = subprocess.Popen(cmd,  shell=True)
  return_code = exe.wait()
  if return_code != 0:
    print('return code :', return_code,
          ', cmd :', ' '.join(cmd)
          )
  '''
  exe = Exec(cmd, cwd)
  while exe.is_running():
    for line in exe.receive_lines():
      print(line, end='', flush=True)
    time.sleep(0.01)
  '''
