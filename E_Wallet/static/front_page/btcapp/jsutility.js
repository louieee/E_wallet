   
   
   function setModalData(modalBody,parameters,type){
   var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
            if (this.readyState === 4) {
      switch(this.status){
          case 200:{
         
   console.log(type+"Result is=="+this.responseText);
   var response = this.responseText;
  
   document.getElementById(modalBody).innerHTML=response;
     
          }
          break;
      case 503:{
  location.reload();          
      }
      break;
      default:{
location.reload();          
      }
      }
  }

  
  };
  xhttp.open("GET", "ajax.php?action=getModalData&type="+type+"&"+parameters, true);
  xhttp.send();
  
  
}

function setSelectOptions(selectID,params){
  
   var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
   console.log("Result is=="+this.responseText);
   var response = this.responseText;
   
   if(response.indexOf("<option value")!== -1){
   
   document.getElementById(selectID).innerHTML =response;   
   }

    }
    
  };
  xhttp.open("GET", "ajax.php?action=updateSelect&param="+params, true);
  xhttp.send();

     }


        function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}




function copyText(elementID) {
  var range, selection, worked;
var element = document.getElementById(elementID);
  if (document.body.createTextRange) {
    range = document.body.createTextRange();
    range.moveToElementText(element);
    range.select();
  } else if (window.getSelection) {
    selection = window.getSelection();        
    range = document.createRange();
    range.selectNodeContents(element);
    selection.removeAllRanges();
    selection.addRange(range);
  }
  
  try {
    document.execCommand('copy');
    alert('Copied!!');
  }
  catch (err) {
    alert('unable to copy text');
  }
}




function getCountDown(timerEl,timestamp){
// Set the date we're counting down to
var countDownDate = timestamp;

// Update the count down every 1 second
var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();
    
  // Find the distance between now and the count down date
  var distance = countDownDate - now;
    
  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
  var miliseconds = Math.floor((distance % (1000 * 60)/100));
    
  // Output the result in an element with id="demo"
  document.getElementById(timerEl).innerHTML = hours + " : "
  + minutes + " : " + seconds;
    
  // If the count down is over, write some text 
  if (distance < 0) {
    clearInterval(x);
    document.getElementById(timerEl).innerHTML = "EXPIRED";
    //location.reload();
  }
}, 100);

}


   function ajaxGetCall(url,callBackFunction){
   var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
   callBackFunction(this.responseText);
    }
  
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}

   function ajaxPostCall(url,param,callBackFunction){
   var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
   callBackFunction(this.responseText);
    }
  
  };
  xhttp.open("POST", url, true);
  xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhttp.send(param);
}

function loadLink(link){
location.replace(link);
}

