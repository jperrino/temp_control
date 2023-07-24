from enum import Enum


class Message(str, Enum):
    WELCOME_MESSAGE = "Bienvenido al servicio de control de temperatura.\n" \
                      "Ingrese el nombre del dispositivo:"

    SELECT_TIME_RANGE_MESSAGE = "Elija una opcion:\n" \
                                "1.Recibir la grafica de temperatura diaria\n" \
                                "2.Recibir la grafica de temperatura semanal\n" \
                                "3.Recibir la grafica de temperatura mensual"

    DEVICE_NOT_FOUND_MESSAGE = "No se encontro el dispositivo: {device}\n" \
                               "Ingrese otro nombre"

    INVALID_TIME_RANGE_MESSAGE = "Opcion no valida: {time_range}\n" \
                                 "Ingrese 1, 2 o 3."

    RECORD_NOT_FOUND_MESSAGE = "No se encontraron registros de temperatura para dispositivo:\n" \
                               "{device}"

    GRAPH_RESPONSE_MESSAGE = "Grafica {time_range} de fermentacion de cerveza para {device}:\n" \
                             "{graph_url}"

    SELECT_FLOW_MESSAGE = "Elija una opcion:\n" \
                          "1.Solicitar grafica de temperatura\n" \
                          "2.Definir rango de temperatura"

    SELECT_TEMP_MIN_MESSAGE = "Ingrese el valor minimo de temperatura:"

    SELECT_TEMP_MAX_MESSAGE = "Ingrese el valor maximo de temperatura:"

    TRANSACTION_COMPLETED_MESSAGE = "Operacion completada."
