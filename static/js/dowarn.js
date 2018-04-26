var url = location.search;
var getid = ""
if (url.indexOf("?") != -1) {  
	var str = url.substr(1);
	getid = str.split("=")[1]; 
} 

$(document).ready(
			$.ajax({
			url:"/pps/putdata/",
			data:{
				task:'getwarn',
				id:getid,
			},
			dataType:"json",
			type:"POST",
			success:callbackdowarn,}
))

function callbackdowarn(result){
	$("#warnid").text(result.warnid);
	$("#warntype").text(result.warntype);
	$("#enviname").text(result.enviname);
	$("#warnlevel").text(result.warnlevel);	
	$("#warndesc").text(result.warndesc);
	$("#createtime").text(result.createtime);
	$("#recoverytime").text(result.recoverytime);
	$("#reason").text(result.reason);
	$("#measure").text(result.measure);
	$("#messid").val(result.messid);
	$("#getid").val(getid);
	
	var warntaskMsg=result.warntaskMsg;
	if( typeof(warntaskMsg.message) != 'undefined'){
		$("#warntaskMsg").text(warntaskMsg.message);
	}else{
		$("#suggest").css("display","none");	
	}
}

function submit(){
	var reason=$("#reason").val();
	var measure=$("#measure").val();
	var messid=$("#messid").val();
	var getid=$("#getid").val();
	if(reason.trim() == ""){
		alert("请您录入问题原因！");
		return;
	}
	if(measure.trim() == ""){
		alert("请您录入解决及预防措施！");
		return;
	}
	
	$.ajax({
			url:"/pps/putdata/",
			data:{
				task:'putwarn',
				id:getid,
				messid:messid,
				reason:reason,
				measure:measure,
			},
			dataType:"json",
			type:"POST",
			success:callback,}
			)
}
function callback(result){
	if(result.status){
		$('#sub').attr("disabled",true); 
		window.location.href="/pps/undo/";
	}		
}

