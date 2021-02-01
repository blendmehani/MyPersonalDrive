//FUNCTION OF THE MODAL WHICH WILL BE USED IN AJAX TO SHOW THE MODAL
function modal(title, message, is_success, extra) {
    $("#title_modal").html(title)
    $("#body_modal").html(message)
    if (is_success === true) {
        $("#body_modal").removeClass()
        $('#body_modal').addClass('alert-success p-3 rounded')
        $("#button_modal").removeClass()
        $('#button_modal').addClass('col-md-12 btn btn-outline-success')
        $("#icon_modal").removeClass()
        $('#icon_modal').addClass('far fa-thumbs-up')

        if (extra !== undefined) {
            document.getElementById('shared_files').style.display = 'block'
        }
        else {
            document.getElementById('shared_files').style.display = 'none'
        }

    } else {
        $("#body_modal").removeClass()
        $('#body_modal').addClass('alert-danger p-3 rounded')
        $("#button_modal").removeClass()
        $('#button_modal').addClass('col-md-12 btn btn-outline-danger')
        $("#icon_modal").removeClass()
        $('#icon_modal').addClass('far fa-thumbs-down')
        document.getElementById('shared_files').style.display = 'none'
    }
    $("#directory_modal").modal('show');
}


// AJAX CREATE DIRECTORY
$(document).on('submit', '#create_directory', function (e) {
    e.preventDefault()
    $.ajax({
        type: 'POST',
        url: $('#create_directory').data('url'),
        data: {
            dir_name: $('#inputDirName').val(),
            url: window.location.href,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {

            modal(response.title, response.message, response.is_success)

        },
        error: function () {
            alert('Something wrong. Try again later.')
        }
    })
})
// ------------------------------

$(document).on('submit', '#share_file', function (e) {
    e.preventDefault()
    $.ajax({
        type: 'POST',
        url: $('#share_file').data('url'),
        data: {
            file_name: $('#file_name').val(),
            share_with: $('#share_with').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {

            if (response.is_success === true) {
                modal(response.title, response.message, response.is_success, 1)
            } else {
                modal(response.title, response.message, response.is_success)
            }

        },
        error: function () {
            alert('Something wrong. Try again later.')
        }
    })
})
