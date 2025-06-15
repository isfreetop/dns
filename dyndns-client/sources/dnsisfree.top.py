##
#
# Soft      : DynDNS Client Agent
# Author    : https://github.com/isfreetop/dns
# Version   ; 1.0.0
# Website   ; https://dns.isfree.top
# Version   : Windows / Linux
# Copyright : MIT
#
##
import os
import base64
import configparser
import platform
import threading
import time
import requests
import tkinter as tk
from tkinter import messagebox, ttk
import pystray
from PIL import Image, ImageDraw
import threading

CONFIG_FILE = "dnsisfree.ini"

def create_image():
    # Icône simple : cercle bleu
    image = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill="blue")
    return image

def minimize_to_tray(root_window):
    root_window.withdraw()

    def on_restore(icon, item):
        icon.stop()
        root_window.deiconify()

    def on_quit(icon, item):
        icon.stop()
        root_window.destroy()

    menu = pystray.Menu(
        pystray.MenuItem("Restaurer", on_restore),
        pystray.MenuItem("Quitter", on_quit)
    )
    icon = pystray.Icon("DynDNS isFree.top", create_image(), "DynDNS isFree.top", menu)
    threading.Thread(target=icon.run, daemon=True).start()

def reverse_base64(value):
    decoded = base64.b64decode(value.encode()).decode('utf-8')
    return decoded[::-1]

def get_public_ip():
    try:
        res = requests.get("https://dns.isfree.top/api.php?app=myip", timeout=5)
        data = res.json()
        if data.get("state") == 1:
            return data.get("ip")
    except:
        pass
    try:
        res = requests.get("https://api.myip.com/", timeout=5)
        data = res.json()
        return data.get("ip")
    except:
        return None

def encode_obfuscated(value):
    reversed_str = value[::-1]
    encoded = base64.b64encode(reversed_str.encode()).decode()
    return encoded

def update_zone(ip, email, token):
    try:

        ob_ip = encode_obfuscated(ip)
        ob_email = encode_obfuscated(email)
        ob_token = encode_obfuscated(token)
        url = f"https://dns.isfree.top/myaccount/api.php?app=update&ip={ob_ip}&email={ob_email}&token={ob_token}"
        res = requests.get(url, timeout=5)
        data = res.json()

        if isinstance(data, list) and len(data) > 0:
            return data[0].get("state") == "1"  # attention : 'state' est une chaîne
        else:
            return False  # en cas de format inattendu
    except Exception as e:
        print(f"ip :  {ob_ip}")
        print(f"url :  {url}")
        print("Erreur de mise à jour :", e)
        return False

def parse_and_update():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    email = config.get("COMUN", "Email", fallback="")
    wait_time = int(config.get("COMUN", "TimeWait", fallback="600"))

    ip = get_public_ip()
    if not ip:
        messagebox.showerror("Erreur", "Impossible d’obtenir l’IP publique.")
        return

    for i in range(1, 11):
        section = f"ZONE_{i}"
        if config.has_section(section):
            state = config.getboolean(section, f"State_zone{i}", fallback=False)
            token = config.get(section, f"Token_zone{i}", fallback="")
            if state and token.strip():
                success = update_zone(ip, email, token)
                print(f"[ZONE_{i}] -> {'OK' if success else 'Erreur'}")

    print(f"Pause {wait_time}s...")
    time.sleep(wait_time)

def start_update_thread():
    threading.Thread(target=parse_and_update, daemon=True).start()

def show_config_editor():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    editor = tk.Toplevel()
    editor.title("Édition de la configuration")
    editor.geometry("600x600")

    frame = tk.Frame(editor)
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    entries = {}

    # Clés à exclure globalement
    excluded_keys = {"timewait", "url", "urlmyip"}

    def is_bool_str(val):
        return val.lower() in ("true", "false")

    def toggle_bool(var):
        # inverse la valeur booléenne stockée dans var (tk.StringVar)
        current = var.get()
        var.set("False" if current == "True" else "True")

    for section in config.sections():
        sec_label = tk.Label(scrollable_frame, text=f"[{section}]", font=("Arial", 10, "bold"), fg="blue")
        sec_label.pack(anchor="w", pady=(10, 0))

        for key, value in config.items(section):
            if key.lower() in excluded_keys:
                continue  # ignore ces clés

            row = tk.Frame(scrollable_frame)
            row.pack(fill="x", padx=10, pady=2)

            label = tk.Label(row, text=key, width=20, anchor="w")
            label.pack(side="left")

            if is_bool_str(value):
                # bouton on/off
                var = tk.StringVar(value=value.capitalize())  # "True"/"False"
                btn = tk.Button(row, text=var.get(), width=6,
                                command=lambda v=var, b=None: (toggle_bool(v), b.config(text=v.get())),
                                relief="raised")
                # Met à jour le texte du bouton après toggle
                def make_cmd(v, b):
                    def cmd():
                        toggle_bool(v)
                        b.config(text=v.get())
                    return cmd
                btn.config(command=make_cmd(var, btn))
                btn.pack(side="left")
                entries[f"{section}.{key}"] = var  # on stocke le StringVar au lieu Entry

            else:
                entry = tk.Entry(row, width=50)
                entry.insert(0, value)
                entry.pack(side="left", fill="x", expand=True)
                entries[f"{section}.{key}"] = entry

    def save_config():
        for key, widget in entries.items():
            section, opt = key.split(".")
            if not config.has_section(section):
                config.add_section(section)
            if isinstance(widget, tk.StringVar):
                # valeur booléenne
                config.set(section, opt, widget.get())
            else:
                config.set(section, opt, widget.get())
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            config.write(f)
        messagebox.showinfo("Enregistré", "Configuration mise à jour.")
        editor.destroy()

    save_btn = tk.Button(editor, text="Enregistrer", command=save_config)
    save_btn.pack(pady=10)

def main_gui():
    root = tk.Tk()
    root.title("Mise à jour IP - DNS Service")
    root.geometry("300x400")
    tk.Label(root, text=f"DNS.isfree.top", fg="blue").pack(pady=7)
    tk.Label(root, text=f"OS : {platform.system()}", fg="gray").pack(pady=5)

    # Lire l'URL de récupération d'IP dans le fichier de config
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    ip_url = config.get("COMUN", "URLMYIP", fallback="https://api.myip.com/")

    # Obtenir l'IP actuelle
    try:
      res = requests.get(ip_url, timeout=5)
      ip_data = res.json()
      current_ip = ip_data.get("ip", "Non disponible")
    except:
      current_ip = "Non disponible"

    tk.Label(root, text=f"IP actuelle : {current_ip}", fg="black").pack(pady=5)
    tk.Button(root, text="Mettre à jour maintenant", width=25, command=start_update_thread).pack(pady=10)
    tk.Button(root, text="Configurer", width=25, command=show_config_editor).pack(pady=5)
    tk.Button(root, text="Minimiser", command=lambda: minimize_to_tray(root)).pack(pady=5)
    tk.Button(root, text="Quitter", width=25, command=root.destroy).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    if not os.path.exists(CONFIG_FILE):
        messagebox.showerror("Erreur", f"Le fichier {CONFIG_FILE} est introuvable.")
    else:
        main_gui()
