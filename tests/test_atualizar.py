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
    assert resposta.get_json() == dados_atualizados

    consulta, parametros = cursor_mock.execute.call_args.args

    assert "UPDATE imoveis" in consulta
    assert "WHERE id = %s" in consulta

    assert parametros == (
        "Rua Nova",
        "Rua",
        "Centro",
        "Campinas",
        "13000-000",
        "Casa",
        750000.00,
        "2026-09-15",
        1,
    )

    conexao_mock.commit.assert_called_once()
    cursor_mock.close.assert_called_once()
    conexao_mock.close.assert_called_once()