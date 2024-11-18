import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import requests

# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Get the working directory of the script
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load the saved models
diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))

# Diagnosis results (initialized as None)
diab_diagnosis = None
heart_diagnosis = None
parkinsons_diagnosis = None
# disease_type = None

# Function to fetch nearby hospitals
def fetch_nearby_hospitals(latitude, longitude,disease_type):
    """
    Fetch top 5 nearby hospitals sorted by rating using a hardcoded API URL.
    """
    disease_keywords = {
        'diabetes': 'diabetes doctor',
        'heart': 'heart doctor',
        'parkinsons': "Parkinson's disease doctor"
    }
    
    # Get the keyword for the selected disease type
    keyword = disease_keywords.get(disease_type, 'doctor')

    st.write(keyword)
    api_url = f"https://maps.gomaps.pro/maps/api/place/nearbysearch/json?keyword={keyword}&location={latitude},{longitude}&radius=5000&key=AlzaSyBPrvZF2bklzIgtDAxwtjqQ2duiHG9PELN"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            hospitals = sorted(
                data.get('results', []),
                key=lambda x: x.get('rating', 0),
                reverse=True
            )[:5]
            return hospitals
        else:
            st.error(f"Error: Unable to fetch hospital data. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    return None

# Sidebar for navigation
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',
                           ['Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Parkinsons Prediction'],
                           menu_icon='hospital-fill',
                           icons=['activity', 'heart', 'person'],
                           default_index=0)

# Disease prediction logic
if selected == 'Diabetes Prediction':
    disease_type = 'diabetes'
    st.title('Diabetes Prediction using ML')
    # User input for diabetes prediction
    col1, col2, col3 = st.columns(3)
    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')
    with col2:
        Glucose = st.text_input('Glucose Level')
    with col3:
        BloodPressure = st.text_input('Blood Pressure value')
    with col1:
        SkinThickness = st.text_input('Skin Thickness value')
    with col2:
        Insulin = st.text_input('Insulin Level')
    with col3:
        BMI = st.text_input('BMI value')
    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
    with col2:
        Age = st.text_input('Age of the Person')

    diab_diagnosis = ''
    if st.button('Diabetes Test Result'):
        try:
            user_input = [float(x) for x in [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                                             BMI, DiabetesPedigreeFunction, Age]]
            diab_prediction = diabetes_model.predict([user_input])
            diab_diagnosis = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'
            st.success(diab_diagnosis)
        except ValueError:
            st.error("Please provide valid numeric inputs for all fields.")


elif selected == 'Heart Disease Prediction':
    disease_type='heart'
    st.title('Heart Disease Prediction using ML')
    # User input for heart disease prediction
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.text_input('Age')
    with col2:
        sex = st.text_input('Sex')
    with col3:
        cp = st.text_input('Chest Pain types')
    with col1:
        trestbps = st.text_input('Resting Blood Pressure')
    with col2:
        chol = st.text_input('Serum Cholesterol in mg/dl')
    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')
    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')
    with col3:
        exang = st.text_input('Exercise Induced Angina')
    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')
    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')
    with col3:
        ca = st.text_input('Major vessels colored by fluoroscopy')
    with col1:
        thal = st.text_input('Thal: 0 = normal; 1 = fixed defect; 2 = reversible defect')

    heart_diagnosis = ''
    if st.button('Heart Disease Test Result'):
        try:
            user_input = [float(x) for x in [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang,
                                             oldpeak, slope, ca, thal]]
            heart_prediction = heart_disease_model.predict([user_input])
            heart_diagnosis = 'The person is having heart disease' if heart_prediction[0] == 1 else 'The person does not have any heart disease'
            st.success(heart_diagnosis)
        except ValueError:
            st.error("Please provide valid numeric inputs for all fields.")

elif selected == "Parkinsons Prediction":
    disease_type = 'parkinsons'
    st.title("Parkinson's Disease Prediction using ML")
    # User input for Parkinson's prediction
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')
    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')
    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')
    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)')
    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')
    with col1:
        RAP = st.text_input('MDVP:RAP')
    with col2:
        PPQ = st.text_input('MDVP:PPQ')
    with col3:
        DDP = st.text_input('Jitter:DDP')
    with col4:
        Shimmer = st.text_input('MDVP:Shimmer')
    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')
    with col1:
        APQ3 = st.text_input('Shimmer:APQ3')
    with col2:
        APQ5 = st.text_input('Shimmer:APQ5')
    with col3:
        APQ = st.text_input('MDVP:APQ')
    with col4:
        DDA = st.text_input('Shimmer:DDA')
    with col5:
        NHR = st.text_input('NHR')
    with col1:
        HNR = st.text_input('HNR')
    with col2:
        RPDE = st.text_input('RPDE')
    with col3:
        DFA = st.text_input('DFA')
    with col4:
        spread1 = st.text_input('spread1')
    with col5:
        spread2 = st.text_input('spread2')
    with col1:
        D2 = st.text_input('D2')
    with col2:
        PPE = st.text_input('PPE')

    parkinsons_diagnosis = ''
    if st.button("Parkinson's Test Result"):
        try:
            user_input = [float(x) for x in [fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP,
                                             Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR,
                                             RPDE, DFA, spread1, spread2, D2, PPE]]
            parkinsons_prediction = parkinsons_model.predict([user_input])
            parkinsons_diagnosis = "The person has Parkinson's disease" if parkinsons_prediction[0] == 1 else "The person does not have Parkinson's disease"
            st.success(parkinsons_diagnosis)
        except ValueError:
            st.error("Please provide valid numeric inputs for all fields.")

# Add Hospital Locator section (outside sidebar)
st.title("Hospital Locator")

# User input for latitude and longitude
latitude = st.text_input("Enter your latitude")
longitude = st.text_input("Enter your longitude")

# Fetch hospitals when button is clicked
if st.button("Search Doctors"):
    try:
        lat = float(latitude)
        lon = float(longitude)
        # st.write(disease_type)
        hospitals = fetch_nearby_hospitals(lat, lon,disease_type)
        if hospitals:
            st.subheader(f"Top 5 Nearby {disease_type} Doctors (Sorted by Rating)")
            for i, hospital in enumerate(hospitals, 1):
                st.write(f"**{i}. {hospital.get('name', 'N/A')}**")
                st.write(f"   - Rating: {hospital.get('rating', 'N/A')}")
                st.write(f"   - Address: {hospital.get('vicinity', 'N/A')}")
        else:
            st.error("No hospitals found near the given location.")
    except ValueError:
        st.error("Please provide valid numeric latitude and longitude.")
