import pandas as pd
from functools import reduce
import math
import numpy
import re

class ParserTool:

    def __init__(self, logfile: str):
        self.df = pd.read_csv(
            logfile,
            delim_whitespace = True,
            escapechar = '\\',
            usecols = [3, 4, 5, 9],
            names = ['timestamp', 'tz', 'method', 'user_agent'],
            converters={
                'timestamp': self.__parse_datetime,
                'tz': self.__parse_tz,
                'method': self.__parse_method}
            )

        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'] + self.df['tz'], format = '%d/%b/%Y:%H:%M:%S%z', errors = 'coerce')
        self.df.drop('tz', axis=1, inplace=True)
        self.df['os'] = self.df['user_agent'].apply(self.__parse_os)

    def __parse_method(self, x):
        try:
            method = x.split(' ', 1)[0]
            return method
        except:
            return None

    def __parse_datetime(self, x):
        return x.lstrip('[')

    def __parse_tz(self, x):
        return x.rstrip(']')

    def __parse_os(self, x):
        os_list = {'Linux': 'Linux', 'Windows': 'Windows', 'Mac': 'MacOSX'}
        try:
            platform = re.search('\((.*)\)', x).group(1)
            found = set(os_list.keys()).intersection(platform.split())
            if len(found) > 0 :
                return os_list[found.pop()]
            else:
                return None
        except:
            return None

    def __get_ratio(self, x):
        counts = [x['GET'].astype(numpy.int64), x['POST'].astype(numpy.int64)]
        denominater = reduce(math.gcd, counts)
        solved = [i/denominater for i in counts]
        return ':'.join(str(int(i)) for i in solved)

    def daily_request(self):
        df_res = (self.df['timestamp']
            .dt.date
            .value_counts()
            .rename_axis('Date')
            .reset_index(name='Request Served'))
        print ('#' * 50)
        print ('Number of requests served by day:')
        print ('#' * 50)
        print (df_res.head().to_string())

    def daily_frequent_ua(self):
        df_res = pd.DataFrame(columns=['Date', 'User Agent'], data=self.df[['timestamp', 'user_agent']].values)
        df_res['Date'] = df_res['Date'].dt.date
        df_res['hits'] = df_res.groupby(['Date', 'User Agent'])['User Agent'].transform('count')
        df_res = df_res.groupby(['Date'])[['Date', 'User Agent', 'hits']].apply(lambda x: x.nlargest(3, columns=['hits']))
        df_res = df_res.drop('hits', axis=1).reset_index(drop = True)
        print ('#' * 50)
        print ('Three most frequent User Agents by day:')
        print ('#' * 50)
        print (df_res.to_string())

    def daily_method_ratio(self):
        df_res = pd.DataFrame(columns=['Date', 'method', 'OS'], data=self.df[['timestamp', 'method', 'os']].values)
        df_res['Date'] = df_res['Date'].dt.date
        df_res = df_res.loc[df_res['method'].isin(['GET', 'POST'])]
        df_res = df_res.groupby(['Date', 'OS'])['method'].value_counts().unstack().fillna(0) #.reset_index()
        df_res.columns = [''.join(col) for col in df_res.columns.values]
        df_res = df_res.reset_index()
        df_res['GETs to POSTs Ratio'] = df_res[['GET', 'POST']].apply(self.__get_ratio, axis=1)
        df_res = df_res.drop(['GET', 'POST'], axis=1)
        print ('#' * 50)
        print ('Ratio of GETs to POSTs by OS by day:')
        print ('#' * 50)
        print (df_res.to_string())
