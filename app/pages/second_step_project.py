import streamlit as st
from jira_workflow import JiraWorkflow
import json


def get_parser():
    with open('config.json') as f:
        config = json.load(f)
    if config['nickname'] is None:
        return None
    jira_parser = JiraWorkflow(config['nickname'],
                               config['email'],
                               config['token'],
                               config['project'])
    try:
        jira_parser.get_data()
        jira_parser.type_count()
        return jira_parser
    except:
        return None


def get_cocomo():
    with open('config.json') as f:
        config = json.load(f)
        return config['cocomo']

def app():
    proj_stage = st.slider(label='Готовность проекта по времени, %',
                           min_value=1,
                           max_value=100)
    jira_parser = get_parser()

    if jira_parser is None:
        st.markdown('## Нет доступа к Jira, ручной ввод')
        costs = st.number_input(label='Текущие затраты в человеко-днях',
                                min_value=1,
                                step=1)
    else:
        st.markdown('## Данные берутся из Jira')
        jira_parser.get_data()
        costs = jira_parser.spent_minutes() / (24*60)
        delay = jira_parser.delay_minutes() / (60)
        st.metric('Просрок по роекту, ч',
                  value=delay)

    estimated_costs = costs*100/proj_stage
    st.metric('Предполагаемые затраты на весь проект, человеко-дни',
                value=estimated_costs)
    cocomo = get_cocomo()
    if cocomo is not None:
        efficiency = 100*(cocomo / estimated_costs)
        st.metric('Текущая эффективность проекта, %',
                    value=efficiency)


if __name__ == '__main__':
    app()
