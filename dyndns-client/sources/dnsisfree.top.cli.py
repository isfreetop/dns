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
import time
import requests

CONFIG_FILE = "/volume1/homes/admin/dnsisfree.ini"  # adaptez le chemin

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
            return data[0].get("state") == "1"
        else:
            return False
    except Exception as e:
        print("Erreur de mise à jour :", e)
        return False

def parse_and_update():
    if not os.path.exists(CONFIG_FILE):
        print(f"Erreur : fichier {CONFIG_FILE} introuvable.")
        return

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    email = config.get("COMUN", "Email", fallback="")
    wait_time = int(config.get("COMUN", "TimeWait", fallback="600"))

    ip = get_public_ip()
    if not ip:
        print("Erreur : Impossible d’obtenir l’IP publique.")
        return

    print(f"IP publique détectée : {ip}")

    for i in range(1, 11):
        section = f"ZONE_{i}"
        if config.has_section(section):
            state = config.getboolean(section, f"State_zone{i}", fallback=False)
            token = config.get(section, f"Token_zone{i}", fallback="")
            if state and token.strip():
                success = update_zone(ip, email, token)
                print(f"[{section}] -> {'OK' if success else 'Échec'}")

    print(f"Attente {wait_time} secondes avant prochaine mise à jour...")

if __name__ == "__main__":
    parse_and_update()
