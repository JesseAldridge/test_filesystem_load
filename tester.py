import os, time, subprocess, random, json

import file_loaders, file_listers

def load_test_data(dir_path, each_filename, read_file):
  start_time = time.time()
  all_data = []

  old_wd = os.getcwd()
  os.chdir(dir_path)

  try:
    for filename in each_filename(dir_path):
      all_data.append(read_file(filename))
  finally:
    os.chdir(old_wd)

  end_time = time.time()
  return end_time - start_time

def sort_by_inode(paths):
  filename_to_stat = {}
  for filename in paths:
    filename_to_stat[filename] = os.stat(filename)
  for filename, stat in sorted(filename_to_stat.items(), key=lambda t: t[1].st_ino):
    yield filename

def main():
  lister_funcs = [os.listdir, file_listers.ls, file_listers.glob_]
  random.shuffle(lister_funcs)
  dir_path = os.path.expanduser("~/Desktop/test_data")
  sort_to_lister_to_times = {}
  for i_run in range(10):
    for should_sort in [True, False]:
      sort_to_lister_to_times.setdefault(should_sort, {})
      for base_lister in lister_funcs:
        sort_to_lister_to_times[should_sort].setdefault(base_lister.__name__, [])
        # Clears memory cache. Need to run this script with sudo to make this line work.
        subprocess.call(['purge'])
        if should_sort:
          final_lister = lambda dir_path: sort_by_inode(base_lister(dir_path))
        else:
          final_lister = base_lister
        print 'lister:', base_lister.__name__, 'should_sort:', should_sort
        # Run generate_fake_data.py to create the data to load.
        time_taken = load_test_data(dir_path, final_lister, file_loaders.normal_load)
        sort_to_lister_to_times[should_sort][base_lister.__name__].append(time_taken)

  json_str = json.dumps(sort_to_lister_to_times, indent=2)
  with open('results.json', 'w') as f:
    f.write(json_str)

if __name__ == '__main__':
  main()
