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
            context: this,
            error: function (json) {
                console.log(json);
            },
            success : function (json) {
                $(".count-" + user_id).val('');
                var sum_el = $("#user-" + user_id + " .sum-" + turf_type + " span:first");
                sum_el.fadeOut(100, function () {
                    old_val = parseFloat(sum_el.html());
                    sum_el.html(old_val + parseFloat(turf_count));
                });
                sum_el.fadeIn(100);
            }
        });
    });



});