import pandas as pd
from io import BytesIO
from fitter import Fitter, get_common_distributions, get_distributions

def distfit( log ):
    
    print(log)
    df = pd.read_csv( BytesIO( log ), sep="," )
    df['start_time'] = pd.to_datetime(df['start_time'], format='%Y-%m-%d %H:%M:%S.%f')
    df['end_time'] = pd.to_datetime(df['end_time'], format='%Y-%m-%d %H:%M:%S.%f')
    #df['duration'] =   df['end_time'].sub(df['start_time']).dt.total_seconds().div(60)
    df = df.sort_values(by='start_time')
    df = df.drop_duplicates(subset=['case_id'])
    df.loc[:,'interval'] = df['start_time'].diff()
    df['interval'] = df['interval'].dt.total_seconds().div(60)
    print(df['interval'])
    f = Fitter( df[ 'interval' ], distributions = get_common_distributions())
    f.fit()
    
    return f