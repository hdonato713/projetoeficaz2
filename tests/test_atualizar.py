from unittest.mock import MagicMock, patch


def test_atualiza_imovel(client):
    conexao_mock = MagicMock()
    cursor_mock = MagicMock()

    conexao_mock.cursor.return_value = cursor_mock
    cursor_mock.rowcount = 1

    dados_atualizados = {
        "logradouro": "Rua Nova",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "Campinas",
        "cep": "13000-000",
        "tipo": "Casa",
        "valor": 750000.00,
        "data_aquisicao": "2026-09-15",
    }

    with patch("app.connect_db", return_value=conexao_mock):
        resposta = client.put(
            "/imoveis/1",
            json=dados_atualizados,
        )

    assert resposta.status_code == 200
    assert resposta.get_json() == {
        "id": 1,
        "logradouro": "Avenida Pernambucana",
        "tipo_logradouro": "Avenida",
        "bairro": "Boa Vista",
        "cidade": "Recife",
        "cep": "01310-100",
        "tipo": "Apartamento",
        "valor": 850000.00,
        "data_aquisicao": "2024-01-15",
    }

    with patch("app.connect_db", return_value=conexao_mock):
        resposta = client.put(
            "/imoveis/1",
            json=dados_atualizados,
        )

    assert resposta.status_code == 200
    assert resposta.get_json() == {
        "mensagem": "Imóvel atualizado com sucesso"
    }

    cursor_mock.execute.assert_called_once_with(
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
            "Rua Nova",
            "Rua",
            "Centro",
            "Campinas",
            "13000-000",
            "Casa",
            750000.00,
            "2026-09-15",
            1,
        ),
    )

    conexao_mock.commit.assert_called_once()
    cursor_mock.close.assert_called_once()
    conexao_mock.close.assert_called_once()