import pandas as pd


DB_PATH = "databases/data.db"


def get_df(database_connection, query_str: str) -> pd.DataFrame:
    """
    Return SQLite query as pandas DataFrame

    :param database_connection: sqlite3.Connection
    :param query_str: query string
    :return: result dataframe
    """
    query = database_connection.execute(query_str)
    database_connection.commit()
    if query.description is None:
        return pd.DataFrame()
    cols = [column[0] for column in query.description]
    df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    return df
