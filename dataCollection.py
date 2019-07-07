import bitfinex
import time
import datetime
import time
import pandas as pd

pair = 'btcusd'
bin_size = '1m'
limit = 1000
time_step = 60000

'''time step has to be converted from microseconds to the bin_size unit
24 hours
60 minutes
'''

t_start = datetime.datetime(2019, 4, 1, 0, 0)
t_start = time.mktime(t_start.timetuple()) * 1000

t_stop = datetime.datetime(2019, 4, 1, 1, 0)
t_stop = time.mktime(t_stop.timetuple()) * 1000

print(t_start-t_stop)

'''
Returns: Open, High, Low, Close 

-------------------To view different pairs---------
api_v1 = bitfinex.bitfinex_v1.api_v1()
pairs = api_v1.symbols()
---------------------------------------------------
'''

# Create api instance
api_v2 = bitfinex.bitfinex_v2.api_v2()
data = []

while t_start<t_stop:
    t_start= t_start+time_step
    #print(len(data))
    print(len(data))
    if (t_start - t_stop) == 0:
        t_stop+=1
        res = api_v2.candles(symbol=pair, interval=bin_size,
                             limit=limit, start=t_start, end=t_stop)
        break

    res = api_v2.candles(symbol=pair, interval=bin_size,
                         limit=limit, start=t_start,end=t_stop)

    time.sleep(2)
    data.extend(res)

names = ['time', 'open', 'close', 'high', 'low', 'volume']
df = pd.DataFrame(data, columns=names)
df.drop_duplicates(inplace=True)
df['time'] = pd.to_datetime(df['time'], unit='ms')
df.set_index('time', inplace=True)
df.sort_index(inplace=True)
df.to_csv('btcusdData.csv')

print(df)
