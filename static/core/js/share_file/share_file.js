function valueChanged() {
    if ($('#shared_files_checkbox').is(":checked")) {

        document.getElementById('shared_from_div').style.display = 'block';
        document.getElementById('shared_to_div').style.display = 'none';


    } else {

        document.getElementById('shared_from_div').style.display = 'none';
        document.getElementById('shared_to_div').style.display = 'block';

    }

}

$(function () {
    $(document).tooltip({
        position: {
            my: "center top-19",
            at: "center bottom",
        }
    })
})

$(document).ready(function() {
       $("#unshare_selected").click(function() {
           $("#manage_shared_files_form").submit();
       });
    });