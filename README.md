# map-tiles-downloader

Crawl map tiles from a specified URL and store them locally.

## Usage

```
usage: crawler.py [-h] [-l {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}] --top-latitude TOP_LATITUDE --top-longitude TOP_LONGITUDE --bottom-latitude
                  BOTTOM_LATITUDE --bottom-longitude BOTTOM_LONGITUDE --level LEVEL --url URL --target-folder TARGET_FOLDER [--parallel-tasks PARALLEL_TASKS]

options:
  -h, --help            show this help message and exit
  -l {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}, --loglevel {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
                        Set log level
  --top-latitude TOP_LATITUDE
  --top-longitude TOP_LONGITUDE
  --bottom-latitude BOTTOM_LATITUDE
  --bottom-longitude BOTTOM_LONGITUDE
  --level LEVEL
  --url URL
  --target-folder TARGET_FOLDER
  --parallel-tasks PARALLEL_TASKS
```
