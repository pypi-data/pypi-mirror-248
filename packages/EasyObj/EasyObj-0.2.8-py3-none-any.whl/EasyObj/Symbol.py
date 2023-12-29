import uuid


class Symbol:
    def __init__(self, symbol=None):
        if symbol == None:
            self.__noname = True
            symbol = uuid.uuid4().hex
        else:
            self.__noname = False
        self.symbol = symbol


__all__ = ["Symbol"]
