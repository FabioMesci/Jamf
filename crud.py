from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import bcrypt
import jamfdb as db
import datetime

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'Jamf', 'secciones')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = "edmundo"

global comprador
global c_producto
global c_precio
global IDpedido


# Interfaz de inicio de sesión

@app.route('/', methods=["GET", "POST"])
def LoginScreen():
    return render_template('loginScreen.html')


# Interfaz de cambio de contraseña

@app.route('/CambioContraseñaScreen', methods=["GET", "POST"])
def CambioContraseñaScreen():
    return render_template('CambioContraseña.html')


# Interfaces del cliente

@app.route('/ClientScreen')
def ClientScreen():
    return render_template('opciones_cliente.html')


# Interfaz para el empleado

@app.route('/empleado')
def EmployeeScreen():
    return render_template('opciones_empleado.html')


# Pedidos pendientes para el cajero

@app.route('/pendientes')
def Pendientes():
    cursorpedidos = db.database.cursor()
    cursorpedidos.execute("SELECT * FROM pedidos")
    myresult = cursorpedidos.fetchall()

    # convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursorpedidos.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursorpedidos.close()

    return render_template('pedidos_cajero.html', pedidos=insertObject)


# pedidos pendientes para el cocinero

@app.route('/pendientes_cocinero')
def PendientesCocinero():

    cursorpedidos = db.database.cursor()
    cursorpedidos.execute("SELECT * FROM pedidos_cobrados")
    myresult = cursorpedidos.fetchall()
    
    cursor = db.database.cursor()
    cursor.execute("SELECT nombre FROM clientes_pendientes")
    nombre_clientes = [row[0] for row in cursor.fetchall()]

    # convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursorpedidos.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursorpedidos.close()

    return render_template('pedidos_cocinero.html', pedidos_cobrados=insertObject, nombre_clientes=nombre_clientes)

# Interfaz para el cocinero

@app.route('/cocinero')
def CookScreen():
    return render_template('opciones_cocinero.html')


# Interfaz para el administrador

@app.route('/Admin')
def AdminScreen():
    return render_template('opciones_admin.html')


# Interfaz del carrito

@app.route('/cart')
def CartScreen():
    cursorusuario = db.database.cursor()
    cursorusuario.execute(f"SELECT tmp_id, comprador, c_producto, c_precio FROM {username}")
    myresult = cursorusuario.fetchall()

    # convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursorusuario.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursorusuario.close()

    #mostrar el ID del cliente
    cursorID = db.database.cursor(buffered=True)
    sql2 = ("SELECT ID_pedido FROM clientes_pendientes WHERE nombre = %s")
    data2 = [username]
    cursorID.execute(sql2, data2)
    IDpedido = cursorID.fetchone()[0]
    db.database.commit()
    cursorID.close()

    return render_template('carrito_principal.html', username=insertObject, ID=IDpedido)


# Interfaz de registro de un cliente

@app.route('/RegisterScreen')
def RegisterScreen():
    if request.method == 'GET':
        return render_template('RegistroCliente.html')


# Interfaz de registro de un trabajador

@app.route('/AdminRegisterScreen')
def AdminRegisterScreen():
    return render_template('RegistroAdmin.html')


# Crud para facturar

@app.route('/facturar', methods=["GET", "POST"])
def Facturar():
    cursor = db.database.cursor()
    cursor.execute("SELECT nombre FROM clientes_pendientes")
    myresult = cursor.fetchall()
    
    cursor = db.database.cursor()
    cursor.execute("SELECT nombre FROM clientes_pendientes")
    nombre_clientes = [row[0] for row in cursor.fetchall()]

    # convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()



    return render_template('facturacion.html', clientes=insertObject, nombre_clientes=nombre_clientes)


# Interfaz de lista de trabajadores

@app.route('/EmployeeList')
def EmployeeList():
    cursorusuario = db.database.cursor()
    cursorusuario.execute(
        "SELECT * FROM users WHERE status='cocinero' OR status='empleado'")
    myresult = cursorusuario.fetchall()

    # convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursorusuario.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursorusuario.close()

    return render_template('lista_empleados.html', users=insertObject)


# interfaz para lista de clientes

@app.route('/clientes')
def ClientList():
    cursorusuario = db.database.cursor()
    cursorusuario.execute(
        "SELECT * FROM users WHERE status='cliente'")
    myresult = cursorusuario.fetchall()

    # convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursorusuario.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursorusuario.close()

    return render_template('lista_clientes.html', users=insertObject)


# interfaz para el inventario

@app.route('/inventario')
def Inventario():

    cursorusuario = db.database.cursor()
    cursorusuario.execute("SELECT product_id, nombre, precio FROM productos")
    myresult = cursorusuario.fetchall()

    # convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursorusuario.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursorusuario.close()

    return render_template('inventario.html', productos=insertObject)


# CRUD para registrar un producto

@app.route("/AddProduct", methods=["GET", "POST"])
def AddProduct():
    try:
        if request.method == "POST":
            nombre = request.form["nombre"]
            precio = request.form["precio"]

            cursor = db.database.cursor()
            query = "INSERT INTO productos (nombre, precio) VALUES (%s, %s)"
            values = (nombre, precio)
            cursor.execute(query, values)
            db.database.commit()

            return redirect(url_for("Inventario"))
    except:
        return "Error: No pueden haber más de un producto con el mismo nombre."


# Interfaz de lista de productos

@app.route('/Catalogo')
def ProductList():
    cursorusuario = db.database.cursor()
    cursorusuario.execute("SELECT nombre, precio FROM productos")
    myresult = cursorusuario.fetchall()

    # convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursorusuario.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursorusuario.close()

    #crear tabla del pedido del cliente
    cursorcarrito = db.database.cursor()
    query = f"CREATE TABLE IF NOT EXISTS {username} (tmp_id INTEGER AUTO_INCREMENT PRIMARY KEY, comprador VARCHAR(255), c_producto VARCHAR(255), c_precio DOUBLE)"
    cursorcarrito.execute(query)
    db.database.commit()
    cursorcarrito.close()
    

    #añadir al cliente a pedidos pendientes
    cursor = db.database.cursor()
    sql = ("INSERT INTO clientes_pendientes (nombre) SELECT (%s) FROM DUAL WHERE NOT EXISTS (SELECT nombre FROM clientes_pendientes WHERE nombre = %s)")
    data = [username, username]
    cursor.execute(sql, data)
    db.database.commit()
    cursor.close()

    #mostrar el ID del cliente
    cursorID = db.database.cursor(buffered=True)
    sql2 = ("SELECT ID_pedido FROM clientes_pendientes WHERE nombre = %s")
    data2 = [username]
    cursorID.execute(sql2, data2)
    IDpedido = cursorID.fetchone()[0]
    db.database.commit()
    cursorID.close()

    return render_template('catalogo.html', productos=insertObject, ID=IDpedido)


# CRUD para registrar a un cliente

@app.route("/AddClient", methods=["GET", "POST"])
def AddClient():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        ci = request.form["ci"]
        # Obtener la contraseña sin encriptar
        password = request.form["password"]
        PhoneNumber = request.form["PhoneNumber"]
        Adress = request.form["Adress"]
        status = 'cliente'
        fecha_registro = datetime.date.today()

        # Encriptar la contraseña antes de almacenarla en la base de datos
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

        cursor = db.database.cursor()
        query = "INSERT INTO users (email, username, ci, password, PhoneNumber, Adress, status, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (email, username, ci, hashed_password,
                  PhoneNumber, Adress, status, fecha_registro)
        cursor.execute(query, values)
        db.database.commit()

        return redirect(url_for("LoginScreen"))
    else:
        return "Ocurrió un error inesperado."


# CRUD para registrarse como trabajador

@app.route("/AddWorker", methods=["GET", "POST"])
def AddWorker():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        ci = request.form["ci"]
        password = request.form["password"]
        PhoneNumber = request.form["PhoneNumber"]
        Adress = request.form["Adress"]
        status = request.form["status"]
        fecha_registro = datetime.date.today()

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

        cursor = db.database.cursor()
        query = "INSERT INTO users (email, username, ci, password, PhoneNumber, Adress, status, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (email, username, ci, hashed_password,
                  PhoneNumber, Adress, status, fecha_registro)
        cursor.execute(query, values)
        db.database.commit()

        return redirect(url_for("LoginScreen"))
    else:
        return "Nope"


# CRUD para registrarse como Admin

@app.route("/AddAdmin", methods=["GET", "POST"])
def AddAdmin():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        ci = request.form["ci"]
        password = request.form["password"]
        PhoneNumber = request.form["PhoneNumber"]
        Adress = request.form["Adress"]
        status = request.form["status"]
        fecha_registro = datetime.date.today()

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

        cursor = db.database.cursor()
        query = "INSERT INTO users (email, username, ci, password, PhoneNumber, Adress, status, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (email, username, ci, hashed_password,
                  PhoneNumber, Adress, status, fecha_registro)
        cursor.execute(query, values)
        db.database.commit()

        return redirect(url_for("AdminScreen"))
    else:
        return "Nope"


# CRUD para iniciar sesion

@app.route("/Login", methods=["GET", "POST"])
def Login():
    if request.method == 'POST':
        global username
        username = request.form["username"]
        password = request.form["password"]

        cursor = db.database.cursor()
        query = "SELECT username, password, status, fecha_registro FROM users WHERE username=%s"
        value = (username,)
        cursor.execute(query, value)
        result = cursor.fetchone()

        try:
            if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
                # Verificar credenciales y redirigir a la pantalla correspondiente
                fecha_registro = result[3]
                dias_pasados = (datetime.date.today() - fecha_registro).days

                if dias_pasados >= 15:
                    flash("Su contraseña ha expirado, debe cambiarla")
                    return render_template("CambioContraseña.html", username=username, password=password)

                if result[2] == 'empleado':
                    return redirect(url_for("EmployeeScreen"))
                elif result[2] == 'cocinero':
                    return redirect(url_for("CookScreen"))
                elif result[2] == 'admin':
                    return redirect(url_for("AdminScreen"))
                else:
                    return redirect(url_for("ClientScreen"))
            else:
                flash("Usuario o contraseña incorrectos")
                return render_template('loginScreen.html')

        except TypeError:
            flash("Usuario o contraseña incorrectos")
            return render_template('loginScreen.html')



# CRUD para cambiar la contraseña

@app.route('/CambiarContraseña', methods=["GET", "POST"])
def CambiarContraseña():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['new_password']
        fecha_registro = datetime.date.today()

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

        cursor = db.database.cursor()
        query = "UPDATE users SET password = %s, fecha_registro = %s WHERE username = %s"
        value = (hashed_password, fecha_registro, username)
        cursor.execute(query, value)
        db.database.commit()

        return redirect(url_for('LoginScreen'))


# CRUD para borrar trabajadores de la bdd

@app.route('/borrar_trabajador/<string:id>')
def DeleteEmployee(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()

    return redirect(url_for('EmployeeList'))


# CRUD para borrar productos de la bdd

@app.route('/borrar_producto/<string:product_id>')
def DeleteProduct(product_id):
    cursor = db.database.cursor()
    sql = "DELETE FROM productos WHERE product_id=%s"
    data = (product_id,)
    cursor.execute(sql, data)
    db.database.commit()

    return redirect(url_for('Inventario'))


#Crud para cobrar a un cliente

@app.route('/Cobrar', methods=["GET", "POST"])
def Cobrar():

    cursor = db.database.cursor()
    sql = f"INSERT INTO pedidos_cobrados (cliente, pedido, precio) SELECT comprador, c_producto, c_precio FROM {ClienteACobrar}"
    cursor.execute(sql)
    db.database.commit()    

    return redirect(url_for('Facturar'))


# CRUD para borrar un item del carrito del cliente & de pedidos
@app.route('/borrar_carrito/<string:tmp_id>')
def DeleteFromCart(tmp_id):
    cursor = db.database.cursor()
    sql = f"DELETE FROM {username} WHERE tmp_id=%s"
    data = (tmp_id,)
    cursor.execute(sql, data)
    db.database.commit()

    return redirect(url_for('CartScreen'))


# CRUD para editar productos

@app.route('/EditProduct', methods=["GET", "POST"])
def EditProduct():
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]

        cursor = db.database.cursor()
        sql = "UPDATE productos SET nombre=%s, precio=%s"
        data = (nombre, precio)
        cursor.execute(sql, data)
        db.database.commit()

        return redirect(url_for('Inventario'))


# CRUD para añadir un producto al carrito

@app.route('/AddToCart', methods=["GET", "POST"])
def AddToCart():
    if request.method == "POST":
        producto = request.form["producto"]
        precio = request.form["precio"]

        #agregar un producto al carrito unico del cliente
        cursor1 = db.database.cursor()
        sql1 = f"INSERT INTO {username} (comprador, c_producto, c_precio) VALUES (%s,%s,%s)"
        data1 = (username, producto, precio)
        cursor1.execute(sql1, data1)
        db.database.commit()

        #agregar el producto a pedidos pendientes
        cursor2 = db.database.cursor()
        sql2 = (f"INSERT INTO pedidos (cliente, producto, precio) SELECT comprador, c_producto, c_precio FROM {username}")
        data2 = (username, producto, precio)
        cursor2.execute(sql2)
        db.database.commit()

        return redirect(url_for('ProductList'))

#CRUD para marcar un pedido como hecho
@app.route('/PedidoHecho', methods=["GET", "POST"])
def PedidoHecho():
    if request.method=="POST":
        clientecobrado = request.form["clientecobrado"]

        cursor1 = db.database.cursor(buffered=True)
        sql = f"DROP TABLE {clientecobrado}"
        cursor1.execute(sql)
        db.database.commit()
        cursor1.close()

        clientecobrado=[clientecobrado]

        cursor3 = db.database.cursor()
        sql = "DELETE FROM clientes_pendientes WHERE nombre=%s"
        cursor3.execute(sql, clientecobrado)
        db.database.commit()

        cursor4 = db.database.cursor()
        sql = "DELETE FROM pedidos_cobrados WHERE cliente=%s"
        cursor4.execute(sql, clientecobrado)
        db.database.commit()

        return redirect(url_for('PendientesCocinero'))

#CRUD para mostrar el pedido del cliente
@app.route('/mostrarpedido', methods=["GET", "POST"])
def mostrarpedido():
    if request.method == "POST":
        global ClienteACobrar
        ClienteACobrar = request.form["nombre"]

        cursor = db.database.cursor()
        sql = f"SELECT * FROM {ClienteACobrar}"
        cursor.execute(sql,)
        myresult = cursor.fetchall()

        insertObject = []
        columnNames = [column[0] for column in cursor.description]
        for record in myresult:
            insertObject.append(dict(zip(columnNames, record)))
        db.database.commit()
        cursor.close()


        return render_template("facturacion2.html", pedidos_cobrados=insertObject)

if __name__ == '__main__':
    app.run(debug=True, port=4000)