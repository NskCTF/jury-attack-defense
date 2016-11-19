from flask import Flask
from flask import jsonify, json
import json
import flask
app = Flask(__name__)

app.debug = True
@app.route('/')
def hello_world():
    dat = json.dumps({
        "method":"get",
        "response": {
            "settings":{
                "time":{
                    "start":1446314400,
                    "end":1448906400
                },
                "name":"",
                "round_length":10,
                "flags": {
                    "lifetime":4,
                    "port":2605
                },
                "admin":{
                    "login":"root",
                    "pass":"qwe"
                },
                "path_to_checkers" : "checkers/"
            },
            "teams":[
                # {"name": "Dima", "network": "10.16.255.0/24", "host": "10.16.255.196", "logo": 'http://sibirctf.org/img/logo_teams/2day.jpg'},
                {"name": "Mu574n9", "network": "192.168.1.110/24", "host": "192.168.1.110", "logo": 'http://sibirctf.org/img/logo_teams/mustang.png'}
            ],
            "services":[
                {"name": "service_1", "timeout": "10", "program": open('checkers/service_1/checker.py', 'r').read()},
                {"name": "service_2", "timeout": "10", "program": open('checkers/service_2/checker.py', 'r').read()},
            ]
        }
    })

    resp = flask.Response(
        response=dat,
        status=200,
        mimetype="application/json"
    )

    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0')
