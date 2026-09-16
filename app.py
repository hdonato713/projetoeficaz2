from flask import Flask, request, url_for
import mysql.connector
import os
from dotenv import load_dotenv
from imoveis import formatar_imovel

load_dotenv(".cred")

app = Flask(__name__)


def links_para_imovel(imovel_id):
    recurso = url_for("buscar_imovel_por_id", imovel_id=imovel_id)
    return {
        "self": {"href": recurso, "method": "GET"},
        "update": {"href": recurso, "method": "PUT"},
        "delete": {"href": recurso, "method": "DELETE"},
        "collection": {
            "href": url_for("listar_imoveis"),
            "method": "GET",
        },
    }


def links_para_filtro(recurso):
    return {
        "self": {"href": recurso, "method": "GET"},
        "collection": {
            "href": url_for("listar_imoveis"),
            "method": "GET",
        },
        "create": {
            "href": url_for("listar_imoveis"),
            "method": "POST",
        },
    }


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
        imovel = formatar_imovel(resultado)
        imovel["_links"] = links_para_imovel(imovel["id"])
        imoveis.append(imovel)

    cursor.close()
    conn.close()
    return {
        "imoveis": imoveis,
        "_links": {
            "self": {"href": url_for("listar_imoveis"), "method": "GET"},
            "create": {
                "href": url_for("listar_imoveis"),
                "method": "POST",
            },
        },
    }, 200


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

    imovel = formatar_imovel(resultado)
    imovel["_links"] = links_para_imovel(imovel_id)
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
    imovel_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"id": imovel_id, "_links": links_para_imovel(imovel_id)}, 201, {
        "Location": f"/imoveis/{imovel_id}"
    }


@app.route("/imoveis/<int:imovel_id>", methods=["PUT"])
def atualizar_imovel(imovel_id):
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
            dados.get("tipo_logradouro"),
            dados.get("bairro"),
            dados["cidade"],
            dados.get("cep"),
            dados.get("tipo"),
            dados.get("valor"),
            dados.get("data_aquisicao"),
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
    return {
        **dados,
        "id": imovel_id,
        "_links": links_para_imovel(imovel_id),
    }, 200


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
    return {
        "mensagem": "Imóvel removido com sucesso",
        "_links": {
            "collection": {
                "href": url_for("listar_imoveis"),
                "method": "GET",
            },
            "create": {
                "href": url_for("listar_imoveis"),
                "method": "POST",
            },
        },
    }, 200


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
        imovel = formatar_imovel(resultado)
        imovel["_links"] = links_para_imovel(imovel["id"])
        imoveis.append(imovel)

    cursor.close()
    conn.close()
    return {
        "imoveis": imoveis,
        "_links": links_para_filtro(
            url_for("buscar_imoveis_por_tipo", tipo=tipo)
        ),
    }, 200


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
        imovel = formatar_imovel(resultado)
        imovel["_links"] = links_para_imovel(imovel["id"])
        imoveis.append(imovel)

    cursor.close()
    conn.close()
    return {
        "imoveis": imoveis,
        "_links": links_para_filtro(
            url_for("buscar_imoveis_por_cidade", cidade=cidade)
        ),
    }, 200
