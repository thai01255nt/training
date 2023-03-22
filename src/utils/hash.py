import hashlib
from typing import Dict, List, Union

import numpy as np
import pandas as pd


class HashUtils:

    @classmethod
    def hash_data(
        cls,
        data: Union[List[Dict], pd.DataFrame],
        entity,
        order_bys=[],
        ascending=(),
        ignore_fields=(),
        include_fields=(),
        drop_duplicate=False,
    ):
        df = pd.DataFrame(data).sort_values(by=order_bys, ascending=ascending)
        df = df.replace({np.nan: None, np.inf: None, -np.inf: None})
        selected_df = df.copy()
        selected_columns = []
        for column in entity.__mapper__.columns.values():
            if len(include_fields) != 0 and column.name not in include_fields:
                continue
            if column.name in ignore_fields:
                continue
            selected_columns.append(column.name)
            if column.name not in selected_df.columns:
                selected_df[column.name] = None
        if len(set(selected_columns)) != len(selected_columns):
            raise Exception("duplicate columns name in hash")
        selected_columns.sort()
        selected_df = selected_df[selected_columns].copy()
        selected_df["__hashID__"] = selected_df.apply(
            lambda row: hashlib.md5("_".join(row.fillna("").values.astype(str)).encode()).hexdigest(), axis=1
        )
        df["__hashID__"] = selected_df["__hashID__"]
        if drop_duplicate:
            df = df.drop_duplicates(subset=["__hashID__"], keep="last")
        return df.to_dict(orient="records")
