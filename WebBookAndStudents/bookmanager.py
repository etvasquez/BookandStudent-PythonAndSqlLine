import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

# enlace a base de datos vía sqlalchemy
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# modelado
class Book(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

# modelado estudiantes
class Student(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(80), unique=False, nullable=False)
    apellido = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return "<Name: {},Apellido:{}>".format(self.nombre,self.apellido)
# vistas
# @app.route("/")
@app.route("/", methods=["GET", "POST"])
def home():
    # return "My flask app"    
    books = Book.query.all()
    students = Student.query.all()
    return render_template("home.html",books=books,students=students)
    # return render_template("home.html")
   
@app.route("/addBook", methods=["POST"])
def addBook():
	book = Book(title=request.form.get("libro"))
	db.session.add(book)
	db.session.commit()
	return redirect("/")

@app.route("/addStudent", methods=["POST"])
def addStudent():
	student_name = Student(nombre=request.form.get("nombre"),apellido=request.form.get("apellido"))
	db.session.add(student_name)
	db.session.commit()
	return redirect("/")

@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    idlibro = request.form.get("idlibro")
    book = Book.query.get(idlibro)
    book.title = newtitle
    db.session.commit()
    return redirect("/")  

@app.route("/delete", methods=["POST"])
def delete():
    idlibro = request.form.get("idlibro")
    book = Book.query.get(idlibro)
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

@app.route("/updateStudent", methods=["POST"])
def updateStudent():
    newname = request.form.get("newname")
    newlast = request.form.get("newlast")
    idstudent = request.form.get("idstudent")
    student = Student.query.get(idstudent)
    student.nombre = newname
    student.apellido = newlast
    db.session.commit()
    return redirect("/")  

@app.route("/deleteStudent", methods=["POST"])
def deleteStudent():
    idstudent = request.form.get("idstudent")
    student = Student.query.get(idstudent)
    db.session.delete(student)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)



