import time
import re
import sqlite3
import requests
import pandas as pd

db_file = "./ped.sqlite"
base_url = ""
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0"


# blood_tableテーブルを取得
pattern = r'<table[\s\S]*?class="blood_table[\s\S]*?>[\s\S]*?</table'
table_compile = re.compile(pattern)

# そのtrを取得
pattern = r'<tr[\s\S]*?>([\s\S]*?)</tr'
tr_compile = re.compile(pattern)

# そのtdのコンパイル
pattern = r'<td[\s\S]*?>([\s\S]*?)</td'
td_compile = re.compile(pattern)

# aのコンパイル urlの一部も取得
pattern = r'<a[\s\S]*?href="/horse/([^/]+?)/"[\s\S]*?>([\s\S]*?)</a>'
a_compile = re.compile(pattern)


class MyClass:
    def __init__(self, dad_id=None, dad=None, mom_id=None, mom=None, grandpa_id=None, grandpa=None):
        self.dad_id = dad_id
        self.dad = dad
        self.mom_id = mom_id
        self.mom = mom
        self.grandpa_id = grandpa_id
        self.grandpa = grandpa


def select_is_null():
    db = sqlite3.connect(db_file)
    cur = db.cursor()
    cur.execute("SELECT my_id FROM family WHERE dad_id IS NULL;")
    my_id = cur.fetchall()
    db.close()

    return my_id


def get_html(id):
    url = f"{base_url}/{id}/"
    headers = {
        "User-Agent": ua
    }

    r = None

    try:
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding
    except Exception as e:
        print(e)
        return r

    return r.text


def get_element(html):
    try:
        # table tr 取得
        table_result = table_compile.findall(html)
        tr_result = tr_compile.findall(table_result[0])

        # 父
        td_result = td_compile.findall(tr_result[0])
        dad_id, dad = a_compile.findall(td_result[0])[0]
        dad = dad.replace("\n", "").split("<br />")[0]

        # 母
        td_result = td_compile.findall(tr_result[16])
        mom_id, mom = a_compile.findall(td_result[0])[0]
        mom = mom.replace("\n", "").split("<br />")[0]

        # 母方の祖父
        grandpa_id, grandpa = a_compile.findall(td_result[1])[0]
        grandpa = grandpa.replace("\n", "").split("<br />")[0]
    except Exception as e:
        print("\n get_element", id, e)
        return MyClass()

    return MyClass(dad_id, dad, mom_id, mom, grandpa_id, grandpa)


def update_db(id, obj):
    db = sqlite3.connect(db_file)
    cur = db.cursor()

    qry = "update family set dad_id=?, dad=?, mom_id=?, mom=?, grandpa_id=?, grandpa=? where my_id=?;"
    cur.execute(qry, (obj.dad_id, obj.dad, obj.mom_id,
                      obj.mom, obj.grandpa_id, obj.grandpa, id))
    db.commit()
    db.close()


def data_set():
    body_df = pd.read_csv("../csv/body.csv")

    ids = body_df["name_id"].unique()

    db = sqlite3.connect(db_file)

    cur = db.cursor()

    cur.execute("""
CREATE TABLE "family" (
    "id"	INTEGER,
    "my_id"	TEXT UNIQUE,
    "dad_id"	TEXT,
    "dad"	TEXT,
    "mom_id"	TEXT,
    "mom"	TEXT,
    "grandpa_id"	TEXT,
    "grandpa"	TEXT,
    PRIMARY KEY("id")
);
    """)

    qry = "insert into family (id, my_id) values(?,?);"

    all = len(ids)
    i = 1
    for v in ids:
        cur.execute(qry, (i, str(v)))

        print(f"\r{i}/{all} {v}", end="")
        i += 1

    db.commit()
    db.close()

    print("\n\n終了")


def main():

    start = time.perf_counter()

    my_id = select_is_null()

    all = len(my_id)
    i = 1

    for v in my_id:
        obj = None
        html = get_html(v[0])
        if html is not None:
            obj = get_element(html)
        if obj is not None and obj.dad_id is not None:
            update_db(v[0], obj)

        print(f"\r{i}/{all} {v[0]}", end="")
        i += 1
        time.sleep(1)

    end = time.perf_counter()
    print(f"\n\n【終了】実行時間:{end-start}秒")


if __name__ == "__main__":
    # 初回のみの関数
    # data_set()
    main()
