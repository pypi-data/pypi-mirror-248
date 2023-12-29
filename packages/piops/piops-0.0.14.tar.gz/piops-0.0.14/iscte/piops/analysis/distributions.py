import pandas as pd
from json import loads
from fitter import Fitter, get_common_distributions, get_distributions

class EventLog:
  
  def __init__(self,log):
    self.data = log
    #df = pd.read_csv( BytesIO( log ), sep="," )
    self.data['start_time'] = pd.to_datetime(self.data['start_time'], format='%Y-%m-%d %H:%M:%S.%f')
    self.data['end_time'] = pd.to_datetime(self.data['end_time'], format='%Y-%m-%d %H:%M:%S.%f')
    self.data['duration'] =   self.data['end_time'].sub(self.data['start_time']).dt.total_seconds().div(60)
    self.data = self.data.sort_values(by='start_time')

    self.activities = {}
    self.interval = {}

  def __str__( self ):
    return self.data.to_csv(index=False)

  def distInterval( self ):
    df = self.data.copy()
    df = df.drop_duplicates(subset=['case_id'])
    df['interval'] = df['start_time'].diff()
    df['interval'] = df['interval'].dt.total_seconds().div(60)
    df.drop(0,axis=0, inplace=True)
    f = Fitter( df[ 'interval' ], distributions = get_common_distributions())
    f.fit()
    #self.interval = f.get_best()
    return f
  
  def intervalStats( self ):
    df = self.data.copy()
    df = df.drop_duplicates(subset=['case_id'])
    df['Cases Interval'] = df['start_time'].diff()
    df['Cases Interval'] = df['Cases Interval'].dt.total_seconds().div(60)
    df.drop(0,axis=0, inplace=True)
    stats = df['Cases Interval'].describe().to_frame().T
    stats.insert(loc = 3, column = 'var', value = stats['std']**2 )
    return stats
  


  def distActivities( self ):

    activities_list = list(self.data['Activity'].unique())
    results = {}
    for activity in activities_list:
        act = self.data[self.data['Activity'] == activity ]
        f = Fitter( act['duration'] , distributions = get_common_distributions())
        f.fit()
        results[activity] = {"distribution": list(f.get_best().keys())[0], "parameters" : list(f.get_best().values())[0] }
        dist = pd.DataFrame.from_dict(results, orient='index')
    return dist


  def activitiesStats( self ):

    df = self.data.copy()
    #df = pd.read_csv( BytesIO( log ), sep="," )
    #df['start_time'] = pd.to_datetime(df['start_time'], format='%Y-%m-%d %H:%M:%S.%f')
    #df['end_time'] = pd.to_datetime(df['end_time'], format='%Y-%m-%d %H:%M:%S.%f')
    #df['duration'] =   df['end_time'].sub(df['start_time']).dt.total_seconds().div(60)
    #df = df.sort_values(by='start_time')
    stats = df.groupby(['Activity'])['duration'].describe()
    stats.insert(loc = 3, column = 'var', value = stats['std']**2 )
    return stats
  

  def eventLogStats( self ):
    
    distributions = self.distActivities()
    statistics = self.activitiesStats()

    return  distributions.join( statistics )

