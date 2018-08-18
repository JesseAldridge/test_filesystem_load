#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <glob.h>
#include <errno.h>

int globerr(const char *path, int eerrno) {
  // printf(stderr, "%s: %s\n", path, strerror(eerrno));
  return 0; /* let glob() keep going */
}

int main(int argc, char *argv[]) {
  int glob_flags = 0;
  char *dir_path = argv[1];
  glob_t results;

  glob(dir_path, glob_flags, globerr, & results);

  char* all_contents[results.gl_pathc];

  int file_counter = 0;
  for (int i = 0; i < results.gl_pathc; i++) {
    char *file_path = results.gl_pathv[i];

    struct stat statbuf;
    stat(file_path, &statbuf);
    int f_len = statbuf.st_size;

    char buff[f_len];
    int fd = open(file_path, O_RDONLY);
    read(fd, buff, f_len);
    close(fd);

    all_contents[i] = buff;
    file_counter++;
  }

  printf("loaded %i files", file_counter);
}
