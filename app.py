import os
import streamlit as st
from PIL import Image
import pandas as pd
from streamlit_option_menu import option_menu

# from wen import register
from wen.forms import form_examen, form_fast_check #motivos, habitos, enfermedades, fotos
# from wen.auth import authenticate
# from wen.register import register
# from wen.utils.bigquery import BigqueryConnector
from wen.location import location


#project_id = os.getenv('project_gcp_wen')
#db = os.getenv('database_gcp_wen')
logo_icon = Image.open("wen/images/logo_wen.ico")

def set_page_details():
    """
    Change Streamlit Page Settings 
    Hide MainMenu and footer, and reduce padding
    """
    st.set_page_config(page_title='WEN Dental', page_icon=logo_icon)
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    padding = 0
    st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

# def set_auth(select_login):    
#    authenticator = authenticate(select_login)
#    authentication_status, data_usr = authenticator.login('Login')
#    return authentication_status, data_usr

def set_register(select_register):    
    reg = register(select_register)
    authentication_status, data_usr = reg.sign_up()
    return authentication_status, data_usr


def set_form_exam(select_examen):
    exam = form_examen(select_examen)
    return exam

def set_form_motivos(exam):
    next_habitos = exam.form_motivos()
    return next_habitos

def set_form_habitos(exam):
    next_enfermedades = exam.form_habitos()
    return next_enfermedades

def set_form_enfermedades(exam):
    next_fotos = exam.form_enfermedades()
    return next_fotos

def set_form_fotos(exam):
    next_save = exam.form_fotos()
    return next_save

# def authenticator():
#    if 'select_login' not in st.session_state:
#        st.session_state['select_login'] = None
#    if 'select_register' not in st.session_state:
#        st.session_state['select_register'] = None

#    if st.session_state['authentication_status'] == None or st.session_state['authentication_status'] == False:

#        st.session_state['index'] = 0
#        selected3 = option_menu(None, ["Login", "Registro"], 
#            icons=['cloud-upload', "list-task"], 
#            menu_icon="cast", default_index=st.session_state['index'], orientation="horizontal",
#            styles={
#                "container": {"padding": "0!important", "background-color": "#fafafa"},
#                "icon": {"color": "green", "font-size": "25px"}, 
#                "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
#                "nav-link-selected": {"background-color": "black"},
#            }
#        )
#        st.markdown('#')
#        st.image("wen/images/logo_wen_horizontal.png", width=400)
#        st.markdown('#')

#        if selected3 == 'Login':
#            st.session_state['index'] = 0
#            st.session_state['select_login'] = True
#            st.session_state['select_register'] = False
#        if selected3 == 'Registro':
#            st.session_state['index'] = 1
#            st.session_state['select_register'] = True
#            st.session_state['select_login'] = False

        
#        if st.session_state['select_login']:
#            st.session_state['authentication_status'], st.session_state['data_usr'] = set_auth(st.session_state['select_login'])
#            if st.session_state['authentication_status'] == False:
#                st.error('Email/password incorrectas. Por favor intentelo de nuevo.')
        
#        if st.session_state['select_register']:
#            st.session_state['authentication_status'], st.session_state['data_usr'] = set_register(st.session_state['select_register'])
    
#    return st.session_state['authentication_status']


def set_location():
    if 'select_location' not in st.session_state:
        st.session_state['select_location'] = True
    loc = location(st.session_state['select_location'])
    actual_loc = loc.get_ubication()
    loc.show_map()
    return actual_loc


def take_exam(): 
    if 'select_examen' not in st.session_state:
        st.session_state['select_examen'] = True
    if 'next_motivos' not in st.session_state:
        st.session_state['next_motivos'] = None
    if 'next_habitos' not in st.session_state:
        st.session_state['next_habitos'] = None
    if 'next_enfermedades' not in st.session_state:
        st.session_state['next_enfermedades'] = None
    if 'next_fotos' not in st.session_state:
        st.session_state['next_fotos'] = None
    if 'next_save' not in st.session_state:
        st.session_state['next_save'] = None

    exam = set_form_exam(st.session_state['select_examen'])
    if st.session_state['select_examen']:
        st.session_state['next_habitos'] = set_form_motivos(exam)
    if st.session_state['next_habitos']:
        st.session_state['next_enfermedades'] = set_form_habitos(exam)
    if st.session_state['next_enfermedades']:
        st.session_state['next_fotos'] = set_form_enfermedades(exam)
    if st.session_state['next_fotos']:
        st.session_state['next_save'] = set_form_fotos(exam)


def main():
    set_page_details()

    if 'authentication_status' not in st.session_state:   
        st.session_state['authentication_status'] = None
    if 'select_examen' not in st.session_state:
        st.session_state['select_examen'] = None
    if 'selected' not in st.session_state:
        st.session_state['selected'] =  0
    if 'find_clinic' not in st.session_state:
        st.session_state['find_clinic'] = None
    if 'results' not in st.session_state:
        st.session_state['results'] = None
    if 'select_location' not in st.session_state:
        st.session_state['select_location'] = None
    
    #if st.session_state['authentication_status'] == True:
    with st.sidebar:
        st.sidebar.markdown('#')
        img_logo = Image.open("wen/images/logo_wen_horizontal.png")
        st.sidebar.image(img_logo)
        st.sidebar.markdown('#')
        selected = option_menu('Home', ['Exámen Rápido','Encuentra una Clinica'], 
            icons=['toothbrush','toothbrush'], default_index=st.session_state['selected'],
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "green", "font-size": "20px"}, 
                "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "black"},
            }
        )
    if selected == 'Exámen Rápido':
        st.session_state['selected'] = 0
        st.session_state['select_fast_check'] = True
        st.session_state['find_clinic'] = False
        st.session_state['results'] = False
    if selected == 'Mis resultados':
        st.session_state['selected'] = 0
        st.session_state['select_fast_check'] = False
        st.session_state['find_clinic'] = False
        st.session_state['results'] = True
    if selected == 'Encuentra una Clinica':
        st.session_state['selected'] = 1
        st.session_state['select_fast_check'] = False
        st.session_state['find_clinic'] = True
        st.session_state['results'] = False
    
    if st.session_state['find_clinic']:
        result = set_location()
        #st.write(result)
    
    if st.session_state['select_fast_check']:
        fast_exam = form_fast_check(st.session_state['select_fast_check'])
        st.session_state['select_fast_check'], st.session_state['results'] = fast_exam.form_exam()
    

        
    #if st.session_state['authentication_status'] != True:
    #    st.session_state['authentication_status'] = authenticator()

if __name__ ==  "__main__":
    main()