import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn
import numpy as np


def reg_graph(file_path):
    df = pd.read_excel(file_path)
    X = df['PAX']
    y = df['WGT']
    corr_score = np.corrcoef(X, y)[0][1]
    corr_score = '{:.2}'.format(corr_score)

    plt.figure()
    plt.title('相関係数：' + corr_score)
    plt.grid()
    seaborn.regplot(x=X, y=y, data=df)
    plt.savefig('download/' + file_path[6:] + '_graph.jpg')
    plt.close('all')
    graph_path = file_path[6:] + '_graph.jpg'
    return graph_path[1:]

if __name__ == '__main__':
    result = reg_graph('static/data.xlsx')
    print(result)
    