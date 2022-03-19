import streamlit as st


class MultiPage:
    """
    Class for combining multiple streamlit applications
    """

    def __init__(self) -> None:
        self.pages = []  # applications list

    def add_page(self, title: str, func) -> None:
        """
        adding page to the project
        :param title: the title of page
        :param func: python function to render this page in streamlit
        :return: None
        """
        self.pages.append({
            "title": title,
            "function": func
        })

    def run(self):
        # selecting the page to run with selectbox
        page = st.sidebar.selectbox(
            'Navigation',
            self.pages,
            format_func=lambda cur_page: cur_page['title']
        )

        # run the app function
        page['function']()
