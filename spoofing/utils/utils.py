

from scapy.all import Ether,IP,UDP,TCP

def udpCopy(packet , sourceMac  , dstMac ):
    et = Ether(src =sourceMac , dst =  dstMac )
    ip =  IP(src=packet[IP].src,dst=packet[IP].dst)
    udp = UDP(dport=packet[UDP].dport,sport=packet[UDP].sport)
    return et/ip/udp 

def tcpCopy(packet , sourceMac  , dstMac ) : 
    et = Ether(src =sourceMac , dst =  dstMac )
    ip =  IP(src=packet[IP].src,dst=packet[IP].dst)
    tcp = TCP(dport=packet[TCP].dport,sport=packet[TCP].sport,seq=packet[TCP].seq , ack =packet[TCP].ack , flags = packet[TCP].flags )
    return  et/ip/tcp