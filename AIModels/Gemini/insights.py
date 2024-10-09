"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os, random
import google.generativeai as genai

genai.configure(api_key="AIzaSyAvTPooV8-J4AQOB9p2P0ZRbVsbhccDF3k")

# def upload_to_gemini(path, mime_type=None):
#   """Uploads the given file to Gemini.

#   See https://ai.google.dev/gemini-api/docs/prompting_with_media
#   """
#   file = genai.upload_file(path, mime_type=mime_type)
#   print(f"Uploaded file '{file.display_name}' as: {file.uri}")
#   return file

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro-002",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# # TODO Make these files available on the local file system
# # You may need to update the file paths
# files = [
#   upload_to_gemini("Unknown File", mime_type="application/octet-stream"),
# ]

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "I feel nauseous and headache, recommend something",
      ],
    },
    {
      "role": "user",
      "parts": [
        "I have a headache, suggest something",
      ],
    },
    {
      "role": "model",
      "parts": [
        "It sounds unpleasant.  Since I'm not a medical professional, I can't give medical advice.  However, I can offer some general suggestions for dealing with headaches,  but **it's crucial to see a doctor if your headache is severe, sudden, or accompanied by other symptoms like fever, stiff neck, vision changes, numbness, or confusion.**\n\nHere are some things you could try:\n\n* **Rest in a quiet, dark room:** Light and noise can often worsen headaches.\n* **Hydrate:** Dehydration can contribute to headaches. Drink plenty of water.\n* **Over-the-counter pain relievers:**  Ibuprofen or acetaminophen can be helpful. Follow the dosage instructions on the package.\n* **Cool compress:** Applying a cold pack or a damp cloth to your forehead can provide some relief.\n* **Warm compress:** Alternatively, a warm compress or a warm bath might help relax tense muscles.\n* **Gentle massage:** Massaging your temples or the back of your neck might ease tension.\n* **Caffeine:**  A small amount of caffeine (like in coffee or tea) can sometimes help, but too much can make headaches worse.\n* **Avoid triggers:** If you know certain things trigger your headaches (like certain foods, stress, or strong smells), try to avoid them.\n\n\nIf your headache persists or worsens, please seek medical attention.  They can properly diagnose the cause and recommend the best course of treatment.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "hey chat, how are you today\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "I'm doing well, thank you for asking! As a large language model, I don't experience emotions or have days in the same way humans do, but I'm functioning optimally and ready to assist you. How can I help you today?\n",
      ],
    },
  ]
)

def generate_insights(user_input="", medical_history=""):
    prompt1 = f"Based on the patient's {medical_history} history, provide general wellness tips. Focus on maintaining a balanced diet, staying active, and managing stress. Ensure the advice is universally applicable and non-medical."
    prompt2 = f"Based on the patient's {medical_history} history and problem description: {user_input}, provide general wellness tips. Focus on maintaining a balanced diet, staying active, and managing stress. Ensure the advice is universally applicable and non-medical."
    prompt3 = f"Offer healthy living suggestions tailored to the patient’s input: {user_input} and medical history {medical_history}, emphasizing lifestyle changes like sleep hygiene, hydration, and physical activity, while avoiding medical-specific advice."
    prompt4 = f"Provide insights on the connection between mental well-being and physical health. Include practical advice on mindfulness, relaxation techniques, and managing emotions. Include a fun fact related to health or wellness that can inspire the patient to pursue healthier living habits."
    prompt5 = f"Based on the user’s description of their issue and their medical history, provide personalized yet general wellness advice. Focus on maintaining good health practices like stretching, posture improvement, or low-impact activities. Offer self-care tips to encourage patients to take care of themselves mentally and physically, emphasizing relaxation and personal time."
    prompt6 = f"Give seasonal wellness tips related to current climate or time of year in the US, such as hydration during summer or immune-boosting tips during winter."

    random_prompts = [prompt4, prompt5, prompt6]

    def select_prompt(user_input, medical_history):
        # Check conditions for each prompt
        if user_input == "" and medical_history != "":
            return prompt1
        elif user_input != "" and medical_history != "":
            return prompt2
        elif user_input != "" and medical_history == "":
            return prompt3
        elif user_input == "" and medical_history == "":
            # Select a random prompt from the remaining ones
            return random.choice(random_prompts)

    prompt = select_prompt(user_input=user_input, medical_history=medical_history)

    response = chat_session.send_message(prompt)

    funresponse = ""

    if response:
        return response.text
    else:
        return funresponse
    