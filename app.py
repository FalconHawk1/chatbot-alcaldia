from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import random

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"message": "No user input provided."}), 400
    
    user_input = user_input.strip().lower()

    if user_input in ["hola", "buenas", "hey"]:
        return jsonify({"response": "¡Hola! ¿En qué puedo ayudarte? <br> Puedes preguntar por trámites o solicitar información sobre un trámite en específico."})
        

    # List of tramites
    if user_input in ["tramites", "trámites"]:
        tramites = fetch_all_tramites()
        if tramites:
            random_tramites = random.sample(tramites, 5)
            tramites_nombres = [t.get("nombre_com_n", "Trámite sin nombre") for t in random_tramites]
            return jsonify({"response": "Lista de trámites: \n " + "\n".join(tramites_nombres)})
        else:
            return jsonify({"response": "No se pudo obtener la lista de trámites."})

    if user_input.isdigit():
        tramite = fetch_tramite_info(user_input, "id")
        if tramite:
            return jsonify({
                "response": f"**Trámite Encontrado:**</br>"
                f"Nombre: {tramite.get('nombre_com_n', 'N/A')}</br>"
                f"Propósito: {tramite.get('prop_sito_del_tr_mite_u_otro', 'N/A')}</br>"
                f"Medio: {tramite.get('medio_por_donde_se_realiza', 'N/A')}</br>"
                f"Tiempo de obtención: {tramite.get('tiempo_obtenci_n', 'N/A')} {tramite.get('tiempo_obtenci_n_descripci_n', 'N/A')}</br>"
                f"URL: {tramite.get('url_del_visor_del_tr_mite', 'No disponible')}"
            })
        else:
            return jsonify({"response": "No se encontró ningún trámite con ese ID."})
    else:
        tramite = fetch_tramite_info(user_input, "name")
        if tramite:
            return jsonify({
                "response": f"**Trámite Encontrado:**\n"
                f"Nombre: {tramite.get('nombre_com_n', 'N/A')}\n"
                f"Propósito: {tramite.get('prop_sito_del_tr_mite_u_otro', 'N/A')}\n"
                f"Medio: {tramite.get('medio_por_donde_se_realiza', 'N/A')}\n"
                f"Tiempo de obtención: {tramite.get('tiempo_obtenci_n', 'N/A')} {tramite.get('tiempo_obtenci_n_descripci_n', 'N/A')}\n"
                f"URL: {tramite.get('url_del_visor_del_tr_mite', 'No disponible')}"
            })
        else:
            return jsonify({"response": "No se encontró ningún trámite con ese nombre."})

if __name__ == "__main__":
    # Running Flask in a separate thread
    app.run(debug=True, host="127.0.0.1", port=8000, threaded=True)
    # Running Telegram bot in the main thread (this should not block Flask)
