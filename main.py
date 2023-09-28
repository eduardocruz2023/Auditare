from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, Response
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import sqlite3
import threading
import webbrowser
import subprocess
import urllib.request
from io import BytesIO
from flask import jsonify
import pandas as pd
import os
import locale
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta
import time
import datetime
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askokcancel, showinfo, WARNING
from tkinter import Menu
from tkinter import filedialog
from tkinter import HORIZONTAL, END, W
from tkinter import BOTTOM
from tkinter import X
from tkinter import font, ttk
import tkinter as tk
import bcrypt
from werkzeug.utils import secure_filename
from io import StringIO
import sys
import io



#"//10.0.0.70/Bando de Dados Integra/Integrasistema.db"
#//10.0.0.59/Faturamento/bdBpaDash.db
caminho ='//10.0.0.70/Bando de Dados Integra/Integrasistema.db'
app = Flask(__name__)
def get_static_path():
    # Obtém o diretório onde o executável está sendo executado
    executable_dir = os.path.dirname(sys.executable)

    # Concatena o diretório com o caminho para os arquivos estáticos
    static_path = os.path.join(executable_dir, 'static')
    return static_path


app.config['CUSTOM_STATIC_PATH'] = get_static_path()
app.secret_key = '211083'
# app.config['CUSTOM_STATIC_PATH'] = 'C:\\Users\\eduardo.cruz\\Desktop\\pythonProject\\POO\\static'
UPLOAD_FOLDER = '//10.0.0.59/Faturamento/'  # Defina o caminho correto
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bcrypt = Bcrypt(app)
# Defina a rota padrão para a página de login
@app.route('/')
def index():
    return redirect(url_for('login'))


bcrypt = Bcrypt()
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')
def create_table():
    connection = sqlite3.connect(caminho)
    cursor = connection.cursor()

    # Defina o código SQL para criar a tabela
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS bdusuarios (
        Id       INTEGER       PRIMARY KEY AUTOINCREMENT,
        Login    VARCHAR (70)  NOT NULL,
        Nome     VARCHAR (100) NOT NULL,
        Senha    TEXT          NOT NULL,  -- Usar TEXT para armazenar hashes de senha
        Cargo    VARCHAR (100) NOT NULL,
        Lotação  VARCHAR (100) NOT NULL,
        Situacao VARCHAR (100) NOT NULL
    );
    """

    # Execute o comando SQL para criar a tabela
    cursor.execute(create_table_sql)
    connection.commit()
    connection.close()
# Rota para listar todos os registros
@app.route('/consulta6')
def consulta6():
    username = session.get('username')
    return render_template('consulta6.html', username=username)
@app.route('/consulta7')
def consulta7():
    username = session.get('username')
    return render_template('consulta7.html', username=username)

@app.route('/consulta5')
def consulta5():
    username = session.get('username')
    return render_template('consulta5.html', username=username)
@app.route('/consulta8')
def consulta8():
    username = session.get('username')
    return render_template('consulta8.html', username=username)
@app.route('/dashboard2')
def dashboard2():
    username = session.get('username')
    return render_template('dashboard2.html', username=username)
@app.route('/dashboard3')
def dashboard3():
    return render_template('dashboard3.html')
@app.route('/dashboard4')
def dashboard4():
    return render_template('dashboard4.html')
@app.route('/dashboard5')
def dashboard5():
    return render_template('dashboard5.html')
@app.route('/dashboard6')
def dashboard6():
    return render_template('dashboard6.html')
@app.route('/dashboard')
def dashboard():
    # Recupere o nome de usuário da sessão
    username = session.get('username')

    # Certifique-se de que 'username' está disponível no contexto do template
    return render_template('dashboard.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = verify_login(username, password)

        if user and bcrypt.check_password_hash(user[3], password):
            session['username'] = user[2]  # Definindo a variável de sessão 'username'
            return redirect(url_for('dashboard'))
        else:
            error_message = 'Usuário ou senha incorretos.'
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')

# Função para verificar usuário no banco de dados
def verify_login(username, password):
    connection = sqlite3.connect(caminho)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bdusuarios WHERE Login = ?", (username,))
    user = cursor.fetchone()
    connection.close()
    return user

# Rota de validação de acesso

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    # Remova a verificação 'if' para 'username' em 'session' e o redirecionamento para 'validacao'

    if request.method == 'POST':
        # Processar o formulário de cadastro
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        nome = request.form['nome']
        cargo = request.form['cargo']
        lotacao = request.form['lotacao']
        situacao = request.form['situacao']

        # Adicionar os dados do usuário ao banco de dados
        connection = sqlite3.connect(caminho)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO bdusuarios (Login, Nome, Senha, Cargo, Lotação, Situacao) VALUES (?, ?, ?, ?, ?, ?)",
            (username, nome, hashed_password, cargo, lotacao, situacao))
        connection.commit()
        connection.close()

        return redirect(url_for('login'))  # Redirecionar após o cadastro

    return render_template('cadastro.html')  # Renderizar o formulário de cadastro


def create_user(username, password, nome, cargo, lotacao, situacao):
    connection = sqlite3.connect(caminho)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO bdusuarios (Login, Nome, Senha, Cargo, Lotação, Situacao) VALUES (?, ?, ?, ?, ?, ?)",
                   (username, nome, password, cargo, lotacao, situacao))
    connection.commit()
    connection.close()


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    # Conectar ao banco de dados
    connection = sqlite3.connect(caminho)
    cursor = connection.cursor()

    # Definir o esquema da tabela mensagens_contato
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensagens_contato (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                Email TEXT NOT NULL,
                Mensagem TEXT NOT NULL
            )
        ''')

    # Commit para salvar as alterações
    connection.commit()

    # Fechar a conexão com o banco de dados
    connection.close()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']

        # Insira a mensagem no banco de dados
        connection = sqlite3.connect(caminho)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO mensagens_contato (Nome, Email, Mensagem) VALUES (?, ?, ?)",
                       (nome, email, mensagem))
        connection.commit()
        connection.close()

        # Redirecione para a página de confirmação ou exiba uma mensagem de sucesso
        flash('Sua mensagem foi enviada com sucesso!', 'success')
        return redirect(url_for('contato'))
    return render_template('contato.html')


# Função para verificar as credenciais e lotação do usuário
def verificar_credenciais(username, password):
    connection = sqlite3.connect(caminho)
    cursor = connection.cursor()
    cursor.execute("SELECT Senha, Lotação FROM bdusuarios WHERE Login=?", (username,))
    result = cursor.fetchone()
    connection.close()

    if result is not None:
        hashed_password_from_db, lotacao = result
        if bcrypt.check_password_hash(hashed_password_from_db, password) and lotacao in ('SAME', 'MASTER'):
            return True



    return False

@app.route('/validacao', methods=['GET', 'POST'])
def validacao():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifique as credenciais do usuário
        if verificar_credenciais(username, password):
            # Se as credenciais estiverem corretas e a lotação for 'SAME', inicie uma sessão
            session['username'] = username
            # Redirecione para a página de atendimento
            return redirect(url_for('dashboard3'))

    # Se as credenciais estiverem incorretas ou se o método for GET, exiba a página de validação
    return render_template('validacao.html')
# Função para criar a tabela se ela não existir
@app.route('/validacao2', methods=['GET', 'POST'])
def validacao2():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifique as credenciais do usuário
        if verificar_credenciais(username, password):
            # Se as credenciais estiverem corretas e a lotação for 'SAME', inicie uma sessão
            session['username'] = username
            # Redirecione para a página de atendimento
            return redirect(url_for('dashboard4'))

    # Se as credenciais estiverem incorretas ou se o método for GET, exiba a página de validação
    return render_template('validacao2.html')
# Função para criar a tabela se ela não existir
@app.route('/validacao3', methods=['GET', 'POST'])
def validacao3():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifique as credenciais do usuário
        if verificar_credenciais(username, password):
            # Se as credenciais estiverem corretas e a lotação for 'SAME', inicie uma sessão
            session['username'] = username
            # Redirecione para a página de atendimento
            return redirect(url_for('dashboard5'))

    # Se as credenciais estiverem incorretas ou se o método for GET, exiba a página de validação
    return render_template('validacao3.html')
@app.route('/validacao4', methods=['GET', 'POST'])
def validacao4():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifique as credenciais do usuário
        if verificar_credenciais(username, password):
            # Se as credenciais estiverem corretas e a lotação for 'SAME', inicie uma sessão
            session['username'] = username
            # Redirecione para a página de atendimento
            return redirect(url_for('dashboard6'))

    # Se as credenciais estiverem incorretas ou se o método for GET, exiba a página de validação
    return render_template('validacao4.html')
@app.route('/atendimento', methods=['GET', 'POST'])
def atendimento():
    connection = sqlite3.connect(caminho)
    cursor = connection.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS tabela_atendimento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT,
                cartao_saude TEXT,
                sexo TEXT,
                municipio TEXT,
                idade INTEGER,
                nome_usuario TEXT,
                nome_social TEXT,
                data_nascimento TEXT,
                raca TEXT,
                etnia TEXT,
                nacionalidade TEXT,
                cep TEXT,
                logradouro TEXT,
                endereco TEXT,
                complemento TEXT,
                numero TEXT,
                bairro TEXT,
                telefone TEXT,
                email TEXT,
                data_hora TEXT
            )
        ''')

    connection.commit()
    connection.close()
    # Verifique se o usuário tem uma sessão válida
    if 'username' in session:
        if request.method == 'POST':
            username = session['username']
            cartao_saude = request.form['cartao_saude']
            sexo = request.form['sexo']
            municipio = request.form['municipio']
            idade = request.form['idade']
            nome_usuario = request.form['nome_usuario']
            nome_social = request.form['nome_social']
            data_nascimento = request.form['data_nascimento']
            raca = request.form['raca']
            etnia = request.form['etnia']
            nacionalidade = request.form['nacionalidade']
            cep = request.form['cep']
            logradouro = request.form['logradouro']
            endereco = request.form['endereco']
            complemento = request.form['complemento']
            numero = request.form['numero']
            bairro = request.form['bairro']
            telefone = request.form['telefone']
            email = request.form['email']

            # Gravar os dados no banco de dados
            connection = sqlite3.connect(caminho)
            cursor = connection.cursor()

            # Inserir os dados na tabela de atendimento
            cursor.execute(
                "INSERT INTO tabela_atendimento (usuario, cartao_saude, sexo, municipio, idade, nome_usuario, "
                "nome_social, data_nascimento, raca, etnia, nacionalidade, cep, logradouro, endereco, complemento, "
                "numero, bairro, telefone, email, data_hora) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (username, cartao_saude, sexo, municipio, idade, nome_usuario, nome_social, data_nascimento, raca,
                 etnia, nacionalidade, cep, logradouro, endereco, complemento, numero, bairro, telefone, email,
                 datetime.datetime.now())  # Use datetime.datetime.now() para obter a data e hora atual
            )

            connection.commit()
            connection.close()

            # Redirecionar para a página de atendimento ou exibir uma mensagem de sucesso
            return redirect(url_for('atendimento'))
        else:
            # Se a solicitação não for POST, simplesmente exiba o formulário
            return render_template('atendimento.html')
    else:
        return "Acesso não autorizado."
###########################
@app.route('/auditar5', methods=['GET', 'POST'])
def auditar5():
    # Verifique se o usuário está logado
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect(caminho)
    cursor = conn.cursor()
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    username = session['username']
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS formulario4 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome CHAR(100),
                Prontuario NUMERIC(100),
                Atendimento NUMERIC(100),
                nomeCompleto CHAR(100),
                Datadenascimento CHAR(100),
                Sexo CHAR(100),
                CPFRG CHAR(100),
                CartãoNacionalSUS CHAR(100),
                Nomecompletodamãe CHAR(100),
                EndereçocCEP CHAR(100),
                Telefoneparacontato CHAR(100),
                GuiadeRequisiçãodoExame CHAR(100),
                TermodeLivre CHAR(100),
                FichadeAdmissão CHAR(100),
                ChecklistProtocolo CHAR(100),
                EvoluçãoMédica CHAR(100),
                EvoluçãodaEnfermagem CHAR(100),
                SolicitaçãodeAnatomopatológico CHAR(100),
                caixaDeTexto CHAR,
                Status CHAR,
                Usuario CHAR(100),
                Data DATETIME
            )
        ''')

    try:

        if request.method == 'POST':
            Nome = request.form['Nome']

            if Nome.strip() == "":
                flash('O campo "Nome" não pode estar em branco.', 'error')
            else:
                Nome = request.form['Nome']
                Prontuario = request.form.get('Prontuario')
                Atendimento = request.form.get('Atendimento')
                nomeCompleto = request.form.get('nomeCompleto')
                Datadenascimento = request.form.get('Datadenascimento')
                Sexo = request.form.get('Sexo')
                CPFRG = request.form.get('CPFRG')  # Correção aqui
                CartãoNacionalSUS = request.form.get('CartãoNacionalSUS')
                Nomecompletodamãe = request.form.get('Nomecompletodamãe')
                EndereçocCEP = request.form.get('EndereçocCEP')
                Telefoneparacontato = request.form.get('Telefoneparacontato')
                GuiadeRequisiçãodoExame = request.form.get('GuiadeRequisiçãodoExame')
                TermodeLivre = request.form.get('TermodeLivre')
                FichadeAdmissão = request.form.get('FichadeAdmissão')
                ChecklistProtocolo = request.form.get('ChecklistProtocolo')
                EvoluçãoMédica = request.form.get('EvoluçãoMédica')
                EvoluçãodaEnfermagem = request.form.get('EvoluçãodaEnfermagem')
                SolicitaçãodeAnatomopatológico = request.form.get('SolicitaçãodeAnatomopatológico')
                comentario = request.form.get('caixaDeTexto')
                if nomeCompleto == "Conforme":
                    nomeCompleto_valor = 1
                elif nomeCompleto == "Não Conforme":
                    nomeCompleto_valor = 0
                elif nomeCompleto == "Não se Aplica":
                    nomeCompleto_valor = 1
                else:
                    nomeCompleto_valor = None
                ######
                if Datadenascimento == "Conforme":
                    Datadenascimento_valor = 1
                elif Datadenascimento == "Não Conforme":
                    Datadenascimento_valor = 0
                elif Datadenascimento == "Não se Aplica":
                    Datadenascimento_valor = 1
                else:
                    Datadenascimento_valor = None
                #########
                if Sexo == "Conforme":
                    Sexo_valor = 1
                elif Sexo == "Não Conforme":
                    Sexo_valor = 0
                elif Sexo == "Não se Aplica":
                    Sexo_valor = 1
                else:
                    Sexo_valor = None
                #########
                if CPFRG == "Conforme":
                    CPFRG_valor = 1
                elif CPFRG == "Não Conforme":
                    CPFRG_valor = 0
                elif CPFRG == "Não se Aplica":
                    CPFRG_valor = 1
                else:
                    CPFRG_valor = None
                ###########
                if CartãoNacionalSUS == "Conforme":
                    CartãoNacionalSUS_valor = 1
                elif CartãoNacionalSUS == "Não Conforme":
                    CartãoNacionalSUS_valor = 0
                elif CartãoNacionalSUS == "Não se Aplica":
                    CartãoNacionalSUS_valor = 1
                else:
                    CartãoNacionalSUS_valor = None
                ############
                if Nomecompletodamãe == "Conforme":
                    Nomecompletodamãe_valor = 1
                elif Nomecompletodamãe == "Não Conforme":
                    Nomecompletodamãe_valor = 0
                elif Nomecompletodamãe == "Não se Aplica":
                    Nomecompletodamãe_valor = 1
                else:
                    Nomecompletodamãe_valor = None
                ######
                EndereçocCEP = request.form.get('EndereçocCEP')
                if EndereçocCEP == "Conforme":
                    EndereçocCEP_valor = 1
                elif EndereçocCEP == "Não Conforme":
                    EndereçocCEP_valor = 0
                elif EndereçocCEP == "Não se Aplica":
                    EndereçocCEP_valor = 1
                else:
                    EndereçocCEP_valor = None

                if Telefoneparacontato == "Conforme":
                    Telefoneparacontato_valor = 1
                elif Telefoneparacontato == "Não Conforme":
                    Telefoneparacontato_valor = 0
                elif Telefoneparacontato == "Não se Aplica":
                    Telefoneparacontato_valor = 1
                else:
                    Telefoneparacontato_valor = None

                if GuiadeRequisiçãodoExame == "Conforme":
                    GuiadeRequisiçãodoExame_valor = 1
                elif GuiadeRequisiçãodoExame == "Não Conforme":
                    GuiadeRequisiçãodoExame_valor = 0
                elif GuiadeRequisiçãodoExame == "Não se Aplica":
                    GuiadeRequisiçãodoExame_valor = 1
                else:
                    GuiadeRequisiçãodoExame_valor = None
                if TermodeLivre == "Conforme":
                    TermodeLivre_valor = 1
                elif TermodeLivre == "Não Conforme":
                    TermodeLivre_valor = 0
                elif TermodeLivre == "Não se Aplica":
                    TermodeLivre_valor = 1
                else:
                    TermodeLivre_valor = None


                if FichadeAdmissão == "Conforme":
                    FichadeAdmissão_valor = 1
                elif FichadeAdmissão == "Não Conforme":
                    FichadeAdmissão_valor = 0
                elif FichadeAdmissão == "Não se Aplica":
                    FichadeAdmissão_valor = 1
                else:
                    FichadeAdmissão_valor = None

                if ChecklistProtocolo == "Conforme":
                    ChecklistProtocolo_valor = 1
                elif ChecklistProtocolo == "Não Conforme":
                    ChecklistProtocolo_valor = 0
                elif ChecklistProtocolo == "Não se Aplica":
                    ChecklistProtocolo_valor = 1
                else:
                    ChecklistProtocolo_valor = None

                if EvoluçãoMédica == "Conforme":
                    EvoluçãoMédica_valor = 1
                elif EvoluçãoMédica == "Não Conforme":
                    EvoluçãoMédica_valor = 0
                elif EvoluçãoMédica == "Não se Aplica":
                    EvoluçãoMédica_valor = 1
                else:
                    EvoluçãoMédica_valor = None

                if EvoluçãodaEnfermagem == "Conforme":
                    EvoluçãodaEnfermagem_valor = 1
                elif EvoluçãodaEnfermagem == "Não Conforme":
                    EvoluçãodaEnfermagem_valor = 0
                elif EvoluçãodaEnfermagem == "Não se Aplica":
                    EvoluçãodaEnfermagem_valor = 1
                else:
                    EvoluçãodaEnfermagem_valor = None

                if SolicitaçãodeAnatomopatológico == "Conforme":
                    SolicitaçãodeAnatomopatológico_valor = 1
                elif SolicitaçãodeAnatomopatológico == "Não Conforme":
                    SolicitaçãodeAnatomopatológico_valor = 0
                elif SolicitaçãodeAnatomopatológico == "Não se Aplica":
                    SolicitaçãodeAnatomopatológico_valor = 1
                else:
                    SolicitaçãodeAnatomopatológico_valor = None





                # Adicione os campos adicionais e seus valores conforme necessário
                valores_conformidade = {
                    "Conforme": 1,
                    "Não se Aplica": 1,
                    "Não Conforme": 0
                }
                campos_conformidade = [
                    request.form.get('nomeCompleto'),
                    request.form.get('Datadenascimento'),
                    request.form.get('Sexo'),
                    request.form.get('CPFRG'),
                    request.form.get('CartãoNacionalSUS'),
                    request.form.get('Nomecompletodamãe'),
                    request.form.get('GuiadeRequisiçãodoExame'),
                    request.form.get('TermodeLivre'),
                    request.form.get('ChecklistProtocolo'),
                    request.form.get('FichadeAdmissão'),
                    request.form.get('EvoluçãodaEnfermagem'),
                    request.form.get('SolicitaçãodeAnatomopatológico'),


                    # Adicione outros campos conforme necessário
                ]

                if (nomeCompleto == "Não Conforme" or
                        Datadenascimento == "Não Conforme" or
                        Sexo == "Não Conforme" or
                        Nomecompletodamãe == "Não Conforme" or
                        CartãoNacionalSUS == "Não Conforme" or
                        EndereçocCEP == "Não Conforme"):
                    Status = "Insuficiente"
                else:
                    # Calcular a pontuação total
                    pontuacao_total = sum(valores_conformidade[conformidade] for conformidade in campos_conformidade)
                    # Calcular o percentual
                    percentual = (pontuacao_total / len(campos_conformidade)) * 100

                    # Definir o campo "Status" com base nos intervalos
                    if percentual >= 90:
                        Status = "Excelente"
                    elif 70 <= percentual < 90:
                        Status = "Bom"
                    elif 50 <= percentual < 70:
                        Status = "Razoável"
                    else:
                        Status = "Insuficiente"
                cursor.execute('''
                                INSERT INTO formulario4 (
                                    Nome, Prontuario, Atendimento, nomeCompleto, Datadenascimento, 
                                    Sexo, CPFRG, CartãoNacionalSUS, Nomecompletodamãe, EndereçocCEP, 
                                    Telefoneparacontato, GuiadeRequisiçãodoExame,
                                    TermodeLivre, FichadeAdmissão,ChecklistProtocolo, EvoluçãoMédica, 
                                    EvoluçãodaEnfermagem, SolicitaçãodeAnatomopatológico, caixaDeTexto, Status, Usuario, Data
                                )
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (Nome, Prontuario, Atendimento, nomeCompleto, Datadenascimento,
                                  Sexo, CPFRG, CartãoNacionalSUS, Nomecompletodamãe, EndereçocCEP,
                                  Telefoneparacontato, GuiadeRequisiçãodoExame,TermodeLivre, FichadeAdmissão, ChecklistProtocolo, EvoluçãoMédica,
                                    EvoluçãodaEnfermagem, SolicitaçãodeAnatomopatológico, comentario, Status, username, data_hora))
                conn.commit()
                conn.close()
                return render_template('auditar5.html', username=username)
    except sqlite3.Error as e:
        # Trate o erro aqui e imprima mensagens para depuração
        print("Erro no banco de dados:", e)
    return render_template('auditar5.html', username=username)
@app.route('/buscar_registro3', methods=['POST'])
def buscar_registro3():
    if request.method == 'POST':
        registro_id = request.form['id']  # Obtém o ID fornecido no formulário
        connection = sqlite3.connect(caminho)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM formulario3 WHERE id = ?", (registro_id,))
        registro = cursor.fetchone()  # Obtém a primeira linha dos resultados
        connection.close()
        if registro:
            dados_registro = {
                "Nome": registro[1],
                "Prontuario": registro[2],
                "Atendimento": registro[3],
                "nomeCompleto": registro[4],
                "Datadenascimento": registro[5],
                "Sexo": registro[6],
                "CPFRG": registro[7],
                "CartaoNacionalSUS": registro[8],
                "Nomecompletodamae": registro[9],
                "EndereçocCEP": registro[10],
                "Telefoneparacontato": registro[11],
                "GuiadeRequisiçãodoExame": registro[12],
                "FichadeOrientação": registro[13],
                "TermodeLivre": registro[14],
                "FichadeAdmissão": registro[15],
                "PrescriçãoMédica": registro[16],
                "EvoluçãoMédica": registro[17],
                "EvoluçãodaEnfermagem": registro[18],
                "SolicitaçãodeAnatomopatológico": registro[19],
                "caixaDeTexto": registro[20],
                "Status": registro[21],
                "Usuario": registro[22]
            }

            # Retorne os dados em formato JSON
            return jsonify(dados_registro)

    # Se o registro não for encontrado, retorne uma mensagem de erro ou redirecione para outra página
    return jsonify({"error": "Registro não encontrado"})
@app.route('/buscar_registro4', methods=['POST'])
def buscar_registro4():
    if request.method == 'POST':
        registro_id = request.form['id']  # Obtém o ID fornecido no formulário
        connection = sqlite3.connect(caminho)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM formulario4 WHERE id = ?", (registro_id,))
        registro = cursor.fetchone()  # Obtém a primeira linha dos resultados
        connection.close()
        if registro:
            dados_registro = {
                "Nome": registro[1],
                "Prontuario": registro[2],
                "Atendimento": registro[3],
                "nomeCompleto": registro[4],
                "Datadenascimento": registro[5],
                "Sexo": registro[6],
                "CPFRG": registro[7],
                "CartaoNacionalSUS": registro[8],
                "Nomecompletodamae": registro[9],
                "EndereçocCEP": registro[10],
                "Telefoneparacontato": registro[11],
                "GuiadeRequisiçãodoExame": registro[12],
                "TermodeLivre": registro[13],
                "FichadeAdmissão": registro[14],
                "ChecklistProtocolo": registro[15],
                "EvoluçãoMédica": registro[16],
                "EvoluçãodaEnfermagem": registro[17],
                "SolicitaçãodeAnatomopatológico": registro[18],
                "caixaDeTexto": registro[19],
                "Status": registro[20],
                "Usuario": registro[21]
            }

            # Retorne os dados em formato JSON
            return jsonify(dados_registro)

    # Se o registro não for encontrado, retorne uma mensagem de erro ou redirecione para outra página
    return jsonify({"error": "Registro não encontrado"})
@app.route('/buscar_registro2', methods=['POST'])
def buscar_registro2():
    if request.method == 'POST':
        registro_id = request.form['id']  # Obtém o ID fornecido no formulário

        # Conecte-se ao banco de dados
        connection = sqlite3.connect(caminho)
        cursor = connection.cursor()

        # Execute a consulta para obter os dados do registro com o ID fornecido
        cursor.execute("SELECT * FROM formulario2 WHERE id = ?", (registro_id,))
        registro = cursor.fetchone()  # Obtém a primeira linha dos resultados

        # Feche a conexão com o banco de dados
        connection.close()

        # Verifique se o registro foi encontrado
        if registro:
            # Os valores do registro serão uma tupla, e você pode acessá-los pelos índices
            # Por exemplo, registro[1] é o valor do campo "Nome"

            # Crie um dicionário com os dados do registro
            dados_registro = {
                "Nome": registro[1],
                "Prontuario": registro[2],
                "Atendimento": registro[3],
                "nomeCompleto": registro[4],
                "Datadenascimento": registro[5],
                "Sexo": registro[6],
                "CPFRG": registro[7],
                "CartaoNacionalSUS": registro[8],
                "Nomecompletodamae": registro[9],
                "EndereçocCEP": registro[10],
                "Telefoneparacontato": registro[11],
                "GuiadeRequisiçãodoExame": registro[12],
                "TermodeLivre": registro[13],
                "FichadeOrientação": registro[14],
                "FichadeAdmissão": registro[15],
                "PrescriçãoMédica": registro[16],
                "PrescriçãoMédicadoContraste": registro[17],
                "EvoluçãoMédicadoProcedimento": registro[18],
                "EvoluçãodaEnfermagem": registro[19],
                "LaudodoExame": registro[20],
                "caixaDeTexto": registro[21],
                "Status": registro[22],
                "Usuario": registro[23]
            }

            # Retorne os dados em formato JSON
            return jsonify(dados_registro)

    # Se o registro não for encontrado, retorne uma mensagem de erro ou redirecione para outra página
    return jsonify({"error": "Registro não encontrado"})
@app.route('/buscar_registro', methods=['POST'])
def buscar_registro():
    if request.method == 'POST':
        registro_id = request.form['id']  # Obtém o ID fornecido no formulário

        # Conecte-se ao banco de dados
        connection = sqlite3.connect(caminho)
        cursor = connection.cursor()

        # Execute a consulta para obter os dados do registro com o ID fornecido
        cursor.execute("SELECT * FROM formulario1 WHERE id = ?", (registro_id,))
        registro = cursor.fetchone()  # Obtém a primeira linha dos resultados

        # Feche a conexão com o banco de dados
        connection.close()

        # Verifique se o registro foi encontrado
        if registro:
            # Os valores do registro serão uma tupla, e você pode acessá-los pelos índices
            # Por exemplo, registro[1] é o valor do campo "Nome"

            # Crie um dicionário com os dados do registro
            dados_registro = {
                "Nome": registro[1],
                "Prontuario": registro[2],
                "Atendimento": registro[3],
                "nomeCompleto": registro[4],
                "Datadenascimento": registro[5],
                "Sexo": registro[6],
                "CPFRG": registro[7],
                "CartaoNacionalSUS": registro[8],
                "Nomecompletodamae": registro[9],
                "EndereçocCEP": registro[10],
                "Telefoneparacontato": registro[11],
                "HistóriadaDoençaAtual": registro[12],
                "AchadosnoExameFísico": registro[13],
                "DescriçãodaConduta": registro[14],
                "HipóteseDiagnóstica": registro[15],
                "Carimboeassinatura": registro[16],
                "Laudomédico": registro[17],
                "GuiadeRequisição": registro[18],
                "ambulatorio_selecionado": registro[19],
                "caixaDeTexto": registro[20],
                "Status": registro[21],
                "Usuario": registro[22]

            }

            # Retorne os dados em formato JSON
            return jsonify(dados_registro)

    # Se o registro não for encontrado, retorne uma mensagem de erro ou redirecione para outra página
    return jsonify({"error": "Registro não encontrado"})
@app.route('/editar_registro', methods=['POST'])
def editar_registro():
    if request.method == 'POST':
        registro_id = request.form['id']
        # Obtenha todos os outros campos do formulário
        novo_nome = request.form['Nome']
        novo_Prontuario = request.form.get('Prontuario')
        novo_Atendimento = request.form.get('Atendimento')
        novo_nomeCompleto = request.form.get('nomeCompleto')
        novo_Datadenascimento = request.form.get('Datadenascimento')
        novo_Sexo = request.form.get('Sexo')
        novo_CPFRG = request.form.get('CPFRG')
        novo_CartãoNacionalSUS = request.form.get('CartaoNacionalSUS')
        novo_Nomecompletodamãe = request.form.get('Nomecompletodamae')
        novo_EndereçocCEP = request.form.get('EndereçocCEP')
        novo_Telefoneparacontato = request.form.get('Telefoneparacontato')
        novo_HistóriadaDoençaAtual = request.form.get('HistóriadaDoençaAtual')
        novo_AchadosnoExameFísico = request.form.get('AchadosnoExameFísico')
        novo_DescriçãodaConduta = request.form.get('DescriçãodaConduta')
        novo_HipóteseDiagnóstica = request.form.get('HipóteseDiagnóstica')
        novo_Carimboeassinatura = request.form.get('Carimboeassinatura')
        novo_Laudomédico = request.form.get('Laudomédico')
        novo_GuiadeRequisição = request.form.get('GuiadeRequisição')
        novo_ambulatorio_selecionado = request.form.get("ambulatorio_selecionado")
        novo_comentario = request.form.get('caixaDeTexto')

        # Conecte-se ao banco de dados
        connection = sqlite3.connect(caminho)
        cursor = connection.cursor()

        # Atualize o registro no banco de dados com os novos valores
        cursor.execute("UPDATE formulario1 SET Nome = ?, Prontuario = ?, Atendimento = ?, nomeCompleto = ?, Datadenascimento = ?, Sexo = ?, CPFRG = ?, "
                       "CartãoNacionalSUS = ?, Nomecompletodamãe = ?, EndereçocCEP = ?, Telefoneparacontato = ?, HistóriadaDoençaAtual = ?, "
                       "AchadosnoExameFísico = ?, DescriçãodaConduta = ?, HipóteseDiagnóstica = ?, Carimboeassinatura = ?, Laudomédico = ?, GuiadeRequisição = ?, ambulatorio_selecionado = ?, caixaDeTexto = ? WHERE id = ?", (novo_nome, novo_Prontuario, novo_Atendimento, novo_nomeCompleto, novo_Datadenascimento, novo_Sexo, novo_CPFRG, novo_CartãoNacionalSUS, novo_Nomecompletodamãe, novo_EndereçocCEP, novo_Telefoneparacontato, novo_HistóriadaDoençaAtual, novo_AchadosnoExameFísico, novo_DescriçãodaConduta, novo_HipóteseDiagnóstica, novo_Carimboeassinatura, novo_Laudomédico, novo_GuiadeRequisição, novo_ambulatorio_selecionado, novo_comentario, registro_id))

        # Confirme as alterações no banco de dados
        connection.commit()

        # Feche a conexão com o banco de dados
        connection.close()

        # Redirecione de volta para a página de listagem após a edição
        return redirect('/dashboard3')
@app.route('/editar_registro2', methods=['POST'])
def editar_registro2():
    if request.method == 'POST':
        registro_id = request.form['id']
        # Obtenha todos os outros campos do formulário
        novo_nome = request.form['Nome']
        novo_Prontuario = request.form.get('Prontuario')
        novo_Atendimento = request.form.get('Atendimento')
        novo_nomeCompleto = request.form.get('nomeCompleto')
        novo_Datadenascimento = request.form.get('Datadenascimento')
        novo_Sexo = request.form.get('Sexo')
        novo_CPFRG = request.form.get('CPFRG')
        novo_CartãoNacionalSUS = request.form.get('CartaoNacionalSUS')
        novo_Nomecompletodamãe = request.form.get('Nomecompletodamae')
        novo_EndereçocCEP = request.form.get('EndereçocCEP')
        novo_Telefoneparacontato = request.form.get('Telefoneparacontato')
        novo_GuiadeRequisiçãodoExame = request.form.get('GuiadeRequisiçãodoExame')
        novo_TermodeLivre = request.form.get('TermodeLivre')
        novo_FichadeOrientação = request.form.get('FichadeOrientação')
        novo_FichadeAdmissão = request.form.get('FichadeAdmissão')
        novo_PrescriçãoMédica = request.form.get('PrescriçãoMédica')
        novo_PrescriçãoMédicadoContraste = request.form.get('PrescriçãoMédicadoContraste')
        novo_EvoluçãoMédicadoProcedimento = request.form.get('EvoluçãoMédicadoProcedimento')
        novo_EvoluçãodaEnfermagem = request.form.get("EvoluçãodaEnfermagem")
        novo_LaudodoExame = request.form.get("LaudodoExame")
        novo_comentario = request.form.get('caixaDeTexto')
        # Conecte-se ao banco de dados
        connection = sqlite3.connect(caminho)
        cursor = connection.cursor()
        # Atualize o registro no banco de dados com os novos valores
        cursor.execute("UPDATE formulario2 SET Nome = ?, Prontuario = ?, Atendimento = ?, nomeCompleto = ?, Datadenascimento = ?, Sexo = ?, CPFRG = ?, CartãoNacionalSUS = ?, Nomecompletodamãe = ?, EndereçocCEP = ?, Telefoneparacontato = ?, GuiadeRequisiçãodoExame = ?, TermodeLivre = ?, FichadeOrientação = ?, FichadeAdmissão = ?, PrescriçãoMédica = ?, PrescriçãoMédicadoContraste = ?, EvoluçãoMédicadoProcedimento = ?, EvoluçãodaEnfermagem = ?, LaudodoExame = ?, caixaDeTexto = ? WHERE id = ?",
                       (novo_nome, novo_Prontuario, novo_Atendimento, novo_nomeCompleto, novo_Datadenascimento, novo_Sexo, novo_CPFRG, novo_CartãoNacionalSUS, novo_Nomecompletodamãe, novo_EndereçocCEP, novo_Telefoneparacontato, novo_GuiadeRequisiçãodoExame, novo_TermodeLivre, novo_FichadeOrientação, novo_FichadeAdmissão,
                        novo_PrescriçãoMédica, novo_PrescriçãoMédicadoContraste, novo_EvoluçãoMédicadoProcedimento, novo_EvoluçãodaEnfermagem, novo_LaudodoExame, novo_comentario, registro_id))

        # Confirme as alterações no banco de dados
        connection.commit()

        # Feche a conexão com o banco de dados
        connection.close()

        # Redirecione de volta para a página de listagem após a edição
        return redirect('/dashboard4')
@app.route('/editar_registro3', methods=['POST'])
def editar_registro3():
    if request.method == 'POST':
        registro_id = request.form['id']
        # Obtenha todos os outros campos do formulário
        novo_nome = request.form['Nome']
        novo_Prontuario = request.form.get('Prontuario')
        novo_Atendimento = request.form.get('Atendimento')
        novo_nomeCompleto = request.form.get('nomeCompleto')
        novo_Datadenascimento = request.form.get('Datadenascimento')
        novo_Sexo = request.form.get('Sexo')
        novo_CPFRG = request.form.get('CPFRG')
        novo_CartãoNacionalSUS = request.form.get('CartaoNacionalSUS')
        novo_Nomecompletodamãe = request.form.get('Nomecompletodamae')
        novo_EndereçocCEP = request.form.get('EndereçocCEP')
        novo_Telefoneparacontato = request.form.get('Telefoneparacontato')

        novo_GuiadeRequisiçãodoExame = request.form.get('GuiadeRequisiçãodoExame')
        novo_FichadeOrientação = request.form.get('FichadeOrientação')
        novo_TermodeLivre = request.form.get('TermodeLivre')
        novo_FichadeAdmissão = request.form.get('FichadeAdmissão')
        novo_PrescriçãoMédica = request.form.get('PrescriçãoMédica')
        novo_EvoluçãoMédica = request.form.get('EvoluçãoMédica')
        novo_EvoluçãodaEnfermagem = request.form.get('EvoluçãodaEnfermagem')
        novo_SolicitaçãodeAnatomopatológico = request.form.get('SolicitaçãodeAnatomopatológico')
        novo_comentario = request.form.get('caixaDeTexto')
        # Conecte-se ao banco de dados
        connection = sqlite3.connect(caminho)
        cursor = connection.cursor()
        # Atualize o registro no banco de dados com os novos valores
        cursor.execute("UPDATE formulario3 SET Nome = ?, Prontuario = ?, Atendimento = ?, nomeCompleto = ?, Datadenascimento = ?, Sexo = ?, CPFRG = ?, CartãoNacionalSUS = ?, Nomecompletodamãe = ?, EndereçocCEP = ?, Telefoneparacontato = ?, GuiadeRequisiçãodoExame = ?,  FichadeOrientação = ?,TermodeLivre = ?, FichadeAdmissão = ?, PrescriçãoMédica = ?, EvoluçãoMédica = ?, EvoluçãodaEnfermagem = ?, SolicitaçãodeAnatomopatológico = ?, caixaDeTexto = ? WHERE id = ?",
                       (novo_nome, novo_Prontuario, novo_Atendimento, novo_nomeCompleto, novo_Datadenascimento, novo_Sexo, novo_CPFRG, novo_CartãoNacionalSUS, novo_Nomecompletodamãe, novo_EndereçocCEP, novo_Telefoneparacontato, novo_GuiadeRequisiçãodoExame,  novo_FichadeOrientação,novo_TermodeLivre, novo_FichadeAdmissão,
                        novo_PrescriçãoMédica, novo_EvoluçãoMédica, novo_EvoluçãodaEnfermagem, novo_SolicitaçãodeAnatomopatológico, novo_comentario, registro_id))

        # Confirme as alterações no banco de dados
        connection.commit()

        # Feche a conexão com o banco de dados
        connection.close()

        # Redirecione de volta para a página de listagem após a edição
        return redirect('/dashboard5')
@app.route('/editar_registro4', methods=['POST'])
def editar_registro4():
    if request.method == 'POST':
        registro_id = request.form['id']
        # Obtenha todos os outros campos do formulário
        novo_nome = request.form['Nome']
        novo_Prontuario = request.form.get('Prontuario')
        novo_Atendimento = request.form.get('Atendimento')
        novo_nomeCompleto = request.form.get('nomeCompleto')
        novo_Datadenascimento = request.form.get('Datadenascimento')
        novo_Sexo = request.form.get('Sexo')
        novo_CPFRG = request.form.get('CPFRG')
        novo_CartãoNacionalSUS = request.form.get('CartaoNacionalSUS')
        novo_Nomecompletodamãe = request.form.get('Nomecompletodamae')
        novo_EndereçocCEP = request.form.get('EndereçocCEP')
        novo_Telefoneparacontato = request.form.get('Telefoneparacontato')

        novo_GuiadeRequisiçãodoExame = request.form.get('GuiadeRequisiçãodoExame')
        novo_TermodeLivre = request.form.get('TermodeLivre')
        novo_FichadeAdmissão = request.form.get('FichadeAdmissão')
        novo_ChecklistProtocolo = request.form.get('ChecklistProtocolo')
        novo_EvoluçãoMédica = request.form.get('EvoluçãoMédica')
        novo_EvoluçãodaEnfermagem = request.form.get('EvoluçãodaEnfermagem')
        novo_SolicitaçãodeAnatomopatológico = request.form.get('SolicitaçãodeAnatomopatológico')
        novo_comentario = request.form.get('caixaDeTexto')
        # Conecte-se ao banco de dados
        connection = sqlite3.connect(caminho)
        cursor = connection.cursor()
        # Atualize o registro no banco de dados com os novos valores
        cursor.execute("UPDATE formulario4 SET Nome = ?, Prontuario = ?, Atendimento = ?, nomeCompleto = ?, Datadenascimento = ?, Sexo = ?, CPFRG = ?, CartãoNacionalSUS = ?, Nomecompletodamãe = ?, EndereçocCEP = ?, Telefoneparacontato = ?, GuiadeRequisiçãodoExame = ?, TermodeLivre = ?, FichadeAdmissão = ?, ChecklistProtocolo = ?, EvoluçãoMédica = ?, EvoluçãodaEnfermagem = ?, SolicitaçãodeAnatomopatológico = ?, caixaDeTexto = ? WHERE id = ?",
                       (novo_nome, novo_Prontuario, novo_Atendimento, novo_nomeCompleto, novo_Datadenascimento, novo_Sexo, novo_CPFRG, novo_CartãoNacionalSUS, novo_Nomecompletodamãe, novo_EndereçocCEP, novo_Telefoneparacontato, novo_GuiadeRequisiçãodoExame,novo_TermodeLivre, novo_FichadeAdmissão, novo_ChecklistProtocolo,
                        novo_EvoluçãoMédica, novo_EvoluçãodaEnfermagem, novo_SolicitaçãodeAnatomopatológico, novo_comentario, registro_id))

        #  GuiadeRequisiçãodoExame
        #         TermodeLivre
        #         FichadeAdmissão
        #         ChecklistProtocolo
        #         EvoluçãoMédica
        #         EvoluçãodaEnfermagem
        #         SolicitaçãodeAnatomopatológico
        connection.commit()

        # Feche a conexão com o banco de dados
        connection.close()

        # Redirecione de volta para a página de listagem após a edição
        return redirect('/dashboard6')
@app.route('/lista1', methods=['GET', 'POST'])
def lista1():
    connection = sqlite3.connect(caminho)
    cursor = connection.cursor()

    if request.method == 'POST':
        data_inicial = request.form['dataInicial']
        data_final = request.form['dataFinal']

        # Converter as datas para objetos datetime
        data_inicial = datetime.datetime.strptime(data_inicial, '%Y-%m-%d')
        data_final = datetime.datetime.strptime(data_final, '%Y-%m-%d')

        # Adicionar um dia à data final para incluir todos os registros da data final
        data_final += timedelta(days=1)

        # Consulta SQL considerando apenas a parte da data
        cursor.execute("SELECT * FROM formulario1 WHERE Data >= ? AND Data < ?", (data_inicial, data_final))
    else:
        cursor.execute("SELECT * FROM formulario1")

    rows = cursor.fetchall()
    connection.close()

    return render_template('consulta1.html', rows=rows, formatarData=formatarData)


@app.route('/lista2', methods=['GET', 'POST'])
def lista2():
    connection = sqlite3.connect(caminho)
    cursor = connection.cursor()

    if request.method == 'POST':
        data_inicial = request.form['dataInicial']
        data_final = request.form['dataFinal']

        # Converter as datas para objetos datetime
        data_inicial = datetime.datetime.strptime(data_inicial, '%Y-%m-%d')
        data_final = datetime.datetime.strptime(data_final, '%Y-%m-%d')

        # Adicionar um dia à data final para incluir todos os registros da data final
        data_final += timedelta(days=1)

        # Consulta SQL considerando apenas a parte da data
        cursor.execute("SELECT * FROM formulario2 WHERE Data >= ? AND Data < ?", (data_inicial, data_final))
    else:
        cursor.execute("SELECT * FROM formulario2")

    rows = cursor.fetchall()
    connection.close()

    return render_template('consulta2.html', rows=rows, formatarData=formatarData)

@app.route('/lista3', methods=['GET', 'POST'])
def lista3():
    connection = sqlite3.connect(caminho)
    cursor = connection.cursor()

    if request.method == 'POST':
        data_inicial = request.form['dataInicial']
        data_final = request.form['dataFinal']

        # Converter as datas para objetos datetime
        data_inicial = datetime.datetime.strptime(data_inicial, '%Y-%m-%d')
        data_final = datetime.datetime.strptime(data_final, '%Y-%m-%d')

        # Adicionar um dia à data final para incluir todos os registros da data final
        data_final += timedelta(days=1)

        # Consulta SQL considerando apenas a parte da data
        cursor.execute("SELECT * FROM formulario3 WHERE Data >= ? AND Data < ?", (data_inicial, data_final))
    else:
        cursor.execute("SELECT * FROM formulario3")

    rows = cursor.fetchall()
    connection.close()

    return render_template('consulta3.html', rows=rows, formatarData=formatarData)
@app.route('/lista4', methods=['GET', 'POST'])
def lista4():
    connection = sqlite3.connect(caminho)
    cursor = connection.cursor()

    if request.method == 'POST':
        data_inicial = request.form['dataInicial']
        data_final = request.form['dataFinal']

        # Converter as datas para objetos datetime
        data_inicial = datetime.datetime.strptime(data_inicial, '%Y-%m-%d')
        data_final = datetime.datetime.strptime(data_final, '%Y-%m-%d')

        # Adicionar um dia à data final para incluir todos os registros da data final
        data_final += timedelta(days=1)

        # Consulta SQL considerando apenas a parte da data
        cursor.execute("SELECT * FROM formulario4 WHERE Data >= ? AND Data < ?", (data_inicial, data_final))
    else:
        cursor.execute("SELECT * FROM formulario4")

    rows = cursor.fetchall()
    connection.close()

    return render_template('consulta4.html', rows=rows, formatarData=formatarData)
###############################
@app.route('/auditar4', methods=['GET', 'POST'])
def auditar4():
    # Verifique se o usuário está logado
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect(caminho)
    cursor = conn.cursor()
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    username = session['username']
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS formulario3 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome CHAR(100),
                Prontuario NUMERIC(100),
                Atendimento NUMERIC(100),
                nomeCompleto CHAR(100),
                Datadenascimento CHAR(100),
                Sexo CHAR(100),
                CPFRG CHAR(100),
                CartãoNacionalSUS CHAR(100),
                Nomecompletodamãe CHAR(100),
                EndereçocCEP CHAR(100),
                Telefoneparacontato CHAR(100),
                GuiadeRequisiçãodoExame CHAR(100),
                FichadeOrientação CHAR(100),
                TermodeLivre CHAR(100),
                FichadeAdmissão CHAR(100),
                PrescriçãoMédica CHAR(100),
                EvoluçãoMédica CHAR(100),
                EvoluçãodaEnfermagem CHAR(100),
                SolicitaçãodeAnatomopatológico CHAR(100),
                caixaDeTexto CHAR,
                Status CHAR,
                Usuario CHAR(100),
                Data DATETIME
            )
        ''')

    try:

        if request.method == 'POST':
            Nome = request.form['Nome']

            if Nome.strip() == "":
                flash('O campo "Nome" não pode estar em branco.', 'error')
            else:
                Nome = request.form['Nome']
                Prontuario = request.form.get('Prontuario')
                Atendimento = request.form.get('Atendimento')
                nomeCompleto = request.form.get('nomeCompleto')
                Datadenascimento = request.form.get('Datadenascimento')
                Sexo = request.form.get('Sexo')
                CPFRG = request.form.get('CPFRG')  # Correção aqui
                CartãoNacionalSUS = request.form.get('CartãoNacionalSUS')
                Nomecompletodamãe = request.form.get('Nomecompletodamãe')
                EndereçocCEP = request.form.get('EndereçocCEP')
                Telefoneparacontato = request.form.get('Telefoneparacontato')
                GuiadeRequisiçãodoExame = request.form.get('GuiadeRequisiçãodoExame')
                TermodeLivre = request.form.get('TermodeLivre')
                FichadeOrientação = request.form.get('FichadeOrientação')
                FichadeAdmissão = request.form.get('FichadeAdmissão')
                PrescriçãoMédica = request.form.get('PrescriçãoMédica')
                EvoluçãoMédica = request.form.get('EvoluçãoMédica')
                EvoluçãodaEnfermagem = request.form.get('EvoluçãodaEnfermagem')
                SolicitaçãodeAnatomopatológico = request.form.get('SolicitaçãodeAnatomopatológico')
                comentario = request.form.get('caixaDeTexto')
                if nomeCompleto == "Conforme":
                    nomeCompleto_valor = 1
                elif nomeCompleto == "Não Conforme":
                    nomeCompleto_valor = 0
                elif nomeCompleto == "Não se Aplica":
                    nomeCompleto_valor = 1
                else:
                    nomeCompleto_valor = None
                ######
                if Datadenascimento == "Conforme":
                    Datadenascimento_valor = 1
                elif Datadenascimento == "Não Conforme":
                    Datadenascimento_valor = 0
                elif Datadenascimento == "Não se Aplica":
                    Datadenascimento_valor = 1
                else:
                    Datadenascimento_valor = None
                #########
                if Sexo == "Conforme":
                    Sexo_valor = 1
                elif Sexo == "Não Conforme":
                    Sexo_valor = 0
                elif Sexo == "Não se Aplica":
                    Sexo_valor = 1
                else:
                    Sexo_valor = None
                #########
                if CPFRG == "Conforme":
                    CPFRG_valor = 1
                elif CPFRG == "Não Conforme":
                    CPFRG_valor = 0
                elif CPFRG == "Não se Aplica":
                    CPFRG_valor = 1
                else:
                    CPFRG_valor = None
                ###########
                if CartãoNacionalSUS == "Conforme":
                    CartãoNacionalSUS_valor = 1
                elif CartãoNacionalSUS == "Não Conforme":
                    CartãoNacionalSUS_valor = 0
                elif CartãoNacionalSUS == "Não se Aplica":
                    CartãoNacionalSUS_valor = 1
                else:
                    CartãoNacionalSUS_valor = None
                ############
                if Nomecompletodamãe == "Conforme":
                    Nomecompletodamãe_valor = 1
                elif Nomecompletodamãe == "Não Conforme":
                    Nomecompletodamãe_valor = 0
                elif Nomecompletodamãe == "Não se Aplica":
                    Nomecompletodamãe_valor = 1
                else:
                    Nomecompletodamãe_valor = None
                ######
                EndereçocCEP = request.form.get('EndereçocCEP')
                if EndereçocCEP == "Conforme":
                    EndereçocCEP_valor = 1
                elif EndereçocCEP == "Não Conforme":
                    EndereçocCEP_valor = 0
                elif EndereçocCEP == "Não se Aplica":
                    EndereçocCEP_valor = 1
                else:
                    EndereçocCEP_valor = None

                if Telefoneparacontato == "Conforme":
                    Telefoneparacontato_valor = 1
                elif Telefoneparacontato == "Não Conforme":
                    Telefoneparacontato_valor = 0
                elif Telefoneparacontato == "Não se Aplica":
                    Telefoneparacontato_valor = 1
                else:
                    Telefoneparacontato_valor = None

                if GuiadeRequisiçãodoExame == "Conforme":
                    GuiadeRequisiçãodoExame_valor = 1
                elif GuiadeRequisiçãodoExame == "Não Conforme":
                    GuiadeRequisiçãodoExame_valor = 0
                elif GuiadeRequisiçãodoExame == "Não se Aplica":
                    GuiadeRequisiçãodoExame_valor = 1
                else:
                    GuiadeRequisiçãodoExame_valor = None



                if FichadeOrientação == "Conforme":
                    FichadeOrientação_valor = 1
                elif FichadeOrientação == "Não Conforme":
                    FichadeOrientação_valor = 0
                elif FichadeOrientação == "Não se Aplica":
                    FichadeOrientação_valor = 1
                else:
                    FichadeOrientação_valor = None

                if TermodeLivre == "Conforme":
                    TermodeLivre_valor = 1
                elif TermodeLivre == "Não Conforme":
                    TermodeLivre_valor = 0
                elif TermodeLivre == "Não se Aplica":
                    TermodeLivre_valor = 1
                else:
                    TermodeLivre_valor = None

                if FichadeAdmissão == "Conforme":
                    FichadeAdmissão_valor = 1
                elif FichadeAdmissão == "Não Conforme":
                    FichadeAdmissão_valor = 0
                elif FichadeAdmissão == "Não se Aplica":
                    FichadeAdmissão_valor = 1
                else:
                    FichadeAdmissão_valor = None


                if PrescriçãoMédica == "Conforme":
                    PrescriçãoMédica_valor = 1
                elif PrescriçãoMédica == "Não Conforme":
                    PrescriçãoMédica_valor = 0
                elif PrescriçãoMédica == "Não se Aplica":
                    PrescriçãoMédica_valor = 1
                else:
                    PrescriçãoMédica_valor = None

                if EvoluçãoMédica == "Conforme":
                    EvoluçãoMédica_valor = 1
                elif EvoluçãoMédica == "Não Conforme":
                    EvoluçãoMédica_valor = 0
                elif EvoluçãoMédica == "Não se Aplica":
                    EvoluçãoMédica_valor = 1
                else:
                    EvoluçãoMédica_valor = None

                if EvoluçãodaEnfermagem == "Conforme":
                    EvoluçãodaEnfermagem_valor = 1
                elif EvoluçãodaEnfermagem == "Não Conforme":
                    EvoluçãodaEnfermagem_valor = 0
                elif EvoluçãodaEnfermagem == "Não se Aplica":
                    EvoluçãodaEnfermagem_valor = 1
                else:
                    EvoluçãodaEnfermagem_valor = None

                if SolicitaçãodeAnatomopatológico == "Conforme":
                    SolicitaçãodeAnatomopatológico_valor = 1
                elif SolicitaçãodeAnatomopatológico == "Não Conforme":
                    SolicitaçãodeAnatomopatológico_valor = 0
                elif SolicitaçãodeAnatomopatológico == "Não se Aplica":
                    SolicitaçãodeAnatomopatológico_valor = 1
                else:
                    SolicitaçãodeAnatomopatológico_valor = None





                # Adicione os campos adicionais e seus valores conforme necessário
                valores_conformidade = {
                    "Conforme": 1,
                    "Não se Aplica": 1,
                    "Não Conforme": 0
                }
                campos_conformidade = [
                    request.form.get('nomeCompleto'),
                    request.form.get('Datadenascimento'),
                    request.form.get('Sexo'),
                    request.form.get('CPFRG'),
                    request.form.get('CartãoNacionalSUS'),
                    request.form.get('Nomecompletodamãe'),
                    request.form.get('GuiadeRequisiçãodoExame'),
                    request.form.get('TermodeLivre'),
                    request.form.get('FichadeOrientação'),
                    request.form.get('FichadeAdmissão'),
                    request.form.get('PrescriçãoMédica'),
                    request.form.get('EvoluçãodaEnfermagem'),
                    request.form.get('SolicitaçãodeAnatomopatológico'),


                    # Adicione outros campos conforme necessário
                ]

                if (nomeCompleto == "Não Conforme" or
                        Datadenascimento == "Não Conforme" or
                        Sexo == "Não Conforme" or
                        Nomecompletodamãe == "Não Conforme" or
                        CartãoNacionalSUS == "Não Conforme" or
                        EndereçocCEP == "Não Conforme"):
                    Status = "Insuficiente"
                else:
                    # Calcular a pontuação total
                    pontuacao_total = sum(valores_conformidade[conformidade] for conformidade in campos_conformidade)
                    # Calcular o percentual
                    percentual = (pontuacao_total / len(campos_conformidade)) * 100

                    # Definir o campo "Status" com base nos intervalos
                    if percentual >= 90:
                        Status = "Excelente"
                    elif 70 <= percentual < 90:
                        Status = "Bom"
                    elif 50 <= percentual < 70:
                        Status = "Razoável"
                    else:
                        Status = "Insuficiente"
                cursor.execute('''
                                INSERT INTO formulario3 (
                                    Nome, Prontuario, Atendimento, nomeCompleto, Datadenascimento, 
                                    Sexo, CPFRG, CartãoNacionalSUS, Nomecompletodamãe, EndereçocCEP, 
                                    Telefoneparacontato, GuiadeRequisiçãodoExame, FichadeOrientação, 
                                    TermodeLivre, FichadeAdmissão, PrescriçãoMédica, EvoluçãoMédica, 
                                    EvoluçãodaEnfermagem, SolicitaçãodeAnatomopatológico, caixaDeTexto, Status, Usuario, Data
                                )
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (Nome, Prontuario, Atendimento, nomeCompleto, Datadenascimento,
                                  Sexo, CPFRG, CartãoNacionalSUS, Nomecompletodamãe, EndereçocCEP,
                                  Telefoneparacontato, GuiadeRequisiçãodoExame, FichadeOrientação,
                                    TermodeLivre, FichadeAdmissão, PrescriçãoMédica, EvoluçãoMédica,
                                    EvoluçãodaEnfermagem, SolicitaçãodeAnatomopatológico, comentario, Status, username, data_hora))
                conn.commit()
                conn.close()
                return render_template('auditar4.html', username=username)
    except sqlite3.Error as e:
        # Trate o erro aqui e imprima mensagens para depuração
        print("Erro no banco de dados:", e)
    return render_template('auditar4.html', username=username)
#################################
@app.route('/auditar3', methods=['GET', 'POST'])
def auditar3():
    # Verifique se o usuário está logado
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect(caminho)
    cursor = conn.cursor()
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    username = session['username']
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS formulario2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome CHAR(100),
                Prontuario NUMERIC(100),
                Atendimento NUMERIC(100),
                nomeCompleto CHAR(100),
                Datadenascimento CHAR(100),
                Sexo CHAR(100),
                CPFRG CHAR(100),
                CartãoNacionalSUS CHAR(100),
                Nomecompletodamãe CHAR(100),
                EndereçocCEP CHAR(100),
                Telefoneparacontato CHAR(100),
                GuiadeRequisiçãodoExame CHAR(100),
                TermodeLivre CHAR(100),
                FichadeOrientação CHAR(100),
                FichadeAdmissão CHAR(100),
                PrescriçãoMédica CHAR(100),
                PrescriçãoMédicadoContraste CHAR(100),
                EvoluçãoMédicadoProcedimento CHAR(100),
                EvoluçãodaEnfermagem CHAR(100),
                LaudodoExame CHAR(100),
                caixaDeTexto CHAR,
                Status CHAR,
                Usuario CHAR(100),
                Data DATETIME
            )
        ''')

    try:

        if request.method == 'POST':
            Nome = request.form['Nome']

            if Nome.strip() == "":
                flash('O campo "Nome" não pode estar em branco.', 'error')
            else:
                Nome = request.form['Nome']
                Prontuario = request.form.get('Prontuario')
                Atendimento = request.form.get('Atendimento')
                nomeCompleto = request.form.get('nomeCompleto')
                Datadenascimento = request.form.get('Datadenascimento')
                Sexo = request.form.get('Sexo')
                CPFRG = request.form.get('CPFRG')  # Correção aqui
                CartãoNacionalSUS = request.form.get('CartãoNacionalSUS')
                Nomecompletodamãe = request.form.get('Nomecompletodamãe')
                EndereçocCEP = request.form.get('EndereçocCEP')
                Telefoneparacontato = request.form.get('Telefoneparacontato')
                GuiadeRequisiçãodoExame = request.form.get('GuiadeRequisiçãodoExame')
                TermodeLivre = request.form.get('TermodeLivre')
                FichadeOrientação = request.form.get('FichadeOrientação')
                FichadeAdmissão = request.form.get('FichadeAdmissão')
                PrescriçãoMédica = request.form.get('PrescriçãoMédica')
                PrescriçãoMédicadoContraste = request.form.get('PrescriçãoMédicadoContraste')
                EvoluçãoMédicadoProcedimento = request.form.get('EvoluçãoMédicadoProcedimento')
                EvoluçãodaEnfermagem = request.form.get('EvoluçãodaEnfermagem')
                LaudodoExame = request.form.get('LaudodoExame')
                comentario = request.form.get('caixaDeTexto')
                if nomeCompleto == "Conforme":
                    nomeCompleto_valor = 1
                elif nomeCompleto == "Não Conforme":
                    nomeCompleto_valor = 0
                elif nomeCompleto == "Não se Aplica":
                    nomeCompleto_valor = 1
                else:
                    nomeCompleto_valor = None
                ######
                if Datadenascimento == "Conforme":
                    Datadenascimento_valor = 1
                elif Datadenascimento == "Não Conforme":
                    Datadenascimento_valor = 0
                elif Datadenascimento == "Não se Aplica":
                    Datadenascimento_valor = 1
                else:
                    Datadenascimento_valor = None
                #########
                if Sexo == "Conforme":
                    Sexo_valor = 1
                elif Sexo == "Não Conforme":
                    Sexo_valor = 0
                elif Sexo == "Não se Aplica":
                    Sexo_valor = 1
                else:
                    Sexo_valor = None
                #########
                if CPFRG == "Conforme":
                    CPFRG_valor = 1
                elif CPFRG == "Não Conforme":
                    CPFRG_valor = 0
                elif CPFRG == "Não se Aplica":
                    CPFRG_valor = 1
                else:
                    CPFRG_valor = None
                ###########
                if CartãoNacionalSUS == "Conforme":
                    CartãoNacionalSUS_valor = 1
                elif CartãoNacionalSUS == "Não Conforme":
                    CartãoNacionalSUS_valor = 0
                elif CartãoNacionalSUS == "Não se Aplica":
                    CartãoNacionalSUS_valor = 1
                else:
                    CartãoNacionalSUS_valor = None
                ############
                if Nomecompletodamãe == "Conforme":
                    Nomecompletodamãe_valor = 1
                elif Nomecompletodamãe == "Não Conforme":
                    Nomecompletodamãe_valor = 0
                elif Nomecompletodamãe == "Não se Aplica":
                    Nomecompletodamãe_valor = 1
                else:
                    Nomecompletodamãe_valor = None
                ######
                EndereçocCEP = request.form.get('EndereçocCEP')
                if EndereçocCEP == "Conforme":
                    EndereçocCEP_valor = 1
                elif EndereçocCEP == "Não Conforme":
                    EndereçocCEP_valor = 0
                elif EndereçocCEP == "Não se Aplica":
                    EndereçocCEP_valor = 1
                else:
                    EndereçocCEP_valor = None

                if Telefoneparacontato == "Conforme":
                    Telefoneparacontato_valor = 1
                elif Telefoneparacontato == "Não Conforme":
                    Telefoneparacontato_valor = 0
                elif Telefoneparacontato == "Não se Aplica":
                    Telefoneparacontato_valor = 1
                else:
                    Telefoneparacontato_valor = None

                if GuiadeRequisiçãodoExame == "Conforme":
                    GuiadeRequisiçãodoExame_valor = 1
                elif GuiadeRequisiçãodoExame == "Não Conforme":
                    GuiadeRequisiçãodoExame_valor = 0
                elif GuiadeRequisiçãodoExame == "Não se Aplica":
                    GuiadeRequisiçãodoExame_valor = 1
                else:
                    GuiadeRequisiçãodoExame_valor = None

                if TermodeLivre == "Conforme":
                    TermodeLivre_valor = 1
                elif TermodeLivre == "Não Conforme":
                    TermodeLivre_valor = 0
                elif TermodeLivre == "Não se Aplica":
                    TermodeLivre_valor = 1
                else:
                    TermodeLivre_valor = None

                if FichadeOrientação == "Conforme":
                    FichadeOrientação_valor = 1
                elif FichadeOrientação == "Não Conforme":
                    FichadeOrientação_valor = 0
                elif FichadeOrientação == "Não se Aplica":
                    FichadeOrientação_valor = 1
                else:
                    FichadeOrientação_valor = None

                if FichadeAdmissão == "Conforme":
                    FichadeAdmissão_valor = 1
                elif FichadeAdmissão == "Não Conforme":
                    FichadeAdmissão_valor = 0
                elif FichadeAdmissão == "Não se Aplica":
                    FichadeAdmissão_valor = 1
                else:
                    FichadeAdmissão_valor = None

                if PrescriçãoMédica == "Conforme":
                    PrescriçãoMédica_valor = 1
                elif PrescriçãoMédica == "Não Conforme":
                    PrescriçãoMédica_valor = 0
                elif PrescriçãoMédica == "Não se Aplica":
                    PrescriçãoMédica_valor = 1
                else:
                    PrescriçãoMédica_valor = None

                if PrescriçãoMédicadoContraste == "Conforme":
                    PrescriçãoMédicadoContraste_valor = 1
                elif PrescriçãoMédicadoContraste == "Não Conforme":
                    PrescriçãoMédicadoContraste_valor = 0
                elif PrescriçãoMédicadoContraste == "Não se Aplica":
                    PrescriçãoMédicadoContraste_valor = 1
                else:
                    PrescriçãoMédicadoContraste = None

                if EvoluçãoMédicadoProcedimento == "Conforme":
                    EvoluçãoMédicadoProcedimento_valor = 1
                elif EvoluçãoMédicadoProcedimento == "Não Conforme":
                    EvoluçãoMédicadoProcedimento_valor = 0
                elif EvoluçãoMédicadoProcedimento == "Não se Aplica":
                    EvoluçãoMédicadoProcedimento_valor = 1
                else:
                    EvoluçãoMédicadoProcedimento_valor = None

                if EvoluçãodaEnfermagem == "Conforme":
                    EvoluçãodaEnfermagem_valor = 1
                elif EvoluçãodaEnfermagem == "Não Conforme":
                    EvoluçãodaEnfermagem_valor = 0
                elif EvoluçãodaEnfermagem == "Não se Aplica":
                    EvoluçãodaEnfermagem_valor = 1
                else:
                    EvoluçãodaEnfermagem_valor = None

                if LaudodoExame == "Conforme":
                    LaudodoExame_valor = 1
                elif LaudodoExame == "Não Conforme":
                    LaudodoExame_valor = 0
                elif LaudodoExame == "Não se Aplica":
                    LaudodoExame_valor = 1
                else:
                    LaudodoExame_valor = None



                # Adicione os campos adicionais e seus valores conforme necessário
                valores_conformidade = {
                    "Conforme": 1,
                    "Não se Aplica": 1,
                    "Não Conforme": 0
                }
                campos_conformidade = [
                    request.form.get('nomeCompleto'),
                    request.form.get('Datadenascimento'),
                    request.form.get('Sexo'),
                    request.form.get('CPFRG'),
                    request.form.get('CartãoNacionalSUS'),
                    request.form.get('Nomecompletodamãe'),
                    request.form.get('GuiadeRequisiçãodoExame'),
                    request.form.get('TermodeLivre'),
                    request.form.get('FichadeOrientação'),
                    request.form.get('FichadeAdmissão'),
                    request.form.get('PrescriçãoMédica'),
                    request.form.get('PrescriçãoMédicadoContraste'),
                    request.form.get('EvoluçãoMédicadoProcedimento'),
                    request.form.get('EvoluçãodaEnfermagem'),
                    request.form.get('LaudodoExame'),

                    # Adicione outros campos conforme necessário
                ]

                if (nomeCompleto == "Não Conforme" or
                        Datadenascimento == "Não Conforme" or
                        Sexo == "Não Conforme" or
                        Nomecompletodamãe == "Não Conforme" or
                        CartãoNacionalSUS == "Não Conforme" or
                        EndereçocCEP == "Não Conforme"):
                    Status = "Insuficiente"
                else:
                    # Calcular a pontuação total
                    pontuacao_total = sum(valores_conformidade[conformidade] for conformidade in campos_conformidade)
                    # Calcular o percentual
                    percentual = (pontuacao_total / len(campos_conformidade)) * 100

                    # Definir o campo "Status" com base nos intervalos
                    if percentual >= 90:
                        Status = "Excelente"
                    elif 70 <= percentual < 90:
                        Status = "Bom"
                    elif 50 <= percentual < 70:
                        Status = "Razoável"
                    else:
                        Status = "Insuficiente"
                cursor.execute('''
                                INSERT INTO formulario2 (
                                    Nome, Prontuario, Atendimento, nomeCompleto, Datadenascimento, 
                                    Sexo, CPFRG, CartãoNacionalSUS, Nomecompletodamãe, EndereçocCEP, 
                                    Telefoneparacontato, GuiadeRequisiçãodoExame, TermodeLivre, 
                                    FichadeOrientação, FichadeAdmissão, PrescriçãoMédica, PrescriçãoMédicadoContraste, 
                                    EvoluçãoMédicadoProcedimento, EvoluçãodaEnfermagem, LaudodoExame, caixaDeTexto, Status, Usuario, Data
                                )
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (Nome, Prontuario, Atendimento, nomeCompleto, Datadenascimento,
                                  Sexo, CPFRG, CartãoNacionalSUS, Nomecompletodamãe, EndereçocCEP,
                                  Telefoneparacontato, GuiadeRequisiçãodoExame, TermodeLivre,
                                    FichadeOrientação, FichadeAdmissão, PrescriçãoMédica, PrescriçãoMédicadoContraste,
                                    EvoluçãoMédicadoProcedimento, EvoluçãodaEnfermagem, LaudodoExame, comentario, Status, username, data_hora))
                conn.commit()
                conn.close()
                return render_template('auditar3.html', username=username)
    except sqlite3.Error as e:
        # Trate o erro aqui e imprima mensagens para depuração
        print("Erro no banco de dados:", e)
    return render_template('auditar3.html', username=username)

################################
@app.route('/auditar2', methods=['GET', 'POST'])
def auditar2():
    # Verifique se o usuário está logado
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect(caminho)
    cursor = conn.cursor()
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    username = session['username']
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS formulario1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome CHAR(100),
            Prontuario NUMERIC(100),
            Atendimento NUMERIC(100),
            nomeCompleto CHAR(100),
            Datadenascimento CHAR(100),
            Sexo CHAR(100),
            CPFRG CHAR(100),
            CartãoNacionalSUS CHAR(100),
            Nomecompletodamãe CHAR(100),
            EndereçocCEP CHAR(100),
            Telefoneparacontato CHAR(100),
            HistóriadaDoençaAtual CHAR(100),
            AchadosnoExameFísico CHAR(100),
            DescriçãodaConduta CHAR(100),
            HipóteseDiagnóstica CHAR(100),
            Carimboeassinatura CHAR(100),
            Laudomédico CHAR(100),
            GuiadeRequisição CHAR(100),
            ambulatorio_selecionado CHAR(100),
            caixaDeTexto CHAR,
            Status CHAR,
            Usuario CHAR(100),
            Data DATETIME
        )
    ''')

    try:

        if request.method == 'POST':
            Nome = request.form['Nome']

            if Nome.strip() == "":
                flash('O campo "Nome" não pode estar em branco.', 'error')
            else:
                Nome = request.form['Nome']
                Prontuario = request.form.get('Prontuario')
                Atendimento = request.form.get('Atendimento')
                nomeCompleto = request.form.get('nomeCompleto')
                Datadenascimento = request.form.get('Datadenascimento')
                Sexo = request.form.get('Sexo')
                CPFRG = request.form.get('CPFRG')  # Correção aqui
                CartãoNacionalSUS = request.form.get('CartãoNacionalSUS')
                Nomecompletodamãe = request.form.get('Nomecompletodamãe')
                EndereçocCEP = request.form.get('EndereçocCEP')
                Telefoneparacontato = request.form.get('Telefoneparacontato')
                HistóriadaDoençaAtual = request.form.get('HistóriadaDoençaAtual')
                AchadosnoExameFísico = request.form.get('AchadosnoExameFísico')
                DescriçãodaConduta = request.form.get('DescriçãodaConduta')
                GuiadeRequisição = request.form.get('GuiadeRequisição')
                HipóteseDiagnóstica = request.form.get('HipóteseDiagnóstica')
                Carimboeassinatura = request.form.get('Carimboeassinatura')
                Laudomédico = request.form.get('Laudomédico')

                ambulatorio_selecionado = request.form.get("ambulatorio")

                comentario = request.form.get('caixaDeTexto')
                if nomeCompleto == "Conforme":
                    nomeCompleto_valor = 1
                elif nomeCompleto == "Não Conforme":
                    nomeCompleto_valor = 0
                elif nomeCompleto == "Não se Aplica":
                    nomeCompleto_valor = 1
                else:
                    nomeCompleto_valor = None
                ######
                if Datadenascimento == "Conforme":
                    Datadenascimento_valor = 1
                elif Datadenascimento == "Não Conforme":
                    Datadenascimento_valor = 0
                elif Datadenascimento == "Não se Aplica":
                    Datadenascimento_valor = 1
                else:
                    Datadenascimento_valor = None
                #########
                if Sexo == "Conforme":
                    Sexo_valor = 1
                elif Sexo == "Não Conforme":
                    Sexo_valor = 0
                elif Sexo == "Não se Aplica":
                    Sexo_valor = 1
                else:
                    Sexo_valor = None
                #########
                if CPFRG == "Conforme":
                    CPFRG_valor = 1
                elif CPFRG == "Não Conforme":
                    CPFRG_valor = 0
                elif CPFRG == "Não se Aplica":
                    CPFRG_valor = 1
                else:
                    CPFRG_valor = None
                ###########
                if CartãoNacionalSUS == "Conforme":
                    CartãoNacionalSUS_valor = 1
                elif CartãoNacionalSUS == "Não Conforme":
                    CartãoNacionalSUS_valor = 0
                elif CartãoNacionalSUS == "Não se Aplica":
                    CartãoNacionalSUS_valor = 1
                else:
                    CartãoNacionalSUS_valor = None
                ############
                if Nomecompletodamãe == "Conforme":
                    Nomecompletodamãe_valor = 1
                elif Nomecompletodamãe == "Não Conforme":
                    Nomecompletodamãe_valor = 0
                elif Nomecompletodamãe == "Não se Aplica":
                    Nomecompletodamãe_valor = 1
                else:
                    Nomecompletodamãe_valor = None
                ######
                EndereçocCEP = request.form.get('EndereçocCEP')
                if EndereçocCEP == "Conforme":
                    EndereçocCEP_valor = 1
                elif EndereçocCEP == "Não Conforme":
                    EndereçocCEP_valor = 0
                elif EndereçocCEP == "Não se Aplica":
                    EndereçocCEP_valor = 1
                else:
                    EndereçocCEP_valor = None

                if Telefoneparacontato == "Conforme":
                    Telefoneparacontato_valor = 1
                elif Telefoneparacontato == "Não Conforme":
                    Telefoneparacontato_valor = 0
                elif Telefoneparacontato == "Não se Aplica":
                    Telefoneparacontato_valor = 1
                else:
                    Telefoneparacontato_valor = None

                if HistóriadaDoençaAtual == "Conforme":
                    HistóriadaDoençaAtual_valor = 1
                elif HistóriadaDoençaAtual == "Não Conforme":
                    HistóriadaDoençaAtual_valor = 0
                elif HistóriadaDoençaAtual == "Não se Aplica":
                    HistóriadaDoençaAtual_valor = 1
                else:
                    HistóriadaDoençaAtual_valor = None

                if AchadosnoExameFísico == "Conforme":
                    AchadosnoExameFísico_valor = 1
                elif AchadosnoExameFísico == "Não Conforme":
                    AchadosnoExameFísico_valor = 0
                elif AchadosnoExameFísico == "Não se Aplica":
                    AchadosnoExameFísico_valor = 1
                else:
                    AchadosnoExameFísico_valor = None

                if DescriçãodaConduta == "Conforme":
                    DescriçãodaConduta_valor = 1
                elif DescriçãodaConduta == "Não Conforme":
                    DescriçãodaConduta_valor = 0
                elif DescriçãodaConduta == "Não se Aplica":
                    DescriçãodaConduta_valor = 1
                else:
                    DescriçãodaConduta_valor = None

                if HipóteseDiagnóstica == "Conforme":
                    HipóteseDiagnóstica_valor = 1
                elif HipóteseDiagnóstica == "Não Conforme":
                    HipóteseDiagnóstica_valor = 0
                elif HipóteseDiagnóstica == "Não se Aplica":
                    HipóteseDiagnóstica_valor = 1
                else:
                    HipóteseDiagnóstica_valor = None

                if Carimboeassinatura == "Conforme":
                    Carimboeassinatura_valor = 1
                elif Carimboeassinatura == "Não Conforme":
                    Carimboeassinatura_valor = 0
                elif Carimboeassinatura == "Não se Aplica":
                    Carimboeassinatura_valor = 1
                else:
                    Carimboeassinatura_valor = None

                if Laudomédico == "Conforme":
                    Laudomédico_valor = 1
                elif Laudomédico == "Não Conforme":
                    Laudomédico_valor = 0
                elif Laudomédico == "Não se Aplica":
                    Laudomédico_valor = 1
                else:
                    Laudomédico_valor = None

                if GuiadeRequisição == "Conforme":
                    GuiadeRequisição_valor = 1
                elif GuiadeRequisição == "Não Conforme":
                    GuiadeRequisição_valor = 0
                elif GuiadeRequisição == "Não se Aplica":
                    GuiadeRequisição_valor = 1
                else:
                    GuiadeRequisição_valor = None
                print("Valores a serem inseridos:")
                print("Nome:", Nome)
                print("Prontuario:", Prontuario)
                print("Atendimento:", Atendimento)
                print("nomeCompleto:", nomeCompleto_valor)
                print("Datadenascimento:", Datadenascimento_valor)
                print("Sexo:", Sexo_valor)
                print("CPFRG:", CPFRG_valor)
                print("CartãoNacionalSUS:", CartãoNacionalSUS_valor)
                print("Nomecompletodamãe:", Nomecompletodamãe_valor)
                print("EndereçocCEP:", EndereçocCEP_valor)
                print("Telefoneparacontato:", Telefoneparacontato_valor)
                print("HistóriadaDoençaAtual:", HistóriadaDoençaAtual_valor)
                print("AchadosnoExameFísico_valor:", AchadosnoExameFísico_valor)
                print("DescriçãodaConduta_valor:", DescriçãodaConduta_valor)
                print("HipóteseDiagnóstica_valor:", HipóteseDiagnóstica_valor)
                print("Carimboeassinatura_valor:", Carimboeassinatura_valor)
                print("Laudomédico_valor:", Laudomédico_valor)
                print("GuiadeRequisição_valor:", GuiadeRequisição_valor)
                print("Valor selecionado:", ambulatorio_selecionado)
                print("caixaDeTexto:", comentario)
                print("username:", username)
                print("data_hora:", data_hora)
                # Adicione os campos adicionais e seus valores conforme necessário
                valores_conformidade = {
                    "Conforme": 1,
                    "Não se Aplica": 1,
                    "Não Conforme": 0
                }
                campos_conformidade = [
                    request.form.get('nomeCompleto'),
                    request.form.get('Datadenascimento'),
                    request.form.get('Sexo'),
                    request.form.get('CPFRG'),
                    request.form.get('CartãoNacionalSUS'),
                    request.form.get('Nomecompletodamãe'),
                    request.form.get('Telefoneparacontato'),
                    request.form.get('HistóriadaDoençaAtual'),
                    request.form.get('AchadosnoExameFísico'),
                    request.form.get('DescriçãodaConduta'),
                    request.form.get('HipóteseDiagnóstica'),
                    request.form.get('Carimboeassinatura'),
                    request.form.get('Laudomédico'),
                    request.form.get('GuiadeRequisição'),




                    # Adicione outros campos conforme necessário
                ]

                if (nomeCompleto == "Não Conforme" or
                        Datadenascimento == "Não Conforme" or
                        Sexo == "Não Conforme" or
                        Nomecompletodamãe == "Não Conforme" or
                        CartãoNacionalSUS == "Não Conforme" or
                        EndereçocCEP == "Não Conforme"):
                    Status = "Insuficiente"
                else:
                    # Calcular a pontuação total
                    pontuacao_total = sum(valores_conformidade[conformidade] for conformidade in campos_conformidade)
                    # Calcular o percentual
                    percentual = (pontuacao_total / len(campos_conformidade)) * 100

                    # Definir o campo "Status" com base nos intervalos
                    if percentual >= 90:
                        Status = "Excelente"
                    elif 70 <= percentual < 90:
                        Status = "Bom"
                    elif 50 <= percentual < 70:
                        Status = "Razoável"
                    else:
                        Status = "Insuficiente"
                cursor.execute('''
                            INSERT INTO formulario1 (
                                Nome, Prontuario, Atendimento, nomeCompleto, Datadenascimento, 
                                Sexo, CPFRG, CartãoNacionalSUS, Nomecompletodamãe, EndereçocCEP, 
                                Telefoneparacontato, HistóriadaDoençaAtual, AchadosnoExameFísico, 
                                DescriçãodaConduta, HipóteseDiagnóstica, Carimboeassinatura, Laudomédico, 
                                GuiadeRequisição, ambulatorio_selecionado, caixaDeTexto, Status, Usuario, Data
                            )
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (Nome, Prontuario, Atendimento, nomeCompleto, Datadenascimento,
                              Sexo, CPFRG, CartãoNacionalSUS, Nomecompletodamãe, EndereçocCEP,
                              Telefoneparacontato, HistóriadaDoençaAtual, AchadosnoExameFísico,
                              DescriçãodaConduta, HipóteseDiagnóstica, Carimboeassinatura,
                              Laudomédico,
                              GuiadeRequisição, ambulatorio_selecionado, comentario, Status, username, data_hora))
                conn.commit()
                conn.close()
                return render_template('auditar.html', username=username)
    except sqlite3.Error as e:
        # Trate o erro aqui e imprima mensagens para depuração
        print("Erro no banco de dados:", e)

    return render_template('auditar2.html', username=username)
def formatarData(dataDB):
    if dataDB:
        partes = dataDB.split(" ")
        dataPartes = partes[0].split("-")

        # Verifica se dataPartes tem pelo menos três elementos
        if len(dataPartes) >= 3:
            dataFormatada = f"{dataPartes[2]}/{dataPartes[1]}/{dataPartes[0]}"
            return dataFormatada
        else:
            return "Data inválida"

@app.route('/exportar_excel', methods=['POST'])
def exportar_excel():

    consulta_sql = "SELECT * FROM formulario1"

    conn = sqlite3.connect(caminho)

    df = pd.read_sql_query(consulta_sql, conn)

    # Crie um objeto BytesIO para armazenar o arquivo Excel
    output = BytesIO()

    # Use o pandas para salvar o DataFrame como um arquivo Excel no objeto BytesIO
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="formulario1")
    writer.close()

    # Configure os cabeçalhos da resposta para indicar um arquivo Excel
    output.seek(0)
    response = Response(output.read())
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response.headers["Content-Disposition"] = "attachment; filename=formulario1.xlsx"

    return response
@app.route('/exportar_excel2', methods=['POST'])
def exportar_excel2():

    consulta_sql = "SELECT * FROM formulario2"

    conn = sqlite3.connect(caminho)

    df = pd.read_sql_query(consulta_sql, conn)

    # Crie um objeto BytesIO para armazenar o arquivo Excel
    output = BytesIO()

    # Use o pandas para salvar o DataFrame como um arquivo Excel no objeto BytesIO
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="formulario2")
    writer.close()

    # Configure os cabeçalhos da resposta para indicar um arquivo Excel
    output.seek(0)
    response = Response(output.read())
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response.headers["Content-Disposition"] = "attachment; filename=formulario2.xlsx"

    return response
@app.route('/exportar_excel3', methods=['POST'])
def exportar_excel3():

    consulta_sql = "SELECT * FROM formulario3"

    conn = sqlite3.connect(caminho)

    df = pd.read_sql_query(consulta_sql, conn)

    # Crie um objeto BytesIO para armazenar o arquivo Excel
    output = BytesIO()

    # Use o pandas para salvar o DataFrame como um arquivo Excel no objeto BytesIO
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="formulario3")
    writer.close()

    # Configure os cabeçalhos da resposta para indicar um arquivo Excel
    output.seek(0)
    response = Response(output.read())
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response.headers["Content-Disposition"] = "attachment; filename=formulario3.xlsx"

    return response
@app.route('/exportar_excel4', methods=['POST'])
def exportar_excel4():

    consulta_sql = "SELECT * FROM formulario4"

    conn = sqlite3.connect(caminho)

    df = pd.read_sql_query(consulta_sql, conn)

    # Crie um objeto BytesIO para armazenar o arquivo Excel
    output = BytesIO()

    # Use o pandas para salvar o DataFrame como um arquivo Excel no objeto BytesIO
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="formulario4")
    writer.close()

    # Configure os cabeçalhos da resposta para indicar um arquivo Excel
    output.seek(0)
    response = Response(output.read())
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response.headers["Content-Disposition"] = "attachment; filename=formulario4.xlsx"

    return response
@app.route('/auditar')
def auditar():
    # Conecte-se ao banco de dados (substitua 'seu_banco.db' pelo caminho do seu banco de dados)
    conn = sqlite3.connect(caminho)
    cursor = conn.cursor()

    # Consulta SQL para obter o último registro do banco de dados
    consulta_sql = "SELECT * FROM formulario1 ORDER BY id DESC LIMIT 1"
    cursor.execute(consulta_sql)
    registro = cursor.fetchone()  # Obtenha um único registro

    # Feche a conexão com o banco de dados
    conn.close()

    return render_template('auditar.html', registro={'id': 123})
@app.route('/relatorio')
def relatorio():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(caminho)  # Substitua pelo caminho correto do seu banco de dados SQLite
    cursor = conn.cursor()

    # Consulta para obter o último registro
    cursor.execute('SELECT * FROM formulario1 ORDER BY id DESC LIMIT 1')
    registro = cursor.fetchone()

    conn.close()

    if registro:
        # Passe os detalhes do registro para a página relatorio.html
        return render_template('relatorio.html', registro=registro, formatarData=formatarData)
    else:
        return "Nenhum registro encontrado", 404

@app.route('/relatorio2')
def relatorio2():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(caminho)  # Substitua pelo caminho correto do seu banco de dados SQLite
    cursor = conn.cursor()

    # Consulta para obter o último registro
    cursor.execute('SELECT * FROM formulario2 ORDER BY id DESC LIMIT 1')
    registro = cursor.fetchone()

    conn.close()

    if registro:
        # Passe os detalhes do registro para a página relatorio.html
        return render_template('relatorio2.html', registro=registro, formatarData=formatarData)
    else:
        return "Nenhum registro encontrado", 404
@app.route('/relatorio3')
def relatorio3():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(caminho)  # Substitua pelo caminho correto do seu banco de dados SQLite
    cursor = conn.cursor()

    # Consulta para obter o último registro
    cursor.execute('SELECT * FROM formulario3 ORDER BY id DESC LIMIT 1')
    registro = cursor.fetchone()

    conn.close()

    if registro:
        # Passe os detalhes do registro para a página relatorio.html
        return render_template('relatorio3.html', registro=registro, formatarData=formatarData)
    else:
        return "Nenhum registro encontrado", 404
@app.route('/relatorio4')
def relatorio4():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(caminho)  # Substitua pelo caminho correto do seu banco de dados SQLite
    cursor = conn.cursor()

    # Consulta para obter o último registro
    cursor.execute('SELECT * FROM formulario4 ORDER BY id DESC LIMIT 1')
    registro = cursor.fetchone()

    conn.close()

    if registro:
        # Passe os detalhes do registro para a página relatorio.html
        return render_template('relatorio4.html', registro=registro, formatarData=formatarData)
    else:
        return "Nenhum registro encontrado", 404
@app.route('/relatorio5')
def relatorio5():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(caminho)  # Substitua pelo caminho correto do seu banco de dados SQLite
    cursor = conn.cursor()

    # Consulta para obter todos os registros
    cursor.execute('SELECT * FROM formulario1')
    registros = cursor.fetchall()

    conn.close()

    if registros:
        # Passe a lista de registros para a página relatorio.html
        return render_template('relatorio5.html', registros=registros)
    else:
        return "Nenhum registro encontrado", 404

@app.route('/CRP')
def CRP():
    username = session.get('username')

    # Certifique-se de que 'username' está disponível no contexto do template
    return render_template('CRP.html', username=username)


@app.route('/analises1', methods=['GET', 'POST'])
def analises1():
    conexao = sqlite3.connect(caminho)
    cursor = conexao.cursor()

    # Consulta SQL para contar os elementos em uma coluna específica
    cursor.execute("""
        SELECT Status, COUNT(*) AS Count
        FROM formulario1
        GROUP BY Status
    """)

    # Obtenha os resultados da contagem
    resultados_status = cursor.fetchall()

    # Consultas SQL para contar "Conforme", "Não Conforme" e "Não se Aplica" para diferentes campos
    campos_para_analisar = [
        'nomeCompleto',
        'Datadenascimento',
        'Sexo',
        'CPFRG',
        'CartãoNacionalSUS',
        'Nomecompletodamãe',
        'EndereçocCEP',
        'Telefoneparacontato',
        'HistóriadaDoençaAtual',
        'AchadosnoExameFísico',
        'DescriçãodaConduta',
        'HipóteseDiagnóstica',
        'Carimboeassinatura',
        'Laudomédico',
        'GuiadeRequisição',

        # Adicione mais campos aqui
    ]

    resultados_status_campos = {}

    for campo in campos_para_analisar:
        cursor.execute(f"""
                SELECT '{campo}' as Campo, 
                SUM(CASE WHEN {campo} = 'Conforme' THEN 1 ELSE 0 END) AS Conforme,
                SUM(CASE WHEN {campo} = 'Não Conforme' THEN 1 ELSE 0 END) AS NaoConforme,
                SUM(CASE WHEN {campo} = 'Não se Aplica' THEN 1 ELSE 0 END) AS NaoSeAplica
                FROM formulario1
            """)

        resultados_status_campos[campo] = cursor.fetchall()


    conexao.close()

    return render_template('analises1.html', resultados_status=resultados_status, resultados_status_campos=resultados_status_campos)
@app.route('/analises2', methods=['GET', 'POST'])
def analises2():
    conexao = sqlite3.connect(caminho)
    cursor = conexao.cursor()

    # Consulta SQL para contar os elementos em uma coluna específica
    cursor.execute("""
        SELECT Status, COUNT(*) AS Count
        FROM formulario2
        GROUP BY Status
    """)

    # Obtenha os resultados da contagem
    resultados_status = cursor.fetchall()

    # Consultas SQL para contar "Conforme", "Não Conforme" e "Não se Aplica" para diferentes campos
    campos_para_analisar = [
        'nomeCompleto',
        'Datadenascimento',
        'Sexo',
        'CPFRG',
        'CartãoNacionalSUS',
        'Nomecompletodamãe',
        'EndereçocCEP',
        'Telefoneparacontato',
        'GuiadeRequisiçãodoExame',
        'TermodeLivre',
        'FichadeOrientação',
        'FichadeAdmissão',
        'PrescriçãoMédica',
        'PrescriçãoMédicadoContraste',
        'EvoluçãoMédicadoProcedimento',
        'EvoluçãodaEnfermagem',
        'LaudodoExame',
        # Adicione mais campos aqui
    ]

    resultados_status_campos = {}

    for campo in campos_para_analisar:
        cursor.execute(f"""
                SELECT '{campo}' as Campo, 
                SUM(CASE WHEN {campo} = 'Conforme' THEN 1 ELSE 0 END) AS Conforme,
                SUM(CASE WHEN {campo} = 'Não Conforme' THEN 1 ELSE 0 END) AS NaoConforme,
                SUM(CASE WHEN {campo} = 'Não se Aplica' THEN 1 ELSE 0 END) AS NaoSeAplica
                FROM formulario2
            """)

        resultados_status_campos[campo] = cursor.fetchall()


    conexao.close()

    return render_template('analises2.html', resultados_status=resultados_status, resultados_status_campos=resultados_status_campos)

@app.route('/analises3', methods=['GET', 'POST'])
def analises3():
    conexao = sqlite3.connect(caminho)
    cursor = conexao.cursor()

    # Consulta SQL para contar os elementos em uma coluna específica
    cursor.execute("""
        SELECT Status, COUNT(*) AS Count
        FROM formulario3
        GROUP BY Status
    """)

    # Obtenha os resultados da contagem
    resultados_status = cursor.fetchall()

    # Consultas SQL para contar "Conforme", "Não Conforme" e "Não se Aplica" para diferentes campos
    campos_para_analisar = [
        'nomeCompleto',
        'Datadenascimento',
        'Sexo',
        'CPFRG',
        'CartãoNacionalSUS',
        'Nomecompletodamãe',
        'EndereçocCEP',
        'Telefoneparacontato',
        'GuiadeRequisiçãodoExame',
        'FichadeOrientação',
        'TermodeLivre',
        'FichadeAdmissão',
        'PrescriçãoMédica',
        'EvoluçãoMédica',
        'EvoluçãodaEnfermagem',
        'SolicitaçãodeAnatomopatológico',

        # Adicione mais campos aqui
    ]

    resultados_status_campos = {}

    for campo in campos_para_analisar:
        cursor.execute(f"""
                SELECT '{campo}' as Campo, 
                SUM(CASE WHEN {campo} = 'Conforme' THEN 1 ELSE 0 END) AS Conforme,
                SUM(CASE WHEN {campo} = 'Não Conforme' THEN 1 ELSE 0 END) AS NaoConforme,
                SUM(CASE WHEN {campo} = 'Não se Aplica' THEN 1 ELSE 0 END) AS NaoSeAplica
                FROM formulario3
            """)

        resultados_status_campos[campo] = cursor.fetchall()


    conexao.close()

    return render_template('analises3.html', resultados_status=resultados_status, resultados_status_campos=resultados_status_campos)
@app.route('/analises4', methods=['GET', 'POST'])
def analises4():
    conexao = sqlite3.connect(caminho)
    cursor = conexao.cursor()

    # Consulta SQL para contar os elementos em uma coluna específica
    cursor.execute("""
        SELECT Status, COUNT(*) AS Count
        FROM formulario4
        GROUP BY Status
    """)

    # Obtenha os resultados da contagem
    resultados_status = cursor.fetchall()

    # Consultas SQL para contar "Conforme", "Não Conforme" e "Não se Aplica" para diferentes campos
    campos_para_analisar = [
        'nomeCompleto',
        'Datadenascimento',
        'Sexo',
        'CPFRG',
        'CartãoNacionalSUS',
        'Nomecompletodamãe',
        'EndereçocCEP',
        'Telefoneparacontato',
        'GuiadeRequisiçãodoExame',
        'TermodeLivre',
        'FichadeAdmissão',
        'ChecklistProtocolo',
        'EvoluçãoMédica',
        'EvoluçãodaEnfermagem',
        'SolicitaçãodeAnatomopatológico',

        # Adicione mais campos aqui
    ]

    resultados_status_campos = {}

    for campo in campos_para_analisar:
        cursor.execute(f"""
                SELECT '{campo}' as Campo, 
                SUM(CASE WHEN {campo} = 'Conforme' THEN 1 ELSE 0 END) AS Conforme,
                SUM(CASE WHEN {campo} = 'Não Conforme' THEN 1 ELSE 0 END) AS NaoConforme,
                SUM(CASE WHEN {campo} = 'Não se Aplica' THEN 1 ELSE 0 END) AS NaoSeAplica
                FROM formulario4
            """)

        resultados_status_campos[campo] = cursor.fetchall()


    conexao.close()

    return render_template('analises4.html', resultados_status=resultados_status, resultados_status_campos=resultados_status_campos)
if __name__ == '__main__':
    create_table()
    threading.Timer(1, open_browser).start()
    app.run()