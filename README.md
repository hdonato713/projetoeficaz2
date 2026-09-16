# Projeto 2 — Programação Eficaz

API REST para gerenciamento de imóveis, desenvolvida em Flask com MySQL hospedado no Aiven.

Desenvolvido por Eduardo Lebre e Heitor Donato.

## Tecnologias

- Python
- Flask
- MySQL Connector/Python
- MySQL no Aiven
- pytest

## Estrutura do projeto

- `app.py`: rotas Flask e conexão com o banco.
- `imoveis.py`: conversão de registros MySQL para JSON.
- `tests/`: testes automatizados por responsabilidade.
- `.cred.example`: modelo de credenciais locais.

## Configuração local

Crie e ative um ambiente virtual:

```powershell
python -m venv env
env\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Crie o arquivo local de credenciais a partir do modelo:

```powershell
Copy-Item .cred.example .cred
```

Preencha `.cred` com os dados do serviço MySQL no Aiven:

```text
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_PORT=
SSL_CA_PATH=ca.pem
```

Baixe o certificado da autoridade certificadora do Aiven e salve-o como `ca.pem` na raiz do projeto. Os arquivos `.cred` e `ca.pem` são locais e não devem ser enviados ao Git.

## Banco de dados

O banco foi criado com o [script oficial de imóveis](https://insper.github.io/ProgramacaoEficaz/projetos/projeto2/imoveis.sql). Não execute o script novamente em um banco já populado, pois ele insere os registros outra vez.

## Testes

Com o ambiente virtual ativo, execute:

```powershell
python -m pytest
```

## Execução local

Com o ambiente virtual ativo e as credenciais configuradas, inicie o servidor:

```powershell
flask --app app run --debug
```

A API ficará disponível em `http://127.0.0.1:5000`.

## Rotas

| Método | Rota | Descrição |
|---|---|---|
| GET | `/imoveis` | Lista todos os imóveis. |
| GET | `/imoveis/<id>` | Busca um imóvel pelo identificador. |
| POST | `/imoveis` | Cria um imóvel. |
| PUT | `/imoveis/<id>` | Atualiza um imóvel. |
| DELETE | `/imoveis/<id>` | Remove um imóvel. |
| GET | `/imoveis/tipo/<tipo>` | Lista imóveis de um tipo. |
| GET | `/imoveis/cidade/<cidade>` | Lista imóveis de uma cidade. |

Os corpos de criação e atualização devem ser JSON. `logradouro` e `cidade` são obrigatórios; os demais campos são opcionais.

Exemplo de corpo para criação ou atualização:

```json
{
  "logradouro": "Rua das Flores",
  "cidade": "São Paulo",
  "tipo": "apartamento",
  "valor": 850000
}
```

## Respostas HTTP

| Situação | Status |
|---|---:|
| Listagem, busca, atualização ou remoção bem-sucedida | 200 |
| Criação bem-sucedida | 201 |
| Dados obrigatórios ausentes | 400 |
| Imóvel inexistente | 404 |
| Falha de conexão com o banco | 500 |

## HATEOAS

As respostas de sucesso incluem controles de hipermídia em `_links`. Cada
controle indica uma ação disponível, a URI do recurso (`href`) e o método HTTP
necessário (`method`). Por exemplo, um imóvel consultado pode trazer:

```json
{
  "id": 1,
  "logradouro": "Rua das Flores",
  "_links": {
    "self": {"href": "/imoveis/1", "method": "GET"},
    "update": {"href": "/imoveis/1", "method": "PUT"},
    "delete": {"href": "/imoveis/1", "method": "DELETE"},
    "collection": {"href": "/imoveis", "method": "GET"}
  }
}
```

## Desenvolvimento orientado a testes

As funcionalidades foram desenvolvidas seguindo o ciclo: teste que falha, implementação mínima para o teste passar e refactor com todos os testes verdes.

## Deploy

A URL pública da API será adicionada após o deploy no AWS EC2.
