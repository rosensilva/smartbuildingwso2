/**
 * Copyright (c) 2017, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
 *
 * WSO2 Inc. licenses this file to you under the Apache License,
 * Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations
 * under the License.
 **/

var floor1_obj = document.getElementById("floor1");
var btn = document.getElementById("btn");
var btn2 = document.getElementById("btn2");
var testPyServerBtn = document.getElementById("testPyServerBtn");

function showValue(newValue)
{
    document.getElementById("range").innerHTML="<b>"+newValue+"<b>";
    if (confirm("Do you want to set the temerature to "+newValue+"?") == true) {
        setTemperature(newValue);
    } else {

    }

}


function updateTemperature() {
    var ourRequest = new XMLHttpRequest();
    var timenow = Date.now();

    ourRequest.open('GET', 'https://localhost:9445/analytics/tables/ORG_WSO2_IOT_DEVICES_TEMPRATURE/'+(timenow-60000)+'/'+timenow,true);
    ourRequest.setRequestHeader("Authorization", "Basic YWRtaW46YWRtaW4=");
    //Send the proper header information along with the request
    ourRequest.setRequestHeader("Content-type", "application/json");

    ourRequest.setRequestHeader("Accept", "application/json");
    ourRequest.setRequestHeader("Access-Control-Allow-Origin", "*");
    ourRequest.onreadystatechange = function() {//Call a function when the state changes.
        if(ourRequest.readyState == 4 && ourRequest.status == 200) {

            if(ourRequest.responseText == "[]"){
                alert("Can't load temperature data");
                return;
            }
            else{
                var json_data  = JSON.parse(ourRequest.responseText);
                var temperature = (JSON.stringify(json_data[0]['values']['Temprature']));
                alert("temp :" +temperature);

                document.getElementById('temperatureDisplay').innerHTML =  temperature;
            }

        }
    }

    ourRequest.onerror = function() {
        console.log("Connection error");
    };

    ourRequest.send();

}

function updatePrediction() {

    var ourRequest = new XMLHttpRequest();
    param = 'date=2016-10-10&time=10:00';


    ourRequest.open('GET', 'https://localhost:5000/currentprediction',true);


    //Send the proper header information along with the request
    ourRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    ourRequest.onreadystatechange = function() {//Call a function when the state changes.
        if(ourRequest.readyState == 4 && ourRequest.status == 200) {
          /*  alert(ourRequest.responseText);*/
            document.getElementById("prdtHeadDisplay").innerHTML = ourRequest.responseText;
            /*   this.floor1_obj.innerHTML("ourRequest.responseText");*/
            /*floor1_obj.innerHTML = "Prediction for next half hour  = " +ourRequest.responseText;
             alert("Prediction = "+floor1_obj);*/

        }
    }
    ourRequest.send();
    /*ourRequest.send("param=21");*/
}
function updateCurrentHeadCount() {
    var ourRequest2 = new XMLHttpRequest();
    param2 = 'date=2016-10-10&time=10:00'


    ourRequest2.open('GET', 'https://localhost:5000/currentoccupancy',true);


    //Send the proper header information along with the request
    ourRequest2.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    ourRequest2.onreadystatechange = function() {//Call a function when the state changes.
        if(ourRequest2.readyState == 4 && ourRequest2.status == 200) {
           /* alert(ourRequest2.responseText);*/
            document.getElementById("currHeadDisplay").innerHTML = ourRequest2.responseText;
            /*   this.floor1_obj.innerHTML("ourRequest.responseText");*/
            //floor1_obj.innerHTML = "Prediction for next half hour  = " +ourRequest2.responseText;
            //alert("Prediction = "floor1_obj)

        }
    }
    ourRequest2.send();
    /*ourRequest.send("param=21");*/
}
function setTemperature(data) {

    var ourRequest = new XMLHttpRequest();
    param = 'date=2016-10-10&time=10:00'

    ourRequest.open('POST', 'https://localhost:8243/ac_controller/1.0.0/device/1hr84h98s16ib/change-status?state='+data,true);

    ourRequest.setRequestHeader("Authorization", "Bearer 2941a3ce-2267-35f4-974d-f7fe5fa3e2c4");
    //Send the proper header information along with the request
    ourRequest.setRequestHeader("Content-type", "application/json");

    ourRequest.setRequestHeader("Accept", "application/json");


    ourRequest.onreadystatechange = function() {//Call a function when the state changes.
        if(ourRequest.readyState == 4 && ourRequest.status == 200) {
            alert(ourRequest.responseText);
            /*   this.floor1_obj.innerHTML("ourRequest.responseText");*/
            floor1_obj.innerHTML = "Prediction for next half hour  = " +ourRequest.responseText;
            alert(floor1_obj)

        }
    }
    ourRequest.send();
    /*ourRequest.send("param=21");*/


}

testPyServerBtn.addEventListener("click", function() {
   updateTemperature();

});


testPyServerBtn.addEventListener("click", function() {


    updateCurrentHeadCount();
    updatePrediction();

});


btn.addEventListener("click", function() {
  var ourRequest = new XMLHttpRequest();
  function callOtherDomain() {
  if(invocation) {    
    invocation.open('GET', url, true);
    invocation.onreadystatechange = handler;
    invocation.send(); 
  }
}
  ourRequest.open('GET', 'https://localhost:5000/cat',true);
  ourRequest.onload = function() {
    if (ourRequest.status >= 200 && ourRequest.status < 400) {
      var ourData = JSON.parse(ourRequest.responseText);

    } else {
      console.log("We connected to the server, but it returned an error.");
    }
    
  };

  ourRequest.onerror = function() {
    console.log("Connection error");
  };

  ourRequest.send();

});




btn2.addEventListener("click", function() {

  var ourRequest = new XMLHttpRequest();
  param = 'date=2016-10-10&time=10:00';
  

  ourRequest.open('GET', 'https://localhost:5000/currentprediction',true);
  
	
	//Send the proper header information along with the request
	ourRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

	ourRequest.onreadystatechange = function() {//Call a function when the state changes.
    if(ourRequest.readyState == 4 && ourRequest.status == 200) {
        alert(ourRequest.responseText);
     /*   this.floor1_obj.innerHTML("ourRequest.responseText");*/
        floor1_obj.innerHTML = "Prediction for next half hour  = " +ourRequest.responseText;
        alert(floor1_obj)

    }
	};
  ourRequest.send();
	/*ourRequest.send("param=21");*/

});

window.setInterval(function(){

  alert("Updating from ML server");

  updateCurrentHeadCount();
  updatePrediction();
  updateTemperature();

}, 60*60*600);




