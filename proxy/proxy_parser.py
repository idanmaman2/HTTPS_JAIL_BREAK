"""
    parse poxy html and js pages ... 
"""
import re
def parse(page , domainName , path  ): 
    page  = page.replace("https://www.","http://vvvvvv.")
    page = page.replace("https://","http://")
    page = page.replace("window.location.href" ,f""" "{domainName+path}" """)
    page = page.replace("document.location.href" ,f""" "{domainName+path}" """)
    return page 

