from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from numba import njit

__all__ = ["CreateCuSumBar"]


class CreateCuSumBar(BaseEstimator, TransformerMixin):
    def __init__(self, col_value: str, col_volume: str, thresh=100):
        self.col_value = col_value
        self.col_volume = col_volume
        self.thresh = thresh

    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame):
        targets = ["diff", self.col_value, self.col_volume]
        if not set(targets) <= set(X.columns):
            raise ValueError(
                f"not existed columns: {list(set(targets) - set(X.columns))}"
            )
        if not pd.api.types.is_datetime64_any_dtype(X.index):
            raise TypeError("type of index is not datetime64")

        X = X.sort_index()
        filter = _symmetryCuSumFilter(self.thresh)
        X["group"] = X["diff"].apply(filter)

        return (
            X[[self.col_value, self.col_volume, "group"]]
            .groupby("group")
            .apply(
                lambda df: pd.Series(
                    {
                        "timestamp": df.index[-1],
                        "Open": df[self.col_value].iloc[0],
                        "High": df[self.col_value].max(),
                        "Low": df[self.col_value].min(),
                        "Close": df[self.col_value].iloc[-1],
                        "Volume": df[self.col_volume].sum(),
                    }
                )
            )
            .set_index("timestamp")
        )


def _symmetryCuSumFilter(thresh):
    sPos, sNeg, group = 0, 0, 0

    def _func(x):
        nonlocal sPos, sNeg, group
        sPos, sNeg = max(0, sPos + x), min(0, sNeg + x)
        if sNeg < -thresh:
            sNeg = 0
            group += 1
        elif sPos > thresh:
            sPos = 0
            group += 1
        return group

    return _func


# class _SymmetryCuSumFilter:
#     def __init__(self, thresh: int):
#         self.sPos, self.sNeg = 0, 0
#         self.thresh = thresh
#         self.group = 0

#     def proc(self, x: int | float):
#         self.sPos, self.sNeg = max(0, self.sPos + x), min(0, self.sNeg + x)
#         if self.sNeg < -self.thresh:
#             self.sNeg = 0
#             self.group += 1
#         elif self.sPos > self.thresh:
#             self.sPos = 0
#             self.group += 1
#         return self.group
