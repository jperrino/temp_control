import matplotlib.pyplot as plt
from app.config import common_settings
from datetime import datetime

'''
    GRAPH CONFIGURATION
'''
GRAPH_FILE_PATH = common_settings.graphs_file_path
X_LABEL = "Time"
Y_LABEL = "Temperature"
DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
FILE_DATE_FORMAT = '%d_%m_%Y_%H_%M_%S'


def plot_graph(m_list: list, device_name: str):
    now = datetime.now()
    file_name = f"{device_name}_{now.strftime(FILE_DATE_FORMAT)}.jpeg"
    file_path = f"{GRAPH_FILE_PATH}/{file_name}"

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

    # return {"path": file_path, "time": now.strftime(DATE_FORMAT)}
    return {"name": file_name, "path": file_path}

