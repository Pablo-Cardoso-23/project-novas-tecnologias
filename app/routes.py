import pandas as pd
import os
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

main_bp = Blueprint('main_bp', __name__)
load_dotenv(dotenv_path="./app/secrets.env")

@main_bp.route('/', methods=['GET'])
def barra():
    return redirect('/login')

@main_bp.route('/status', methods=['GET'])
def status():

    return jsonify({"message": "SISTEMA RODANDO"})

@main_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        print(f'username: {username}, password: {password}')

        usuarios = {"pablo": "123456",
                    "pedro": "123456"}

        if username in usuarios and usuarios[username] == password:

            print("Login Successful")
            return redirect(url_for('main_bp.menu'))


        else:

            print("Login Failed")
            flash("Matrícula ou Senha Incorretos", "error")

    return render_template('login.html')

@main_bp.route('/menu')
def menu():

    return render_template('menu.html')

@main_bp.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')

@main_bp.route('/registarocorrencia')
def registar_ocorrencia():

    return render_template('ocorrencia.html')

@main_bp.route('/dados_ocorrencias')
def dados_ocorrencias_api():

   try:

       caminho_csv = os.path.join(os.path.dirname(__file__), 'data', 'ocorrenciasdf.csv')

       if not os.path.exists(caminho_csv):

           return jsonify({"error": f"Arquivo não encontrado: {caminho_csv}"})

       df = pd.read_csv(caminho_csv, sep=';')
       df = df.fillna("null")

       br_filtro = request.args.get('br', '')
       tipo_acidente = request.args.get('tipo_acidente', '')
       ano_filtro = request.args.get('ano', '')

       if tipo_acidente:

           df = df[df['tipo_acidente'].str.contains(tipo_acidente, case=False, na=False)]

       if br_filtro:

           df = df[df['br'].astype(str) == br_filtro]

       if ano_filtro:

           df = df[df['ano'].astype(str) == ano_filtro]

       df_agrupado = df.groupby('br').agg({'id': 'count'}).reset_index()
       df_agrupado.rename(columns={'id': 'quantidade'}, inplace=True)

       return jsonify(df_agrupado.to_dict(orient='records'))

   except Exception as e:

       return jsonify({'error': f"Erro ao carregar os dados de ocorrências: {str(e)}"})

@main_bp.route('/mapa')
def mapa():
    google_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    return render_template("mapa.html", google_api_key = google_api_key)