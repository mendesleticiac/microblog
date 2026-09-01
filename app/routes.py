from app import app
from flask import render_template

@app.route('/')
@app.route('/index/<nome>')

def index(nome):
    dados={"Profissao": "Professora","Status": "Casada"}
    return render_template('index.html', nome=nome, dados=dados)


@app.route ('/contato')
def contato():
    return render_template('contato.html')