import sqlite3
from os import path

from sklearn.linear_model import LinearRegression

from sql_utils import get_df


def process_df(df, rm_cols=False):
    if rm_cols:
        df = df[["type", "kloc", "reliability", "db_size", "complexity", "runtime_limits", "memory_limits",
                 "vm_instability", "recovery_time", "analytic_skills", "dev_experience", "dev_skills", "vm_experience",
                 "language_experience", "dev_methods", "toolkit_usage", "schedule_req", "labor_costs"]]
    df.loc[:, "type"] = df["type"].map({'organic': 1, 'intermediate': 2, 'embedded': 3})
    df = df.fillna(df.mean())
    return df


def predict(data):
    conn = sqlite3.connect(path.join("databases", "data.db"))
    df_db = get_df(conn, "select * from projects")
    df_db = process_df(df_db, True)
    lr = LinearRegression()
    lr.fit(df_db.drop(columns='labor_costs'), df_db['labor_costs'])
    return lr.predict(process_df(data))
