from flask import Flask, request, jsonify
import requests
import telebot
from dotenv import load_dotenv
import random

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Get the token from the environment variable
#TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_TOKEN = "7749454915:AAHelKrNwA3uBeKYhJ4oGOabBFiza-Arqvs"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

API_URL = "https://www.datos.gov.co/resource/mntw-htj4.json?municipio=SOGAMOSO"

def fetch_all_tramites():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def fetch_tramite_info(query, query_type="name"):
    tramites = fetch_all_tramites()
    for tramite in tramites:
        if query_type == "id" and tramite.get("n_mero_nico") == query:
            return tramite
        elif query_type == "name" and query.lower() in tramite.get("nombre_com_n", "").lower():
            return tramite
    return None

# Text message handler with predefined responses
@bot.message_handler(content_types=["text"])
def bot_mensajes_texto(message):
    # Define your predefined responses
    user_input = message.text.strip().lower()

    # Predefined responses
    if user_input in ["hola", "buenas", "hey"]:
        bot.send_message(message.chat.id, "¡Hola! ¿En qué puedo ayudarte?")
        return

    # List of tramites
    if user_input in ["tramites", "trámites"]:
        tramites = fetch_all_tramites()
        if tramites:
            random_tramites = random.sample(tramites, 5)
            tramites_nombres = [t.get("nombre_com_n", "Trámite sin nombre") for t in random_tramites]
            bot.send_message(message.chat.id, "Lista de trámites:\n" + "\n".join(tramites_nombres))
        else:
            bot.send_message(message.chat.id, "No se pudo obtener la lista de trámites.")
        return

    if user_input.isdigit():
        tramite = fetch_tramite_info(user_input, "id")
        if tramite:
            bot.send_message(
                message.chat.id,
                f"**Trámite Encontrado:**\n"
                f"Nombre: {tramite.get('nombre_com_n', 'N/A')}\n"
                f"Propósito: {tramite.get('prop_sito_del_tr_mite_u_otro', 'N/A')}\n"
                f"Medio: {tramite.get('medio_por_donde_se_realiza', 'N/A')}\n"
                f"Tiempo de obtención: {tramite.get('tiempo_obtenci_n', 'N/A')} {tramite.get('tiempo_obtenci_n_descripci_n', 'N/A')}\n"
                f"URL: {tramite.get('url_del_visor_del_tr_mite', 'No disponible')}"
            )
        else:
            bot.send_message(message.chat.id, "No se encontró ningún trámite con ese ID.")
    else:
        tramite = fetch_tramite_info(user_input, "name")
        if tramite:
            bot.send_message(
                message.chat.id,
                f"**Trámite Encontrado:**\n"
                f"Nombre: {tramite.get('nombre_com_n', 'N/A')}\n"
                f"Propósito: {tramite.get('prop_sito_del_tr_mite_u_otro', 'N/A')}\n"
                f"Medio: {tramite.get('medio_por_donde_se_realiza', 'N/A')}\n"
                f"Tiempo de obtención: {tramite.get('tiempo_obtenci_n', 'N/A')} {tramite.get('tiempo_obtenci_n_descripci_n', 'N/A')}\n"
                f"URL: {tramite.get('url_del_visor_del_tr_mite', 'No disponible')}"
            )
        else:
            bot.send_message(message.chat.id, "No se encontró ningún trámite con ese nombre.")
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"message": "No user input provided."}), 400
    
    user_input = user_input.text.strip().lower()

    if user_input in ["hola", "buenas", "hey"]:
        return jsonify({"response": "¡Hola! ¿En qué puedo ayudarte?"});
        

    # List of tramites
    if user_input in ["tramites", "trámites"]:
        tramites = fetch_all_tramites()
        if tramites:
            random_tramites = random.sample(tramites, 5)
            tramites_nombres = [t.get("nombre_com_n", "Trámite sin nombre") for t in random_tramites]
            return jsonify({"Lista de trámites:\n" + "\n".join(tramites_nombres)})
        else:
            return jsonify({"No se pudo obtener la lista de trámites."})

    if user_input.isdigit():
        tramite = fetch_tramite_info(user_input, "id")
        if tramite:
            return jsonify({
                f"**Trámite Encontrado:**\n"
                f"Nombre: {tramite.get('nombre_com_n', 'N/A')}\n"
                f"Propósito: {tramite.get('prop_sito_del_tr_mite_u_otro', 'N/A')}\n"
                f"Medio: {tramite.get('medio_por_donde_se_realiza', 'N/A')}\n"
                f"Tiempo de obtención: {tramite.get('tiempo_obtenci_n', 'N/A')} {tramite.get('tiempo_obtenci_n_descripci_n', 'N/A')}\n"
                f"URL: {tramite.get('url_del_visor_del_tr_mite', 'No disponible')}"
            })
        else:
            return jsonify({"No se encontró ningún trámite con ese ID."})
    else:
        tramite = fetch_tramite_info(user_input, "name")
        if tramite:
            return jsonify({
                f"**Trámite Encontrado:**\n"
                f"Nombre: {tramite.get('nombre_com_n', 'N/A')}\n"
                f"Propósito: {tramite.get('prop_sito_del_tr_mite_u_otro', 'N/A')}\n"
                f"Medio: {tramite.get('medio_por_donde_se_realiza', 'N/A')}\n"
                f"Tiempo de obtención: {tramite.get('tiempo_obtenci_n', 'N/A')} {tramite.get('tiempo_obtenci_n_descripci_n', 'N/A')}\n"
                f"URL: {tramite.get('url_del_visor_del_tr_mite', 'No disponible')}"
            })
        else:
            return jsonify({"No se encontró ningún trámite con ese nombre."})

if __name__ == "__main__":

    bot.infinity_polling()