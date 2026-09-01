from app import app
from flask import render_template
from flask import request #recuperar dados do formulário

@app.route('/')
@app.route('/index' , defaults={"nome":"usuário"})
@app.route('/index/<nome>/<Profissao>/<Status>')

def index(nome, Profissao, Status):

    dados={"Profissao": Profissao ,"Status": Status}
    return render_template('index.html', nome=nome, dados=dados)


@app.route ('/contato')
def contato():
    return render_template('contato.html')

@app.route ('/login')
def login():
    return render_template('login.html')

@app.route ('/autentificar', methods=['POST'])
def autentificar():
    usuario = request.form.get('usuario') #pega o valor do campo usuario do formulário
    senha = request.form.get('senha')
    return(f"usuario: {usuario} e senha: {senha}")