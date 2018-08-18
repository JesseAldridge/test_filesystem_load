import sys, subprocess

def clear_ram_cache():
  if sys.platform == "linux" or sys.platform == "linux2":
    subprocess.call(['sync'])
    subprocess.call('echo 3 > /proc/sys/vm/drop_caches', shell=True)
  elif sys.platform == "darwin":
    # Clears memory cache. Need to run this script with sudo to make this line work.
    subprocess.call(['purge'])
  elif sys.platform == "win32":
     print 'windows'
