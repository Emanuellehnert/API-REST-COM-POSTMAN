import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_migrate import Migrate
from db import db
load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    from models.book import Book
    db.create_all()
    if Book.query.count() == 0:
        livro1 = Book(
            title="O Hobbit",
            author="J.R.R. Tolkien",
            description="Uma aventura pela Terra Média.",
            is_reading=True,
            is_finished=False,
            is_favorite=True
        )
        livro2 = Book(
            title="Dom Casmurro",
            author="Machado de Assis",
            description="Clássico da literatura brasileira.",
            is_finished=True
        )
        db.session.add(livro1)
        db.session.add(livro2)
        db.session.commit()
@app.route("/", methods=["GET"])
def inicio():
    from models.book import Book
    livros = Book.query.all()
    return {"livros": [livro.to_dict() for livro in livros]}, 200
@app.route("/livros", methods=["GET"])
def listar_livros():
    from models.book import Book
    livros = Book.query.all()
    return {"livros": [livro.to_dict() for livro in livros]}, 200
@app.route("/livros", methods=["POST"])
def criar_livro():
    from models.book import Book
    dados = request.get_json()
    novo_livro = Book(
        title=dados["title"],
        author=dados["author"],
        description=dados.get("description"),
        is_reading=dados.get("is_reading", False),
        is_finished=dados.get("is_finished", False),
        is_favorite=dados.get("is_favorite", False)
    )
    db.session.add(novo_livro)
    db.session.commit()
    return novo_livro.to_dict(), 201
if __name__ == "__main__":
    app.run(debug=True)
@app.route("/livros/<uuid:livro_id>", methods=["GET"])
def obter_livro(livro_id):
    from models.book import Book
    livro = Book.query.get_or_404(livro_id)
    return {
        "livro": livro.to_dict()
    }, 200
#definir rota para atualizar um livro
@app.route("/livros/<uuid:livro_id>", methods=["PUT"])
def atualizar_livro(livro_id):
    from flask import request
    from models.book import Book
    livro = Book.query.get_or_404(livro_id)
    dados = request.get_json()
    livro.title = dados.get("title", livro.title)
    livro.author = dados.get("author", livro.author)
    livro.description = dados.get("description", livro.description)
    livro.is_reading = dados.get("is_reading", livro.is_reading)
    livro.is_finished = dados.get("is_finished", livro.is_finished)
    livro.is_favorite = dados.get("is_favorite", livro.is_favorite)
    db.session.commit()
    return {
        "mensagem": "Livro atualizado com sucesso!",
        "livro": livro.to_dict()
    }, 200
#definir rota para deletar um livro
@app.route("/livros/<uuid:livro_id>", methods=["DELETE"])
def deletar_livro(livro_id):
    from models.book import Book
    livro = Book.query.get_or_404(livro_id)
    db.session.delete(livro)
    db.session.commit()
    return {
        "mensagem": "Livro deletado com sucesso!"
    }, 200