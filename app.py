from flask import Flask, request
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
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error:
        return None


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


@app.route("/imoveis/<int:imovel_id>", methods=["GET"])
def buscar_imovel_por_id(imovel_id):
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (imovel_id,))
    resultado = cursor.fetchone()

    if resultado is None:
        cursor.close()
        conn.close()
        return {"erro": "Imóvel não encontrado"}, 404

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
    cursor.close()
    conn.close()
    return imovel, 200


@app.route("/imoveis", methods=["POST"])
def criar_imovel():
    dados = request.get_json()
    if not dados or not dados.get("logradouro"):
        return {"erro": "logradouro é obrigatório"}, 400
    if not dados.get("cidade"):
        return {"erro": "cidade é obrigatório"}, 400

    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO imoveis (
            logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            dados["logradouro"],
            dados.get("tipo_logradouro"),
            dados.get("bairro"),
            dados["cidade"],
            dados.get("cep"),
            dados.get("tipo"),
            dados.get("valor"),
            dados.get("data_aquisicao"),
        ),
    )
    conn.commit()
    return {"id": cursor.lastrowid}, 201, {
        "Location": f"/imoveis/{cursor.lastrowid}"
    }


@app.route("/imoveis/<int:imovel_id>", methods=["PUT"])
def atualizar_imovel(imovel_id):
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    dados = request.get_json()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE imoveis
        SET logradouro = %s,
            tipo_logradouro = %s,
            bairro = %s,
            cidade = %s,
            cep = %s,
            tipo = %s,
            valor = %s,
            data_aquisicao = %s
        WHERE id = %s
        """,
        (
            dados["logradouro"],
            dados["tipo_logradouro"],
            dados["bairro"],
            dados["cidade"],
            dados["cep"],
            dados["tipo"],
            dados["valor"],
            dados["data_aquisicao"],
            imovel_id,
        ),
    )
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return {"erro": "Imóvel não encontrado"}, 404

    conn.commit()
    cursor.close()
    conn.close()
    return dados, 200


@app.route("/imoveis/<int:imovel_id>", methods=["DELETE"])
def remover_imovel(imovel_id):
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    cursor = conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id = %s", (imovel_id,))
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return {"erro": "Imóvel não encontrado"}, 404

    conn.commit()
    cursor.close()
    conn.close()
    return {"mensagem": "Imóvel removido com sucesso"}, 200


@app.route("/imoveis/tipo/<tipo>", methods=["GET"])
def buscar_imoveis_por_tipo(tipo):
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo,))
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


@app.route("/imoveis/cidade/<cidade>", methods=["GET"])
def buscar_imoveis_por_cidade(cidade):
    conn = connect_db()
    if conn is None:
        return {"erro": "Erro ao conectar ao banco de dados"}, 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade,))
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
