import subprocess, glob, os

def ls(dir_path):
  proc = subprocess.Popen(['ls', dir_path], stdout=subprocess.PIPE)
  return proc.communicate()[0].splitlines()

def glob_(dir_path):
  return glob.glob(os.path.join(dir_path, '*.txt'))
