# 馬と騎手のurlのidを取得
# 馬の場合後で血統調査用
import os
import re
import csv
import time

path = r"C:\Users\user\Documents\keiba_data_file\data_file"
# path = "./data_test"
head_csv = "./head.csv"
body_csv = "./body.csv"

# 正規表現コンパイル

# date racecourse event_date
pattern = r'class="smalltxt">(\d+?年\d+?月\d+?日)[\s\S]*?回([\s\S]+?)(\d+?)日[\s\S]*?<'
race_date_compile = re.compile(pattern)

# race_number
pattern = r'"data_intro">[\s\S]*?<dt>[\s\S]*?(\d?\d)[\s\S]*?<'
race_number_compile = re.compile(pattern)

# race_name
pattern = r'"data_intro">[\s\S]*?<h1>([\s\S]*?)<'
race_name_compile = re.compile(pattern)

# types distance weather state
pattern = r'"data_intro">[\s\S]*?<diary_snap_cut>[\s\S]*?<span>([\s\S]+?)(\d+?)m[\s\S]+?天候 : ([\s\S]+?)&[\s\S]+? : ([\s\S]+?)&[\s\S]*?<'
race_state_compile = re.compile(pattern)

# race_table_01テーブルを取得
pattern = r'<table class="race_table_01[\s\S]*?>([\s\S]+?)</table'
table_compile = re.compile(pattern)

# そのtrを取得
pattern = r'<tr[\s\S]*?>([\s\S]*?)</tr'
tr_compile = re.compile(pattern)

# そのtdのコンパイル
pattern = r'<td[\s\S]*?>([\s\S]*?)</td'
td_compile = re.compile(pattern)

# aのコンパイル urlの一部も取得
pattern = r'<a[\s\S]*?href="/[\s\S]*?/(\d*?)/"[\s\S]*?>([\s\S]*?)</a'
a_compile = re.compile(pattern)

# spanのコンパイル
pattern = r'<span[\s\S]*?>([\s\S]*?)</span'
span_compile = re.compile(pattern)

# 調教師のコンパイル
pattern = r'[\s\S]*?\[([\s\S]*?)\][\s\S]*?<a[\s\S]*?>([\s\S]*?)<'
trainer_compile = re.compile(pattern)

# 馬連のコンパイル
pattern = r'class="pay_table_01"[\s\S]*?馬連[\s\S]*?<td>[\s\S]*?</td>[\s\S]*?<td class="txt_r">([\s\S]*?)</td>'
uren_compile = re.compile(pattern)

# 三連複のコンパイル
pattern = r'class="pay_table_01"[\s\S]*?三連複[\s\S]*?<td>[\s\S]*?</td>[\s\S]*?<td class="txt_r">([\s\S]*?)</td>'
sanfuku_compile = re.compile(pattern)


def makeCsv(file_name, lst):
    with open(file_name, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for v in lst:
            writer.writerow(v)


def calcSpeed(distance, race_time):
    tmp = race_time.split(":")
    fun = int(tmp[0]) * 60
    byo = float(tmp[1])
    # 走行距離(m)÷1000÷走行時間(秒)×60×60
    speed = int(distance) / 1000 / (float(fun) + byo) * 60 * 60
    return speed


def getAll(html, race_id):
    race_date = None
    race_number = None
    race_name = None
    race_course = None
    event_date = None
    race_type = None
    race_distance = None
    race_weather = None
    race_state = None
    top_time = None
    horses = None
    uren = None
    sanfuku = None

    table_result = None
    tr_result = None

    # race_date_compile
    try:
        result = race_date_compile.findall(html)
        race_date, race_course, event_date = result[0]
    except Exception as e:
        print("\n race_date_compile", race_id, e)

    # race_state_compile
    try:
        result = race_state_compile.findall(html)
        race_type, race_distance, race_weather, race_state = result[0]
    except Exception as e:
        print("\n race_state_compile", race_id, e)

    # race_number_compile
    try:
        result = race_number_compile.findall(html)
        race_number = result[0]
    except Exception as e:
        print("\n race_number_compile", race_id, e)

    # race_name_compile
    try:
        result = race_name_compile.findall(html)
        race_name = result[0]
    except Exception as e:
        print("\n race_name_compile", race_id, e)

    # uren_compile
    try:
        result = uren_compile.findall(html)
        uren = result[0].replace("\n", "").replace(",", "")
    except Exception as e:
        print("\n uren_compile", race_id, e)

    # sanfuku_compile
    try:
        result = sanfuku_compile.findall(html)
        sanfuku = result[0].replace("\n", "").replace(",", "")
    except Exception as e:
        print("\n sanfuku_compile", race_id, e)

    # table tr 取得
    try:
        table_result = table_compile.findall(html)
        tr_result = tr_compile.findall(table_result[0])
    except Exception as e:
        print("\n table_compile", race_id, e)

    # 出場頭数
    horses = len(tr_result) - 1

    bodys = []

    for v in tr_result:
        td_result = None
        order = None
        frame = None
        number = None
        name_id = None
        name = None
        gender = None
        age = None
        jockey_id = None
        jockey = None
        race_time = None
        speed = None
        agari = None
        odds = None
        popular = None
        area = None
        trainer = None
        prize = None

        # tdを取得
        try:
            td_result = td_compile.findall(v)
        except Exception as e:
            print("\n td_compile", race_id, e)

        if len(td_result) > 0:
            try:
                # 順位(中、除などの文字はすべてパス)
                order = int(td_result[0])

                # 枠
                frame = span_compile.findall(td_result[1])[0]

                # 馬番
                number = td_result[2]

                # 馬名
                name_id, name = a_compile.findall(td_result[3])[0]

                # 性別・年齢
                gender = td_result[4][0]
                age = td_result[4][1]

                # 騎手
                jockey_id, jockey = a_compile.findall(td_result[6])[0]

                # タイム
                race_time = td_result[7]
                if order == 1:
                    top_time = race_time

                speed = calcSpeed(race_distance, race_time)

                # 上り
                agari = span_compile.findall(td_result[11])[0]

                # 単勝
                odds = td_result[12]

                # 人気
                popular = int(span_compile.findall(td_result[13])[0])

                # トレーナー
                area, trainer = trainer_compile.findall(td_result[18])[0]

                # 賞金
                prize = td_result[20].replace(",", "")
                if prize == "":
                    prize = 0.0

            except Exception as e:
                print("\n order etc.", race_id, e)
                continue

            bodys.append([
                race_id,
                order,
                frame,
                number,
                name_id,
                name,
                gender,
                age,
                jockey_id,
                jockey,
                race_time,
                speed,
                agari,
                odds,
                popular,
                area,
                trainer,
                prize
            ])

    # head 書き込み
    makeCsv(head_csv, [[
        race_id,
        race_date,
        race_number,
        race_name,
        race_course,
        event_date,
        race_type,
        race_distance,
        race_weather,
        race_state,
        top_time,
        horses,
        uren,
        sanfuku
    ]])

    # body 書き込み
    makeCsv(body_csv, bodys)


def main():

    start = time.perf_counter()

    all_files = os.listdir(path)

    # ファイル抽出
    files = \
        [v for v in all_files if v.startswith("2020")] + \
        [v for v in all_files if v.startswith("2019")] + \
        [v for v in all_files if v.startswith("2018")] + \
        [v for v in all_files if v.startswith("2017")] + \
        [v for v in all_files if v.startswith("2016")] + \
        [v for v in all_files if v.startswith("2015")] + \
        [v for v in all_files if v.startswith("2014")] + \
        [v for v in all_files if v.startswith("2013")] + \
        [v for v in all_files if v.startswith("2012")] + \
        [v for v in all_files if v.startswith("2011")] + \
        [v for v in all_files if v.startswith("2010")] + \
        [v for v in all_files if v.startswith("2009")] + \
        [v for v in all_files if v.startswith("2008")]

    makeCsv(head_csv, [[
        "race_id",
        "race_date",
        "race_number",
        "race_name",
        "race_course",
        "event_date",
        "race_type",
        "race_distance",
        "race_weather",
        "race_state",
        "top_time",
        "horses",
        "uren",
        "sanfuku"
    ]])

    makeCsv(body_csv, [[
        "race_id",
        "order",
        "frame",
        "number",
        "name_id",
        "name",
        "gender",
        "age",
        "jockey_id",
        "jockey",
        "race_time",
        "speed",
        "agari",
        "odds",
        "popular",
        "area",
        "trainer",
        "prize"
    ]])

    all = len(files)
    i = 1

    for v in files:

        with open(f"{path}/{v}", "r", encoding="utf-8") as f:
            html = f.read()

        # レースID ファイル名
        race_id = v.replace(".txt", "")

        print(f"\r{i}/{all} {race_id}", end="")

        getAll(html, race_id)

        i += 1

    end = time.perf_counter()
    print(f"\n\n【終了】実行時間:{end-start}秒")


if __name__ == "__main__":
    main()
