const xhr = new XMLHttpRequest();
xhr.open("POST", "/application/1", true);

// Send the proper header information along with the request
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

xhr.onreadystatechange = () => {
  // Call a function when the state changes.
  if (xhr.readyState === XMLHttpRequest.DONE) {
    // Request finished. Do processing here.
    console.log(xhr.status);
  }
};
xhr.send("action=Accept");