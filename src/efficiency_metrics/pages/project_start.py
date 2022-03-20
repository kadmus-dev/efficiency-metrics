from collections import defaultdict

import pandas as pd
import plotly.express as px
import streamlit as st


def app():
    proj_data = {}
    st.markdown('# Параметры проекта')
    project_name = st.text_input(label='Название проекта')
    proj_data['project_name'] = project_name

    planned_time = st.number_input(label='Планируемое время, которое будет затрачено на проект',
                                   help='в неделях',
                                   min_value=0,
                                   step=1)
    proj_data['planned_time'] = planned_time

    num_workers = st.number_input(label='Количество участников проекта',
                                  min_value=1,
                                  step=1)
    proj_data['num_workers'] = num_workers

    additional_metrics = {'m1': 'Охват клиентуры, тыс. человек',
                          'm2': 'Уровень экологичности проекта',
                          'm3': 'Количество серверов'}

    ops = st.multiselect(label='Выберите дополнительные параметры',
                         options=[additional_metrics['m1'],
                                  additional_metrics['m2'],
                                  additional_metrics['m3']])

    proj_data['clients'] = None
    proj_data['environmental'] = None
    proj_data['num_servers'] = None
    if additional_metrics['m1'] in ops:
        client_coverage = st.number_input(label=additional_metrics['m1'],
                                          help='Введите количество человек в тыс., которое будет пользоваться конечным продуктом',
                                          min_value=0,
                                          step=1)
        proj_data['clients'] = client_coverage

    if additional_metrics['m2'] in ops:
        environmental = st.slider(label=additional_metrics['m2'],
                                  min_value=1,
                                  max_value=5)
        proj_data['environmental'] = environmental

    if additional_metrics['m3'] in ops:
        num_servers = st.number_input(label=additional_metrics['m3'],
                                      min_value=0,
                                      step=1)
        proj_data['num_servers'] = num_servers

    st.markdown('# Данные участников проекта')
    res = st.selectbox(label='Загрузите таблицу с данными об участниках проекта или введите их вручную',
                       options=['Загрузить таблицу', 'Ручной ввод'])

    workers_data = defaultdict(list)

    if res == 'Загрузить таблицу':
        dataframe = st.file_uploader(label='Таблица с данными об участниках проекта. Столбцы: '
                                           'ФИО, Должность, Отдел, Часов в неделю, Опыт работы, Возраст, Ожидаемая сложность задач',
                                     type=['csv'],
                                     help='Опыт работы в годах, сложность задач от 1 до 10.')
        if dataframe is not None:
            dataframe = pd.read_csv(dataframe)
            workers_data = {
                'name': dataframe['ФИО'].tolist(),
                'position': dataframe['Должность'].tolist(),
                'hours_per_week': dataframe['Часов в неделю'].tolist(),
                'department': dataframe['Отдел'].tolist(),
                'work_experience': dataframe['Опыт работы'].tolist(),
                'age': dataframe['Возраст'].tolist(),
                'estimated_difficulty': dataframe['Ожидаемая сложность задач'].tolist()
            }

    elif res == 'Ручной ввод':
        dataframe = st.text_area(label='Ввод информации по каждому сотруднику: ФИО, должность, '
                                       'отдел, количество часов в неделю на работу, опыт работы (лет), возраст,ожидаемая сложность задач (от 1 до 10)',
                                 help='Через запятую перечисление полей, каждый новый сотрудник с новой строки.\n')
        if len(dataframe) > 0:
            strings = dataframe.split('\n')
            for string in strings:
                if len(string.split(',')) == 7:
                    name, pos, department, hpw, exp, age, diff = string.split(
                        ',')
                    workers_data['name'].append(name)
                    workers_data['position'].append(pos)
                    workers_data['department'].append(department)
                    workers_data['work_experience'].append(exp)
                    workers_data['age'].append(age)
                    workers_data['estimated_difficulty'].append(diff)
                    workers_data['hours_per_week'].append(hpw)

    if workers_data:
        st.write(pd.DataFrame(workers_data))

    st.markdown('# Графики')
    if workers_data:
        st.markdown('## Количество людей в каждом отделе')
        fig = px.bar(pd.DataFrame(workers_data),
                     x='department',
                     color='department')
        st.plotly_chart(fig)

        st.markdown('## Количество людей на каждой должности')
        fig = px.bar(pd.DataFrame(workers_data),
                     x='position',
                     color='position')
        st.plotly_chart(fig)

        st.markdown('## Сложность решаемых задач от количества часов в неделю')
        fig = px.scatter(pd.DataFrame(workers_data),
                         x='hours_per_week',
                         y='estimated_difficulty',
                         color='name',
                         symbol='name')
        fig.update_traces(marker_size=13)
        st.plotly_chart(fig)

        st.markdown('## Сложность решаемых задач от опыта работы')
        fig = px.scatter(pd.DataFrame(workers_data),
                         x='work_experience',
                         y='estimated_difficulty',
                         color='name',
                         symbol='name')
        fig.update_traces(marker_size=13)
        st.plotly_chart(fig)

    return proj_data, workers_data


if __name__ == '__main__':
    app()
