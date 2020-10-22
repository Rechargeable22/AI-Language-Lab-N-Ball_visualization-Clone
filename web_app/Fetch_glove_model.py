import os, sys, time
import shutil
import urllib.request
import zipfile


def _reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                     (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def fetch_glove() -> None:
    """Fetches 50D-glove model and stores it under ./res/glove.6B.50d.txt
        Does return immediately if file already exits"""
    if not os.path.exists("res/glove.6B.50D.txt"):
        if not os.path.exists("res/glove.zip"):
            urllib.request.urlretrieve("http://nlp.stanford.edu/data/glove.6B.zip", "res/glove.zip", _reporthook)

        with zipfile.ZipFile("res/glove.zip") as zip_file:
            for member in zip_file.namelist():
                filename = os.path.basename(member)
                # skip directories
                if not filename:
                    continue

                # copy file (taken from zipfile's extract)
                if member.endswith('6B.50d.txt'):
                    source = zip_file.open(member)
                    target = open(os.path.join("res", filename), "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)

if __name__ == '__main__':
    fetch_glove()