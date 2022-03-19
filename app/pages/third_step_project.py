import pandas as pd
import plotly.express as px
import streamlit as st

test_projects_database = {"id": ["1", "2", "3", "4", "5"],
                          "people_exit": [None, None, None, None, None],
                          "hosting_costs": [None, None, None, None, None],
                          "bugfix_hours": [None, None, None, None, None],
                          "num_tasks": [None, None, None, None, None]
                          }

projects_database = pd.DataFrame(test_projects_database)


def translate(s):
    if s == "Затраты на хостинг":
        return "hosting_costs"
    elif s == "Количество людей, покинувших проект":
        return "people_exit"
    elif s == "Время на исправление ошибок (часов)":
        return "bugfix_hours"
    elif s == "Количество подзадач":
        return "num_tasks"


def app():
    st.markdown("# 3 этап для проектов")

    use_jira = st.selectbox("Mode", ["Jira", "User Interface"])
    if use_jira == "Jira":
        use_jira = True
    else:
        use_jira = False

    if use_jira is False:

        proj_id = st.selectbox("ID проекта", projects_database["id"])
        project_n = projects_database[projects_database["id"]
                                      == proj_id].index[0]

        hosting = st.number_input("Затраты на хостинг", min_value=0)
        exit_people = st.number_input(
            "Количество людей, покинувших проект", min_value=0)
        bugfix_h = st.number_input(
            "Время на исправление ошибок (часов)", min_value=0)
        num_tasks = st.number_input("Количество подзадач", min_value=0)

        add = st.button("Добавить")
        if add:
            projects_database.iloc[project_n].loc["hosting_costs"] = hosting
            projects_database.iloc[project_n].loc["people_exit"] = exit_people
            projects_database.iloc[project_n].loc["bugfix_hours"] = bugfix_h
            projects_database.iloc[project_n].loc["num_tasks"] = num_tasks

        X_name = st.selectbox("Axis X", ["Затраты на хостинг",
                                         "Количество людей, покинувших проект",
                                         "Время на исправление ошибок (часов)",
                                         "Количество подзадач"])

        Y_name = st.selectbox("Axis Y", ["Затраты на хостинг",
                                         "Количество людей, покинувших проект",
                                         "Время на исправление ошибок (часов)",
                                         "Количество подзадач"])

        plot_data = pd.DataFrame({X_name: projects_database[translate(X_name)],
                                  Y_name: projects_database[translate(X_name)],
                                  "ID": projects_database["id"]}).dropna()

        result_plot = px.scatter(
            plot_data, x=X_name, y=Y_name, hover_data=["ID"])
        result_plot.update_traces(marker={'size': 12})
        st.plotly_chart(result_plot)


if __name__ == '__main__':
    app()
