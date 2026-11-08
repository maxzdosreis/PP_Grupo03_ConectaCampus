from rest_framework import status
from rest_framework.exceptions import APIException


class ServicoIndisponivel(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_code = "servico_indisponivel"
