from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(25))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html", name="Home")

@app.route("/<path>")
def all_page(path):
    print(path)
    if path == "index":
        redirect(url_for("main"))
    if path == "service":
        with open("blog-database.json","r") as f:
            blog_list = json.loads(f.read())[:6]
        return render_template(f"{path}.html",blogs=blog_list, length=[i for i in range(len(blog_list))], name=path)
    return render_template(f"{path}.html",name=path)

@app.route("/membersblog/<path>")
def blog_view(path):
    with open(f"templates/blogs/{path}.md") as f:
        text = f.read()
    return render_template("blog.html",text=text, name=path)

@app.route("/app/<dirname>/<filename>")
def webapp(dirname, filename):
    return render_template(f"app/{dirname}/{filename}")

@app.route("/lab/home")
def store():
    return render_template("ECsite/home.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user == None:
            return redirect("/login")
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect('/lab/home')
            else:
                return redirect("/login")
    else:
        return render_template("login.html")
    
@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User(username=username, password=generate_password_hash(password, method="sha256"))
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    else:
        return render_template("signup.html")
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/ddd")
@login_required
def ddd():
    return render_template("ddd.html")

@app.route("/.well-known/acme-challenge/Xv4qeNwPiY9U-Z_Vn2gASPc160q24U2m-s7R_uNAezk")
def ssl():
    return "Xv4qeNwPiY9U-Z_Vn2gASPc160q24U2m-s7R_uNAezk.pyhsdZOqfHUU5gBKC6xDBU2HFqQQbDiN3p6SKuZ9mKY"

@app.route("/test")
def test():
    return render_template("test.html")

if __name__ == "__main__":
    app.run(port=5002, debug=True,host="0.0.0.0")
