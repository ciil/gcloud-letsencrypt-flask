from flask import Flask
from flask import Response
app = Flask(__name__)
app.config['DEBUG'] = True

credentials = {
        '[challenge]' : '[response]',
        '[challenge]' : '[response]'
     }

@app.route('/.well-known/acme-challenge/<challenge>')
def letsencrypt(challenge):
    return Response(credentials[challenge], mimetype='text/plain')

