import os, random, string

dir_path = os.path.expanduser('~/Desktop/test_data')

if not os.path.exists(dir_path):
  os.mkdir(dir_path)

for i in range(10000):
  print 'i:', i
  file_path = os.path.join(dir_path, str(i)) + '.txt'
  with open(file_path, 'w') as f:
    f.write(''.join(random.choice(string.letters) for _ in range(1000)))
