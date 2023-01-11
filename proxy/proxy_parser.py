"""
    parse poxy html and js pages ... 
"""
import re
import os 
from bs4 import BeautifulSoup , Tag 

def argsParse(args: dict , domaName : str , path : str  )->dict: 
    def parser(value ):
        return value.replace(f"vvvvvv.{domaName}" , f"www.{domaName}").replace("http","https")
    newArgs = args.copy()
    for key,value in newArgs.items() : 
        print(value)
        newArgs[key] = parser(value)
    return newArgs

def parse(page:bytes , domainName :str , path : str  , pageType : str  ): 
    def addXmlHttpReqScript(parent:Tag): 
        script:Tag  = Tag(name="script")
        scriptText = "console.log('working')"
        script.append(scriptText)
        parent.append(script)


    page =  page.replace("http://","http://vvvvvv.")
    page  = page.replace("https://www.","http://vvvvvv.")
    page = page.replace("https://","http://")
    print(pageType)
    if  "text/html" not  in pageType : 
        return page
    # script injection 
    print("injecting...")
    soup = BeautifulSoup(page, "html.parser")
    for fileName in os.listdir("../cy-bugs"):
        if fileName.endswith(".js"):
            scriptInject: Tag = Tag(name="script")
            scriptInject.attrs['src'] = f"/cybugs/{fileName}"
            soup.head.insert(0,scriptInject)
    page =  soup.prettify('latin-1')
    return page 

