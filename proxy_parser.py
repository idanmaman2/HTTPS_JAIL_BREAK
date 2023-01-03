"""
    parse poxy html and js pages ... 
"""
import re
def parse(page , domainName ): 
    page = re.sub("https://",lambda match :  f"http://",page ) 
    return page 

