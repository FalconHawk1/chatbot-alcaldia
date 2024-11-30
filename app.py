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

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"message": "No user input provided."}), 400
    
    user_input = user_input.strip().lower()

    if user_input in [
        "hola", "buenas", "hey", "buenos dias", "buenas tardes", "buenas noches", "que tal", "como estas", "como va todo", 
        "todo bien", "saludos", "como te va", "que pasa", "que onda", "como te encuentras", "que hay", "que haces", 
    ]:
        return jsonify({"response": "¡Hola! ¿En qué puedo ayudarte? <br> Puedes preguntar por trámites o solicitar información sobre un trámite en específico."})

    if user_input in [
        "adios", "hasta luego", "nos vemos", "hasta pronto", "chau", "hasta mañana", "hasta la proxima", "adios amigo", 
        "hasta la vista", 
    ]:
        return jsonify({"response": "¡Adiós! Si necesitas más ayuda, no dudes en contactarnos nuevamente."})

    if user_input in [
        "horarios de atencion", "horarios", "cuales son los horarios", "cuando abren", "horarios de apertura", "cuando estan disponibles", 
        "qué horarios tienen", "a qué hora abren", "cuándo están abiertos", "que dias abren",
    ]:
        return jsonify({"response": "Nuestros horarios de atención son de lunes a viernes, de 9:00 AM a 6:00 PM."})

    if user_input in [
        "dónde están ubicados", "donde se encuentran", "cómo puedo llegar", "dónde es la oficina", "dónde está la sede", 
        "ubicación de la oficina", "cómo llegar a la oficina", "dirección de la oficina", 
    ]:
        return jsonify({"response": "Nuestra oficina está ubicada en la Calle Ficticia 123, Ciudad ABC. Puedes llegar fácilmente en transporte público o por carretera."})

    if user_input in [
        "qué trámites realizan", "qué servicios ofrecen", "qué tipo de trámites puedo hacer", "qué servicios tienen disponibles", 
        "qué tipo de trámites puedo gestionar", "cuáles son los servicios que ofrecen",
    ]:
        return jsonify({"response": "Ofrecemos trámites de inscripción, renovación de documentos, cambios de dirección, y otros servicios administrativos."})

    if user_input in [
        "información sobre trámites", "información sobre requisitos", "necesito saber los requisitos", "qué documentos necesito", 
        "qué papeles son necesarios", "requisitos para trámites", "qué necesito para hacer el trámite", 
    ]:
        return jsonify({"response": "Para realizar el trámite, necesitarás una copia de tu documento de identidad, comprobante de domicilio y un formulario llenado."})

    if user_input in [
        "cuánto cuesta", "costos de los trámites", "precio", "tarifas", "cuánto tengo que pagar", "cómo pago", 
        "cómo se realiza el pago", "tarifas de los servicios",
    ]:
        return jsonify({"response": "El costo de los trámites varía según el tipo de servicio. Por favor consulta nuestra página web o contáctanos para más detalles."})

    if user_input in [
        "cómo puedo pagar", "formas de pago", "qué formas de pago aceptan", "cómo pago el trámite", "puedo pagar con tarjeta", 
        "aceptan pagos en línea", "aceptan transferencias", "cómo realizar el pago",
    ]:
        return jsonify({"response": "Aceptamos pagos en línea, transferencia bancaria y pagos con tarjeta de crédito."})

    if user_input in [
        "hay algún descuento", "tienen descuentos", "tienen alguna oferta", "ofertas especiales", "descuentos para estudiantes", 
        "descuentos en trámites", "promociones", "tienen promociones",
    ]:
        return jsonify({"response": "Actualmente, ofrecemos un descuento del 10% para nuevos usuarios y promociones especiales en ciertos trámites."})

    if user_input in [
        "cómo contactar", "contacto", "quiero hablar con un agente", "quiero ayuda", "necesito asistencia", 
        "cómo me comunico", "quién me atiende", "cómo puedo hablar con alguien",
    ]:
        return jsonify({"response": "Puedes comunicarte con nosotros a través de nuestro correo electrónico contacto@empresa.com o llamando al (123) 456-7890."})

    if user_input in [
        "me pueden ayudar", "necesito soporte", "ayuda", "me pueden asistir", "pueden ayudarme", "quiero soporte", 
        "tengo dudas", "necesito una aclaración", "no entiendo bien",
    ]:
        return jsonify({"response": "Claro, ¿en qué te puedo ayudar? Cuéntame más sobre tu duda o problema y con gusto te asistiré."})

    if user_input in [
        "es posible hacer el trámite online", "puedo hacer el trámite en línea", "cómo hacer el trámite en línea", 
        "se puede hacer el trámite por internet", "puedo hacerlo online", 
    ]:
        return jsonify({"response": "Sí, la mayoría de nuestros trámites se pueden realizar de manera completamente online. Visita nuestra página web para más detalles."})

    if user_input in [
        "tienen algún número de teléfono", "cuál es el número de teléfono", "dónde puedo llamar", "teléfono de contacto", 
        "número de atención al cliente", "me puedes dar el número de teléfono", 
    ]:
        return jsonify({"response": "Puedes llamarnos al (123) 456-7890 para cualquier consulta o pregunta."})

    if user_input in [
        "cuánto tiempo tarda", "cuánto demora", "cuánto tiempo se tarda", "tiempo estimado", "cuánto tiempo debo esperar", 
        "cuando se resuelve", "cuánto se demora el trámite", 
    ]:
        return jsonify({"response": "El tiempo de procesamiento de trámites depende del tipo de servicio, pero generalmente oscila entre 2 y 5 días hábiles."})

    if user_input in [
        "dónde puedo encontrar más detalles", "quiero saber más sobre el servicio", "necesito más información", 
        "quiero más detalles sobre el trámite", "dónde puedo leer más", "información adicional", "dónde puedo consultar más",
    ]:
        return jsonify({"response": "Puedes obtener más información visitando nuestra página web o poniéndote en contacto con nosotros a través de los canales indicados."})

    if user_input in [
        "me pueden enviar un correo", "me mandan un correo", "quiero recibir más información por correo", "enviame un correo", 
        "me mandan un correo de confirmación", "me envían la información por email", 
    ]:
        return jsonify({"response": "Claro, ¿a qué dirección de correo electrónico te gustaría que te enviemos la información?"})




    # List of tramites
    if user_input in ["tramites", "trámites"]:
        tramites = fetch_all_tramites()
        if tramites:
            random_tramites = random.sample(tramites, 5)
            tramites_nombres = [t.get("nombre_com_n", "Trámite sin nombre") for t in random_tramites]
            return jsonify({"response": "Lista de trámites: </br> " + "</br>".join(tramites_nombres)})
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
                "response": f"**Trámite Encontrado:**</br>"
                f"Nombre: {tramite.get('nombre_com_n', 'N/A')}</br>"
                f"Propósito: {tramite.get('prop_sito_del_tr_mite_u_otro', 'N/A')}</br>"
                f"Medio: {tramite.get('medio_por_donde_se_realiza', 'N/A')}</br>"
                f"Tiempo de obtención: {tramite.get('tiempo_obtenci_n', 'N/A')} {tramite.get('tiempo_obtenci_n_descripci_n', 'N/A')}</br>"
                f"URL: {tramite.get('url_del_visor_del_tr_mite', 'No disponible')}"
            })
        else:
            return jsonify({"response": "No se encontró ningún trámite con ese nombre."})

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000, threaded=True)
