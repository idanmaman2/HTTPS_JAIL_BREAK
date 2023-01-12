//⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️


// created by Idan Maman © 
// Script for overriding the xmlhttprequest function which heavly used in ajax to create http requests (get,post,delete,patch,put,etc...)
// Got help from https://github.com/joshdick/miniProxy/blob/65cbed2907d16f0f25ecdabb420b44c83a36df08/miniProxy.php#L508


// original function that we want to override 
var originalXmlHttpReq = window.XMLHttpRequest.prototype.open ; 
 
// 😈 hooking 😈
//window.XMLHttpRequest.prototype.open = function (){
  //  console.log(`hooked - XMLHttpRequest :  ${arguments}`)
//}


//⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️
