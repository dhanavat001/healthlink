import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import pickle
from sklearn.preprocessing import LabelEncoder
import os

# Get the absolute path of the current directory where the integration file is located
current_dir = os.path.dirname(os.path.abspath(__file__))






nltk.download('stopwords')
nltk.download('punkt')
nltk.download("punkt_tab")
# Define stopwords and unnecessary phrases
stop_words = set(stopwords.words('english'))
unnecessary_phrases = ['please', 'kindly', 'doctor', 'feeling', 'having', 'like', 'i feel', 'i have', 'symptom', 'feeling', 'suffering from']

# Construct the full path to the model file
disease_model_path = os.path.join(current_dir, 'best_knn_model.pkl')
disease_dataset = os.path.join(current_dir, 'healthcare.csv') 

doctor_model_path = os.path.join(current_dir, 'best_random_forest_model.pkl')
doctor_dataset = os.path.join(current_dir, 'Specialist.xlsx') 

doctor_df = pd.read_excel(doctor_dataset)
disease_df = pd.read_csv(disease_dataset)


# Function to predict top 3 probable diseases
def predict_disease(patient_input):
    symptoms = disease_df.columns[:-1].tolist()

    label_encoder = LabelEncoder()
    label_encoder.fit(disease_df['prognosis']) 

    with open(disease_model_path, "rb") as model_file:
        model = pickle.load(model_file)


    # Clean and match symptoms
    def clean_input(user_input):
        user_input = user_input.lower()
        
        # Remove unnecessary phrases
        for phrase in unnecessary_phrases:
            user_input = user_input.replace(phrase, "")
        
        # Tokenize and remove stopwords
        tokens = nltk.word_tokenize(user_input)
        cleaned_tokens = [token for token in tokens if token not in stop_words]
        
        return cleaned_tokens

    def match_symptoms(user_input, symptoms):
        cleaned_tokens = clean_input(user_input)
        matched_symptoms = []
        
        for symptom in symptoms:
            for token in cleaned_tokens:
                if token in symptom.replace("_", " ").lower():
                    matched_symptoms.append(symptom)
                    break
                    
        return matched_symptoms

    # Create input vector for model based on matched symptoms
    def create_input_vector(matched_symptoms, symptoms):
        input_vector = [0] * len(symptoms)  # Initialize input vector with zeros
        for symptom in matched_symptoms:
            if symptom in symptoms:
                idx = symptoms.index(symptom)
                input_vector[idx] = 1  # Set 1 for matched symptoms
        return input_vector

    # Clean and match symptoms
    matched_symptoms = match_symptoms(patient_input, symptoms)
    
    if not matched_symptoms:
        return "No matching symptoms found."
    
    # Create input vector for model based on matched symptoms
    input_vector = create_input_vector(matched_symptoms, symptoms)
    input_df = pd.DataFrame([input_vector], columns=symptoms)

    # Predict using the model
    predicted_probs = model.predict_proba(input_df)[0]
    
    # Get top 3 most probable diseases
    n = 3
    top_n_predictions = np.argsort(predicted_probs)[-n:][::-1]
    
    # Convert predicted disease numbers back to text
    predicted_diseases = label_encoder.inverse_transform(top_n_predictions)
    
    # Display predictions
    results = []
    for i, disease in enumerate(predicted_diseases):
        results.append(f"Suggestion {i+1}: {disease}")
    
    return results


def predict_doctor(patient_input):
    symptoms = doctor_df.columns[:-1].tolist()

    label_encoder = LabelEncoder()
    label_encoder.fit(doctor_df['Doctor']) 

    symptoms = doctor_df.columns[:-1].tolist()

    # Load the trained model 
    with open(doctor_model_path, "rb") as model_file:
        model = pickle.load(model_file)

    
    # Clean and match symptoms
    def clean_input(user_input):
        user_input = user_input.lower()
        
        # Remove unnecessary phrases
        for phrase in unnecessary_phrases:
            user_input = user_input.replace(phrase, "")
        
        # Tokenize and remove stopwords
        tokens = nltk.word_tokenize(user_input)
        cleaned_tokens = [token for token in tokens if token not in stop_words]
        
        return cleaned_tokens

    def match_symptoms(user_input, symptoms):
        cleaned_tokens = clean_input(user_input)
        matched_symptoms = []
        
        for symptom in symptoms:
            for token in cleaned_tokens:
                if token in symptom.replace("_", " ").lower():
                    matched_symptoms.append(symptom)
                    break
                    
        return matched_symptoms

    # Create input vector for model based on matched symptoms
    def create_input_vector(matched_symptoms, symptoms):
        input_vector = [0] * len(symptoms)  # Initialize input vector with zeros
        for symptom in matched_symptoms:
            if symptom in symptoms:
                idx = symptoms.index(symptom)
                input_vector[idx] = 1  # Set 1 for matched symptoms
        return input_vector


    # Clean and match symptoms
    matched_symptoms = match_symptoms(patient_input, symptoms)
    
    if not matched_symptoms:
        return "No matching symptoms found."
    
    input_vector = create_input_vector(matched_symptoms, symptoms)

    input_df = pd.DataFrame([input_vector], columns=symptoms)

    predicted_doctor_num = model.predict(input_df)[0]

    print(predicted_doctor_num)
    predicted_doctor = label_encoder.inverse_transform([predicted_doctor_num])

    print(f"Predicted Doctor: {predicted_doctor}")

    # Predict using the model
    predicted_probs = model.predict_proba(input_df)[0]
    
    # Get top 3 most probable doctors
    n = 3
    top_n_predictions = np.argsort(predicted_probs)[-n:][::-1]
    
    # Convert predicted disease numbers back to text
    predicted_doctors = label_encoder.inverse_transform(top_n_predictions)
    
    # Display predictions
    results = []
    for i, doctor in enumerate(predicted_doctors):
        results.append(f"Suggestion {i+1}: {doctor}")
    
    return results