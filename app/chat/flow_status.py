from enum import Enum


class FlowStatus(int, Enum):
    STARTED = 1
    REQUEST_GRAPH = 2
    SET_MIN_TEMPERATURE = 3
    SET_MAX_TEMPERATURE = 4
    COMPLETED = 5
