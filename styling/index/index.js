$(document).ready(function () {

    $(".article_tab").click(function () {
        $(".active_tab").removeClass("active_tab");
        $(this).addClass("active_tab");
        $(".upcoming_events").fadeOut("fast", function () {
            $(".recent_articles").fadeIn("slow");
            $(".recent_articles").css("display", "grid");
        });
    });

    $(".event_tab").click(function () {
        $(".active_tab").removeClass("active_tab");
        $(this).addClass("active_tab");
        $(".recent_articles").fadeOut("slow", function () {
            $(".upcoming_events").fadeIn("slow");
            $(".upcoming_events").css("display", "grid");
        });
    });

});
