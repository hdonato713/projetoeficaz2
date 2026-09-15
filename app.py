from flask import Flask
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv(".cred")

app = Flask(__name__)

def connect_db():
    config = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "ssl_ca": os.getenv("SSL_CA_PATH"),
    }

    return mysql.connector.connect(**config)

@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    conn = connect_db()

    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM imoveis")
    resultados = cursor.fetchall()

    imoveis = []

    for resultado in resultados:
        imovel = {
            "id": resultado[0],
            "logradouro": resultado[1],
            "tipo_logradouro": resultado[2],
            "bairro": resultado[3],
            "cidade": resultado[4],
            "cep": resultado[5],
            "tipo": resultado[6],
            "valor": resultado[7],
            "data_aquisicao": resultado[8],
        }
        imoveis.append(imovel)

    return {"imoveis": imoveis}, 200