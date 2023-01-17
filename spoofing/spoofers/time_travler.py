import time as valid_time
YEARS_TO_TRAVEL =3 
DAY_IN_YEAR = 365 
HOURS_IN_DAY = 24 
MINUTES_IN_HOUR = 60
SECS_IN_MINUTE = 60 
def time() : 
    ''' time libary that preforms time travel to the ---> ---> future ---> ---> 
        - the time is in UNIX EPOUCH FORMAT . 
    '''
    
    return (valid_time.time() + valid_time.timezone) \
            + (YEARS_TO_TRAVEL * DAY_IN_YEAR + 1) \
            * HOURS_IN_DAY \
            * MINUTES_IN_HOUR \
            *SECS_IN_MINUTE
     
            
def sleep(secs:int): 
    ''' sleep method - no extra features '''
    valid_time.sleep(secs)
