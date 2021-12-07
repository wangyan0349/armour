function selectResponse(keypoint) {
    var postdata = {};
    var tab = $('#curr-tab').val();
    var reply = '';
    var ncdesc = '';

    $.each($("input[name='repl-" + keypoint + "']:checked"), function () {
        reply = $(this).val();
    });

    if (reply === '0') {
        $('#nc-' + keypoint).show();
        ncdesc = $('#nc-' + keypoint).val();
    } else {
        $('#nc-' + keypoint).hide();
        $('#nc-' + keypoint).val('');
    }

    postdata['keypoint'] = keypoint;
    postdata['keypointnote'] = $('#note-' + keypoint).val();

    postdata['ncdesc'] = ncdesc;
    postdata['reply'] = reply;
    postdata['topic'] = $('#id_topic').val();
    postdata['location'] = $('#id_location').val();
    postdata['position'] = tab;

    $.ajax({
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        url: urls.dataset,
        data: JSON.stringify(postdata),

        success: function (data) {
            setProgress(data.prdprogress, $('#progress-product'));
            setProgress(data.allprogress, $('#progress-overall'));
            handleNav();
        },

        error: function (data) {
        }
    });

}

function refreshData() {
    var location = $('#id_location').val();
    var topic = $('#id_topic').val();

    $.ajax({
        type: 'GET',
        url: urls.datacontent,
        data: {
            location: location,
            topic: topic,
        },
    })
        .done(function (data) {
            $("#leg-content").empty();
            $("#leg-content").html(data.content);
            $(".ltopics").hide();
            $("#tab-1").show();
            $('.curr-tab').val(1);
            setProgress(data.prdprogress, $('#progress-product'));
            setProgress(data.allprogress, $('#progress-overall'));
            $(".lg-counter").text("/ " + data.counter)
            setTimeout(function () {
                handleNav();
            }, 1);
        })
        .fail(function (data) {

        });
}

function nextView() {
    var tab = $('.curr-tab').val();
    var next = parseInt(tab) + 1;
    setView(next);
}

function prevView() {
    var tab = $('.curr-tab').val();
    var next = parseInt(tab) - 1;
    setView(next);
}

function setView(next) {

    if ($(next).is('#curr-tab')) {
        next = $('.curr-tab').val();
    }

    if (next < 1 || $("#tab-" + next).length == 0) {
        return false;
    } else {
        $(".ltopics").hide();
        $("#tab-" + next).show();
        $('.curr-tab').val(next);
        $(window).scrollTop(0);
        handleNav();
    }
}

function selectQuestion(question, reply) {
    var postdata = {};
    postdata['question'] = question;
    postdata['reply'] = reply;

    $.ajax({
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        url: urls.setquestion,
        data: JSON.stringify(postdata),
        /*
        beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    },
    */
        success: function (data) {
        },

        error: function (data) {
        }
    });
}

function handleErrors() {
    $('.keyp-wrapper').each(function () {
        var $row = $(this);
        var index = $row.index();
        if ($(this).find('.form-radio-input:checked').length == 0) {
            $row.addClass('error');
            $row.find('.form-radio-input').on('change', function () {
                $row.removeClass('error');
            });
        }
        $('.page-nav').find('.btn-nav').each(function () {
            if ($(this).hasClass('open')) {
                $(this).removeClass('open').addClass('error');
            }
        });
    });
}

function handleNav() {
    var tab = $('.curr-tab').val();
    var index = 0;
    $('.page-nav').empty();
    $('#tab-' + tab).find('.keyp-wrapper').each(function () {
        var $row = $(this);
        var status;
        index += 1;
        // check status
        if ($row.find('.form-radio-input:checked').length == 0) {
            if ($row.hasClass('error')) {
                status = 'error';
            } else {
                status = 'open';
            }
        } else {
            status = 'completed';
        }
        // handle button creation
        var btn = "<button class='btn-nav " + status + "' data-index='" + index + "'></button>";
        $('.page-nav').append(btn);
        // handle complete
        $row.find('.form-radio-input').on('change', function () {
            $('.btn-nav[data-index=' + index + ']').removeClass('error').removeClass('open').addClass('completed');
        });
    });
    // handle scrollTo
    $('.btn-nav').on('click', function () {
        var index = $(this).attr('data-index')
        var $scrollTo = $('#tab-' + tab).find(".keyp-wrapper:nth-of-type(" + index + ")");
        $('html, body').animate({
            scrollTop: $scrollTo.offset().top - 110 - 66
        }, 300);
    })
}

$(document).ready(function () {
    refreshData();
    // handle nav affix
    $(window).scroll(function () {
        var $nav = $('#page-nav-wrapper');
        var scroll = $(window).scrollTop();
        if (scroll >= 284) {
            $nav.addClass('fixed');
        } else {
            $nav.removeClass('fixed');
        }
    });
});
