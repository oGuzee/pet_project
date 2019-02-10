import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn import metrics


def outer_function():
    ''' Closure, prints the time the function is called'''
    now = datetime.datetime.now()
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

def compute_time_diff(df):
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
    m = np.delete(m, (0), axis=0)
    return m

# Higher Order Function
def time_execution(f):
    def wrapped(*args, **kws):
        now = datetime.datetime.now()
        print('[' + str(now) + '] Call Function: ' + f.__name__ + '()')
        return f(*args, **kws)
    return wrapped

@time_execution
def k_means(m, figurename):
    '''
    KMeans algorithm is applied. \
    Parameters: m = np.array (shape==(X,2))\
                figurename = str; example =  "hamilton_australia_2011.png"\
    returns list; clustered labels of the instances
    '''
    kmeans = KMeans(n_clusters=5, random_state=41).fit(m)
    labels = kmeans.labels_

    plt.scatter(m[:, 0], m[:, 1], c=labels, cmap='rainbow')
    plt.savefig('figures/'+figurename)

    print('Silhouette score: ', metrics.silhouette_score(m, labels, metric='euclidean'))
    return labels

def label_data(m, df, outname):
    m = m.astype(str)
    m = np.insert(m, 0, outname)
    df['label'] = m
    df.to_csv('saved_data/'+outname)
    return df

if __name__ == '__main__':
    outer_function() # Closure
    DATA_FRAME = load_csv('lap_times.csv')
    FILTERED_FRAME = filter_by_race_and_driver_id(DATA_FRAME, 841, 20)
    COMPUTED_FRAME = compute_time_diff(FILTERED_FRAME)
    MATRIX = to_numpy_matrix(COMPUTED_FRAME)
    LABELS_LIST = k_means(MATRIX, 'vettel_australia_2011.png')
    FINAL_FRAME = label_data(LABELS_LIST, COMPUTED_FRAME, 'vettel_australia_2011.csv')
