// var path2class = {
//   "/articles": ".articles_icon",
//   "/events": ".events_icon",
//   "/submit": ".submit_icon",
//   "/profile": ".profile_icon",
//   "/login": ".profile_icon",
//   "/signup": ".profile_icon"
// }
//
// var elemFromPath = function() {
//     var pathName = window.location.pathname;
//     if(pathName === "/") {
//       return $(".logo_icon");
//     }
//     for(var key in path2class) {
//         if(pathName.indexOf(key) !== -1) {
//             return $(path2class[key])
//         }
//     }
//     return $(".logo_icon");
// }
//
// $(document).ready(function() {
//     var element = elemFromPath().parent();
//     console.log(element);
//     $(".active_icon").removeClass("active_icon");
//     element.addClass("active_icon");
// });
//
