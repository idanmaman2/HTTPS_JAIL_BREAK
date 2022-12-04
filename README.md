# HTTPS_JAIL_BREAK
# Escape from the HTTPS jail and go to freedom(HTTP) 
# the plan : 
  -1 . open evil twin access point ;-)
  1. get MITM between the victim and the gateway(and if the dns server is on ower network and so posion him too ) .
  2. steal appropriate dns qeueries and ask from (8.8.8.8 ) for the domain and posion the answer to be our flask server 
  3. the flask server will return HTTP 307 error code `307 Temporary Redirect` and in the Location header change a bit to unicode chars that look                 like the alpahbet the uri for example 'a' -> `ą` 
  4. do ssl strip with him - be proxy 
  5. plan in the answers BeEF like tool that we will make that we  will help us to get extra data and steal other stuff 
  6. auto recognize of form post data (high probabilty to be password or other useful data ) and save it in log file 
  7. the flask website will provide control panael as well for the admins that will be able to watch the page and control in all the victimis 
 
 * in the future we will maybe  create ower own singed ssl key so other thief will not steal our data 
  --- problems with exploit only on first time hsts websites  with sslstriping only --- : 
    Hsts prload : only big companies has it 
    
    our answer : 
      <img width="399" alt="image" src="https://user-images.githubusercontent.com/90776557/205504601-40678b5b-b20d-49cb-81d7-c9e5c1ac8362.png">

  
  protection : 
    
    never trust http or pself singed ssl signtures 
