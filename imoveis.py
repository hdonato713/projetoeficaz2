def formatar_imovel(resultado):
    return {
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
