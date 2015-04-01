/**
*content:发表话题js
*author:zxc
**/
var oRealese = {
    realease:function(){
        $(".realease_wrap").on("click","#realease_btn",function(e){
            e.preventDefault();
            var title = $(".topic_title").val(),
                classify = $(".topic_classify :selected").val(),
                content = $(".realease_textarea").val();
                if(title.length==0){
                    alert("请输入话题标题！");
                    return;
                }
                if(content.length==0){
                	alert("请输入话题内容！");
                    return;
                }             
            $.post("/posttopic/",{
                title:title,
                classify:classify,
                content:content
            },function(response){
                if(response.data=="0"){
                    alert("发表失败");
                }else{
                    location.href="/index/";
                }
            },"json");
        })
    },
    init:function(){
        this.realease();
    }
}

$(function(){
    oRealese.init();
})