import glob, os, threading, time

all_data = []

def load_notes(dir_path, each_filename, read_file):
  start_time = time.time()
  old_wd = os.getcwd()
  os.chdir(dir_path)

  try:
    filename_to_stat = {}
    for filename in each_filename(dir_path):
      filename_to_stat[filename] = os.stat(filename)
    for filename, stat in sorted(filename_to_stat.items(), key=lambda t: t[1].st_ino):
    # for filename in each_filename(dir_path):
      all_data.append(read_file(filename, stat))
  finally:
    os.chdir(old_wd)

  end_time = time.time()

def normal_load(path, stat):
  with open(path) as f:
    return f.read()

start_time = time.time()

DIR_PATH = os.path.expanduser("~/Desktop/test_data")
all_paths = glob.glob(os.path.join(DIR_PATH, '*.txt'))

threads = []

def first_half(dir_path):
  for i in range(0, len(all_paths) / 2):
    yield all_paths[i]

def second_half(dir_path):
  for i in range(len(all_paths) / 2, len(all_paths)):
    yield all_paths[i]

targets = [
  lambda: load_notes(DIR_PATH, first_half, normal_load),
  lambda: load_notes(DIR_PATH, second_half, normal_load),
]

for target in targets:
  t = threading.Thread(target=target)
  t.daemon = True  # allow parent process to kill it
  t.start()
  threads.append(t)

for thread in threads:
  thread.join()

print 'total time:', time.time() - start_time
