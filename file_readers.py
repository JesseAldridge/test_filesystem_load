import glob
from multiprocessing import pool

def normal_read(paths):
  text_list = []
  for path in paths:
    with open(path) as f:
      text = f.read()
    text_list.append(text)
  return text_list

def concurrent_read(paths):
  def read_file(path):
    with open(path) as f:
      text = f.read()
    text_list.append(text)

  text_list = []
  pool_ = pool.ThreadPool(2)
  for path in paths:
    pool_.apply_async(read_file, (path,))
  pool_.close()
  pool_.join()
  return text_list

# mmap doesn't help (or maybe I just don't understand how to use it)
# apparently normal read is faster than mmap on macOS
# https://github.com/ggreer/the_silver_searcher/blob/e2bb8d4997c5bdf0c52862b1c17dbc2bf6d1c1cf/src/options.c#L153
def mmap_load(path, stat):
  if stat.st_size == 0:
    return ''
  else:
    with open(path) as f:
      mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
      return mm.read(stat.st_size)

if __name__ == '__main__':
  def test():
    python_files = glob.glob('*.py')

    text_list = normal_read(python_files)
    print 'loaded:', len(text_list)
    assert len(text_list) == len(python_files)

    text_list = concurrent_read(python_files)
    print 'loaded:', len(text_list)
    assert len(text_list) == len(python_files)
  test()
