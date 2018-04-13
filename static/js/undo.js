$(document).ready(
			$.ajax({
			url:"/pps/putdata/",
			data:{
				task:'getundo',
				page:'1',
				display_num:'11'
			},
			dataType:"json",
			type:"POST",
			success:callbackundo,}
))

function callbackundo(result){ 
    var totalpage=result.num_pages;
	$("#undo_num").text(result.undo_num);
	$("#totalpage").val(totalpage);
	var curpage=$("#currentpage").val();
	var data=result.list;
	$("#undoList tbody").empty();
	for(var i=0;i<data.length;i++){
		$("#undoList tbody")
		.append("<tr><td width='65%'><span class='glyphicon glyphicon-fire'>&nbsp;</span><a href='"
		+ data[i].path
		+ "'>"
		+ data[i].activityname
		+ "</a></td><td width='35%'>"
		+ data[i].createtime
		+ "</td></tr>");
	}
	if( data.length == 0 ){
		$("#undoList tbody")
		.append("<tr><td colspan='2' align='center'><img src='/static/img/coffe.png'></img></td></tr>"
		+ "<tr><td colspan='2' align='center'>您没有待处理工作啦！休息一会吧！</td></tr>");
			
		$("#page").css("display","none");	
	}
	$("#showpage").text("第 "+curpage+" 页 / 共 "+totalpage+" 页");
}

function getlastpage(){
	var curpage=$("#currentpage").val();
	if(curpage==1){
		alert("您已经在第一页了！");
		return;
	}
	var page = curpage-1
	$("#currentpage").val(page);
	$.ajax({
			url:"/pps/putdata/",
			data:{
				task:'getundo',
				page:page,
				display_num:'11'
			},
			dataType:"json",
			type:"POST",
			success:callbackundo,}
			)	
}

function getnextpage(){
	var curpage=$("#currentpage").val();
	var totalpage=$("#totalpage").val();
	if(curpage==totalpage){
		alert("您已经在最后一页了！");
		return;
	}
	var page=Number(curpage)+Number(1);
	$("#currentpage").val(page);
	$.ajax({
			url:"/pps/putdata/",
			data:{
				task:'getundo',
				page:page,
				display_num:'11'
			},
			dataType:"json",
			type:"POST",
			success:callbackundo,}
			)	
}




