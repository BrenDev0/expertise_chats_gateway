
class ExpiredToken(Exception):
    def __init__(self, detail: str = "Token expired"):
        super().__init__(detail)

class InvalidToken(Exception):
    def __init__(self, detail: str = "Ivalid token"):
        super().__init__(detail)