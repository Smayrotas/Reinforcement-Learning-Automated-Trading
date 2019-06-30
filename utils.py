import matplotlib
import matplotlib.dates as mdates
import numpy as np


def convert_date(date_bytes):
    return mdates.strpdate2num('%Y%m%d%H%M%S')(date_bytes.decode('ascii'))

def getData():
    date, bid, ask = np.loadtxt('GBPUSD1d.txt',
                                unpack=True,
                                delimiter=',',
                                converters={0:convert_date})
    return date, bid, ask

