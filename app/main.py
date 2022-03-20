import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'pages'))

import streamlit as st
from multi_page import MultiPage
from pages import cocomo, sqlite, project_start, second_step_project
from pages import third_step_project
from pages import third_step_staff
from pages import init_jira


def main():
    # Create an instance of the app
    app = MultiPage()

    # Title of the main page
    st.title("Efficiency Metrics Evaluation")

    # Add all your applications (pages) here
    app.add_page("Project Start", project_start.app)
    app.add_page("Cocomo metric", cocomo.app)
    app.add_page("SQLite", sqlite.app)
    app.add_page("Jira Connection", init_jira.app)
    app.add_page('2 этап', second_step_project.app)
    app.add_page("3 этап (проекты)", third_step_project.app)
    app.add_page("3 этап (сотрудники)", third_step_staff.app)

    # The main app
    app.run()


if __name__ == '__main__':
    main()
