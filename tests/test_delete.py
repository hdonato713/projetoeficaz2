from unittest.mock import MagicMock, patch


def test_remove_imovel(client):
    conexao_mock = MagicMock()
    cursor_mock = MagicMock()

    conexao_mock.cursor.return_value = cursor_mock
    cursor_mock.rowcount = 1

    with patch("app.connect_db", return_value=conexao_mock):
        resposta = client.delete("/imoveis/1")

    assert resposta.status_code == 200
    assert resposta.get_json() == {
        "mensagem": "Imóvel removido com sucesso"
    }

    cursor_mock.execute.assert_called_once_with(
        "DELETE FROM imoveis WHERE id = %s",
        (1,),
    )

    conexao_mock.commit.assert_called_once()
    cursor_mock.close.assert_called_once()
    conexao_mock.close.assert_called_once()