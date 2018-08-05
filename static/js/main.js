$(document).ready(function () {

    $(".expand_nav").click(function () {
        $(".sidenav").css("width", "80px");
        $(".container").css("margin-left", "80px");
    });

    $(".close_nav").click(function () {
        $(".sidenav").css("width", "0px");
        $(".container").css("margin-left", "0px");
    });


});
