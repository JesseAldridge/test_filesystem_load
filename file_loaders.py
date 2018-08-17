
def normal_load(path):
  with open(path) as f:
    return f.read()

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
