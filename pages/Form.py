import streamlit as st
import pandas as pd
import time

from processing.Model import recommend_profiles

st.set_page_config(page_title = "Formulaire de recommandation de profils Linkedin", layout = "wide")

st.title("Formulaire")

@st.cache_data
def load_dataset(dataset_path):
  return pd.read_csv(dataset_path)

def showDataset(dataset, index):
  st.dataframe(dataset, use_container_width = st.session_state.use_container_width)

with st.spinner('Chargement des données en cours...'):
  updated_df_simple = load_dataset('./data/updated_linkedin_simple_data.csv')
  updated_df = load_dataset('./data/updated_linkedin_data.csv')


st.markdown("""
  <style>
    .st-cr, .st-df {
      cursor: pointer !important;
    }
    .css-1rtsdbg:hover, .css-1rtsdbg:active {
      background-color: #005A9C !important;
      color: #FFFFFF !important;
      border: none !important;
    }
    .css-1a5dplj:hover:enabled, .css-1a5dplj:focus:enabled, .css-1rtsdbg:focus:not(:active) {
      background-color: #005A9C !important;
      color: #FFFFFF !important;
      border: none !important;
    }
    .st-eu {
      background-color: #005A9C !important;
      border: none !important
    }
    .stButton {
      height: 35px;
    }
    .css-xclnog {
      border-color: rgb(0, 90, 156, 1) rgba(0, 0, 0, 0.2) rgba(0, 0, 0, 0.2) !important;
    }
    .st-bz, .st-c0, .st-c1, .st-c2 {
      border: none !important;
    }
  </style>
""", unsafe_allow_html = True)

with st.form("my_form"):
  cols1 = st.columns(3)
  age_estimate = cols1[0].number_input("Age :", value = 32, min_value = 1)
  company_follower_count = cols1[1].number_input("Nombre de followers de l'entreprise :", value = 1000, min_value = 1)
  company_staff_count = cols1[2].number_input("Nombre d'employés de l\'entreprise :", value = 1200, min_value = 1)
  
  st.write("\n")
  cols2 = st.columns(3)
  connections_count = cols2[0].number_input("Nombre de connections linkedin de l'employé :", value = 500, min_value = 1)
  followers_count = cols2[1].number_input("Nombre de followers de l'employé :", value = 300, min_value = 1)
  avg_employee_job_duration = cols2[2].number_input("Durée moyenne du contrat de l'employé en années :", value = 3, min_value = 1)

  companies_name = {1: "Atlassian", 2: "IBM", 3: "Paypal", 4: "Nestlé", 5: "WiseTech Global", 6: "Canva"}
  employees_location = {1: "Sydney", 2: "Melbourne", 3: "Newtown", 4: "Oatlands", 5: "Wangaratta", 6: "Carlton"}
  employee_title = {1: "Data Scientist", 2: "Project Manager", 3: "Marketing Manager", 4: "Software Engineer", 5: "Web Developer", 6: "Research Leader"}
   
  def format_companies_name(option):
    return companies_name[option]
   
  def format_employees_location(option):
    return employees_location[option]
  
  def format_employee_title(option):
    return employee_title[option]
  
  st.write("\n")
  cols3 = st.columns(3)
  avg_company_job_duration = cols3[0].number_input("Durée moyenne des contrats de l'entreprise en années :", value = 3, min_value = 1)
  selected_companies_name = cols3[1].selectbox("Nom de l'entreprise :", options = companies_name.keys(), format_func = format_companies_name, index = 0)
  selected_job_location = cols3[2].selectbox("Lieux de travail :", options = employees_location.keys(), format_func = format_employees_location, index = 0)
  
  st.write("\n")
  cols4 = st.columns(3)
  selected_job_title = cols4[0].selectbox("Intitulé du job recherché :", options = employee_title.keys(), format_func = format_employee_title, index = 0)
  selected_employee_location = cols4[1].selectbox("Adresse de résidence de l'employé :", options = employees_location.keys(), format_func = format_employees_location, index = 0)
  selected_employee_title = cols4[2].selectbox("Intitulé du job de l'employé :", options = employee_title.keys(), format_func = format_employee_title, index = 0)

  st.write("\n")
  submitted = st.form_submit_button("Valider")

if submitted:
  new_job = {
    'ageEstimate': age_estimate, 'companyFollowerCount': company_follower_count, 'companyStaffCount': company_staff_count, 
    'connectionsCount': connections_count, 'followersCount': followers_count, 'avgEmployeeJobDuration': avg_employee_job_duration, 
    'avgCompanyJobDuration': avg_employee_job_duration, 'companyName': companies_name[selected_companies_name], 
    'employeeLocation': employees_location[selected_employee_location], 'employeeTitle': employee_title[selected_employee_title],
    'jobLocation': employees_location[selected_job_location], 'jobTitle': employee_title[selected_job_title]
  }

  with st.spinner('Calcul des recommandations en cours...'):
    recommended_profiles = recommend_profiles(updated_df_simple, new_job, 5)
    filtered_recommended_profiles = updated_df.loc[list(recommended_profiles.index)]
  
  st.subheader("Profils Recommandés")
  st.checkbox("Utiliser la largeur du conteneur", value = True, key = "use_container_width")
  showDataset(filtered_recommended_profiles, 1)
  st.markdown(f"Le dataset contient {len(filtered_recommended_profiles)} lignes et {len(filtered_recommended_profiles.columns)} colonnes. ")
  st.balloons()
