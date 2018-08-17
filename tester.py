import os, time, glob, subprocess, random, sys, codecs, locale, mmap

import hardcoded_list, generate_fake_data

def load_notes(dir_path, each_filename, read_file):
  start_time = time.time()
  all_data = []

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
  print '  time taken:', end_time - start_time

def ls(dir_path):
  proc = subprocess.Popen(['ls', dir_path], stdout=subprocess.PIPE)
  return proc.communicate()[0].splitlines()

def glob_(dir_path):
  return glob.glob(os.path.join(dir_path, '*.txt'))

def normal_load(path, stat):
  with open(path) as f:
    return f.read()

# mmap doesn't seem to help (or maybe I just don't understand how to use it)
def mmap_load(path, stat):
  if stat.st_size == 0:
    return ''
  else:
    with open(path) as f:
      mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
      return mm.read(stat.st_size)

def main():
  lister_funcs = [os.listdir, ls, glob_]
  random.shuffle(lister_funcs)
  for lister in lister_funcs:
    # print 'generating fake data...'
    # generate_fake_data.generate_fake_data()
    print 'lister:', lister.__name__
    load_notes(os.path.expanduser("~/Desktop/test_data"), lister, normal_load)

if __name__ == '__main__':
  main()
