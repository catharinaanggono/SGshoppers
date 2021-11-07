var PRODUCTION = false;
var HOST = '';
var USER_HOST = '';
var ORDER_HOST = '';
var PRODUCT_HOST = '';
var REWARD_HOST = '';

if (PRODUCTION) {
  HOST = "https://ui4we1cjuj.execute-api.us-east-1.amazonaws.com";
  USER_HOST = HOST;
  ORDER_HOST = HOST;
  PRODUCT_HOST = HOST;
  REWARD_HOST = HOST;
}

else{
  HOST = "http://localhost";
  USER_HOST = HOST + ":5000";
  ORDER_HOST = HOST + ":5003";
  PRODUCT_HOST = HOST + ":5001";
  REWARD_HOST = HOST + ":5002";
}

// Function to create the cookie
function createCookie(name, value, days) {
  var expires;

  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = "; expires=" + date.toGMTString();
  } else {
    expires = "";
  }

  document.cookie = escape(name) + "=" + escape(value) + expires + "; path=/";
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(";");

  for (let c of ca) {
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function deleteCookie(name) {
  if (getCookie(name)) {
    document.cookie =
      name +
      "=;expires=Thu, 01 Jan 1970 00:00:01 GMT" +
      ("/" ? "; path=" + "/" : "");
  }
}

function listCookies() {
  var theCookies = document.cookie.split(";");
  var aString = "";
  for (var i = 1; i <= theCookies.length; i++) {
    aString += i + " " + theCookies[i - 1] + "\n";
  }
  return aString;
}

function getURL() {
  alert("The URL of this page is: " + window.location.href);
}

function deleteAllCookies() {
  var allCookies = document.cookie.split(";");

  for (let c of allCookies) {
    document.cookie =
      c +
      "=;expires=Thu, 01 Jan 1970 00:00:01 GMT" +
      ("/" ? "; path=" + "/" : "");
  }
}
