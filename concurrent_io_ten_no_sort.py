import glob, os, threading, time

all_data = []

def load_notes(dir_path, each_filename, read_file):
  start_time = time.time()
  old_wd = os.getcwd()
  os.chdir(dir_path)

  try:
    for filename in each_filename(dir_path):
      all_data.append(read_file(filename))
  finally:
    os.chdir(old_wd)

  end_time = time.time()
  print '  time taken:', end_time - start_time
  print '  files loaded:', len(all_data)

def normal_load(path):
  with open(path) as f:
    return f.read()

start_time = time.time()

for i in range(10):
  threads = []
  def make_loader(i):
    def globber(dir_path):
      return glob.glob(os.path.join(dir_path, '{}*.txt'.format(i)))

    return load_notes(os.path.expanduser("~/Desktop/test_data"), globber, normal_load)

  t = threading.Thread(target=make_loader(i))
  t.daemon = True  # allow parent process to kill it
  t.start()
  threads.append(t)

for thread in threads:
  thread.join()

print 'total time:', time.time() - start_time
