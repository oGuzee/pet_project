import unittest
import main as a
import pandas as pd
import numpy as np

class TestMethods(unittest.TestCase):
    def test_load_csv(self):
        columns_ = ['race_id', 'driver_id', 'lap', 'position', 'lap_time', 'lap_milliseconds']
        assert all([x==y for x, y in zip(a.load_csv('lap_times.csv').columns, columns_)])

    def test_filter_by_race_and_driver_id(self):
        df = pd.read_csv('f1db_csv/lap_times.csv', index_col=0)
        df = a.filter_by_race_and_driver_id(df, 841, 20)
        assert (df['driver_id'].unique()[0] == 20) & (len(df['race_id'].unique()) == 1)

    def test_compute_diff(self):
        df = pd.read_csv('f1db_csv/lap_times.csv', index_col=0)
        df = a.filter_by_race_and_driver_id(df, 841, 20)
        columns_ = ['driver_id', 'lap', 'race_id', 'position', 'lap_time', 'lap_milliseconds', 'lap_milliseconds_diff']
        assert all([x==y for x, y in zip(a.compute_time_diff(df).columns, columns_)])

    def test_to_numpy_matrix(self):
        df = pd.read_csv('f1db_csv/lap_times.csv', index_col=0)
        df = a.filter_by_race_and_driver_id(df, 841, 20)
        df = a.compute_time_diff(df)
        m = a.to_numpy_matrix(df)
        assert (len(m) == len(df) - 1) & ((len(df) - 1, 2) == m.shape)


if __name__ == '__main__':
    unittest.main()