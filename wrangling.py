import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans 
from sklearn import metrics

# Higher Function Wrapper
def time_execution(f):
    def wrapped(*args, **kws):
        now = datetime.datetime.now()
        print('[' + str(now) + '] Call Function: ' + f.__name__ + '()')
        return f(*args, **kws)
    return wrapped


circuits = pd.read_csv('f1db_csv/circuits.csv', header=None)
circuits.columns = ['circuit_id', 'circuit_ref', 'circuit_name', 'circuit_location', 'circuit_country', 'circuit_lat', 'circuit_lon', 'circuit_alt', 'circuit_url']
circuit_id = circuits['circuit_id']

status = pd.read_csv('f1db_csv/status.csv', header=None)
status.columns = ['status_id', 'status']
status_id = status['status_id']

lap_times = pd.read_csv('f1db_csv/.csv', header=None)
lap_times.columns = ['race_id', 'driver_id', 'lap', 'position', 'lap_time', 'lap_milliseconds']

races = pd.read_csv('f1db_csv/races.csv', header=None)
races.columns = ['race_id', 'race_year', 'race_round', 'circuit_id', 'race_name', 'race_date', 'race_time', 'race_url']
races_ = races[['race_id', 'race_year', 'race_round', 'circuit_id', 'race_date', 'race_time']]

constructors = pd.read_csv('f1db_csv/constructors.csv', header=None)
constructors.columns = ['constructor_id', 'constructor_ref', 'constructor_name', 'constructor_nationality', 'constructor_url']
constructor_id = constructors['constructor_id']

constructor_standings = pd.read_csv('f1db_csv/constructor_standings.csv', header=None)
constructor_standings.columns = ['constructor_standings_id', 'race_id', 'constructor_id','constructor_standings_points','constructor_standings_position','constructor_standings_positionText','constructor_standings_wins']
constructor_standings_ = constructor_standings[['constructor_standings_id', 'race_id', 'constructor_id','constructor_standings_points','constructor_standings_position','constructor_standings_wins']]

drivers = pd.read_csv('f1db_csv/driver.csv', header=None)
drivers.columns = ['driver_id', 'driver_red', 'driver_number', 'driver_code', 'driver_forename', 'driver_surname', 'driver_dob', 'driver_nationality', 'driver_url']
driver_id = drivers['driver_id']

qualifyings = pd.read_csv('f1db_csv/qualifying.csv', header=None)
qualifyings.columns = ['qualifyings_id', 'race_id', 'driver_id', 'constructor_id', 'driver_number', 'qualifyings_position', 'q1', 'q2', 'q3']
qualifyings_ = qualifyings[['qualifyings_id', 'race_id', 'driver_id', 'constructor_id', 'qualifyings_position', 'q1', 'q2', 'q3']]

driver_standings = pd.read_csv('f1db_csv/driver_standings.csv', header=None)
driver_standings.columns = ['driver_standings_id', 'race_id', 'driver_id', 'driver_standings_points', 'driver_standings_position', 'driver_standings_position_text','driver_standings_wins']
driver_standings_ = driver_standings[['driver_standings_id', 'race_id', 'driver_id', 'driver_standings_points', 'driver_standings_position','driver_standings_wins']]

constructor_results = pd.read_csv('f1db_csv/constructor_results.csv', header=None)
constructor_results.columns = ['constructor_results_id', 'race_id', 'constructor_id', 'constructor_results_points', 'constructor_results_status']

pit_stops = pd.read_csv('f1db_csv/pit_stops.csv', header=None)
pit_stops.columns = ['race_id', 'driver_id', 'pit_stop_number', 'pit_lap', 'pit_time', 'pit_duration', 'pit_milliseconds']

seasons = pd.read_csv('f1db_csv/seasons.csv', header=None)
seasons.columns = ['year', 'url']
season = seasons['year']

results = pd.read_csv('f1db_csv/results.csv', header=None)
results.columns = ["result_id","race_id","driver_id","constructor_id","driver_number","starting_position","result_position","result_position_text","result_position_order","result_points","driven_laps","race_time","race_time_milliseconds","race_fastest_lap","fastest_lap_rank","fastest_lap_time","fastest_lap_speed_km/h","status_id"]
results['fastest_lap_speed_km/h'] = results['fastest_lap_speed_km/h'].replace(r'\N', np.NaN).astype(float) *1.609
