
import re 
DNS_SETTINGS_FILE ="/etc/resolv.conf"
VALID_PATTERN = r"^nameserver (([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"

def get_dns_local_server(): 
    ''' gets the dns server of the machine - works only on unix based machine '''
    with open(DNS_SETTINGS_FILE,'r') as file : 
        for line in file.readlines(): 
            if re.match(VALID_PATTERN,line.strip("\n ")): 
                return line[len("nameserver "):].strip("\n ")
        
    return None 
            
