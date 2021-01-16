let dir = document.getElementById('create_directory')
let file = document.getElementById('upload_file')

// SHOW HIDE DIRECTORY FORM
function show_create_directory() {
    dir.style.display = 'block'
    file.style.display = 'none'
    $("#create_directory input:visible").first().focus()
    window.setTimeout(function () {
        dir.style.opacity = 1
        dir.style.transform = 'scale(1)'
    }, 0)
}

function hide_create_directory() {
    dir.style.opacity = 0
    dir.style.transform = 'scale(0)'
    window.setTimeout(function () {
        dir.style.display = 'none'
    }, 500)
}
// -------------------------------------------

//SHOW HIDE UPLOAD FILE FORM
function show_upload_file() {
    file.style.display = 'block'
    dir.style.display = 'none'
    $("#upload_file input:visible").first().focus()
    window.setTimeout(function () {
        file.style.opacity = 1
        file.style.transform = 'scale(1)'
    }, 0)
}

function hide_upload_file() {
    file.style.opacity = 0
    file.style.transform = 'scale(0)'
    window.setTimeout(function () {
        file.style.display = 'none'
    }, 500)
}
// ------------------------------------------

// SHOW HIDE IMAGES THUMBNAILS
function show_hide_thumbnail(){
    let thumbnail = document.getElementById('show_thumbnail')
    let thumbnail_text = document.getElementById('thumbnail_text')
    let nested_image_a = document.getElementsByClassName('nested_image_a')
    let nested_image_b = document.getElementsByClassName('nested_image_b')
    if(thumbnail.style.display === 'block'){
        thumbnail.style.display = 'inline-block'
        thumbnail_text.innerText = ' Hide Thumbnails'
        $('#thumbnail_logo').removeClass()
        $("#thumbnail_logo").addClass('far fa-eye-slash')
        for(let i= 0; i < nested_image_a.length; i++) {
            nested_image_a[i].style.display = 'initial'
            nested_image_b[i].style.display = 'none'
        }
    }
    else if(thumbnail.style.display === 'inline-block'){
        thumbnail.style.display = 'block'
        thumbnail_text.innerText = ' Show Thumbnails'
        $('#thumbnail_logo').removeClass()
        $("#thumbnail_logo").addClass('far fa-eye')
                for(let i= 0; i < nested_image_a.length; i++) {
            nested_image_a[i].style.display = 'none'
            nested_image_b[i].style.display = 'block'
        }
    }
}
// -----------------------------------------------
