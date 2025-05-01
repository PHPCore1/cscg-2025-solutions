function filterinput(e) {
  var chrTyped,
    chrCode = 0,
    evt = e ? e : event;
  if (evt.charCode != null) chrCode = evt.charCode;
  else if (evt.which != null) chrCode = evt.which;
  else if (evt.keyCode != null) chrCode = evt.keyCode;

  if (chrCode == 0) chrTyped = "SPECIAL KEY";
  else chrTyped = String.fromCharCode(chrCode);

  if (chrTyped.match(/[^<>=]/)) return true;
  if (evt.altKey || evt.ctrlKey || chrCode < 28 || chrTyped == "SPECIAL KEY")
    return true;

  if (evt.preventDefault) evt.preventDefault();
  evt.returnValue = false;
  return false;
}

function addEventHandler(elem, eventType, handler) {
  if (elem.addEventListener) elem.addEventListener(eventType, handler, false);
  else if (elem.attachEvent) elem.attachEvent("on" + eventType, handler);
  else return 0;
  return 1;
}

function init() {
  elem = document.getElementById("content");
  if (elem) {
    addEventHandler(elem, "keypress", filterinput);
  }
}

init();
