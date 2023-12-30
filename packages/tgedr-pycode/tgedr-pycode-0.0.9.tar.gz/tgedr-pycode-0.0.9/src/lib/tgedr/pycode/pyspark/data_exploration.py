import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import DataFrame
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from typing import List
from matplotlib.ticker import StrMethodFormatter


def missing_values_ratio(df: DataFrame) -> DataFrame:
    count = df.count()
    numeric_cols = [c for c, t in df.dtypes if t in ["int", "float", "double"]]

    numeric_func = lambda c: (F.col(c) == "") | (F.col(c).isNull()) | (F.isnan(F.col(c)))
    non_numeric_func = lambda c: (F.col(c) == "") | (F.col(c).isNull())

    return df.select(
        [
            (F.count(F.when(numeric_func(c) if c in numeric_cols else non_numeric_func(c), c)) / count).alias(c)
            for c in df.columns
        ]
    )


def frequencies(df: DataFrame, col: str) -> DataFrame:
    return df.groupBy(F.col(col)).count().sort(F.desc("count"))


def cast(df: DataFrame, cols: List[str], type: T.DataType) -> DataFrame:
    for col in cols:
        df = df.withColumn(col, F.col(col).cast(type))
    return df


def deciles(df: DataFrame, col: str) -> list:
    df_filtered = df.filter((F.col(col) != 0) & (F.col(col).isNotNull()) & (~F.isnan(col)))
    return df_filtered.approxQuantile(col, [x / 10 for x in range(10)], 0.1)


def cardinalities(df: DataFrame) -> DataFrame:
    return df.select([F.countDistinct(F.col(c)).alias(c) for c in df.columns])


def plot_hist(df: DataFrame, col: str, bins: int = 12, fig_size: tuple = (12, 8), title: str = None) -> None:
    data = df.select(col).rdd.flatMap(lambda x: x).histogram(bins)
    ds = pd.DataFrame(list(zip(*data)), columns=[col, "frequency"])
    plt.clf()
    sns.set(rc={"figure.figsize": fig_size})
    sns.barplot(ds, x=col, y="frequency")
    if title is not None:
        plt.title(title)
    plt.show()
