import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

test_staff_database = {"name" : ["Vasya", "Pushkin", "Oleg", "Tinkoff", "Gagarin"],
                       "proj_id" : ["1", "2", "1", "2", "1"],
                       "estimated_difficulty" : [10, 5, 9, 2, 7],
                       "proj_rate" : [None, None, None, None, None],
                       "real_difficulty" : [None, None, None, None, None]
                      }

staff_database = pd.DataFrame(test_staff_database)

def translate(s):
    if s == "Фактическая сложность работы над проектом":
        return "real_difficulty"
    elif s == "Оценка проекта":
        return "proj_rate"

def app():
    st.markdown("# 3 этап для сотрудников")

    use_jira = st.selectbox("Mode", ["User Interface", "Jira"])
    if use_jira == "Jira":
        use_jira = True
    else:
        use_jira = False

    if use_jira is False:

        emp_id = st.selectbox("ФИО сотрудника", staff_database["name"])
        emp_n = staff_database[staff_database["name"] == emp_id].index[0]

        real_difficulty = st.number_input("Фактическая сложность работы над проектом", min_value = 0)
        proj_rate = st.number_input("Оценка проекта", min_value = 0)

        add = st.button("Добавить")
        if add:
            staff_database.iloc[emp_n, staff_database.columns.get_loc('real_difficulty')] = real_difficulty
            staff_database.iloc[emp_n, staff_database.columns.get_loc('proj_rate')] = proj_rate

        st.markdown("## Коэффициент удовлетворённости сотрудников")

        plot_info = {"Score": [], "Project ID": [], "Type": []}
        X = np.unique(staff_database["proj_id"])
        for d in X:
            plot_info["Score"].append(
                np.mean(staff_database[staff_database["proj_id"] == d]["estimated_difficulty"]))
            plot_info["Type"].append("Expected")
            plot_info["Project ID"].append(d)

            plot_info["Score"].append(
                np.mean(staff_database[staff_database["proj_id"] == d]["real_difficulty"]))
            plot_info["Type"].append("Actual")
            plot_info["Project ID"].append(d)

        fig = px.bar(plot_info, x="Project ID", y="Score",
                     color="Type", barmode='group')
        st.plotly_chart(fig)

        if len(staff_database["real_difficulty"].dropna()) == 0:
            coef = 0
        else:
            coef = np.mean(np.array(staff_database["estimated_difficulty"].dropna()) / np.array(staff_database["real_difficulty"].dropna()))

        satisfaction_level = None
        if coef > 1.3:
            satisfaction_level = "High"
        elif coef < 0.7:
            satisfaction_level = "Low"
        else:
            satisfaction_level = "Moderate"

        st.metric("Mean satisfaction coefficient", coef)
        st.metric("Satisfaction level", satisfaction_level)

if __name__ == '__main__':
    app()
