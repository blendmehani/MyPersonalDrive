
let input_password = document.getElementById('inputPassword')
let input_confirm_password = document.getElementById('inputConfirmPassword')
first_icon = document.getElementById('togglePassword')
second_icon = document.getElementById('togglePassword1')

function Toggle1(){
    if (input_password.className === 'form-control active'){
        input_password.setAttribute('type', 'text')
        first_icon.className = 'far fa-eye'
        input_password.className='form-control'
    }
    else{
        input_password.setAttribute('type','password')
        first_icon.className = 'far fa-eye-slash'
        input_password.className='form-control active'
    }
}

function Toggle2(){
    if (input_confirm_password.className === 'form-control active'){
        input_confirm_password.setAttribute('type', 'text')
        second_icon.className = 'far fa-eye'
        input_confirm_password.className='form-control'
    }
    else{
        input_confirm_password.setAttribute('type','password')
        second_icon.className = 'far fa-eye-slash'
        input_confirm_password.className='form-control active'
    }
}