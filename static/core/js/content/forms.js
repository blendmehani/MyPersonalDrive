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
            $("#title_modal").html(response.title)
            $("#body_modal").html(response.message)
            if (response.is_success === true) {
                $("#body_modal").removeClass()
                $('#body_modal').addClass('alert-success p-3 rounded')
                $("#button_modal").removeClass()
                $('#button_modal').addClass('col-md-12 btn btn-outline-success')
                $("#icon_modal").removeClass()
                $('#icon_modal').addClass('far fa-thumbs-up')

            } else {
                $("#body_modal").removeClass()
                $('#body_modal').addClass('alert-danger p-3 rounded')
                $("#button_modal").removeClass()
                $('#button_modal').addClass('col-md-12 btn btn-outline-danger')
                $("#icon_modal").removeClass()
                $('#icon_modal').addClass('far fa-thumbs-down')
            }
            $("#directory_modal").modal('show');

        },
        error: function () {
            alert('Something wrong. Try again later.')
        }
    })
})
// ------------------------------

// SUBMIT CHANGE NAME FORM ON CHANGE TEXT
$(document).ready(function(){
   $('.name_input').on('change',function(){
      $('#change_name2').submit();
   });
});
// -------------------------------------