$(document).ready(function () {

    $(".article_tab").click(function () {
        $(".active_tab").removeClass("active_tab");
        $(this).addClass("active_tab");
        $(".upcoming_events").slideUp("fast", function () {
            $(".recent_articles").slideDown("slow");
            $(".recent_articles").css("display", "grid");
        });
    });

    $(".event_tab").click(function () {
        $(".active_tab").removeClass("active_tab");
        $(this).addClass("active_tab");
        $(".recent_articles").slideUp("slow", function () {
            $(".upcoming_events").slideDown("slow");
            $(".upcoming_events").css("display", "grid");
        });
    });

});
