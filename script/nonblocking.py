from threading import Thread
from queue import Queue, Empty


class NonBlockingStreamReader:
  def __init__(self, stream):
    self._s = stream
    self._q = Queue()
    self.is_running = True

    def _populateQueue(stream, queue):
      try:
        for line in iter(stream.readline, b''):
          queue.put(line)
      except:
        pass
      stream.close()

    self._t = Thread(target=_populateQueue,
                     args=(self._s, self._q))
    self._t.daemon = True
    self._t.start()

  def readline(self):
    try:
      return self._q.get_nowait()
    except Empty:
      return None
