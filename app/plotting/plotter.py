import matplotlib.pyplot as plt
from ..config import settings
from datetime import datetime

X_LABEL = "Time"
Y_LABEL = "Temperature"
DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
FILE_DATE_FORMAT = '%d_%m_%Y_%H_%M_%S'


def plot_graph(m_list: list, device_name: str):
    now = datetime.now()
    file_path = f"{settings.graphs_file_path}/{device_name}_{now.strftime(FILE_DATE_FORMAT)}.jpeg"

    x_values = []
    y_values = []
    for m in m_list:
        x_values.append(m.created_at)
        y_values.append(m.temperature)

    plt.plot(x_values, y_values, 'o-r')
    plt.xlabel(X_LABEL)
    plt.ylabel(Y_LABEL)
    plt.xticks(rotation=45, ha='right')
    plt.savefig(file_path, bbox_inches="tight")

    return {"path": file_path, "time": now.strftime(DATE_FORMAT)}

