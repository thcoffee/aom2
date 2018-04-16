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
				task:'getaut',
				id:getid,
			},
			dataType:"json",
			type:"POST",
			success:callbackreview,}
))

function callbackreview(result){
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
	var data=result.warntaskMsg;
	$("#undoList tbody").empty();
	for(var i=0;i<data.length;i++){
		$("#reviewList tbody")
		.append("<tr><td style='text-align:center;'>"
		+ Number(i+1)
		+ "</td><td style='text-align:center;'>"
		+ data[i].name
		+ "</td><td>"
		+ data[i].message
		+ "</td><td style='text-align:center;'>"
		+ data[i].createtime
		+ "</td></tr>");
	}
}

function agree(){
	var warntaskMsg=$("#warntaskMsg").val();
	var messid=$("#messid").val();
	var getid=$("#getid").val();
	if(warntaskMsg.trim() == ""){
		warntaskMsg="同意！";
		$("#warntaskMsg").text(warntaskMsg);
	}
	$.ajax({
			url:"/pps/putdata/",
			data:{
				task:'putaud',
				id:getid,
				messid:messid,
				warntaskMsg:warntaskMsg,
				status:'1',
			},
			dataType:"json",
			type:"POST",
			success:callback,}
			)
}

function unagree(){
	var warntaskMsg=$("#warntaskMsg").val();
	var messid=$("#messid").val();
	var getid=$("#getid").val();
	if(warntaskMsg.trim() == ""){
		warntaskMsg="不同意！";
		$("#warntaskMsg").text(warntaskMsg);
	}
	$.ajax({
			url:"/pps/putdata/",
			data:{
				task:'putaud',
				id:getid,
				messid:messid,
				warntaskMsg:warntaskMsg,
				status:'0',
			},
			dataType:"json",
			type:"POST",
			success:callback,}
			)
}

function callback(result){
	var data=result.warntaskMsg;
	$("#undoList tbody").empty();
	for(var i=0;i<data.length;i++){
		$("#reviewList tbody")
		.append("<tr><td style='text-align:center;'>"
		+ Number(i+1)
		+ "</td><td style='text-align:center;'>"
		+ data[i].name
		+ "</td><td style='word-wrap:break-word;word-break:break-all;'>"
		+ data[i].message
		+ "</td><td style='text-align:center;'>"
		+ data[i].createtime
		+ "</td></tr>");
	}
}

