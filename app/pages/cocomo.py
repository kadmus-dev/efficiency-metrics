import math
import sqlite3
import streamlit as st

# constants
DB_PATH = "./databases/data.db"

rates_rus_woman = ('Очень низкая', 'Низкая', 'Средняя', 'Высокая', 'Очень высокая', 'Критическая')
rates_rus_man = ('Очень низкий', 'Низкий', 'Средний', 'Высокий', 'Очень высокий', 'Критический')
rates_rus_third = ('Очень низкое', 'Низкое', 'Среднее', 'Высокое', 'Очень высокое', 'Критическое')
rates_rus_mult = ('Очень низкие', 'Низкие', 'Средние', 'Высокие', 'Очень высокие', 'Критические')


def app():
    st.markdown("# Cocomo Metric Evaluation")

    # params: [type, kloc, reliability, db_size, complexity, runtime_limits, memory_limits, vm_instability,
    # recovery_time, analytic_skills, dev_experience, dev_skills, vm_experience, language_experience, dev_methods,
    # toolkit_usage, schedule_req]
    db_record = dict()

    # getting type of project
    proj_types_rus = ('Органический', 'Полуразделенный', 'Встроенный')
    proj_types_eng = ('organic', 'intermediate', 'embedded')
    type_rus = st.selectbox(
        'Выберите тип проекта',
        options=proj_types_rus
    )

    types_mapping = {
        'Органический': (3.2, 1.05),
        'Полуразделенный': (3.0, 1.12),
        'Встроенный': (2.8, 1.2)
    }

    a, b = types_mapping[type_rus]

    # adding type to tuple for database
    db_record['type'] = proj_types_eng[proj_types_rus.index(type_rus)]

    # getting kilo lines of code
    kloc = st.number_input(
        'Введите оценочный размер программы',
        help='В тысячах строк исходного кода',
        min_value=0, step=None
    )

    # adding kloc to tuple for database
    db_record['kloc'] = kloc

    # for all coefficients
    laboriousness_coefs = []

    st.markdown("### Характеристики продукта")

    # software reliability slider
    reliability = {
        'Очень низкая': 0.75,
        'Низкая': 0.88,
        'Средняя': 1.0,
        'Высокая': 1.15,
        'Очень высокая': 1.4
    }
    reliability_str = st.select_slider('Требуемая надежность ПО', options=reliability)
    laboriousness_coefs.append(reliability[reliability_str])

    # adding reliability to db
    db_record['reliability'] = rates_rus_woman.index(reliability_str) + 1

    # dbms size slider
    dbms_size = {
        'Низкий': 0.94,
        'Средний': 1.0,
        'Высокий': 1.08,
        'Очень высокий': 1.16
    }
    dbms_size_str = st.select_slider('Размер базы данных приложения', options=dbms_size)
    laboriousness_coefs.append(dbms_size[dbms_size_str])

    # adding db size to db
    db_record['db_size'] = rates_rus_man.index(dbms_size_str) + 1

    # product complexity slider
    product_complexity = {
        'Очень низкая': 0.7,
        'Низкая': 0.85,
        'Средняя': 1.0,
        'Высокая': 1.15,
        'Очень высокая': 1.3,
        'Критическая': 1.65
    }
    product_complexity_str = st.select_slider('Сложность продукта', options=product_complexity)
    laboriousness_coefs.append(product_complexity[product_complexity_str])

    # adding complexity to db
    db_record['complexity'] = rates_rus_woman.index(product_complexity_str) + 1

    st.markdown("### Характеристики аппаратного обеспечения")

    # program execution speed limits slider
    runtime_limits = {
        'Средние': 1.0,
        'Высокие': 1.11,
        'Очень высокие': 1.3,
        'Критические': 1.66
    }
    runtime_limits_str = st.select_slider('Ограничения быстродействия при выполнении программы', options=runtime_limits)
    laboriousness_coefs.append(runtime_limits[runtime_limits_str])

    # adding runtime limits to db
    db_record['runtime_limits'] = rates_rus_mult.index(runtime_limits_str) + 1

    # memory limits slider
    memory_limits = {
        'Средние': 1.0,
        'Высокие': 1.06,
        'Очень высокие': 1.21,
        'Критические': 1.56
    }
    memory_limits_str = st.select_slider('Ограничения памяти', options=memory_limits)
    laboriousness_coefs.append(memory_limits[memory_limits_str])

    # adding memory limits to db
    db_record['memory_limits'] = rates_rus_mult.index(memory_limits_str) + 1

    # instability of the virtual machine environment slider
    vm_instability = {
        'Низкая': 0.87,
        'Средняя': 1.0,
        'Высокая': 1.15,
        'Очень высокая': 1.3
    }
    vm_instability_str = st.select_slider('Неустойчивость окружения виртуальной машины', options=vm_instability)
    laboriousness_coefs.append(vm_instability[vm_instability_str])

    # adding vm instability to db
    db_record['vm_instability'] = rates_rus_woman.index(vm_instability_str) + 1

    # required recovery time slider
    recovery_time = {
        'Низкая': 0.87,
        'Средняя': 1.0,
        'Высокая': 1.07,
        'Очень высокая': 1.15
    }
    recovery_time_str = st.select_slider('Требуемое время восстановления', options=recovery_time)
    laboriousness_coefs.append(recovery_time[recovery_time_str])

    # adding recovery time to db
    db_record['recovery_time'] = rates_rus_woman.index(recovery_time_str) + 1

    st.markdown("### Характеристики персонала")

    # analytic skills
    analytic_skills = {
        'Очень низкие': 1.46,
        'Низкие': 1.19,
        'Средние': 1.0,
        'Высокие': 0.86,
        'Очень высокие': 0.71
    }
    analytic_skills_str = st.select_slider('Аналитические способности', options=analytic_skills)
    laboriousness_coefs.append(analytic_skills[analytic_skills_str])

    # adding analytic skills to db
    db_record['analytic_skills'] = float(rates_rus_mult.index(analytic_skills_str) + 1)

    # development experience
    dev_experience = {
        'Очень низкий': 1.29,
        'Низкий': 1.13,
        'Средний': 1.0,
        'Высокий': 0.91,
        'Очень высокий': 0.82
    }
    dev_experience_str = st.select_slider('Опыт разработки', options=dev_experience)
    laboriousness_coefs.append(dev_experience[dev_experience_str])

    # adding dev exp to db
    db_record['dev_experience'] = float(rates_rus_man.index(dev_experience_str) + 1)

    # software development skills
    dev_skills = {
        'Очень низкие': 1.42,
        'Низкие': 1.17,
        'Средние': 1.0,
        'Высокие': 0.86,
        'Очень высокие': 0.7
    }
    dev_skills_str = st.select_slider('Способности к разработке ПО', options=dev_skills)
    laboriousness_coefs.append(dev_skills[dev_skills_str])

    # adding dev skills to db
    db_record['dev_skills'] = float(rates_rus_mult.index(dev_skills_str) + 1)

    # experience with virtual machines
    vm_experience = {
        'Очень низкий': 1.21,
        'Низкий': 1.1,
        'Средний': 1.0,
        'Высокий': 0.9
    }
    vm_experience_str = st.select_slider('Опыт использования виртуальных машин', options=vm_experience)
    laboriousness_coefs.append(vm_experience[vm_experience_str])

    # adding experience with virtual machines to db
    db_record['vm_experience'] = float(rates_rus_man.index(vm_experience_str) + 1)

    # development experience in programming languages
    lang_experience = {
        'Очень низкий': 1.14,
        'Низкий': 1.07,
        'Средний': 1.0,
        'Высокий': 0.95
    }
    lang_experience_str = st.select_slider('Опыт разработки на языках программирования', options=lang_experience)
    laboriousness_coefs.append(lang_experience[lang_experience_str])

    # adding dev experience in programming languages to db
    db_record['language_experience'] = float(rates_rus_man.index(lang_experience_str) + 1)

    st.markdown("### Характеристики проекта")

    # application of software development methods
    dev_methods = {
        'Очень низкое': 1.24,
        'Низкое': 1.1,
        'Среднее': 1.0,
        'Высокое': 0.91,
        'Очень высокое': 0.82
    }
    dev_methods_str = st.select_slider('Применение методов разработки ПО', options=dev_methods)
    laboriousness_coefs.append(dev_methods[dev_methods_str])

    # adding dev methods to db
    db_record['dev_methods'] = rates_rus_third.index(dev_methods_str) + 1

    # using the software development toolkit
    toolkit_usage = {
        'Очень низкое': 1.24,
        'Низкое': 1.1,
        'Среднее': 1.0,
        'Высокое': 0.91,
        'Очень высокое': 0.83
    }
    toolkit_usage_str = st.select_slider('Использование инструментария разработки ПО', options=toolkit_usage)
    laboriousness_coefs.append(toolkit_usage[toolkit_usage_str])

    # adding toolkit usage to db
    db_record['toolkit_usage'] = rates_rus_third.index(toolkit_usage_str) + 1

    # development schedule requirements
    schedule_req = {
        'Очень низкие': 1.23,
        'Низкие': 1.08,
        'Средние': 1.0,
        'Высокие': 1.04,
        'Очень высокие': 1.1
    }
    schedule_req_str = st.select_slider('Требования соблюдения графика разработки', options=schedule_req)
    laboriousness_coefs.append(schedule_req[schedule_req_str])

    # adding schedule req to db
    db_record['schedule_req'] = rates_rus_mult.index(schedule_req_str) + 1

    if st.button('Нажмите, чтобы сохранить проект в базу данных'):
        columns = ', '.join(db_record.keys())
        placeholders = ':' + ', :'.join(db_record.keys())
        query = 'INSERT INTO projects (%s) VALUES (%s)' % (columns, placeholders)

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute(query, db_record)
        con.commit()

    st.markdown("## Итоговое значение метрики Cocomo")

    laboriousness = math.prod(laboriousness_coefs)
    metric_value = a * kloc ** b * laboriousness
    st.metric("Трудоемкость (в человеко-месяцах)", metric_value)


if __name__ == '__main__':
    app()
