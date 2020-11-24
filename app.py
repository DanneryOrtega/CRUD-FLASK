from flask import Flask, render_template, request, redirect, url_for, flash

import sqlite3

app = Flask(__name__)
db = sqlite3.connect('data.db', check_same_thread=False)

# Rutas
@app.route('/', methods=['GET']) # / significa la ruta raiz
def index():
    return render_template('index.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    #Obteniendo formulario de contacto
    if request.method == 'GET':
        return render_template('contacto.html')
    
    #Guardando la información de contacto
    """nombres = request.form.get('nombres')
    email = request.form.get('email')
    celular = request.form.get('celular')"""

    observacion = request.form.get('observacion')



    return 'Guardando información ' + observacion

@app.route('/usuarios')
def usuarios():
    usuarios = db.execute('select * from usuarios')

    usuarios = usuarios.fetchall()

    return render_template('usuarios/listar.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuarios():
    if request.method == 'GET':
        return render_template('usuarios/crear.html')
    
    nombres = request.form.get('nombres')
    apellidos = request.form.get('apellidos')
    email = request.form.get('email')
    password = request.form.get('password')

    cursor = db.cursor()

    cursor.execute("""insert into usuarios(
            nombres,
            apellidos,
            email,
            password
        )values (?,?,?,?)
    """, (nombres, apellidos, email, password))

    db.commit()
    #flash('Usuario Agregado')
    return redirect(url_for('usuarios'))

@app.route('/usuarios/editar/<id>' )
def editar_usuarios(id):

        cursor = db.cursor()
        query='SELECT * FROM usuarios WHERE id = ?'

        cursor.execute(query, (id))
        datos = cursor.fetchone()
        db.commit()

        return render_template('usuarios/editar.html', usuarios = datos)

@app.route('/actualizar/<id>', methods=['GET','POST'])
def actualizar_usuario(id):
    if request.method == 'POST':

        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        email = request.form.get('email')
        
        cursor = db.cursor()
        query="""
        UPDATE usuarios
        SET nombres = ?,
            apellidos = ?,
            email = ?"""
        query+='WHERE id = ?'
        
        cursor.execute(query, (nombres, apellidos, email, id))
        db.commit()
        #flash('Usuario Actualizado') 
        return redirect(url_for('usuarios'))
        
@app.route('/eliminar/<id>')
def eliminar_usuarios(id):
    cursor = db.cursor()

    query='DELETE FROM usuarios WHERE id=?'
    cursor.execute(query, (id))
    db.commit()

    return redirect(url_for('usuarios'))

app.run(debug=True)