import os, time, glob, subprocess, random, sys, codecs, locale

def load_notes(dir_path, each_filename):
  start_time = time.time()
  all_data = []

  old_wd = os.getcwd()
  os.chdir(dir_path)

  try:
    filename_to_stat = {}
    for filename in each_filename():
      filename_to_stat[filename] = os.stat(filename)
    for filename, stat in sorted(filename_to_stat.items(), key=lambda t: t[1].st_ino):
    # for filename in each_filename(dir_path):
      if stat.st_size > 0:
        with open(filename) as f:
          all_data.append(f.read(1))
      else:
        all_data.append('')
  finally:
    os.chdir(old_wd)

  end_time = time.time()
  print '  time taken:', end_time - start_time

def each_filename():
  return sys.stdin.read().splitlines()

load_notes(os.path.expanduser("~/Desktop/test_data"), each_filename)
