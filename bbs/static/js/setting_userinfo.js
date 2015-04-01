/**
*content:个人信息设置js
*author:zxc
**/
var oSettingInfo = {
    info:function(){
        $("#reset_info_form").on("click","#reset_info",function(e){
            e.preventDefault();
            var nickname = $("#nickname").val(),
                description = $("#description").val();                 
            $.post("/setting_userinfo/",{
                screen_name:nickname,
                description:description
            },function(response){
                if(response.data=="0"){
                    alert(response.msg);
                }else{
                    alert("修改成功!");
                }
            },"json");
        })
    },
    init:function(){
        this.info();
    }
}

$(function(){
    oSettingInfo.init();
})