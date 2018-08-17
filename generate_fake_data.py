import os, random, string, shutil

import config

def generate_fake_data():
  shutil.rmtree(config.DIR_PATH)
  os.mkdir(config.DIR_PATH)

  for i in range(1000):
    file_path = os.path.join(config.DIR_PATH, str(i)) + '.txt'
    with open(file_path, 'w') as f:
      f.write(''.join(random.choice(string.letters) for _ in range(1000)))

if __name__ == '__main__':
  generate_fake_data()
