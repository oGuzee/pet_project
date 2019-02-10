import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn import metrics


def outer_function(now=datetime.datetime.now()):
    def inner_function():
        print('Application started at: ', now)
    inner_function()

def load_csv(filename):
    ''' Read lap_times.csv and return a Pandas DataFrame '''
    return pd.read_csv('f1db_csv/'+filename, index_col=0)


def filter_by_race_and_driver_id(df, race, driver):
    ''' Filter lap_times DataFrame by race_id and driver_id
        race_id = int, driver_id = int'''
    return df[(df.race_id == race) & (df.driver_id == driver)]\
        .sort_values(['lap', 'position'])

def compute_diff(df):
    ''' Computing difference of each lap time difference
        df['lap_milliseconds_diff'] = previous lap + current lap '''
    df = df.set_index(['driver_id', 'lap'])
    df_ = df.groupby(level=0)
    df_ = df_['lap_milliseconds'].diff()
    df = df.join(df_, on=['driver_id', 'lap'], lsuffix='', rsuffix='_diff')
    df = df.reset_index(level='lap')
    df = df.reset_index()
    df = df.fillna(0)
    return df

def to_numpy_matrix(df):
    '''Transform DataFrame to numpy ndarray [lap, lap_time_difference]'''
    df = df.drop(columns=['lap_milliseconds', 'position', 'lap_time', 'race_id', 'driver_id'])
    m = df.values
    print(type(m))
    m = np.delete(m, (0), axis=0)
    return m

def time_execution(f):
    def wrapped(*args, **kws):
        now = datetime.datetime.now()
        print('[' + str(now) + '] Call Function: ' + f.__name__ + '()')
        return f(*args, **kws)
    return wrapped

@time_execution
def k_means(m):
    ''' KMeans '''
    kmeans = KMeans(n_clusters=5, random_state=41)
    kmeans.fit(m)
    labels = kmeans.labels_
    print("Cluster centers: ", kmeans.cluster_centers_)
    print('Labels: ', kmeans.labels_)

    plt.scatter(m[:, 0], m[:, 1], c=labels, cmap='rainbow')
    plt.show()

    print('Silhouette score: ', metrics.silhouette_score(m, labels, metric='euclidean'))
    print('Score: ', kmeans.score(m))

if __name__ == '__main__':
    outer_function() # Closure
    LAP_TIMES = load_csv('lap_times.csv')
    LAP_TIMES = filter_by_race_and_driver_id(LAP_TIMES, 841, 20)
    LAP_TIMES = compute_diff(LAP_TIMES)
    LAP_TIMES = to_numpy_matrix(LAP_TIMES)
    # print(LAP_TIMES)
    k_means(LAP_TIMES)
