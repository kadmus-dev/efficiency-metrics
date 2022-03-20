import streamlit as st
from efficiency_metrics.multi_page import MultiPage
from efficiency_metrics.pages import cocomo
from efficiency_metrics.pages import init_jira
from efficiency_metrics.pages import project_start
from efficiency_metrics.pages import second_step_project
from efficiency_metrics.pages import sqlite
from efficiency_metrics.pages import third_step_project
from efficiency_metrics.pages import third_step_staff


def main():
    # Create an instance of the app
    app = MultiPage()

    # Title of the main page
    st.title("Метрики оценки эффективности")

    # Add all your applications (pages) here
    app.add_page("Инициализация проекта", project_start.app)
    app.add_page("Метрика COCOMO", cocomo.app)
    app.add_page("SQLite", sqlite.app)
    app.add_page("Присоединение к Jira", init_jira.app)
    app.add_page('Оценка текущего состояния проекта', second_step_project.app)
    app.add_page("Итоги по проекту", third_step_project.app)
    app.add_page("Итоги работы сотрудников по проекту", third_step_staff.app)

    # The main app
    app.run()


if __name__ == '__main__':
    main()
