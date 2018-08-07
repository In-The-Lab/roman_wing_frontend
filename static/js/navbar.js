var path2class = {
  "/articles": ".articles_icon",
  "/events": ".events_icon",
  "/submit": ".submit_icon",
  "/profile": "profile_icon"
}

var elemFromPath = function() {
    var pathName = window.location.pathname;
    if(pathName === "/") {
      return $(".logo_icon");
    }
    for(var key in path2class) {
        if(pathName.indexOf(key) !== -1) {
            return $(key)
        }
    }
}

$(document).ready(function() {
    var element = elemFromPath();
    console.log(element);
    $(".active_icon").removeClass("active_icon");
    element.addClass("active_icon");
});
