import json

def main():
  with open('results.json') as f:
    json_text = f.read()
  sort_to_lister_to_reader_to_times = json.loads(json_text)

  reader_to_means = {}
  config_to_mean = {}
  for should_sort, lister_to_reader_to_times in sort_to_lister_to_reader_to_times.iteritems():
    for lister_name, reader_to_times in lister_to_reader_to_times.iteritems():
      for reader_name, times in reader_to_times.iteritems():
        mean_time = mean(times)
        print '{}, {}, {}, {}'.format(mean_time, should_sort, lister_name, reader_name)
        reader_to_means.setdefault(reader_name, [])
        reader_to_means[reader_name].append(mean_time)
        config_to_mean[(should_sort, lister_name, reader_name)] = mean_time

  print 'concurrent reads:', mean(reader_to_means['concurrent_read'])
  print 'synchronous reads:', mean(reader_to_means['normal_read'])

  print 'sorted by mean time:'
  for config, mean_time in sorted(config_to_mean.items(), key=lambda t: t[1]):
    print mean_time, config

def mean(list_):
  return sum(list_) / len(list_)

if __name__ == '__main__':
  main()
