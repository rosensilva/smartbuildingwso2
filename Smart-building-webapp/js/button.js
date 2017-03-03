/*var number1 = document.getElementById("num1");
var number2 = document.getElementById("num2");
var number3 = document.getElementById("num3");


number2.addEventListener("blur",function(){
	alert("Clicked!");
	number3.innerHTML = parseFloat(number1.value)+parseFloat(number2.value);
});
*/
angular.module('app', ['uiSwitch'])

.controller('MyController', function($scope) {
  $scope.enabled = true;
  $scope.onOff = true;
  $scope.yesNo = true;
  $scope.disabled = true;


  $scope.changeCallback = function() {
    console.log('This is the state of my model ' + $scope.enabled);
    /*alert("Smart Controll is now toggling")*/
  };
});