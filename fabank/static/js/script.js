$(document).ready(function(){
do_ajax();

/////////////////////////////////////////////////
/////////////is login/ /////////////////////////
///////////////////////////////////////////////
if(true){

    $.ajax({
        type: "POST",
        url: "/users/is_login/",
        dataType:"json",

        success: function (data) {
                if(data.response){
                        $("#login").hide();
                        $("#logout").show();
                        $("#profile").show();
                }
                else{
                    $("#login").show();
                    $("#logout").hide();
                    $("#profile").hide();
                }
                
                            },
        error:function(){
            console.log("error");
        }
    });

}






/////////////////////////////////////////////////
/////////////login//////////////////////////////
///////////////////////////////////////////////

$("#login").click(function(){
    $('.ui.modal.login').modal({blurring: true}).modal('show');
});
$('.ui.accordion').accordion();
$('.ui.checkbox').checkbox();
$(".menu .item").tab();
$('.tabular.menu .item').tab();

$("#confirm_reg").click(function(){
    
   window.location='/home/';
   $("#inner_success_modal").html("شما با موفقیت وارد شدید");
    $('#success_reg')
    .modal('hide')
    ;


});

$("#confirm_err").on('click',function(){
 
    $("#inner_error_modal").html("نام کاربری یا رمز عبور اشتباه است");
    $('#error_reg')
    .modal('hide')
    ;

    $("#username_field").addClass("error");
});


$("#login_submit").click(function(){
     $("#reg_dimmer2").addClass("active");
    $.ajax({
        type: "POST",
        url: "/users/login/",
        dataType:"json",
        data :{
            username:$("#login_username").val(),
            password :$("#login_password").val()
                    },
        success: function (data) {
            $("#reg_dimmer2").removeClass("active");
            if(data.response){
                    $('#success_reg')
                    .modal('show')
                    ;
                    $("#login").hide();

            }
            else{
                  $('#error_reg')
                    .modal('show')
                    ;
            }
        },
        error:function(){
            console.log("error");
        }
    });
});
/////////////////////////////////////////////////
/////////////logout/// /////////////////////////
///////////////////////////////////////////////
$("#logout").click(function(){

    $.ajax({
        type: "POST",
        url: "/users/logout/",
        dataType:"json",

        success: function (data) {
               if(data.response)
                window.location="/home/";
                            },
        error:function(){
            console.log("error");
        }
    });
});



/////////////////////////////////////////////////
/////////////about us///////////////////////////
///////////////////////////////////////////////
$("#about_us").click(function(){
    window.location.href="/users/about/";
});


/////////////////////////////////////////////////
/////////////profile////////////////////////////
///////////////////////////////////////////////
$("#profile").click(function(){
    window.location.href="/users/profile/";

});



/////////////////////////////////////////////////
/////////////change password////////////////////
///////////////////////////////////////////////
$("#change_pw").click(function(){

    $.ajax({
        type: "POST",
        url: "/users/change_pw/",
        dataType:"json",
        data:{
            password1:$("#change_pw1").val(),
            password2:$("#change_pw2").val(),
        },
        success: function (data) {
            if(data.response){
                $("#inner_success_modal").html("رمز شما با موفقیت تغییر یافت");
                $('#success_reg').modal('show');
            }
            else{
                $("#inner_error_modal").html("خطا در ورود اطلاعات");

                    $('#error_reg')
                    .modal('show')
                    ;
            }
                            },
        error:function(){
            console.log("error");
        }
    });
});
$('#change_pw_form')
  .form({
    password1: {
        identifier: 'password1',
        rules: [
          {
          type   : 'length[6]',
          prompt : 'رمز عبور شما باید حداقل شش رقم باشد'
        }
        ]
      },
      password2: {
        identifier: 'password2',
        rules: [
          {
          type   : 'length[6]',
          prompt : 'رمز عبور شما باید حداقل شش رقم باشد'
        },
        {
          type   : 'match[password1]',
          prompt : 'رمز ها مطابقت ندارند'
        }
        ]
      }
  });



/////////////////////////////////////////////////
/////////////transport money////////////////////
///////////////////////////////////////////////
$("#submit_transport").click(function(){

    $.ajax({
        type: "POST",
        url: "/users/transport/",
        dataType:"json",
        data:{
            number1:$("#own_number_account").val(),
            number2:$("#dest_number_account").val(),
            password:$("#pw1").val(),
            money:$("#transport_money").val(),

        },
        success: function (data) {
            if(data.response){
                $("#inner_success_modal").html(data.message);
                $('#success_reg').modal('show');
            }
            else{
                $("#inner_error_modal").html(data.message);

                    $('#error_reg')
                    .modal('show')
                    ;
            }
                            },
        error:function(){
            console.log("error");
        }
    });
});
$('#transport_form')
  .form({
    own_number_account: {
        identifier: 'own_number_account',
        rules: [
          {
          type   : 'length[16]',
          prompt : 'شماره حساب 16 رقمی است'
        }
        ]
      },
      dest_number_account: {
        identifier: 'dest_number_account',
        rules: [
          {
          type   : 'length[16]',
          prompt : 'شماره حساب 16 رقمی است'
        }
        ]
      },
      password1: {
        identifier: 'password1',
        rules: [
          {
          type   : 'length[6]',
          prompt : 'رمز عبور شما باید حداقل شش رقم باشد'
        }
        ]
      }
  });



/////////////////////////////////////////////////
/////////////contatc us/////////////////////////
///////////////////////////////////////////////

$("#contact_us").click(function(){
    window.location.href="/users/contact/";

});


$("#home").click(function(){
    window.location.href="/home/";
});



/////////////////////////////////////////////////
/////////////shaba gir/// //////////////////////
///////////////////////////////////////////////
$("#shaba_gir").click(function(){

    $.ajax({
        type: "POST",
        url: "/users/shaba/",
        dataType:"json",

        success: function (data) {
               if(data.response)
                        $("#card_number").html(data.number1);
                        $("#shaba_number").html(data.number2);

                            },
        error:function(){
            console.log("error");
        }
    });
});



/////////////////////////////////////////////////
/////////////remained/// //////////////////////
///////////////////////////////////////////////
$("#remained_money").click(function(){

    $.ajax({
        type: "POST",
        url: "/users/remained/",
        dataType:"json",

        success: function (data) {
               if(data.response)
                        $("#remained").html(data.remained + " ریال");

                            },
        error:function(){
            console.log("error");
        }
    });
});

});





/////////////////////////////////////////////////
////////////CSRF token//////////////////////////
///////////////////////////////////////////////
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
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


    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }




/////////////////////////////////////////////////
////////////ajax////////////////////////////////
///////////////////////////////////////////////
function do_ajax(){

var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        crossDomain: true, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}