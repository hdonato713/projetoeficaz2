from unittest.mock import MagicMock, patch

from app import connect_db


@patch("app.mysql.connector.connect")
def test_connect_db_retorna_conexao(mock_mysql_connect):
    mock_conn = MagicMock()
    mock_conn.is_connected.return_value = True
    mock_mysql_connect.return_value = mock_conn

    assert connect_db() is mock_conn


@patch("app.mysql.connector.connect")
@patch("app.os.getenv")
def test_connect_db_usa_variaveis_de_ambiente(
    mock_getenv, mock_mysql_connect
):
    valores = {
        "DB_HOST": "host-teste",
        "DB_USER": "usuario-teste",
        "DB_PASSWORD": "senha-teste",
        "DB_NAME": "banco-teste",
        "DB_PORT": "1234",
        "SSL_CA_PATH": "ca-teste.pem",
    }
    mock_getenv.side_effect = lambda chave, padrao=None: valores.get(
        chave, padrao
    )

    mock_conn = MagicMock()
    mock_conn.is_connected.return_value = True
    mock_mysql_connect.return_value = mock_conn

    assert connect_db() is mock_conn
    mock_mysql_connect.assert_called_once_with(
        host="host-teste",
        user="usuario-teste",
        password="senha-teste",
        database="banco-teste",
        port=1234,
        ssl_ca="ca-teste.pem",
    )
