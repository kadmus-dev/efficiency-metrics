import sqlite3
import streamlit as st

from sql_utils import get_df

# constants
DB_PATH = "./databases/data.db"


def app():
    st.markdown("# Интеграция с SQLite")

    data_connection = sqlite3.connect(DB_PATH)
    query_str = st.text_input("Введите SQLite команду:", value="SELECT * From projects",
                              placeholder="SELECT * From projects")
    df = get_df(data_connection, query_str)
    st.dataframe(df)


if __name__ == '__main__':
    app()
