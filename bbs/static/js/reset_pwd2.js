/**
*content:重置密码2js
*author:zxc
**/
var oReset = {
    reset:function(){
        $("#reset_form").on("click","#reset_btn",function(e){
            e.preventDefault();
            var password = $("#password").val(),
                repassword = $("#repassword").val();                         
                if(password.length<6){
                    alert("密码长度为6位数以上");
                    return;
                }
                if(password!=repassword){
                    alert("两次密码不一样");
                    return;
                }
            var username = location.toString().split("&u=")[1];               
            $.post("/resetpwd2/",{
                username:username,
                password:password
            },function(response){
                if(response.data=="0"){
                    alert(response.msg);
                }else{
                    location.href="/index/";
                }
            },"json");
        })
    },
    init:function(){
        this.reset();
    }
}

$(function(){
    oReset.init();
})