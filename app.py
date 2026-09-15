import mysql.connector
from flask import Flask

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect()

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