/**
*content:注册js
*author:zxc
**/
var oSignup = {
    signup:function(){
        $("#signup_form").on("click","#signup_btn",function(e){
            e.preventDefault();
            var username = $("#username").val(),
                password = $("#password").val(),
                repassword = $("#repassword").val(),
                email = $("#email").val();
                if(username.length<4||username.length>16){
                    alert("用户名长度为4-16");
                    return;
                }
                if(email.length==0){
                	alert("邮箱不能为空");
                    return;
                }
                if(password.length<6){
                    alert("密码长度为6位数以上");
                    return;
                }
                if(password!=repassword){
                    alert("两次密码不一样");
                    return;
                }                
            $.post("/signup/",{
                username:username,
                password:password,
                email:email
            },function(response){
                if(response.data=="0"){
                    alert("注册失败");
                }else{
                    location.href="/index/";
                }
            },"json");
        })
    },
    init:function(){
        this.signup();
    }
}

$(function(){
    oSignup.init();
})