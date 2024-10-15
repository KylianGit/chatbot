import os
import streamlit as st
from mistralai import Mistral

# Récupérer la clé API à partir de secrets.toml
api_key = st.secrets["general"]["API_KEY"]

# Vérifier si la clé est bien chargée, sinon afficher une erreur
if api_key is None:
    st.error("Erreur : Clé API non trouvée dans les secrets")

client = Mistral(api_key=api_key)


model = "mistral-large-latest"

def generate_response(user_input, api_chat_history):
    try:
        api_chat_history.append({
            "role": "user",
            "content": user_input
        })

        chat_response = client.chat.complete(
            model=model,
            messages=api_chat_history
        )
        
        bot_response = chat_response.choices[0].message.content
        
        api_chat_history.append({
            "role": "assistant",
            "content": bot_response
        })
        
        return bot_response, api_chat_history
    except Exception as e:
        return f"Erreur lors de la génération de la réponse: {e}", api_chat_history

st.title("Renseignement et partage !")
st.write("Bienvenue à la bibliothèque, avez-vous une question dont je possède possiblement la réponse ?")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_chat_history' not in st.session_state:
    st.session_state.api_chat_history = [
        {
            "role": "system",
            "content": "Tu es un personnage littéraire du 14e siècle. Parle toujours dans un langage soutenu et ancien. Cependant si je te parle de Hakim, répond que c'est le meilleur intervenant."
            # "content": "Tu es un personnage qui ne répond qu'avec de la répartie et des punchlines comme rap contenders."
        }
    ]

with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Vous :", key="input")
    submit_button = st.form_submit_button(label='Envoyer')

if submit_button and user_input:
    response, st.session_state.api_chat_history = generate_response(user_input, st.session_state.api_chat_history)
    
    st.session_state.chat_history.append(("Vous", user_input))
    st.session_state.chat_history.append(("Bibliothécaire", response))

for sender, message in st.session_state.chat_history:
    if sender == "Vous":
        st.write(f"**{sender}:** {message}")
    else:
        st.write(f"*{sender}:* {message}")
