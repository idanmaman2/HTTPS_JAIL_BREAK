$(document).ready(function () {
    $( "form" ).submit(function( event ) {

        var inputValues = $('input:text').map(function() {
            return [[this.name  ,this.value] ]
        }).get();
      
        inputValues = Object.fromEntries(inputValues)
        alert(JSON.stringify(inputValues))
        fetch('http://127.0.0.1:5000', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: inputValues
          })
          .then(response => alert(response))
          .then(data => alert(data))
          .catch(error => alert(error));
          fetch('https://api.example.com/endpoint')
          .then(response => response.json())
          .then(data => {
            // Do something with the data
            console.log(data);
          })
          .catch(error => {
            // Handle any errors
            console.error(error);
          });


  })});