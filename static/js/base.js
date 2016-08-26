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
    $(".turf-form").on('submit', function(event){
        event.preventDefault();
    });

    $(".btn-turf").click(function(){

        var user_id = $(this).attr("data-user");
        var turf_type = $(this).attr("data-type");
        var turf_count = $("#count-" + user_id).val();

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
                $("#count-" + user_id).val('');
                old_val = parseFloat($("#user-" + user_id + " .sum-" + turf_type).html());
                $("#user-" + user_id + " .sum-" + turf_type).html(old_val + parseFloat(turf_count));
            }
        });
    });

});