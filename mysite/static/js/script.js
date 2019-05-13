$(document).ready(function() {
  $('[data-toggle="tooltip"]').tooltip();
});


// Instructor Details
function loadAllInstructorDetails() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("InstructorDetails").innerHTML =
      this.responseText;
    }
  };
  xhttp.open("GET", "http://schoolgradebook.pythonanywhere.com/api/instructor", true);
  xhttp.send();
}












