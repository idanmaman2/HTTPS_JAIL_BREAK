"""
    parse poxy html and js pages ... 
"""
import re


def argsParse(args: dict , domaName : str , path : str  )->dict: 
    def parser(value ):
        return value.replace(f"vvvvvv.{domaName}" , f"www.{domaName}").replace("http","https")
    newArgs = args.copy()
    for key,value in newArgs.items() : 
        print(value)
        newArgs[key] = parser(value)
    return newArgs

def parse(page , domainName , path  ): 
    page =  page.replace("http://","http://vvvvvv.")
    page  = page.replace("https://www.","http://vvvvvv.")
    page = page.replace("https://","http://")
    page = page.replace("window.location.port",'"80"')
    page = page.replace("document.location.port",'"80"')
    """
        window.location.host
        window.location.protocol 
        
        Problem Problem Problem Problem Problem Problem  Problem Problem Problem  Problem Problem Problem  Problem Problem Problem  
        $('#form-search').on('submit', function() {
            var action = $(this).attr('action');
            var value = $(this).find('.apachesolr-autocomplete').val();
            var lang = $("html").attr("lang");
            if (lang != "he") {
                action = lang + "/" + action;
            }

            var protocol = window.location.protocol;####
            var host = window.location.host; ####
            ### document.location.etc###
            window.location.href = encodeURI(protocol + '//' + host + '/' + action + '/' + value);

            return false;
        });
        Problem Problem Problem  Problem Problem Problem  Problem Problem Problem  Problem Problem Problem  Problem Problem Problem  
    
    
    """
    #page = page.replace("window.location.href" ,f""" "{domainName+path}" """)
    
    #page = page.replace("document.location.href" ,f""" "{domainName+path}" """)
    
    return page 

