"""
    parse poxy html and js pages ... 
"""
import re
def parse(page , domainName ): 
    page = re.sub('src="\/(.*?)"',lambda match : f'src="/{domainName}@/{match.group(1)}"',page)
    page = re.sub('href="\/(.*?)"',lambda match : f'href="/{domainName}@/{match.group(1)}"',page)
    page = re.sub('action="\/(.*?)"',lambda match : f'action="/{domainName}@/{match.group(1)}"',page)
    page = re.sub("([^\/])https",lambda match :  f"{match.group(1)}/https",page )
    page = re.sub('url\(\/(.*?)\)',lambda match : f'url(/{domainName}@/{match.group(1)})',page)
    return page 

