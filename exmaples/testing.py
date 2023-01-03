
"""
Example for Raw HTTP : 
    b'HTTP/1.1 200 OK\r\n
    Date: Wed, 28 Dec 2022 21:08:24 GMT\r\n
    Server: Apache\r\nLast-Modified: Fri, 17 Sep 2021 19:26:14 GMT\r\n
    Accept-Ranges: bytes\r\n
    Vary: Accept-Encoding,User-Agent\r\n
    Content-Encoding: gzip\r\n
    Content-Length: 12038\r\n
    Keep-Alive: timeout=15, max=95\r\n
    Connection: Keep-Alive\r\nContent-Type: text/html\r\n
    Set-Cookie: BIGipServer~CUIT~www.columbia.edu-80-pool=1764244352.20480.0000; expires=Thu, 29-Dec-2022 03:08:24 GMT; path=/; Httponly\r\n\r\n'

"""






ht = HTTP.FromRawPack(b'HTTP/1.1 200 OK\r\nDate: Wed, 28 Dec 2022 21:08:24 GMT\r\nServer: Apache\r\nLast-Modified: Fri, 17 Sep 2021 19:26:14 GMT\r\nAccept-Ranges: bytes\r\nVary: Accept-Encoding,User-Agent\r\nContent-Encoding: gzip\r\nContent-Length: 12038\r\nKeep-Alive: timeout=15, max=95\r\nConnection: Keep-Alive\r\nContent-Type: text/html\r\nSet-Cookie: BIGipServer~CUIT~www.columbia.edu-80-pool=1764244352.20480.0000; expires=Thu, 29-Dec-2022 03:08:24 GMT; path=/; Httponly\r\n\r\nhelllo ')
print(ht)