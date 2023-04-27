from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///livraria.sqlite3"

db = SQLAlchemy(app)


class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    autor = db.Column(db.String(30))
    genero = db.Column(db.String(30))
    npaginas = db.Column(db.Integer)
    editora = db.Column(db.String(30))
    ano = db.Column(db.Integer)
    descricao = db.Column(db.String(300))
    avaliacao = db.Column(db.Integer, db.CheckConstraint(
        'avaliacao >= 0 AND avaliacao <= 5'))

    def __init__(self, nome, autor, genero, npaginas, editora, ano, descricao, avaliacao):
        self.nome = nome
        self.autor = autor
        self.genero = genero
        self.npaginas = npaginas
        self.editora = editora
        self.ano = ano
        self.descricao = descricao
        self.avaliacao = avaliacao


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lista', methods=["GET", "POST", ])
def lista():
    return (render_template('lista.html', livros=Livro.query.all()))


@app.route('/listarlivro', methods=["GET", "POST"])
def listarlivro():
    nome = request.form.get('nome')
    autor = request.form.get('autor')
    genero = request.form.get('genero')
    npaginas = request.form.get('npaginas')
    editora = request.form.get('editora')
    ano = request.form.get('ano')
    descricao = request.form.get('descricao')
    avaliacao = request.form.get('avaliacao')

    if request.method == 'POST':
        livro = Livro(nome, autor, genero, npaginas,
                      editora, ano, descricao, avaliacao)
        db.session.add(livro)
        db.session.commit()
        return redirect(url_for('lista'))
    return render_template("listarlivro.html")


@app.route('/<int:id>/atualiza_livro', methods=['GET', 'POST'])
def atualiza_livro(id):
    livro = Livro.query.filter_by(id=id).first()
    if request.method == 'POST':
        nome = request.form.get('nome')
        autor = request.form.get('autor')
        genero = request.form.get('genero')
        npaginas = request.form.get('npaginas')
        editora = request.form.get('editora')
        ano = request.form.get('ano')
        descricao = request.form.get('descricao')
        avaliacao = request.form.get('avaliacao')
        Livro.query.filter_by(id=id).update({"nome": nome, "autor": autor, "genero": genero, "npaginas": npaginas,
                                             "editora": editora, "ano": ano, "descricao": descricao, "avaliacao": avaliacao})
        db.session.commit()
        return redirect(url_for('lista'))
    return render_template('atualiza_livro.html', livro=livro)

@app.route('/<int:id>/remover_livro', methods=['GET', 'POST'])
def remover_livro(id):
    livro = Livro.query.filter_by(id=id).first()
    db.session.delete(livro)
    db.session.commit()
    return redirect(url_for('lista'))


with app.app_context():
    db.create_all()
    app.run(debug=True)
