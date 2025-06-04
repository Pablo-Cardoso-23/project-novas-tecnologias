import logging

import pandas as pd
import os
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from app.controllers import gerar_pontos_criticos
from app.config import get_db_connection
from datetime import datetime

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

logging.basicConfig(level=logging.DEBUG)

@main_bp.route('/registrarocorrencia', methods=['GET', 'POST'])
def registrar_ocorrencia():

    br_maping = {

        "dez": 10,
        "vinte": 20,
        "quarenta": 40,
        "sessenta": 60,
        "setenta": 70,
        "oitenta": 80,
        "dois_cinco_um": 251

    }

    if request.method == 'GET':

        return render_template('ocorrencia.html')

    try:

        horario = request.form['horario'] + ":00"
        br_str = request.form['br']
        br_numeric = br_maping.get(br_str, 0)
        latitude = float(request.form['latitude'].replace(",", "."))
        longitude = float(request.form['longitude'].replace(",", "."))

        data_form = (

            request.form['data_inversa'],
            request.form['dias'],
            horario,
            request.form['uf'],
            br_numeric,
            request.form['km'],
            request.form['municipio'],
            request.form['causa_acidente'],
            request.form['tipo_acidente'],
            request.form['classificacao_acidente'],
            request.form['fase_dia'],
            request.form['sentido_via'],
            request.form['condicao_metereologica'],
            request.form['tipo_pista'],
            request.form['tracado_via'],
            request.form['uso_solo'],
            request.form['pessoas'],
            request.form['mortos'],
            request.form['feridos_leves'],
            request.form['feridos_graves'],
            request.form['ilesos'],
            request.form['ignorados'],
            request.form['feridos'],
            request.form['veiculos'],
            latitude,
            longitude,
            request.form['regional'],
            request.form['delegacia'],
            request.form['uop'],
            request.form['ano']

        )

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""

                   INSERT INTO ocorrencias (
                       data_inversa, dia_semana, horario, uf, br, km, municipio,
                       causa_acidente, tipo_acidente, classificacao_acidente, fase_dia, sentido_via,
                       condicao_metereologica, tipo_pista, tracado_via, uso_solo, pessoas, mortos,
                       feridos_leves, feridos_graves, ilesos, ignorados, feridos, veiculos,
                       latitude, longitude, regional, delegacia, uop, ano
                   ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               """, data_form)

        conn.commit()
        cursor.close()
        conn.close()

        return render_template('ocorrenciaregistrada.html')
        #return jsonify({"message": "Registro de ocorrência realizado com sucesso!"})

    except Exception as e:

        logging.error(f"Erro ao registrar ocorrência: {str(e)}")
        return jsonify({"error": f"Erro ao registrar ocorrência: {str(e)}"})



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
    if not google_api_key:
        print("ROUTES.PY: ALERTA CRÍTICO! Maps_API_KEY não foi encontrada no ambiente.")
        google_api_key = ""

    caminho_base_app = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(caminho_base_app, "data", "ocorrenciasdf.csv")

    lista_de_pontos_criticos = []
    if os.path.exists(caminho_csv):
        try:
            lista_de_pontos_criticos = gerar_pontos_criticos(caminho_csv)
            if lista_de_pontos_criticos is None:
                print("ROUTES.PY: ALERTA! gerar_pontos_criticos retornou None. Usando lista vazia.")
                lista_de_pontos_criticos = []
        except Exception as e:
            print(f"ROUTES.PY: ERRO EXCEPCIONAL ao chamar gerar_pontos_criticos: {e}")
            import traceback
            traceback.print_exc()
            lista_de_pontos_criticos = [] 
    else:
        print(f"ROUTES.PY: ALERTA! Arquivo CSV não encontrado em '{caminho_csv}'. 'pontos_criticos' será uma lista vazia.")

    return render_template(
        "mapa.html",
        pontos_criticos=lista_de_pontos_criticos,
        google_api_key=google_api_key
    )
