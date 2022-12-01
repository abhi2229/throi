function validate(){
    var receiver_mail= document.getElementById("email").value;
    var Name = document.getElementById("Name").value;
    var yes= document.getElementById("myCheck1"); 
    if (yes.checked == true && no.checked == true){  
        return document.getElementById("error").innerHTML = "Please mark only one checkbox either Yes or No";  
      } 



    else {  
        return document.getElementById("error").innerHTML = "*Please mark any of checkbox";  
      } 
    
    }