/**
*content:重置密码提交注册邮箱js
*author:zxc
**/
var oForgetPwd = {
    forget:function(){
        $("#forget_form").on("click","#forget_btn",function(e){
            e.preventDefault();
           var email = $("#email").val();
               if(email.length==0){
                    alert("邮箱不能为空");
                    return;
                }
            $.post("/forget/",{
                email:email
            },function(response){
                if(response.data=="0"){
                    alert(response.msg);
                }else{
                    alert("重置密码链接已经发送到您注册的邮箱，请查收！")
                }
            },"json");
        })
    },
    init:function(){
        this.forget();
    }
}

$(function(){
    oForgetPwd.init();
})
