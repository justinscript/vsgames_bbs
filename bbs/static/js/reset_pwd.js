/**
*content:重置密码js
*author:zxc
**/
var oReset = {
    reset:function(){
        $("#reset_pwd_form").on("click","#reset_pwd_1",function(e){
            e.preventDefault();
            var password = $("#newpassword").val(),
                repassword = $("#renewpassword").val(),
                oldpassword = $("#oldpassword").val();                   
                if(password.length<6||oldpassword.length<6){
                    alert("密码长度为6位数以上");
                    return;
                }
                if(password==oldpassword){
                    alert("新旧密码相同");
                    return;
                }
                if(password!=repassword){
                    alert("两次密码不一样");
                    return;
                }
                
            $.post("/resetpwd/",{
                old_password:oldpassword,
                new_password:password
            },function(response){
                if(response.data=="0"){
                    alert(response.msg);
                }else{
                    alert("修改成功!");
                    location.href="/setting_index/";
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