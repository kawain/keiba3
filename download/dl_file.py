import os
import time
import requests

urls_file = "./urls.txt"
save_dir = r"C:\Users\user\Documents\keiba_data_file\data_file"

with open(urls_file, "r", encoding="utf-8") as f:
    urls = [s.strip() for s in f.readlines()]

all = len(urls)

c = 1

for v in urls:

    print(f"{c}/{all}", v)

    file_name = f"{save_dir}/{v.split('/')[4]}.txt"

    if os.path.exists(file_name):
        print("あるのでpass")
        c += 1
        continue

    try:
        r = requests.get(v)
        r.encoding = r.apparent_encoding
        with open(file_name, mode="w", encoding="utf-8") as f:
            f.write(r.text)

    except Exception as e:
        print(v, e)

    c += 1
    time.sleep(1)


print("終了")
