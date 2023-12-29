from __future__ import annotations

import pandas as pd

from tests.utils import convert_dataframe_to_pandas_numpy
from tests.utils import integer_dataframe_1
from tests.utils import interchange_to_pandas


def test_float_powers_column(library: str) -> None:
    df = integer_dataframe_1(library)
    df.__dataframe_namespace__()
    ser = df.col("a")
    other = df.col("b") * 1.0
    result = df.assign(ser.__pow__(other).rename("result"))
    result_pd = interchange_to_pandas(result)
    expected = pd.DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6], "result": [1.0, 32.0, 729.0]},
    )
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    pd.testing.assert_frame_equal(result_pd, expected)


def test_float_powers_scalar_column(library: str) -> None:
    df = integer_dataframe_1(library)
    df.__dataframe_namespace__()
    ser = df.col("a")
    other = 1.0
    result = df.assign(ser.__pow__(other).rename("result"))
    result_pd = interchange_to_pandas(result)
    expected = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "result": [1.0, 2.0, 3.0]})
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    pd.testing.assert_frame_equal(result_pd, expected)


def test_int_powers_column(library: str) -> None:
    df = integer_dataframe_1(library)
    df.__dataframe_namespace__()
    ser = df.col("a")
    other = df.col("b") * 1
    result = df.assign(ser.__pow__(other).rename("result"))
    result_pd = interchange_to_pandas(result)
    expected = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "result": [1, 32, 729]})
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    if library in ("polars", "polars-lazy"):
        result_pd = result_pd.astype("int64")
    pd.testing.assert_frame_equal(result_pd, expected)


def test_int_powers_scalar_column(library: str) -> None:
    df = integer_dataframe_1(library)
    df.__dataframe_namespace__()
    ser = df.col("a")
    other = 1
    result = df.assign(ser.__pow__(other).rename("result"))
    result_pd = interchange_to_pandas(result)
    expected = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "result": [1, 2, 3]})
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    if library in ("polars", "polars-lazy"):
        result_pd = result_pd.astype("int64")
    pd.testing.assert_frame_equal(result_pd, expected)
