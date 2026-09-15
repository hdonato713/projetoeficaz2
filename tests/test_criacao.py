from unittest.mock import MagicMock, patch


def test_criar_imovel(client):
    dados = {
        "logradouro": "Rua das Flores",
        "tipo_logradouro": "Rua",
        "bairro": "Vila Mariana",
        "cidade": "São Paulo",
        "cep": "04123-000",
        "tipo": "apartamento",
        "valor": 850000,
        "data_aquisicao": "2026-09-15",
    }

    with patch("app.connect_db") as mock_connect_db:
        conexao = MagicMock()
        cursor = MagicMock()
        mock_connect_db.return_value = conexao
        conexao.cursor.return_value = cursor
        cursor.lastrowid = 1001

        resposta = client.post("/imoveis", json=dados)

    assert resposta.status_code == 201
    assert resposta.json == {"id": 1001}
    assert resposta.headers["Location"] == "/imoveis/1001"
    conexao.commit.assert_called_once()

def test_criar_imovel_sem_logradouro(client):
    dados = {
        "cidade": "São Paulo",
    }

    with patch("app.connect_db") as mock_connect_db:
        resposta = client.post("/imoveis", json=dados)

    assert resposta.status_code == 400
    assert resposta.json == {"erro": "logradouro é obrigatório"}
    mock_connect_db.assert_not_called()

def test_criar_imovel_sem_cidade(client):
    dados = {
        "logradouro": "Rua das Flores",
    }

    with patch("app.connect_db") as mock_connect_db:
        resposta = client.post("/imoveis", json=dados)

    assert resposta.status_code == 400
    assert resposta.json == {"erro": "cidade é obrigatório"}
    mock_connect_db.assert_not_called()