import streamlit as st
from efficiency_metrics.config import write_parser


def app():

    nickname = st.text_input(label='Введите nickname')
    email = st.text_input(label='Введите email')
    token = st.text_input(label='Введите jira token',
                          help='https://id.atlassian.com/manage/api-tokens')
    project = st.text_input(label='Имя проекта в Jira')

    if nickname and email and token and project:
        st.markdown('# Jira initialized!')
        write_parser(nickname, email, token, project)


if __name__ == '__main__':
    app()
