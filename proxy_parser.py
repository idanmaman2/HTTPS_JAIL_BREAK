"""
    parse poxy html and js pages ... 
"""
import re
def parse(page , domainName ): 
    page  = page.replace("https://www.","http://vvvvvv.")
    page = page.replace("https://","http://")

    return page 

