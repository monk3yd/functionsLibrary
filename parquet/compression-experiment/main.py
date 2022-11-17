import time
import pandas as pd


def main():
    df = pd.read_excel("mb.xlsx")
    df.to_parquet("file_parquet.parquet", compression="gzip")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')
