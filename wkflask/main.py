from flask import Flask, render_template, request, redirect, session, flash, url_for

class Usuario():
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Rafael Show','Rafa', '123')
usuario2 = Usuario('Cleber Machado','CM', 'gol')
usuario3 = Usuario('Jean Dias','JD','cambalhota')

usuarios = {usuario1.nickname : usuario1,
            usuario2.nickname : usuario2,
            usuario3.nickname : usuario3 }


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Tetris','Puzzle','Atari')
jogo2 = Jogo('The Witcher 3', 'RPG', 'PC')
jogo3 = Jogo('Super Mario', 'plataforma', 'Super Nintendo')
lista = [jogo1, jogo2, jogo3]


app = Flask(__name__)
app.secret_key = '123'

@app.route('/')
def index():

    return render_template('lista.html', titulo = 'Jogos', jogos = lista)

@app.route('/insere')
def insere():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect (url_for('login', proxima = url_for('insere')))
    return render_template('insere.html', titulo = 'Inserir novo jogo')

@app.route('/criar', methods =['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route('/autenticar', methods =['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso! <3')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)          

        else:
            flash('Senha incorreta :( , tente novamente')
            return redirect(url_for('login'))       

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuario deslogado com sucesso! <3')
    return redirect(url_for('index'))

app.run(debug=True)

