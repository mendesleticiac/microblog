from flask import render_template, request, flash, redirect
from app import app
import psycopg


def conectar_banco():
    conexao = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="leeonh23#"
    )
    return conexao



@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/login')
def login():
    return render_template('login.html')

# CADASTRO

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    confirmar_senha = request.form.get('confirmar_senha')
    
    if senha != confirmar_senha:
        return """
        <script> alert("As senhas não são iguais!"); window.history.back(); 
        </script>
        """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO USUARIOS (NOME, EMAIL, SENHA)
        VALUES (%s, %s, %s)
    """, (nome, email, senha))

    conexao.commit()

    cursor.close()
    conexao.close()

    return """
        <script>
        alert("Usuário cadastrado com sucesso!");
        window.location.href = "/usuarios"; 
        </script>
    """

# LISTAR USUÁRIOS - READ

@app.route('/usuarios')
def usuarios():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT ID, NOME, EMAIL, SENHA
        FROM USUARIOS
        ORDER BY ID
    """)

    usuarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        'usuarios.html',
        usuarios=usuarios
    )

# EDITAR USUÁRIO

@app.route('/editar/<int:id>')
def editar(id):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT ID, NOME, EMAIL, SENHA
        FROM USUARIOS
        WHERE ID = %s
    """, (id,))

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template(
        'editar.html',
        usuario=usuario
    )

# ATUALIZAR USUÁRIO - UPDATE

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    confirmar_senha = request.form.get('confirmar_senha')

    if senha != confirmar_senha:
        return """
        <script> alert("As senhas não são iguais!"); window.history.back(); 
        </script>
        """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE USUARIOS
        SET NOME = %s,
            EMAIL = %s,
            SENHA = %s
        WHERE ID = %s
    """, (nome, email, senha, id))

    conexao.commit()

    cursor.close()
    conexao.close()
    return """
        <script>
            alert("Usuário atualizado com sucesso!");
            window.location.href = "/usuarios";
        </script>
    """

 # EXCLUIR USUÁRIO - DELETE

@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM USUARIOS
        WHERE ID = %s
    """, (id,))

    conexao.commit()

    cursor.close()
    conexao.close()

    return """
        <script>
            alert("Usuário excluído com sucesso!");
            window.location.href = "/usuarios";
        </script>
    """

@app.route('/autentificar', methods=['POST'])
def autentificar():

    email = request.form.get('email')
    senha = request.form.get('senha')

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT ID, NOME, EMAIL, SENHA
        FROM USUARIOS
        WHERE EMAIL = %s AND SENHA = %s
    """, (email, senha))

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    if usuario:
        return f"""
            <script>
                alert("Login bem-sucedido! Bem-vindo, {usuario[1]}!");
                window.location.href = "/index";
            </script>
        """
    else:
        return """
            <script>
                alert("Email ou senha incorretos!");
                window.history.back();
            </script>
        """

@app.route('/nova-solicitacao')
def nova_solicitacao():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT ID, NOME, SIGLA
        FROM SETORES
        ORDER BY NOME
    """)

    setores = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        'nova_solicitacao.html',
        setores=setores
    )

@app.route('/setores')
def setores():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT ID, NOME, SIGLA
        FROM SETORES
        ORDER BY ID
    """)

    setores = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template(
        'setores.html',
        setores=setores
    )

@app.route('/editar-setor/<int:id>')
def editar_setor(id):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT ID, NOME, SIGLA
        FROM SETORES
        WHERE ID = %s
    """, (id,))

    setor = cursor.fetchone()
    cursor.close()
    conexao.close()

    return render_template(
        'editar_setor.html',
        setor=setor
    )


@app.route('/atualizar-setor/<int:id>', methods=['POST'])
def atualizar_setor(id):

    nome = request.form.get('nome')
    sigla = request.form.get('sigla')

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE SETORES
        SET NOME = %s,
            SIGLA = %s
        WHERE ID = %s
    """, (nome, sigla, id))

    conexao.commit()

    cursor.close()
    conexao.close()

    return """
        <script>
            alert("Setor atualizado com sucesso!");
            window.location.href = "/setores";
        </script>
    """    

@app.route('/excluir-setor/<int:id>', methods=['POST'])
def excluir_setor(id):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM SETORES
        WHERE ID = %s
    """, (id,))

    conexao.commit()
    cursor.close()
    conexao.close()

    return """
        <script>
            alert("Setor excluído com sucesso!");
            window.location.href = "/setores";
        </script>
    """

@app.route('/novo-setor')
def novo_setor():
    return render_template('novo_setor.html')

@app.route('/cadastrar-setor', methods=['POST'])
def cadastar_setor():

    nome = request.form.get('nome')
    sigla = request.form.get('sigla')

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO SETORES (NOME, SIGLA)
        VALUES (%s, %s)
        """, (nome, sigla))

    conexao.commit()
    cursor.close()
    conexao.close()

    return """
        <script>
            alert ("Setor cadastrado com sucesso!");
            window.location.href = "/setores";  
        </script> 
    """    


@app.route('/criar-solicitacao', methods=['POST'])
def criar_solicitacao():

    setor = request.form.get('setor')
    material = request.form.get('material')
    quantidade = request.form.get('quantidade')
    justificativa = request.form.get('justificativa')

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO SOLICITACOES
        (SETOR, MATERIAL, QUANTIDADE, JUSTIFICATIVA)
        VALUES (%s, %s, %s, %s)
    """, (setor, material, quantidade, justificativa))

    conexao.commit()
    cursor.close()
    conexao.close()

    return """
        <script>
            alert("Solicitação criada com sucesso!");
            window.location.href = "/index";
        </script>
    """    

#FAZ MOSTRAR AS SOLICITAÇÕES CADASTRADAS
@app.route('/')
@app.route('/index')
def index():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Total de solicitações
    cursor.execute("""
        SELECT COUNT(*)
        FROM SOLICITACOES
    """)

    total_solicitacoes = cursor.fetchone()[0]

    # Solicitações em análise
    cursor.execute("""
        SELECT COUNT(*)
        FROM SOLICITACOES
        WHERE STATUS = 'EM ANÁLISE'
    """)

    em_analise = cursor.fetchone()[0]

    # Solicitações aprovadas
    cursor.execute("""
        SELECT COUNT(*)
        FROM SOLICITACOES
        WHERE STATUS = 'APROVADA'
    """)

    aprovadas = cursor.fetchone()[0]

    # Solicitações concluídas
    cursor.execute("""
        SELECT COUNT(*)
        FROM SOLICITACOES
        WHERE STATUS = 'ADQUIRIDA'
    """)

    concluidas = cursor.fetchone()[0]

    cursor.close()
    conexao.close()

    return render_template(
        'index.html',
        total_solicitacoes=total_solicitacoes,
        em_analise=em_analise,
        aprovadas=aprovadas,
        concluidas=concluidas
    )

#LISTA AS SOLICITAÇÕES CADASTRADAS
@app.route('/solicitacoes')
def solicitacoes():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT 
            ID, 
            SETOR,
            MATERIAL,
            QUANTIDADE, 
            JUSTIFICATIVA,
            DATA_SOLICITACAO,
            STATUS
        FROM SOLICITACOES
        ORDER BY DATA_SOLICITACAO DESC
    """)

    solicitacoes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        'solicitacoes.html',
        solicitacoes=solicitacoes
    )

@app.route('/atualizar-status/<int:id>', methods=['POST'])
def atualizar_status(id):

    status = request.form.get('status')

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE SOLICITACOES
        SET STATUS = %s
        WHERE ID = %s
    """, (status, id))

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect('/solicitacoes')

@app.route('/relatorios')
def relatorios():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Total
    cursor.execute("""
        SELECT COUNT(*)
        FROM SOLICITACOES
    """)
    total = cursor.fetchone()[0]

    # Em análise
    cursor.execute("""
        SELECT COUNT(*)
        FROM SOLICITACOES
        WHERE STATUS = 'EM ANÁLISE'
    """)
    em_analise = cursor.fetchone()[0]

    # Aprovadas
    cursor.execute("""
        SELECT COUNT(*)
        FROM SOLICITACOES
        WHERE STATUS = 'APROVADA'
    """)
    aprovadas = cursor.fetchone()[0]

    # Não aprovadas
    cursor.execute("""
        SELECT COUNT(*)
        FROM SOLICITACOES
        WHERE STATUS = 'NÃO APROVADA'
    """)
    nao_aprovadas = cursor.fetchone()[0]

    # Em processo de compra
    cursor.execute("""
        SELECT COUNT(*)
        FROM SOLICITACOES
        WHERE STATUS = 'EM PROCESSO DE COMPRA'
    """)
    em_processo = cursor.fetchone()[0]

    # Adquiridas
    cursor.execute("""
        SELECT COUNT(*)
        FROM SOLICITACOES
        WHERE STATUS = 'ADQUIRIDA'
    """)
    adquiridas = cursor.fetchone()[0]

    # Todas as solicitações
    cursor.execute("""
        SELECT
            ID,
            DATA_SOLICITACAO,
            SETOR,
            MATERIAL,
            QUANTIDADE,
            STATUS
        FROM SOLICITACOES
        ORDER BY ID DESC
    """)

    solicitacoes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        'relatorios.html',
        total=total,
        em_analise=em_analise,
        aprovadas=aprovadas,
        nao_aprovadas=nao_aprovadas,
        em_processo=em_processo,
        adquiridas=adquiridas,
        solicitacoes=solicitacoes
    )