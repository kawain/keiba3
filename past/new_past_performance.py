import sys
import time
import pandas as pd


def func1(df, item):
    arr = []
    all = len(df)
    i = 0
    for date, name in zip(df["race_date"], df["name_id"]):
        arr.append(df.loc[(df["race_date"] < date) & (
            df["name_id"] == name), item].head(2).mean())
        print(f"\r {item} {i}/{all}", end="")
        i += 1

    return arr


def func2(df, item):
    arr = []
    all = len(df)
    i = 0
    for date, name in zip(df["race_date"], df["name_id"]):
        arr.append(df.loc[(df["race_date"] < date) & (
            df["name_id"] == name), item].head(2).sum())
        print(f"\r {item} {i}/{all}", end="")
        i += 1

    return arr


def main():
    start = time.perf_counter()

    dic = {
        1: "order",
        2: "speed_min_max",
        3: "agari_min_max",
        4: "diff_min_max",
        5: "prize"
    }

    args = sys.argv
    try:
        s = int(args[1])
    except Exception as e:
        print(e)
        sys.exit()

    df = pd.read_pickle("過去実績集計用.pkl")
    print(df.shape)

    if 1 <= s <= 4:
        arr = func1(df, dic[s])
    elif s == 5:
        arr = func2(df, dic[s])

    df2 = pd.DataFrame({f"past_{dic[s]}": arr})
    df2.to_pickle(f"past_{dic[s]}.pkl")

    end = time.perf_counter()
    print(f"\n\n【終了】実行時間:{end-start}秒")


if __name__ == "__main__":
    main()
