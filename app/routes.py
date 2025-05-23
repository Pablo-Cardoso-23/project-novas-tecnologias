from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/status', methods=['GET'])
def status():

    return jsonify({"message": "SISTEMA RODANDO"})

@main_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        print(f'username: {username}, password: {password}')

        usuarios = {"pablo": "123456"}

        if username in usuarios and usuarios[username] == password:

            print("Login Successful")
            return redirect(url_for('main_bp.dashboard'))


        else:

            print("Login Failed")
            flash("Matrícula ou Senha Incorretos", "error")

    return render_template('login.html')

@main_bp.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')
