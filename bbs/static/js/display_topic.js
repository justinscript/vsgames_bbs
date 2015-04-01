/**
*content:帖子具体内容js
*author:zxc
**/
var oDisplay = {
    /*发表回复*/
    replay:function(){
        $("#reply_form").on("click","#reply_btn",function(e){
            e.preventDefault();
            var topic_id = $(".topic_id").val(),
                content = $(".realease_textarea").val(),
                /*回复人id号*/
                userid = $(".user_id").val(),
                avatar_url = $('.avatar_image').attr("src"),
                username = $('.username').html();
                
                if(content.length<1){
                    alert("回复内容不能为空！");
                    return;
                }
            $.post("/reply/",{
                topic_id:topic_id,
                content:content
            },function(response){
                if(response.data=="0"){
                    alert("发表回复失败！");
                }else{
                	/*更改右边个人信息*/
                	var reply_num = $(".status-reply").find("a").html();
                	reply_num++;
                	$(".status-reply").find("a").html(reply_num);   
                    if($(".no_replies").length==1){
                        //以前没有人回复
                        $append = '<div class="reply_wrap">\
                        <div class="reply_div first_reply clearfix">\
                            <div class="reply_avatar">\
                                <img src="'+avatar_url+'"/>\
                            </div>\
                            <div class="reply_content">\
                                <p>\
                                    <a href="javascript:void(0);" class="reply_name">'+username+'</a>\
                                    <span class="reply_time">1 分钟前</span>\
                                </p>\
                                <p class="reply">'+content+'</p>\
                            </div>\
                        </div>\
                        </div>';
                        $(".no_replies").remove();
                        $('.topic_wrap').after($append);
                    }else{
                        //已经有人回复了
                        $append = '<div class="reply_div clearfix">\
                            <div class="reply_avatar">\
                                <img src="'+avatar_url+'"/>\
                            </div>\
                            <div class="reply_content">\
                                <p>\
                                    <a href="javascript:void(0);" class="reply_name">'+username+'</a>\
                                    <span class="reply_time">1 分钟前</span>\
                                </p>\
                                <p class="reply">'+content+'</p>\
                            </div>\
                        </div>';
                        $(".reply_wrap").append($append);
                    }
                }
            },"json");
        })
    },
    /*点赞功能*/
    dianzan:function(){
        $(".date").on("click",".dianzan_link",function(){
            var topic_id = $(".topic_id").val();
            $.post("/vote/",{
                topic_id:topic_id
            },function(response){
                if(response.data=="0"){
                    alert("服务器繁忙！");
                }else{
                   $(".dianzan_link").remove();
                   var $span = "<span>·您已点赞!</span>"; 
                   $(".date").append($span);
                }
            },"json");
        })
    },
    /*删帖功能*/
    shantie:function(){
        $("#delete").on("click",function(){
            var topic_id = $(".topic_id").val();
            $.post("/delete/",{
                topic_id:topic_id
            },function(response){
                if(response.data=="0"){
                    alert("服务器繁忙！");
                }else{
                  	location.href=document.referrer;
                }
            },"json");
        })
    },
    /*收藏功能*/
    shouchang:function(){
        $("#fav").on("click",function(){
            var topic_id = $(".topic_id").val();
            $.post("/favtopic/",{
                topic_id:topic_id
            },function(response){
                if(response.data=="0"){
                    alert("服务器繁忙！");
                }else{
                  	alert("收藏成功!");
                }
            },"json");
        })
    },
    init:function(){
        this.replay();
        this.dianzan();
        this.shantie();
        this.shouchang();
    }
}

$(function(){
    oDisplay.init();
})