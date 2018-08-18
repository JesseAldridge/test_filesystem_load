import sys, time

import file_listers, file_readers

print 'sys.argv:', sys.argv

dir_path = sys.argv[1]
start_time = time.time()
paths = file_listers.glob_(dir_path)
file_readers.normal_read(paths)
print 'time taken:', time.time() - start_time
