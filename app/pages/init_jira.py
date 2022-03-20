import streamlit as st
from jira_workflow import JiraWorkflow
import json


def app():

    nickname = st.text_input(label='Введите nickname')
    email = st.text_input(label='Введите email')
    token = st.text_input(label='Введите jira token',
                          help='https://id.atlassian.com/manage/api-tokens')
    project = st.text_input(label='Имя проекта в Jira')

    if nickname and email and token and project:
        st.markdown('# Jira initialized!')
        with open('config.json') as f:
            config = json.load(f)
        config['nickname'] = nickname
        config['email'] = email
        config['token'] = token
        config['project'] = project
        with open('config.json', 'w') as f:
            json.dump(config, f)


if __name__ == '__main__':
    app()
