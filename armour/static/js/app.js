// Alerts

function addAlert(type, header, message) {
    var alert = '<div class="alert alert-' + type + '">' +
    '<h4 class="alert-heading">' + header + '</h4>' +
    '<p>' + message + '</p>' +
    '</div>';

    $(alert).appendTo('.alerts').delay(2000).slideUp(500).queue(function() {
        $(this).remove();
    });
}

function handlePasswordField() {
    $(".password-group").on('click', '.input-group-text', function() {
        $input = $(this).siblings("input");
        $icon = $(this);
        console.log('click');
        if ($input.attr("type") == "text") {
            $input.attr('type', 'password');
            $icon.addClass("show");
        } else if($input.attr("type") == "password") {
            $input.attr('type', 'text');
            $icon.removeClass("show");
        }
    });
}

function setProgress(val, $pbar) {
    $pbar.children('.progress-bar').css('width', val + '%').attr('aria-valuenow', val);
}

$(document).ready(function() {
    $(".sidebar-toggle").on('click', function() {
        $("body").toggleClass('sidebar-open');
    });
    handlePasswordField();
});
