import pyttsx3
import speech_recognition as sr 
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
import tkinter as tk
from tkinter import messagebox


# escuchar microfono y devolver el audio como texto 

def transformar_audio_en_texto():

    #almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el microfono 

    with sr.Microphone() as origen:
        # tiempo de espera
        r.pause_threshold = 0.8 

        #Informar que comonzo la grabacion 
        inicio_conversacion = "Ya estoy listo para escucharte"
        panel_lectura.config(text=inicio_conversacion)
        print(inicio_conversacion)
        aplicacion.update()

        #guardar lo que escuche como audio 
        audio = r.listen(origen)

        try: 
            # buscar en google 
            pedido = r.recognize_google(audio,language="es-MX")
            # prueba de que pudo ingresar 
            print("Dijiste: " + pedido)
            panel_resultado.config(text="Dijiste: "+pedido)

            return pedido
        except sr.UnknownValueError:

            # preba de que no comprendio audio
            panel_resultado.config(text="ups, no hay servicio")
            print("ups, no hay servicio")

            return "sigo esperando"

        except sr.RequestError:

            panel_resultado.config(text="ups, no entendi")
            print("ups, no entendi")

            return "sigo esperando"
        
        except:
            panel_resultado.config(text="ups, no todo salio mal")
            print("ups, no todo salio mal")

            return "sigo esperando"

# funcion para que el asistente pueda ser escuchado 
def hablar(mensaje):
    # encender el motor de pyttsx3
    engine = pyttsx3.init()

    #pronunciar mensaje 
    engine.say(mensaje)
    engine.runAndWait()

def pedir_dia():

    #crear variabe con datos de hoy 
    fecha = datetime.date.today()

    #crear variable para el dia de la semana
    dias = ['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']
    dia_id = fecha.weekday()
    dia_semana = dias[dia_id]
    hablar(f'Hoy es {dia_semana}')

def pedir_hora():
    hora = datetime.datetime.now()
    hora = f"En este momento son las {hora.hour} horas con {hora.minute} minutos"
    hablar(hora)

def saludo_inicial():
    hora = datetime.datetime.now().hour
    if hora > 9 and hora < 14:
        saludo = "Buenos dias" 
    else:   
        saludo = "Buenas noches"
    presentacion = f"{saludo} soy Saphirá tu asistente personal"
    hablar(presentacion)


def pedidos():
    saludo_inicial()
    comenzar = True
    while comenzar:
        pedido = transformar_audio_en_texto().lower()

        if "abrir youtube" in pedido:
            hablar("Claro abrire youtube")
            webbrowser.open('https://www.youtube.com/')
            continue
        elif "abrir google" in pedido:
            hablar("Claro abrire google")
            webbrowser.open('https://www.google.com.mx/')
        elif "pedir dia" in pedido:
            pedir_dia()
        elif "que hora es" in pedido:
            pedir_hora()
        elif "busca en wikipedia" in pedido:
            hablar("Buscar en wikipedia")
            pedido = pedido.replace("busca en wikipedia",'')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido,sentences=1)
            hablar("Wikipedia dice lo siguiente")
            hablar(resultado)
        elif "busca en google" in pedido:
            pedido = pedido.replace("busca en google","")
            pywhatkit.search(pedido)
            hablar("Esto es lo que he encontrado")
        elif "hasta luego" in pedido
            hablar("Nos vemos cualquier cosa me buscar")
            break
            
#iniciar tkinter 
aplicacion = tk.Tk()

#tamaño de la ventana +0+0 ubicacion del sistema 
aplicacion.geometry("400x200+0+0")

#titulo de la ventana
aplicacion.title("asistente de voz")

# color del fondo 
aplicacion.config(bg="white")

#layout 
#Panel superior
panel_superior = tk.Frame(aplicacion,bd=1,relief="flat")
panel_superior.pack(side="top")
etiqueta_titulo = tk.Label(panel_superior,
                           text="Asistente de voz",
                           fg="black",
                           font=('Dosis',14),
                           bg="white",
                           width=27)
etiqueta_titulo.grid(row=0,column=0)
#Panel izquierdo 
panel_izquierdo = tk.Frame(aplicacion,bd=1,relief="flat")
panel_izquierdo.pack(side="left")

#panel lectura 
panel_lectura = tk.Label(panel_izquierdo,
                         text="Haz click en el boton para comenzar",
                         font=("Arial",12))
panel_lectura.pack(side="top")

#etiqueta para mostrar el resultado
panel_resultado = tk.Label(panel_izquierdo,
                           text="",
                           font=("Arial",12))
panel_resultado.pack(side="bottom")

#Boton para comenzar el reconocimiento de voz
button_iniciar = tk.Button(panel_izquierdo,text="Iniciar",command=pedidos)
button_iniciar.pack(side="bottom")


#evitar que la pantalla se cierre 
aplicacion.mainloop()
