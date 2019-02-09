import unittest
import main as a
import pandas as pd

class TestStringMethods(unittest.TestCase):
    df = pd.read_csv('f1db_csv/lap_times.csv', index_col=0)

    def test_csv(self):
        columns_ = ['race_id', 'driver_id', 'lap', 'position', 'lap_time', 'lap_milliseconds']
        assert all([x==y for x,y in zip(a.load_csv('lap_times.csv').columns, columns_)])



if __name__ == '__main__':
    unittest.main()