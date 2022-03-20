import sqlite3

import streamlit as st
from efficiency_metrics.sql_utils import DB_PATH
from efficiency_metrics.sql_utils import get_df


def app():
    st.markdown("# Интеграция с SQLite")

    data_connection = sqlite3.connect(DB_PATH)
    query_str = st.text_input("Введите SQLite команду:", value="SELECT * From projects",
                              placeholder="SELECT * From projects")
    df = get_df(data_connection, query_str)
    st.dataframe(df)


if __name__ == '__main__':
    app()
