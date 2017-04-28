function update_storage() {
  var xhttp = new XMLHttpRequest()
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      document.getElementById("storage").innerHTML = xhttp.responseText;
    }
  }
  xhttp.open("GET", storage_url, true);
  xhttp.send();
}

function quick_action(req_url) {
  var xhttp = new XMLHttpRequest()
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      update_storage();
    }
  }
  xhttp.open("GET", req_url, true);
  xhttp.send();
}
