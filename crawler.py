import argparse
import asyncio
import logging
import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse

import aiofiles
import aiohttp
from tqdm.asyncio import tqdm_asyncio
from tqdm.contrib.logging import logging_redirect_tqdm


class CrawlerArgs(argparse.Namespace):
    top_latitude: float
    top_longitude: float
    bottom_latitude: float
    bottom_longitude: float
    level: int
    url: str
    target_folder: str
    parallel_tasks: int

@dataclass
class Tile:
    x: int
    y: int
    z: int

async def worker(queue: asyncio.Queue, progress: Optional[tqdm_asyncio] = None):
    while True:
        task_coro = await queue.get()
        try:
            await task_coro
        except Exception as e:
            logging.error(f"Error in task: {e}")
        finally:
            queue.task_done()

            if progress:
                progress.update(1)

class Crawler:
    def __init__(self):
        self.tile_size = 256
        self.path_template = "{z}/{x}/{y}"

    async def download_tile(self, session: aiohttp.ClientSession, source, target):
        logging.debug(f"Downloading {source} to {target}")
        dirname = os.path.dirname(target)
        os.makedirs(dirname, exist_ok=True)
        async with session.get(source) as resp:
            if resp.status == 200:
                async with aiofiles.open(target, mode='wb') as f:
                    await f.write(await resp.read())
                    logging.info(f"Downloaded {source} to {target}")
            else:
                raise Exception(f"{source} returned status {resp.status}")

    def find_tile(self, latitude, longitude, level) -> Tile:
        sin_latitude = math.sin(latitude * math.pi / 180)
        pixel_x = ((longitude + 180) / 360) * self.tile_size * (2 ** level)
        pixel_y = (0.5 - math.log((1 + sin_latitude) / (1 - sin_latitude)) / (4 * math.pi)) * self.tile_size * (2 ** level)
        
        return Tile(
            x=int(pixel_x / self.tile_size),
            y=int(pixel_y / self.tile_size),
            z=level
        )

    def replace_path_tile(self, path: str, tile: Tile):
        return path.format(x=tile.x, y=tile.y, z=tile.z)

    async def crawl_box(self, session, bounding_box: Tuple[Tile, Tile], url: str, folder, num_workers: int):
        queue = asyncio.Queue()

        for x in range(bounding_box[0].x, bounding_box[1].x + 1):
            for y in range(bounding_box[0].y, bounding_box[1].y + 1):
                tile = Tile(x=x, y=y, z=bounding_box[0].z)
                source = self.replace_path_tile(url, tile)
                parsed_url = urlparse(url)
                path = Path(parsed_url.path)
                target = f"{folder}/{self.replace_path_tile(self.path_template, tile)}{path.suffix}"

                await queue.put(self.download_tile(session, source, target))

        progress = tqdm_asyncio(total=queue.qsize(), desc="Downloading tiles")

        with logging_redirect_tqdm(tqdm_class=tqdm_asyncio):
            # start worker coroutines
            workers = [asyncio.create_task(worker(queue, progress)) for _ in range(num_workers)]
            
            # wait for all tasks to be completed
            await queue.join()

            # cancel all worker coroutines after the queue is empty
            for worker_task in workers:
                worker_task.cancel()

        progress.close()

    async def crawl(self, args: CrawlerArgs):
        top_left_tile = self.find_tile(args.top_latitude, args.top_longitude, args.level)
        bottom_right_tile = self.find_tile(args.bottom_latitude, args.bottom_longitude, args.level)

        connector = aiohttp.TCPConnector(limit=0)
        async with aiohttp.ClientSession(connector=connector) as session:
            await self.crawl_box(session, (top_left_tile, bottom_right_tile), args.url, args.target_folder, args.parallel_tasks)

def parse_arguments() -> CrawlerArgs:
    parser = argparse.ArgumentParser(description="Crawl map tiles from a specified URL and store them locally.")
    parser.add_argument('-l', '--loglevel', help='Set log level', choices=logging._nameToLevel.keys(), default='INFO')
    parser.add_argument('--top-latitude', type=float, required=True)
    parser.add_argument('--top-longitude', type=float, required=True)
    parser.add_argument('--bottom-latitude', type=float, required=True)
    parser.add_argument('--bottom-longitude', type=float, required=True)
    parser.add_argument('--level', type=int, required=True)
    parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--target-folder', type=str, required=True)
    parser.add_argument('--parallel-tasks', type=int, default=10)

    return parser.parse_args(namespace=CrawlerArgs())

def main():
    args = parse_arguments()
    logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    crawler = Crawler()
    asyncio.run(crawler.crawl(args))

if __name__ == "__main__":
    main()
