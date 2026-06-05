# Модуль для унифицированных сообщений об ошибках
class ErrorMessages:
    INVALID_PARAMETERS = "Все параметры должны быть больше 0"

class NotFoundError(Exception):
    INVALID_PARAMETERS = "По запросу ничего нет"

class AlreadyExistsError(Exception):
    INVALID_PARAMETERS = "Такой объект уже существует"