import os
import json
import requests
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
app = Flask(__name__)

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(override=True)
load_dotenv(dotenv_path)
roleID = os.getenv("RoleID")
wsid = os.getenv("WSID")
url = 'http://172.20.20.10:8200/v1/sys/wrapping/unwrap'
headers = {
    'X-Vault-Token': wsid
}
response = requests.post(url, headers=headers)
resp_dict = response.json()
sid=resp_dict['data']['secret_id']
print("Secret ID is:" +sid)

@app.route("/")
def hello():

    url = 'http://172.20.20.10:8200/v1/auth/approle/login'
    data = {'role_id': roleID, 'secret_id': sid}
    response2 = requests.post(url, data=json.dumps(data).encode("utf-8"))
    resp_dict2 = response2.json()
    token=resp_dict2['auth']['client_token']
    print("Token is:" +token)

    url = 'http://172.20.20.10:8200/v1/GDL/Demo/Hello'
    headers = {
        'X-Vault-Token': token
    }
    response3 = requests.get(url, headers=headers)
    resp_dict3 = response3.json()
    secret=resp_dict3['data']['World']
    print("Secret is:" +secret)

    return render_template('index.html', greeting= 'hello', roleID=roleID, wsid=wsid, sid=sid, token=token, secret=secret)

#@app.route("/login")
#def login():
#    url = 'http://172.20.20.10:8200/v1/auth/approle/login'
#    data = {
#        'role_id': roleID,
#        'secret_id': sid
#    }
#    response = requests.post(url, data=data)
#    resp_dict = response.json()
#    token=resp_dict['auth']['client_token']
#    return render_template('index.html', token=token)
#
#@app.route("/secret")
#def secret():
#    url = 'http://172.20.20.10:8200/v1/GDL/Demo/Hello'
#    headers = {
#        'X-Vault-Token': token
#    }
#    response = requests.post(url, headers=headers)
#    resp_dict = response.json()
#    secret=resp_dict['data']['World']
#    return render_template('index.html', secret=secret)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
