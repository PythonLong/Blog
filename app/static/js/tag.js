function Tag(inputId){
	var obj = new Object();
	if(inputId==null||inputId==""){
		alert("初始化失败，请检查参数！");
		return;
	}
	obj.inputId = inputId;
	
	//初始化
	obj = (function(obj){
		obj.tagValue="";
		obj.isDisable = false;
		return obj;
	})(obj);
	
	//初始化界面
	obj.initView=function()
	{

		var inputObj = $("#"+this.inputId);
		var inputId = this.inputId;
		//生成Html标签
		inputObj.css("display","none");
		var appendStr='';
		appendStr+='<div class="tagsContaine" id="'+inputId+'_tagcontaine">';
		appendStr+='<div class="tagList"></div><input type="text" class="tagInput"/>';
		appendStr+='</div>';
		inputObj.after(appendStr);

		var tagInput = $("#"+inputId+"_tagcontaine .tagInput");
		//div 下面的Input

		if(!this.isDisable){
			$("#"+inputId+"_tagcontaine").attr("ds","1");
			tagInput.keydown(function(event){
				//keydown  键盘被按下
				//keycode 13  回车键
				if(event.keyCode==13){
			         var inputValue = $(this).val();
			         tagTake.setInputValue(inputId,inputValue);
			         $(this).val('');
			    }
			});
		}
		else{
			$("#"+inputId+"_tagcontaine").attr("ds","0");
			tagInput.remove();
		}
		if(this.tagValue!=null&&this.tagValue!=""){
			tagTake.setInputValue(inputId,this.tagValue);
			if(this.isDisable){
				$("#"+inputId+"_tagcontaine .tagList .tagItem .delete").remove();
			}
		}
	}

	obj.disableFun=function(){
		if(this.isDisable){
			return;
		}
		var inputId = this.inputId;
		var tagInput = $("#"+inputId+"_tagcontaine .tagInput");
		tagInput.remove();
		this.isDisable = true;
		$("#"+inputId+"_tagcontaine").attr("ds","0");
		$("#"+inputId+"_tagcontaine .tagList .tagItem .delete").remove();
		tagTake.initTagEvent(inputId);
		
	}
	obj.unDisableFun = function(){
		if(!this.isDisable){
			return;
		}
		var inputId = this.inputId;
		var tagContaine = $("#"+inputId+"_tagcontaine");
		tagContaine.append('<input type="text" class="tagInput"/>');
		this.isDisable = false;
		$("#"+inputId+"_tagcontaine").attr("ds","1");
		var tagInput = $("#"+inputId+"_tagcontaine .tagInput");
		tagInput.keydown(function(event){
				if(event.keyCode==13){
			         var inputValue = $(this).val();
			         tagTake.setInputValue(inputId,inputValue);
			         $(this).val("");
			    }
		});
		$("#"+inputId+"_tagcontaine .tagList .tagItem").append('<div class="delete"></div>');
		tagTake.initTagEvent(inputId);
		
	}

	obj.getTags_data = function (){
		TagElement = $('.tagItem span');
			Tags = [];
			for(var i=0;i<TagElement.length;i++){
				Tags.push(TagElement.eq(i).html())
			}
		return Tags
	}
	
	return obj;
}


0
var tagTake ={
	var:num = 0,

	"setInputValue":function(inputId,inputValue)
	{
		if(inputValue==null||inputValue==""){
			return;
		}
		var tagListContaine = $("#"+inputId+"_tagcontaine .tagList");
		inputValue = inputValue.replace(/，/g,",");
		//如果添加多个标签可用逗号：','或者'，'分开
		var inputValueArray = inputValue.split(",");
		for(var i=0;i<inputValueArray.length;i++)
		{
			var valueItem = $.trim(inputValueArray[i]);
			if(valueItem!="")
			{
				if(num<5)
				{
					var appendListItem = tagTake.getTagItemModel(valueItem);
					tagListContaine.append(appendListItem);
				}
				
			}
		}
		tagTake.resetTagValue(inputId);
		tagTake.initTagEvent(inputId);
	},

	"initTagEvent":function(inputId){
		$("#"+inputId+"_tagcontaine .tagList .tagItem .delete").off();
		$("#"+inputId+"_tagcontaine .tagList .tagItem").off();
		var ds =  $("#"+inputId+"_tagcontaine").attr("ds");
		if(ds=="0"){
			return;
		}

		//删除事件
		$("#"+inputId+"_tagcontaine .tagList .tagItem .delete").mousedown(function(){
			num -= 1;
			var current_data = $(this).prev().html();
			$(this).parent().remove();
			// tagTake.resetTagValue(inputId);
		});
		
		//双击事件
		$("#"+inputId+"_tagcontaine .tagList .tagItem").dblclick(function(){
			var tagItemObj = $(this);
			 $(this).css("display","none");
			var updateInputObj = $("<input type='text' class='updateInput' value='"+tagItemObj.find("span").html()+"'>");
			updateInputObj.insertAfter(this);
			updateInputObj.focus();
			updateInputObj.blur(function(){
				var inputValue = $(this).val();
				if(inputValue!=null&&inputValue!=""){
					tagItemObj.find("span").html(inputValue);
					tagItemObj.css("display","block");
				}else{
					num -= 1;
					tagItemObj.remove();
				}
				updateInputObj.remove();
				tagTake.resetTagValue(inputId);
			});
			updateInputObj.keydown(function(event){
				if(event.keyCode==13){
			        var inputValue = $(this).val();
					if(inputValue!=null&&inputValue!=""){
						tagItemObj.find("span").html(inputValue);
						tagItemObj.css("display","block");
					}
					else{
						num -= 1;
						tagItemObj.remove();
					}
					updateInputObj.remove();
					tagTake.resetTagValue(inputId);
			    }
			});
		});
	},
	"resetTagValue":function(inputId){
		var tags = $("#"+inputId+"_tagcontaine .tagList .tagItem");
		var tagsStr="";
		for(var i=0;i<tags.length;i++){
			tagsStr+=tags.eq(i).find("span").html()+",";
		}
		tagsStr = tagsStr.substr(0,tagsStr.length-1);
		$("#"+inputId).val(tagsStr);
	},

	//生成标签
	"getTagItemModel":function(valueStr){
		num += 1;
		return '<div class="tagItem"><span>'+valueStr+'</span><div class="delete"></div></div>';
	}
}
