class Color(): 
    Red = "\033[0;31m"
    GREEN = "\033[0;32m"
    Yellow = "\033[0;33m"
    BLUE = "\033[0;34m"
    Purple = "\033[0;35m"
    Cyan = "\033[0;36m"
    WHITE ="\033[0;37m"
    
    
class Printing():     
    
    DefaultColor = Color.WHITE
    
    def __changeColor__(color:Color)->None: 
        print(color , end="")
        
    def __printInColor__(*args : list  , sep : str , end  : str,color:Color  ): 
        Printing.__changeColor__(color)
        print(*args , sep = sep , end  = end )
        Printing.__changeColor__(Printing.DefaultColor)
          
    def printSuccess(*args : list  , sep : str = " " , end  : str = "\n" )->None : 
        Printing.__printInColor__(*args ,sep =  sep , end = end , color =Color.GREEN)
        
    def printError(*args : list  , sep : str = " " , end  : str = "\n" )->None : 
        Printing.__printInColor__(*args ,sep =  sep , end = end , color =Color.Red)
        
    def printLog(*args : list  , sep : str = " " , end  : str = "\n" )->None : 
        Printing.__printInColor__(*args ,sep =  sep , end = end , color = Color.BLUE)
        
    def printWarning(*args : list  , sep : str = " " , end  : str = "\n" )->None : 
        Printing.__printInColor__(*args ,sep =  sep , end = end , color = Color.Yellow)
        
    def printNotes(*args : list  , sep : str = " " , end  : str = "\n" )->None : 
        Printing.__printInColor__(*args ,sep =  sep , end = end , color = Color.Purple)
