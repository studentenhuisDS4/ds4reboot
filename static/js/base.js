$(document).ready(function () {

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
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    if (window.location.pathname === "/bierlijst/" || window.location.pathname === "/") {
        update_medals();
    }

    function update_medals() {
        return $.ajax({
            url: "/bierlijst/medals/",
            type: "GET",
            dataType: "json",
            context: this,
            error: function (json) {
                console.log(json);
            },
            success: function (json) {
                var medals = json.medals;
                $(".medal").removeClass("gold")
                    .removeClass("silver")
                    .removeClass("bronze");
                $(".user-" + medals.gold + " .medal").addClass("gold");
                $(".user-" + medals.silver + " .medal").addClass("silver");
                $(".user-" + medals.bronze + " .medal").addClass("bronze");

                $(".medal-quick").removeClass("gold-icon")
                    .removeClass("silver-icon")
                    .removeClass("bronze-icon");
                // Also make medals work on quick access, inefficient for now
                // console.log($(".user-" + medals.bronze + " .medal-quick"));
                $(".user-" + medals.gold + " .medal-quick").addClass("gold-icon");
                $(".user-" + medals.silver + " .medal-quick").addClass("silver-icon");
                $(".user-" + medals.bronze + " .medal-quick").addClass("bronze-icon");

            }
        });
    }

    // Prevent default form submit behavior
    $(".turf-form,.profile-form,.signup-form").on('submit', function (event) {
        event.preventDefault();
    });

    var currAudio = new Audio;
    var last_file = 0;

    // Set onclicks for turf buttons
    $(".btn-turf").click(function (event) {
        var user_id = $(this).attr("data-user");
        var turf_type = $(this).attr("data-type");
        var audio_url = $(this).data("audio-src");
        var turf_count = $(".count-" + user_id).val();

        if (turf_count === '') {
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
            success: function (json) {
                if (json.status === 'success') {
                    UIkit.notify("<i class='uk-icon-check'></i> " + json.result, {status: 'success'});

                    // Update user beer & total value
                    var sum_el = $(".user-" + user_id + " .sum-" + turf_type + " span");
                    var total_el = $("#total-" + turf_type + " span");
                    fadeUpdateLabel(sum_el, json.new_value);
                    fadeUpdateLabel(total_el, json.new_value_total);
                    $(".count-" + user_id).val('');

                    // Update wine totals (medium view class only views sum)
                    if (turf_type === 'wwijn' || turf_type === 'rwijn') {
                        var sum_wijn_el = $(".user-" + user_id + " .sum-wijn span");
                        fadeUpdateLabel(sum_wijn_el, sum_wijn_el.html() + turf_count);

                        var total_wijn_el = $("#total-wijn span");
                        fadeUpdateLabel(total_wijn_el, total_wijn_el.html() + turf_count);

                        // Check if whole wine turfed (should be warned about)
                        if (json.new_value_total % 1.0 !== 0.0) {
                            if (turf_type === 'rwijn') {
                                UIkit.notify("<i class='uk-icon-warning'></i> Er is geen hele fles rode wijn geturfd!", {status: 'warning'});
                            }
                            else if (turf_type === 'wwijn') {
                                UIkit.notify("<i class='uk-icon-warning'></i> Er is geen hele fles witte wijn geturfd!", {status: 'warning'});
                            }
                        }
                        else if (total_val_both % 1.0 !== 0.0) {
                            if (turf_type === 'rwijn') {
                                UIkit.notify("<i class='uk-icon-warning'></i> Er is geen hele fles witte wijn geturfd!", {status: 'warning'});
                            }
                            else if (turf_type === 'wwijn') {
                                UIkit.notify("<i class='uk-icon-warning'></i> Er is geen hele fles rode wijn geturfd!", {status: 'warning'});
                            }
                        }
                    } else {
                        playSound(audio_url);
                        update_medals();
                    }
                } else {
                    $(".count-" + user_id).val('');
                    UIkit.notify("<i class='uk-icon-remove'></i> " + json.result, {status: 'danger'});
                }
            }
        });

        var fadeUpdateLabel = function (selector, new_value) {
            selector.fadeOut(100, function () {
                selector.html(parseFloat(new_value));
            });
            selector.fadeIn(100);
        };

        var playSound = function (url) {
            if (currAudio && currAudio.currentTime !== 0) {
                var fadeOut = setInterval(function () {
                    currAudio.volume = currAudio.volume -= 0.33;
                    if (currAudio.volume < 0.2) {
                        clearInterval(fadeOut);
                        defaultAudio(currAudio, url);
                    }
                }, 100);
            }
            else {
                defaultAudio(currAudio, url);
            }
        };

        var defaultAudio = function(audio, url) {
            url_ext = Math.floor((Math.random() * 13 * 5) + 1);
            console.log(url_ext);
            while (url_ext === last_file) {
                url_ext = Math.floor((Math.random() * 13*5) + 1);
            }

            currAudio.volume = 0.5;
            if (url_ext <= 13) {
                last_file = url_ext;

                currAudio.src = url + url_ext.toString() + ".mp3";
                currAudio.play();
            }
        }
    });

    // Set onclicks for signup buttons
    $(".btn-signup").click(function () {

        var user_id = $(this).attr("data-user");
        var enroll_type = $(this).attr("data-type");
        var enroll_date = $(this).attr("data-date");

        $.ajax({
            url: "/eetlijst/enroll/",
            type: "POST",
            data: {user_id: user_id, enroll_type: enroll_type, enroll_date: enroll_date},
            dataType: "json",
            context: this,
            error: function (json) {
                console.log(json);
            },
            success: function (json) {
                if (json.status == 'success') {
                    UIkit.notify("<i class='uk-icon-check'></i> " + json.result, {status: 'success'});

                    // Update total value
                    var total_el = $('.total-date-' + enroll_date);
                    total_el.fadeOut(100, function () {
                        total_el.html(parseInt(json.total_amount));
                    });
                    total_el.fadeIn(100);

                    row_id = ".user-" + user_id + " .date-" + enroll_date;

                    // Update user-date value
                    if (enroll_type == 'signup') {
                        // Need to update cook span as well
                        var enroll_el = $(row_id + " .td-enroll");
                        enroll_el.removeClass('eetlijst-item-hidden');
                        enroll_el.fadeIn(100);

                        if (json.enroll_amount > 1) {
                            var count_el = $(row_id + " .td-count");
                            count_el.fadeOut(100, function () {
                                count_el.html(parseInt(json.enroll_amount));
                            });
                            count_el.fadeIn(100);
                        }
                    }
                    else if (enroll_type == 'cook') {
                        // Need to update cook span as well
                        var cook_el = $(row_id + " .td-cook");
                        if (json.enroll_amount == 1) {
                            cook_el.fadeIn(100);
                            $(".btn-signup.btn-cook:not([disabled])").attr('disabled', true);
                            $(this).attr('disabled', false);
                            // If user is cook add shopping cart
                            if (json.login_user == user_id) {
                                $(".closing-button").fadeIn(100);
                            }
                            else {
                                $(".closing-button").fadeOut(100);
                            }
                        }
                        else {
                            cook_el.fadeOut(100);
                            $(".btn-signup:disabled").attr('disabled', false);
                            $(".closing-button").fadeOut(100);
                        }
                    }
                    else if (enroll_type == 'sponge') {
                        // Need to update cross and number span as well
                        var unroll_el = $(row_id + " .td-enroll");
                        unroll_el.fadeOut(100);
                        var count_el = $(row_id + " .td-count");
                        count_el.fadeOut(100);
                        unroll_el.addClass('eetlijst-item-hidden');
                        count_el.addClass('eetlijst-item-hidden');
                    }
                } else {
                    $(".count-" + user_id).val('');
                    UIkit.notify("<i class='uk-icon-remove'></i> " + json.result, {status: 'danger'});
                }
            }
        });
    });

    // Set onclicks for signup buttons
    $(".btn-signup-home").click(function () {

        var user_id = $(this).attr("data-user");
        var enroll_type = $(this).attr("data-type");
        var enroll_date = $(this).attr("data-date");

        $.ajax({
            url: "/eetlijst/enroll/",
            type: "POST",
            data: {user_id: user_id, enroll_type: enroll_type, enroll_date: enroll_date},
            dataType: "json",
            context: this,
            error: function (json) {
                console.log(json);
            },
            success: function (json) {
                if (json.status == 'success') {
                    UIkit.notify("<i class='uk-icon-check'></i> " + json.result, {status: 'success'});

                    // Update total value
                    var total_el = $('.eating-number');
                    total_el.fadeOut(100, function () {
                        total_el.html(parseInt(json.total_amount));
                    });
                    total_el.fadeIn(100);

                    // Update signup/unenroll
                    var span_sign_text = $('.home-quick-signup');
                    var but_signup = $('.btn-signup-home');
                    var icon_signup = $('.signup-icon');
                    var but_colored = $('.but_colored');            // The buttons which the color needs to be toggled
                    if (enroll_type == 'signup') {
                        span_sign_text.fadeOut(100, function () {
                            span_sign_text.html(' Uitschrijven');
                        });
                        span_sign_text.fadeIn(100);
                        // Update signup type
                        but_signup.attr('data-type', 'sponge');
                        // Update row color
                        but_colored.removeClass('uk-button-success');
                        but_colored.addClass('uk-button-danger');
                        icon_signup.removeClass('uk-icon-plus-circle');
                        icon_signup.addClass('uk-icon-minus-circle');
                    }
                    else if (enroll_type == 'sponge') {
                        span_sign_text.fadeOut(100, function () {
                            span_sign_text.html(' Mee eten');
                        });
                        span_sign_text.fadeIn(100);
                        // Update signup type
                        but_signup.attr('data-type', 'signup');
                        // Update row color
                        but_colored.removeClass('uk-button-danger');
                        but_colored.addClass('uk-button-success');
                        icon_signup.removeClass('uk-icon-minus-circle');
                        icon_signup.addClass('uk-icon-plus-circle');
                    }
                } else {
                    $(".count-" + user_id).val('');
                    UIkit.notify("<i class='uk-icon-remove'></i> " + json.result, {status: 'danger'});
                }
            }
        });
    });

    // Submit form on datepicker change event
    // Prevent event-trigger + page-reload loop by disabling default events
    $('#eetlijst-datepick').on('change', function (event) {
        event.preventDefault();
        $('#eetlijst-dateform').submit();
    });
});