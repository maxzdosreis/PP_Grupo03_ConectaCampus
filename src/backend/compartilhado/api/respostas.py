from rest_framework.response import Response


def resposta_sucesso(mensagem, dados=None, status=200):
    return Response({"mensagem": mensagem, "dados": dados}, status=status)


def corpo_de_erro(codigo, mensagem, campos=None):
    erro = {"codigo": codigo, "mensagem": mensagem}
    if campos:
        erro["campos"] = campos
    return {"erro": erro}


def resposta_erro(codigo, mensagem, status, campos=None):
    return Response(corpo_de_erro(codigo, mensagem, campos), status=status)
