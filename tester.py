import os, time, subprocess, random, json, threading, sys
from multiprocessing.pool import ThreadPool

import file_readers, file_listers, config, clear_ram_cache


def load_test_data(dir_path, each_filename, read_files):
  start_time = time.time()

  old_wd = os.getcwd()
  os.chdir(dir_path)

  try:
    text_list = read_files(each_filename(dir_path))
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
  class Reader:
    def __init__(self, name, func):
      self.name = name
      self.func = func

  true_false = [True, False]
  lister_funcs = [os.listdir, file_listers.glob_]
  readers = [
    Reader('normal_read', file_readers.normal_read),
    Reader('pool 2', file_readers.make_pooled_reader(2)),
    Reader('pool 4', file_readers.make_pooled_reader(4)),
    Reader('pool 8', file_readers.make_pooled_reader(8)),
    Reader('pool 16', file_readers.make_pooled_reader(16)),
  ]

  sort_to_lister_to_times = {}
  for i_run in range(10):
    random.shuffle(lister_funcs)
    random.shuffle(readers)
    random.shuffle(true_false)
    for should_sort in true_false:
      sort_to_lister_to_times.setdefault(should_sort, {})
      for base_lister in lister_funcs:
        sort_to_lister_to_times[should_sort].setdefault(base_lister.__name__, {})
        if should_sort:
          final_lister = lambda dir_path: sort_by_inode(base_lister(config.DIR_PATH))
        else:
          final_lister = base_lister

        for reader in readers:
          reader_to_times = sort_to_lister_to_times[should_sort][base_lister.__name__]
          reader_to_times.setdefault(reader.name, [])

          clear_ram_cache.clear_ram_cache()

          print 'i_run:', i_run, 'should_sort:', should_sort, 'lister:', base_lister.__name__, \
                'reader:', reader.name

          # Run generate_fake_data.py to create the data to load.
          time_taken = load_test_data(config.DIR_PATH, final_lister, reader.func)
          reader_to_times[reader.name].append(time_taken)

  json_str = json.dumps(sort_to_lister_to_times, indent=2)
  with open('results.json', 'w') as f:
    f.write(json_str)

if __name__ == '__main__':
  main()
