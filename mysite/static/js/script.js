// Instructor Details
function loadAllInstructorDetails() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById("InstructorDetails").innerHTML = this.responseText;
        //var result = JSON.parse(this.responseText);
        //displayInstructorDetails(this.responseText);
    }
  };
  xhttp.open("GET", "http://schoolgradebook.pythonanywhere.com/api/instructor", true);
  xhttp.send();
}




function displayInstructorDetails(arr) {
  var out = "";
  var i;
  for(i = 0; i < arr.length; i++) {
    out += '<a href="' + arr[i].url + '">' +
    arr[i].display + '</a><br>';
  }
  document.getElementById("InstructorDetails").innerHTML = out;
}

