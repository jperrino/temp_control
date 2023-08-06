from enum import Enum


class TimeRange(str, Enum):
    diaria = "1"
    semanal = "2"
    mensual = "3"
