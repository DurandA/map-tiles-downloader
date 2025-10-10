# map-tiles-downloader

Download map tiles from any tile server for a specific bounding box (geographic area).

## Quick Start

**With uv (dependencies installed automatically):**
```bash
uv run crawler.py \
  --top-latitude 47.5 \
  --top-longitude 7.5 \
  --bottom-latitude 47.0 \
  --bottom-longitude 8.0 \
  --level 12 \
  --url "https://tile.openstreetmap.org/{z}/{x}/{y}.png" \
  --target-folder ./tiles
```

**Without uv:**
```bash
pip install aiohttp aiofiles tqdm

python crawler.py \
  --top-latitude 47.5 \
  --top-longitude 7.5 \
  --bottom-latitude 47.0 \
  --bottom-longitude 8.0 \
  --level 12 \
  --url "https://tile.openstreetmap.org/{z}/{x}/{y}.png" \
  --target-folder ./tiles
```

## Usage

```
usage: crawler.py [-h]
                  [-l {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
                  --top-latitude TOP_LATITUDE --top-longitude TOP_LONGITUDE
                  --bottom-latitude BOTTOM_LATITUDE --bottom-longitude
                  BOTTOM_LONGITUDE --level LEVEL --url URL --target-folder
                  TARGET_FOLDER [--parallel-tasks PARALLEL_TASKS]

Crawl map tiles from a specified URL and store them locally.

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
