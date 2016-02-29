import glob
import multiprocessing
import os
import shutil
import sys

import urllib3

from concurrent.futures import ThreadPoolExecutor, as_completed

TEN_MB = 10 * 1024 * 1024
HUNDRED_MB = 10 * TEN_MB
pm = urllib3.PoolManager()


def get_content_size(url):
    with pm.urlopen('GET', url, preload_content=False) as url_fd:
        size = url_fd.getheader('Content-Length')
    return int(size)


def combine_parts(url):
    fname = url.split('/')[-1]
    fname = fname.split('#')[0] if '#' in fname else fname

    # Get list of all file parts
    fparts = glob.glob('fpart*')

    if not fparts:
        print 'something went terribly wrong'
        return

    # Need to sort inplace, does not return anything
    fparts.sort()

    with open(fname, 'wb') as finalFname:
        for fpart in fparts:
            with open(fpart, 'rb') as tempFname:
                shutil.copyfileobj(tempFname, finalFname, TEN_MB)
                print 'copying {0}'.format(fpart)

    for fpart in fparts:
        os.remove(fpart)

    print 'done merging'


def download_worker(url, file_start, file_end, fpart_name):
    # XXX check if url supports range
    print '{0} downloading'.format(fpart_name)

    chunk_size = file_end - file_start
    headers = {'Range': 'bytes={0}-{1}'.format(file_start, file_end)}
    with pm.urlopen('GET', url, headers=headers,
                    preload_content=False) as url_fd:
        with open(fpart_name, 'wb') as fp:
            while chunk_size > HUNDRED_MB:
                fp.write(url_fd.read(HUNDRED_MB))
                chunk_size -= HUNDRED_MB
            else:
                fp.write(url_fd.read())
            fp.flush()
    print '{0} done'.format(fpart_name)
    return True


def download_url(url):
    cpu_count = multiprocessing.cpu_count()
    remote_file_sz = get_content_size(url)
    chunk_size = remote_file_sz/cpu_count
    start = 0
    end = chunk_size

    print 'Downloading {0} {1} bytes'.format(
        url.split('/')[-1], remote_file_sz)

    with ThreadPoolExecutor(max_workers=cpu_count) as executor:
        futures_to_parts = {}

        for idx in range(cpu_count):
            if end > remote_file_sz:
                end = remote_file_sz
            fpart_name = 'fpart{0}'.format(idx)
            futures_to_parts[executor.submit(download_worker, url, start,
                                             end, fpart_name)] = fpart_name
            start = end + 1
            end += chunk_size

        for future in as_completed(futures_to_parts):
            try:
                if future.done():
                    print future.result()
            except Exception as e:
                print e
    executor.shutdown(wait=True)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage: dwnldr.py <url>'
        sys.exit(1)
    download_url(sys.argv[1])
    combine_parts(sys.argv[1])
