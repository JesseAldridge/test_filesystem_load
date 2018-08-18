package main

import(
  "fmt"
  "time"
  "path/filepath"
  "os/user"
  "os/exec"
)

func load_notes(dir_path string) {
  type Index struct {
    basename_to_content, basename_to_content_lower map[string]string
  }

  index := Index{map[string]string{}, map[string]string{}}

  glob_path := filepath.Join(dir_path, "*.txt")

  paths, _ := filepath.Glob(glob_path)

  for _, path := range paths {
    fmt.Println(path)
    start_time := time.Now()

    basename := filepath.Base(path)

    fmt.Println("Hello, 世界", start_time, basename)


    // basename = os.path.splitext(os.path.basename(path))[0]
    // with open(path) as f:
    //   index.basename_to_content[basename] = f.read()
    // index.basename_to_content_lower[basename] = index.basename_to_content[basename].lower()
    // end_time = time.time()
    // delta = end_time - start_time
    // path_to_load_time[path] = delta
  }


  // filepath.Glob

  // basename_to_content["test"] = "foo bar"



  fmt.Println("Hello, 世界", index)
}

func main() {
  usr, _ := user.Current()
  load_notes(filepath.Join(usr.HomeDir, "test_filesystem_load_data"))
}
