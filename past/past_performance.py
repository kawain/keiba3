import sys
import time
import pandas as pd


def horse_order_mean(df):
    arr = []
    all = len(df)
    i = 0
    for date, name in zip(df["race_date"], df["name"]):
        arr.append(df.loc[(df["race_date"] < date) & (
            df["name"] == name), "order"].head(2).mean())

        print(f"\r horse_order_mean {i}/{all}", end="")
        i += 1

    return arr


def horse_prize_sum(df):
    arr = []
    all = len(df)
    i = 0
    for date, name in zip(df["race_date"], df["name"]):
        arr.append(df.loc[(df["race_date"] < date) & (
            df["name"] == name), "prize"].head(2).sum())

        print(f"\r horse_prize_sum {i}/{all}", end="")
        i += 1

    return arr


def horse_speed_mean(df):
    arr = []
    all = len(df)
    i = 0
    for date, name in zip(df["race_date"], df["name"]):
        arr.append(df.loc[(df["race_date"] < date) & (
            df["name"] == name), "speed_min_max"].head(2).mean())

        print(f"\r horse_speed_mean {i}/{all}", end="")
        i += 1

    return arr


def horse_agari_mean(df):
    arr = []
    all = len(df)
    i = 0
    for date, name in zip(df["race_date"], df["name"]):
        arr.append(df.loc[(df["race_date"] < date) & (
            df["name"] == name), "agari_min_max"].head(2).mean())

        print(f"\r horse_agari_mean {i}/{all}", end="")
        i += 1

    return arr


def jockey_order_mean(df):
    arr = []
    all = len(df)
    i = 0
    for date, name in zip(df["race_date"], df["jockey"]):
        arr.append(df.loc[(df["race_date"] < date) & (
            df["jockey"] == name), "order"].head(50).mean())

        print(f"\r jockey_order_mean {i}/{all}", end="")
        i += 1

    return arr


def jockey_prize_sum(df):
    arr = []
    all = len(df)
    i = 0
    for date, name in zip(df["race_date"], df["jockey"]):
        arr.append(df.loc[(df["race_date"] < date) & (
            df["jockey"] == name), "prize"].head(50).sum())

        print(f"\r jockey_prize_sum {i}/{all}", end="")
        i += 1

    return arr


def trainer_order_mean(df):
    arr = []
    all = len(df)
    i = 0
    for date, name in zip(df["race_date"], df["trainer"]):
        arr.append(df.loc[(df["race_date"] < date) & (
            df["trainer"] == name), "order"].head(100).mean())

        print(f"\r trainer_order_mean {i}/{all}", end="")
        i += 1

    return arr


def trainer_prize_sum(df):
    arr = []
    all = len(df)
    i = 0
    for date, name in zip(df["race_date"], df["trainer"]):
        arr.append(df.loc[(df["race_date"] < date) & (
            df["trainer"] == name), "prize"].head(100).sum())

        print(f"\r trainer_prize_sum {i}/{all}", end="")
        i += 1

    return arr


def main():
    start = time.perf_counter()

    args = sys.argv

    a = int(args[1])

    df = pd.read_pickle("merge40col.pkl")

    print(df.shape)

    if a == 1:
        arr = horse_order_mean(df)
        df2 = pd.DataFrame({"past_horse_order_mean": arr})
        df2.to_pickle("past_horse_order_mean.pkl")
    elif a == 2:
        arr = horse_prize_sum(df)
        df2 = pd.DataFrame({"past_horse_prize_sum": arr})
        df2.to_pickle("past_horse_prize_sum.pkl")
    elif a == 3:
        arr = horse_speed_mean(df)
        df2 = pd.DataFrame({"past_horse_speed_mean": arr})
        df2.to_pickle("past_horse_speed_mean.pkl")
    elif a == 4:
        arr = horse_agari_mean(df)
        df2 = pd.DataFrame({"past_horse_agari_mean": arr})
        df2.to_pickle("past_horse_agari_mean.pkl")
    elif a == 5:
        arr = jockey_order_mean(df)
        df2 = pd.DataFrame({"past_jockey_order_mean": arr})
        df2.to_pickle("past_jockey_order_mean.pkl")
    elif a == 6:
        arr = jockey_prize_sum(df)
        df2 = pd.DataFrame({"past_jockey_prize_sum": arr})
        df2.to_pickle("past_jockey_prize_sum.pkl")
    elif a == 7:
        arr = trainer_order_mean(df)
        df2 = pd.DataFrame({"past_trainer_order_mean": arr})
        df2.to_pickle("past_trainer_order_mean.pkl")
    elif a == 8:
        arr = trainer_prize_sum(df)
        df2 = pd.DataFrame({"past_trainer_prize_sum": arr})
        df2.to_pickle("past_trainer_prize_sum.pkl")

    end = time.perf_counter()
    print(f"\n\n【終了】実行時間:{end-start}秒")


if __name__ == "__main__":
    main()
