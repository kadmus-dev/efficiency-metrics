import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

def get_ax_data(Axis_name, data):

    if Axis_name == "Working time on the project (%)":
        axis_data = np.array(data["Time spent on the project"])
        axis_data = axis_data / axis_data.sum() * 100

    elif Axis_name == "Working time on the project (hours)":
        axis_data = np.array(data["Time spent on the project"])

    else:
        axis_data = np.array(data[Axis_name])

    return axis_data

def app():

    random_data = {"Name" : ["Name1", "Name2", "Name3", "Name4", "Name5"],
        "Department" : ["1", "2", "1", "3", "2"],
        "Time spent on the project" : [10, 20, 10, 15, 20],
        "Manager's assessment" : [7,8,6,7,9],
        "Metric 1" : [0.5, 0.6, 0.3, 0.1, 0.4],
        "Metric 2" : [0.1, 0.3, 0.4, 0.5, 0.3]
    }
    data = pd.DataFrame(random_data)

    st.write("# 3rd step plots")

    departments = ["all"]
    departments.extend(list(np.unique(data["Department"])))

    chosen_dep = st.selectbox("Department", departments)
    if chosen_dep != "all":
        data = data[data["Department"] == chosen_dep]

    X_name = st.selectbox("Axis X", ["Working time on the project (%)", 
                            "Working time on the project (hours)",
                            "Manager's assessment",
                            "Metric 1",
                            "Metric 2"])

    X = get_ax_data(X_name, data)

    Y_name = st.selectbox("Axis Y", ["Working time on the project (%)", 
                            "Working time on the project (hours)",
                            "Manager's assessment",
                            "Metric 1",
                            "Metric 2"])

    Y = get_ax_data(Y_name, data)

    result_plot = pd.DataFrame({X_name:X, Y_name:Y, "Department":data["Department"], "Name":data["Name"]})
    result_plot = px.scatter(result_plot, x=X_name, y=Y_name, symbol="Department", hover_data=["Name"])
    result_plot.update_traces(marker={'size': 12})
    st.plotly_chart(result_plot)


if __name__ == '__main__':
    app()