import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  

from sklearn.cluster import KMeans 
from sklearn import metrics

# Closure
def outerFunction(now = datetime.datetime.now()):
    def innerFunction(): 
        print('Application started at: ', now) 
    innerFunction()

def load_csv():
    ''' Read lap_times.csv and set the column-headers
        returns pandas.DataFrame '''
    df = pd.read_csv('f1db_csv/lap_times.csv', header=None)
    df.columns = ['race_id', 'driver_id', 'lap', 'position', 'lap_time', 'lap_milliseconds']
    return df


def filter_by_race_and_driver_id(df, race, driver):
    ''' Filter lap_times DataFrame by race_id and driver_id
        race_id = int, driver_id = int'''
    return df[(df.race_id == race) & (lap_times.driver_id == driver)].sort_values(['lap', 'position'])

def compute_diff(df):
    ''' Computing difference of each lap time difference 
        df['diff'] = previous lap + current lap '''
    df = df.set_index(['driver_id', 'lap'])
    df_ = df.groupby(level=0)
    df_ = df_['lap_milliseconds'].diff()
    df = df.join(df_, on=['driver_id', 'lap'], lsuffix='', rsuffix='_diff')
    df = df.reset_index(level='lap')
    df = df.reset_index()
    df = df.fillna(0)
    return df

def to_numpy_matrix(df):
    ''' Transform DataFrame to numpy ndarray [lap, lap_time_difference] '''
    df = df.drop(columns=['lap_milliseconds','position','lap_time', 'race_id', 'driver_id'])  
    m = df.values
    print(type(m))
    m = np.delete(m, (0), axis=0)
    return m

def kmeans(m):
    kmeans = KMeans(n_clusters=5, random_state=41)  
    kmeans.fit(m)
    labels = kmeans.labels_
    print("Cluster centers: ", kmeans.cluster_centers_)
    print('Labels: ', kmeans.labels_) 

    plt.scatter(m[:,0], m[:,1], c= labels, cmap= 'rainbow') 
    plt.show()

    print('Silhouette score: ', metrics.silhouette_score(m, labels, metric='euclidean'))
    print('Score: ', kmeans.score(m))

if __name__ == '__main__': 
    outerFunction() # Closure
    lap_times = load_csv()
    lap_times = filter_by_race_and_driver_id(lap_times, 841, 20)
    lap_times = compute_diff(lap_times)
    lap_times = to_numpy_matrix(lap_times)
    # print(lap_times)
    kmeans(lap_times)
