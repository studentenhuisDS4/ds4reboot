$(document).ready(function(){

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    update_medals();

    function update_medals() {
        return $.ajax({
            url: "/bierlijst/medals/",
            type: "GET",
            dataType: "json",
            context: this,
            error: function (json) {
                console.log(json);
            },
            success : function (json) {
                var medals = json.medals;
                $(".medal").removeClass("gold");
                $(".medal").removeClass("silver");
                $(".medal").removeClass("bronze");
                $("#user-" + medals.gold + " .medal").addClass("gold");
                $("#user-" + medals.silver + " .medal").addClass("silver");
                $("#user-" + medals.bronze + " .medal").addClass("bronze");

            }
        });
    }

    // Prevent default form submit behavior
    $(".turf-form,.profile-form").on('submit', function(event){
        event.preventDefault();
    });

    // Set onclicks for turf buttons
    $(".btn-turf").click(function(){

        var user_id = $(this).attr("data-user");
        var turf_type = $(this).attr("data-type");
        var turf_count = $(".count-" + user_id).val();

        if (turf_count === ''){
            turf_count = 1;
        }

        $.ajax({
            url: "/bierlijst/turf/" + user_id + "/",
            type: "POST",
            data: {count: turf_count, turf_type: turf_type},
            dataType: "json",
            context: this,
            error: function (json) {
                console.log(json);
            },
            success : function (json) {
                if (json.status =='success') {
                    UIkit.notify("<i class='uk-icon-check'></i> " + json.result, {status:'success'});
                    $(".count-" + user_id).val('');

                    // Update user value
                    var sum_el = $("#user-" + user_id + " .sum-" + turf_type + " span:first");
                    sum_el.fadeOut(100, function () {
                        old_val = parseFloat(sum_el.html());
                        sum_el.html(old_val + parseFloat(turf_count));
                    });
                    sum_el.fadeIn(100);

                    // Update total value
                    var total_el = $("#total-" + turf_type + " span");
                    total_el.fadeOut(100, function () {
                        old_val = parseFloat(total_el.html());
                        total_el.html(old_val + parseFloat(turf_count));
                    });
                    total_el.fadeIn(100);

                    // Update wine totals
                    if (turf_type == 'wwijn' || turf_type == 'rwijn') {
                        var sum_wijn_el = $("#user-" + user_id + " .sum-wijn span:first");
                        sum_wijn_el.fadeOut(100, function () {
                            old_val = parseFloat(sum_wijn_el.html());
                            sum_wijn_el.html(old_val + parseFloat(turf_count));
                        });
                        sum_wijn_el.fadeIn(100);
                        var total_wijn_el = $("#total-wijn span");
                        total_wijn_el.fadeOut(100, function () {
                            old_val = parseFloat(total_wijn_el.html());
                            total_wijn_el.html(old_val + parseFloat(turf_count));
                        });
                        total_wijn_el.fadeIn(100);

                        // Warn if partial wine bottle
                        if (parseFloat(total_wijn_el.html()) % 1 != 0) {
                            UIkit.notify("<i class='uk-icon-warning'></i> Er is geen hele fles wijn geturfd!", {status:'warning'});
                        }
                    } else {
                        update_medals();
                    }
                } else {
                    $(".count-" + user_id).val('');
                    UIkit.notify("<i class='uk-icon-remove'></i> " + json.result, {status:'danger'});
                }
            }
        });
    });

});