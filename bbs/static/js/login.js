/**
*content:登录js
*author:zxc
**/
var oLogin = {
    login:function(){
        $("#login_form").on("click","#submit-btn",function(e){
            e.preventDefault();
            var username = $("#username").val(),
                password = $("#password").val();
                var before = location.toString().split("?next=")[1];
                if(username.length<4){
                    alert("用户名长度为4-16");
                    return;
                }
                if(password.length<6){
                    alert("密码长度为6位数以上");
                    return;
                }
            $.post("/login/",{
                username:username,
                password:password
            },function(response){
                if(response.data=="0"){
                    alert("用户名或密码错误");
                }else{
                    if(before!=undefined){
                       location.href = before;
                    }else{
                        location.href="/index/";
                    }
                }
            },"json");
        })
    },
    init:function(){
        this.login();
    }
}

$(function(){
    oLogin.init();
})