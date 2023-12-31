import pkg_resources
import pandas as pd
from json import loads
from fitter import Fitter, get_common_distributions, get_distributions
import logging
import warnings
warnings.simplefilter(action = "ignore") 
pd.set_option('display.max_colwidth', None)

logger = logging.getLogger()

#distributions = get_common_distributions()
distributions = [ 'norm','expon','uniform','triang','lognorm','gamma' ]

start_time = 'start_time'
end_time = 'end_time'
case_id =  'case_id' 
interval = 'interval'
timeout = 120


class EventLog:
  
  def __init__(self, log, timestamp_format = '%Y-%m-%d %H:%M:%S.%f', verbose = False ):
    #df = pd.read_csv( BytesIO( log ), sep="," )
    
    
    self.data = log
    self.distributions = distributions
    columns = list( self.data.columns )   
    new_columns = [ case_id if c.lower().startswith('case') else c for c in columns ]
    new_columns = [ start_time if c.lower().startswith('start') else c for c in new_columns ]
    new_columns = [ end_time if c.lower().startswith('end') else c for c in new_columns ]
    self.data[new_columns] = self.data[ columns ] 
    self.data[ start_time ] = pd.to_datetime(self.data[ start_time ], format = timestamp_format )
    self.data[ end_time ] = pd.to_datetime(self.data[ end_time ], format = timestamp_format )

    if verbose:  
      msg = "Using piops version: " + pkg_resources.get_distribution("piops").version
      print(msg)
      print( "Log with the following columns: ", new_columns )
      print( "Testing the following distributions by default: ", self.distributions )

    self.data[ 'duration' ] =   self.data[ end_time ].sub(self.data[ start_time ]).dt.total_seconds().div(60)
    self.data = self.data.sort_values(by= start_time )
    
    

  def __str__( self ):
    return self.data.to_csv( index=False )


  def distInterval( self ):
    df = self.data.copy()
    df = df.drop_duplicates(subset=[ case_id ])
    df[ interval ] = df[ start_time ].diff()
    df[ interval ] = df[ interval ].dt.total_seconds().div(60)
    df.drop(0,axis=0, inplace=True)
    logger.disabled = True
    f = Fitter( df[  interval  ], timeout = timeout, distributions = self.distributions )
    f.fit()
    self.distributions = distributions
    logger.disabled = False
    results= {"Cases Interval": {"distribution": list(f.get_best().keys())[0], "parameters" : list(f.get_best().values())[0] }}
    dist = pd.DataFrame.from_dict(results, orient='index')
    #self.interval = f.get_best()
    return dist
  

  def intervalStats( self ):
    df = self.data.copy()
    df = df.drop_duplicates(subset=[ case_id ])
    df['Cases Interval'] = df[ start_time ].diff()
    df['Cases Interval'] = df['Cases Interval'].dt.total_seconds().div(60)
    df.drop(0,axis=0, inplace=True)
    stats = df['Cases Interval'].describe().to_frame().T
    stats.insert(loc = 3, column = 'var', value = stats['std']**2 )
    return stats
  

  def distActivities( self ):

    activities_list = list(self.data[ 'Activity' ].unique())
    results = {}
    logger.disabled = True
    for activity in activities_list:
        act = self.data[self.data[ 'Activity' ] == activity ]
        f = Fitter( act[ 'duration' ], timeout = timeout, distributions = self.distributions )
        f.fit()
        results[activity] = {"distribution": list(f.get_best().keys())[0], "parameters" : list(f.get_best().values())[0] }
        dist = pd.DataFrame.from_dict(results, orient='index')
    self.distributions = distributions
    logger.disabled = False    
    return dist


  def activitiesStats( self ):

    df = self.data.copy()
    #df = pd.read_csv( BytesIO( log ), sep="," )
    #df[ start_time ] = pd.to_datetime(df[ start_time ], format='%Y-%m-%d %H:%M:%S.%f')
    #df[ end_time ] = pd.to_datetime(df[ end_time ], format='%Y-%m-%d %H:%M:%S.%f')
    #df['duration'] =   df[ end_time ].sub(df[ start_time ]).dt.total_seconds().div(60)
    #df = df.sort_values(by= start_time )
    stats = df.groupby([ 'Activity' ])[ 'duration' ].describe()
    stats.insert(loc = 3, column = 'var', value = stats['std']**2 )
    return stats
  

  def summary( self, distributions = None, verbose = False ):
    if distributions is not None: 
      self.distributions = distributions
    if verbose:  print( "Using the following distributions:", self.distributions )
    return  pd.concat([ self.distInterval().join( self.intervalStats() ), self.distActivities().join( self.activitiesStats() ) ]) 

