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
				task:'getquerywarninfo',
				id:getid,
			},
			dataType:"json",
			type:"POST",
			success:callback,}
))

function callback(result){
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

