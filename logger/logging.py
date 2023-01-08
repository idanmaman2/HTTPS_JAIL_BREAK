class Logger :
    
    __logger__ = None 
     
     
    def __init__(self , path ):
         ...
     
    def log(self):
        ...
     
     
    def getInstance():
        if not Logger.__logger__ : 
            __logger__ = Logger() 
        return __logger__ 