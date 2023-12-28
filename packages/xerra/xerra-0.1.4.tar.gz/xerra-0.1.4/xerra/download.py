import concurrent
import json
import tempfile
from pathlib import Path

import aiohttp
import asyncio
import os

import cv2
from loguru import logger
from mhdwriter.args import WriteArgs
from mhdwriter.writer import write_mhd_raw
from tqdm import tqdm


def handle_cft_download(url: str):
    logger.info(f"Downloading cft dataset from '{url}'")
    token_url = parse_token(url)
    json_result = asyncio.run(download_single(token_url))
    result_dict = json.loads(json_result)
    write_args = WriteArgs(
        fov=result_dict["fov"],
        protocol=result_dict["protocol"],
        study_description=result_dict["study_description"],
        series_description=result_dict["series_description"],
        downsample_factor=int(result_dict["downsample_factor"]),
        date_time=result_dict["study_date"],
        skip_files=False,
    )
    if "RGB" in result_dict["series_description"]:
        write_args.is_rgb = True
    if len(result_dict["urls"]) == 0:
        logger.error(f"No files found for study.")
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        logger.info(f"Found {len(result_dict['urls'])} files to download")
        logger.info(f"Downloading to temp dir {temp_dir}")
        file_len = 0
        retry_count = 3
        file_list = []
        while len(file_list) < len(result_dict["urls"]) and retry_count > 0:
            asyncio.run(download_urls(result_dict["urls"], temp_dir))
            file_list = list(Path(temp_dir).glob("*"))
            retry_count -= 1

        if len(file_list) != len(result_dict["urls"]):
            logger.error(f"Failed to download all files. Only got {file_len}/{len(result_dict['urls'])}")
            return
        if str(file_list[0]).endswith(".jp2"):
            logger.info(f"Found jp2 files to extract")
            with tqdm(total=len(file_list)) as progress_bar:
                progress_bar.set_description(f"Extracting jp2 files")
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    futures = [executor.submit(convert_jp2, str(task)) for task in file_list]
                    for _ in concurrent.futures.as_completed(futures):
                        progress_bar.update(1)

        curr_dir = os.getcwd()
        logger.info(f"Writing raw file")

        write_mhd_raw(
            Path(temp_dir),
            write_args,
            Path(curr_dir)
        )
        logger.info(f"Wrote file to output path: {curr_dir}")


def parse_token(url_string: str):
    logger.info(f"Downloading cft dataset from '{url_string}'")
    token_args = url_string.split("_")
    base_url = asyncio.run(expand_url(token_args[0]))
    token_url = f"{base_url}/exports/{_expand_uid(token_args[1])}/{_expand_uid(token_args[2])}"
    return token_url


def _expand_uid(suid):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet_hash = {char: index for index, char in enumerate(alphabet)}
    base = len(alphabet)
    num = 0
    for i, char in enumerate(reversed(suid)):
        num += alphabet_hash[char] * (base ** i)
    hex_str = format(num, '032x')
    return '-'.join([hex_str[0:8], hex_str[8:12], hex_str[12:16], hex_str[16:20], hex_str[20:32]])


async def download_file(session, url, destination, progress_bar, retries=3):
    progress_bar.set_description(f"Downloading {os.path.basename(destination)}")
    try:
        async with session.get(url) as response:
            if response.status == 200:
                with open(destination, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                    progress_bar.update(1)  # Update the progress bar
    except aiohttp.ClientError as e:
        if retries > 0:
            await asyncio.sleep(1)  # Wait a bit before retrying
            await download_file(session, url, destination, progress_bar, retries - 1)
        else:
            raise e


async def download_urls(urls, dest_folder):
    async with aiohttp.ClientSession() as session:
        with tqdm(total=len(urls)) as progress_bar:
            tasks = []
            for url in urls:
                clean_url = url.split('?')[0]
                filename = os.path.basename(clean_url)
                destination = os.path.join(dest_folder, filename)
                task = asyncio.create_task(download_file(session, url, destination, progress_bar))
                tasks.append(task)

            # Await all tasks
            await asyncio.gather(*tasks)


async def download_single(url):
    async with aiohttp.ClientSession() as session:
        return await fetch(session, url)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def expand_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://tinyurl.com/" + url) as response:
            return response.url


def convert_jp2(jp2_filename: str):
    image = cv2.imread(jp2_filename, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError("Could not load the JP2 image. Make sure the file exists and your OpenCV installation "
                         "supports JPEG 2000.")
    tiff_filename = jp2_filename.replace(".jp2", ".tiff")
    cv2.imwrite(tiff_filename, image)
    os.remove(jp2_filename)
