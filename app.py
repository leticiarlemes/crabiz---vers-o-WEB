from flask import Flask, render_template, request, jsonify, redirect, session
from usuario import Usuario
from chat import Chat
from contato import Contato
from mensagem import Mensagem
from conexao import Conexao

app = Flask(__name__)

app.secret_key = "batatinhafrita123"

@app.route("/", methods=["GET", "POST"])
def pagina_cadastro():
    if request.method == 'GET':
        return render_template("cadastro.html")
    else:
        # recebendo os dados em json
        dados_cadastro = request.get_json()

        nome = dados_cadastro['nome']
        tel = dados_cadastro['tel']
        senha = dados_cadastro['senha']

        # instanciando usuario
        usuario = Usuario()
        if usuario.cadastrar(tel, nome, senha) == True:
            return jsonify({'mensagem':''}), 200
        else:
            return jsonify({'mensagem':'Erro ao cadastrar!'}), 500

@app.route("/login", methods=["GET", "POST"])
def pagina_login():
    if request.method == 'GET':
        return render_template("login.html")
    
    else:
        usuario = Usuario()
        tel = request.form["tel"]
        senha = request.form["senha"]

        usuario.logar(tel, senha)

        if usuario.logado == True:
            session['usuario_logado'] = {"nome":usuario.nome,
                                        "telefone":usuario.tel}
            return redirect("/chat")
        else:
            return redirect("/login")
        
@app.route("/chat")
def pag_chat():
    if "usuario_logado" in session:
        return render_template("chat.html")
    else:
        return redirect("")
        
@app.route("/get/usuarios")
def api_get_usuarios():
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)

    contatos = chat.retorna_contatos()

    return jsonify(contatos), 200



@app.route('/get/mensagens/<tel_destinatario>')
def api_get_mensagens(tel_destinatario):
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)

    contato_destinatario = Contato("", tel_destinatario)

    lista_de_mensagens = chat.verificar_mensagem(0, contato_destinatario)

    return jsonify(lista_de_mensagens), 200



@app.route("/post/enviarMSG", methods=["POST"])
def enviar_mensagem_ajax():
    if request.method == "POST":
# comentario
        dados = request.json
        destinatario = dados["destinatario"]
        mensagem = dados["mensagem"]

        nome_usuario = session["usuario_logado"]["nome"]
        telefone_usuario = session["usuario_logado"]["telefone"]
   
        chat = Chat(nome_usuario, telefone_usuario)
      
        contato_destinatario = Contato("", destinatario)
        envia = chat.enviar_mensagem(mensagem,contato_destinatario)
        return jsonify(envia), 200
    else:
       
        return jsonify({"status": "Erro ao enviar mensagem"}), 500




app.run(debug=True)
