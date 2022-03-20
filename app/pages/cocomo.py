import math
import streamlit as st
import json


def app():
    st.markdown("# Посдсчет метрики COCOMO")
    proj_type_rus = st.selectbox(
        'Выберите тип проекта',
        (
            'Органический',
            'Полуразделенный',
            'Встроенный'
        )
    )

    proj_types_mapping = {
        'Органический': (3.2, 1.05),
        'Полуразделенный': (3.0, 1.12),
        'Встроенный': (2.8, 1.2)
    }

    a, b = proj_types_mapping[proj_type_rus]

    kloc = st.number_input(
        'Введите оценочный размер программы',
        help='В тысячах строк исходного кода',
        min_value=0, step=None
    )

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

    # dbms size slider
    dbms_size = {
        'Низкий': 0.94,
        'Средний': 1.0,
        'Высокий': 1.08,
        'Очень высокий': 1.16
    }
    dbms_size_str = st.select_slider('Размер базы данных приложения', options=dbms_size)
    laboriousness_coefs.append(dbms_size[dbms_size_str])

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

    # memory limits slider
    memory_limits = {
        'Средние': 1.0,
        'Высокие': 1.06,
        'Очень высокие': 1.21,
        'Критические': 1.56
    }
    memory_limits_str = st.select_slider('Ограничения памяти', options=memory_limits)
    laboriousness_coefs.append(memory_limits[memory_limits_str])

    # instability of the virtual machine environment slider
    vm_instability = {
        'Низкая': 0.87,
        'Средняя': 1.0,
        'Высокая': 1.15,
        'Очень высокая': 1.3
    }
    vm_instability_str = st.select_slider('Неустойчивость окружения виртуальной машины', options=vm_instability)
    laboriousness_coefs.append(vm_instability[vm_instability_str])

    # required recovery time slider
    recovery_time = {
        'Низкая': 0.87,
        'Средняя': 1.0,
        'Высокая': 1.07,
        'Очень высокая': 1.15
    }
    recovery_time_str = st.select_slider('Требуемое время восстановления', options=recovery_time)
    laboriousness_coefs.append(recovery_time[recovery_time_str])

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

    # experience with virtual machines
    vm_experience = {
        'Очень низкий': 1.21,
        'Низкий': 1.1,
        'Средний': 1.0,
        'Высокий': 0.9
    }
    vm_experience_str = st.select_slider('Опыт использования виртуальных машин', options=vm_experience)
    laboriousness_coefs.append(vm_experience[vm_experience_str])

    # development experience in programming languages
    lang_experience = {
        'Очень низкий': 1.14,
        'Низкий': 1.07,
        'Средний': 1.0,
        'Высокий': 0.95
    }
    lang_experience_str = st.select_slider('Опыт разработки на языках программирования', options=lang_experience)
    laboriousness_coefs.append(lang_experience[lang_experience_str])

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

    st.markdown("## Итоговое значение метрики Cocomo")

    laboriousness = math.prod(laboriousness_coefs)
    metric_value = a * kloc ** b * laboriousness
    st.metric("Трудоемкость (в человеко-месяцах)", metric_value)

    with open('config.json') as f:
        config = json.load(f)
    config['cocomo'] = metric_value
    with open('config.json', 'w') as f:
        json.dump(config, f)

if __name__ == '__main__':
    app()
