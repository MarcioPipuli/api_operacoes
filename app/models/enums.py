from enum import Enum

class OperationType(str, Enum):
    compra = "compra"
    venda = "venda"

class Tickers(str, Enum):
    VALE3 = "VALE3"
    BBAS3 = "BBAS3"
    B3SA3 = "B3SA3"
    PRIO3 = "PRIO3"
    VIVT3 = "VIVT3"
    HAPV3 = "HAPV3"
    SLCE3 = "SLCE3"
    ITUB4 = "ITUB4"
    MELI34 = "MELI34"
    TAEE11 = "TAEE11"
