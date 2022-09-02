import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
import pyaudio

# Visualizar opciones de voces
"""engine = pyttsx3.init()
for voz in engine.getProperty("voices"):
    print(voz)"""

id1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"


# Escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():

    # Almacenar recognizer en variable
    r = sr.Recognizer()

    # Configurar el microfono
    with sr.Microphone() as origen:
        # Tiempo de espera
        r.pause_threshold = 0.8
        # Informar que comenzo la grabación
        print("Ya puedes hablar")
        # Guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # Buscar en Google
            pedido = r.recognize_google(audio, language="es-ar")
            # Prueba de que pudo ingresar
            print("Dijiste: " + pedido)
            # Devolver pedido
            return pedido

        # En caso de que no comprenda el audio
        except sr.UnknownValueError:
            # Prueba de que no comprendio el audio
            print("Ups, no entendí")
            # Devolver error
            return "Sigo esperando"

        # En caso de no resolver el pedido
        except sr.RequestError:
            # Prueba de que no comprendio el audio
            print("Ups, no hay servicio")
            # Devolver error
            return "Sigo esperando"

        # Error inesperado
        except:
            # Prueba de que no comprendio el audio
            print("Ups, algo salio mal")
            # Devolver error
            return "Sigo esperando"


# Función para que el asistente pueda ser escuchado
def hablar(mensaje):
    #  Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", id1)
    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# Informar el día de la semana
def pedir_dia():
    # Crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)
    # Crear variable para el día de la semana
    dia_semana = dia.weekday()
    print(dia_semana)
    # Diccionario con los nombres de los días
    calendario = {0: "Lunes",
                  1: "Martes",
                  2: "Miércoles",
                  3: "Jueves",
                  4: "Viernes",
                  5: "Sábado",
                  6: "Domingo"}

    # Decir el día de la semana
    hablar(f"Hoy es {calendario[dia_semana]}, {dia.today()}")


# Informar que hora es
def pedir_hora():
    # Crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f"En este momento son las, {hora.hour} horas, con {hora.minute} minutos"
    print(hora)
    # Decir la hora
    hablar(hora)


# Función saludo inicial
def saludo_inicial():
    # Crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13: # Simplificado de: hora.hour >= 6 and hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"

    # Decir saludo
    hablar(f"""{momento}, soy la Katerin, tu asistente personal, 
    por favor, dime en que te puedo ayudar """)
    '''pedir_dia()
    pedir_hora()'''


# Función central del asistente
def pedir():
    # Activar el saludo inicial
    saludo_inicial()

    # Variable de corte
    comenzar = True
    while comenzar:
        # Activar el microfono y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if "abrir" and "youtube" in pedido:
            hablar("Con gusto, ya le abro YouTube")
            webbrowser.open("https://www.youtube.com/")
            continue
        elif "abrir" and "navegador" in pedido:
            hablar("""Claro que sí, voy abrirle el navegador Brave, 
            el que es su preferido""")
            webbrowser.open("https://www.google.com")
            continue

        elif "día" in pedido:
            pedir_dia()
            continue
        elif "qué hora es" in pedido:
            pedir_hora()
            continue
        elif "buscar en wikipedia" in pedido:
            pedido = pedido.replace("buscar en wikipedia", "")
            hablar(f"Buscando en wikipedia {pedido}")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar("Wikipedia dice lo siguiente:")
            print(resultado)
            hablar(resultado)
            continue
        elif "busca en internet" in pedido:
            pedido = pedido.replace("busca en internet", "")
            hablar("Ya mismo estoy en eso...")
            pywhatkit.search(pedido)
            hablar(f"Esto es lo que he encontrado sobre {pedido}")
            continue
        elif "reproducir" in pedido:
            hablar("Ya comienzo a reproducirlo")
            pywhatkit.playonyt(pedido)
            continue
        elif "chiste" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue
        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strip()
            cartera = {"apple": "APPL",
                       "amazon": "AMAZN",
                       "google": "GOOGL"}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info["regularMarketPrice"]
                hablar(f"La encontré, el precio de {accion} es {precio_actual}")
                continue
            except:
                hablar("Perdón, pero no la he encontrado")
                continue
        elif "adiós" in pedido:
            hablar("Ha sido un placer ayudarte, cualquier cosa me avisas")
            break


pedir()




