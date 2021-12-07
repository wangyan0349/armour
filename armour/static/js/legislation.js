var ActionFormSuccess = function showResponse(responseText, statusText, xhr, $form)  {
    $("#action-close").click();
    $("#actionModalContent").empty();
    var row = "#row-"+responseText.pk;
    $(row).remove();
}

var ActionFormError = function showResponse(responseText, statusText, xhr, $form)  {
    $("#actionModalContent").empty();
    $("#actionModalContent").html(responseText.responseJSON.content);
    $('#action-form').ajaxForm({success:ActionFormSuccess,error:ActionFormError});
}

function loadDeleteForm(item)
{
$.ajax({type: 'GET', url: urls.objdelete.replace("0",item)})
        .done(function (data) {
           $("#actionModalContent").empty();
           $("#actionModalContent").html(data.content);
           $('#action-form').ajaxForm({success:ActionFormSuccess,error:ActionFormError});
        })
        .fail(function (data) {
            console.log(data.response.error);
        });
}

function handleUpdate() {
    var qTotal = 0;
    var qDone = 0;
    var qYes = false;
    $('#updateModal').find('.question-wrapper').each(function() {
        qTotal += 1;
        if ($(this).find('.form-radio-input:checked').length > 0) {
            qDone += 1;
            if ($(this).find('.form-radio-input:checked').siblings('label').text() == 'Yes') {
                qYes = true;
            }
        }
    });
    if (qDone == qTotal) {
        if (qYes == true) {
            $('#update-apply-1').removeClass('d-none');
            $('#update-apply-0').addClass('d-none');
        } else {
            $('#update-apply-0').removeClass('d-none');
            $('#update-apply-1').addClass('d-none');
        }
    }
}

$(document).ready(function() {
    handleUpdate();
});
