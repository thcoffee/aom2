var display_num=10;
$(function(){
	$.ajax({
				url:"/pps/putdata/",
				data:{
					task:'putquerywarn',
					page:'1',
					display_num:display_num
				},
				dataType:"json",
				type:"POST",
				success:callbackquery,})
});

function callbackquery(result){ 
    var pageCount=result.num_pages;
	var total_num=result.total_num;
	$("#total_num").text(total_num);
	$("#totalpage").val(pageCount);
	var curpage=$("#currentpage").val();
	var data=result.list;
	$("#queryList tbody").empty();
	var bg="";
	for(var i=0;i<data.length;i++){
		if(data[i].status == '已完成'){
			bg='success';
		}else{
			bg='warning';
		}
		$("#queryList tbody")
		.append("<tr class='"
		+ bg
		+ "'><td width='40%'>"
		+ data[i].warndesc
		+ "</td><td style='text-align:center;'>"
		+ data[i].createtime
		+ "</td><td style='text-align:center;'>"
		+ data[i].status
		+ "</td><td style='text-align:center;'><a href='"
		+ data[i].url
		+ "' target='_blank'><img src='/static/img/pageDown.png'></a></td></tr>");
	}
	$("#showpage").text("共 "+pageCount+" 页 "+total_num+" 笔");
	
	//根据总页数判断，如果小于5页，则显示所有页数，如果大于5页，则显示5页。根据当前点击的页数生成
	//生成分页按钮
	if(pageCount>5){
		page_icon(1,5,0);
	}else{
		page_icon(1,pageCount,0);
	}
	
	//点击分页按钮触发
	$("#pageGro li").live("click",function(){
		var pageNum = parseInt($(this).html());//获取当前页数
		if(pageCount > 5){
			pageGroup(pageNum,pageCount);
		}else{
			$(this).addClass("on");
			$(this).siblings("li").removeClass("on");
		}
		$("#currentpage").val(pageNum);
		$.ajax({
			url:"/pps/putdata/",
			data:{
				task:'putquerywarn',
				page:pageNum,
				display_num:display_num
			},
			dataType:"json",
			type:"POST",
			success:callback,}
			)	
	});

	//点击第一页触发
	$("#pageGro .first").click(function(){
		if(pageCount>5){
			page_icon(1,5,0);
		}else{
			page_icon(1,pageCount,0);
		}
		$("#currentpage").val('1');
		$.ajax({
			url:"/pps/putdata/",
			data:{
				task:'putquerywarn',
				page:'1',
				display_num:display_num
			},
			dataType:"json",
			type:"POST",
			success:callback,}
			)		
		});
	
	//点击最后一页触发
	$("#pageGro .tail").click(function(){
		if(pageCount>5){
			page_icon(pageCount-4,pageCount,4);
		}else{
			page_icon(1,pageCount,0);
		}
		$("#currentpage").val(pageCount);
		$.ajax({
			url:"/pps/putdata/",
			data:{
				task:'putquerywarn',
				page:pageCount,
				display_num:display_num
			},
			dataType:"json",
			type:"POST",
			success:callback,}
			)		
		});
		
	//点击上一页触发
	$("#pageGro .pageUp").click(function(){
		var pageNum = parseInt($("#pageGro li.on").html());//获取当前页
		if(pageCount > 5){
			pageUp(pageNum,pageCount);
		}else{
			var index = $("#pageGro ul li.on").index();//获取当前页
			if(index > 0){
				$("#pageGro li").removeClass("on");//清除所有选中
				$("#pageGro ul li").eq(index-1).addClass("on");//选中上一页
			}
		}
		if(pageNum > 1){
			pageNum=Number(pageNum)- Number(1);
		}
		$("#currentpage").val(pageNum);
		$.ajax({
			url:"/pps/putdata/",
			data:{
				task:'putquerywarn',
				page:pageNum,
				display_num:display_num
			},
			dataType:"json",
			type:"POST",
			success:callback,}
		)	
		
	});
	
	//点击下一页触发
	$("#pageGro .pageDown").click(function(){
		var pageNum = parseInt($("#pageGro li.on").html());//获取当前页
		if(pageCount > 5){
			pageDown(pageNum,pageCount);
		}else{
			var index = $("#pageGro ul li.on").index();//获取当前页
			if(index+1 < pageCount){
				$("#pageGro li").removeClass("on");//清除所有选中
				$("#pageGro ul li").eq(index+1).addClass("on");//选中上一页
			}
		}

		if(pageNum < pageCount){
			pageNum=Number(pageNum)+Number(1);
		}
		$("#currentpage").val(pageNum);
		$.ajax({
			url:"/pps/putdata/",
			data:{
				task:'putquerywarn',
				page:pageNum,
				display_num:display_num
			},
			dataType:"json",
			type:"POST",
			success:callback,}
		)
	});
}

//点击跳转页面
function pageGroup(pageNum,pageCount){
	switch(pageNum){
		case 1:
			page_icon(1,5,0);
		break;
		case 2:
			page_icon(1,5,1);
		break;
		case pageCount-1:
			page_icon(pageCount-4,pageCount,3);
		break;
		case pageCount:
			page_icon(pageCount-4,pageCount,4);
		break;
		default:
			page_icon(pageNum-2,pageNum+2,2);
		break;
	}
}

//根据当前选中页生成页面点击按钮
function page_icon(page,count,eq){
	var ul_html = "";
	for(var i=page; i<=count; i++){
		ul_html += "<li>"+i+"</li>";
	}
	$("#pageGro ul").html(ul_html);
	$("#pageGro ul li").eq(eq).addClass("on");
}

//上一页
function pageUp(pageNum,pageCount){
	switch(pageNum){
		case 1:
		break;
		case 2:
			page_icon(1,5,0);
		break;
		case pageCount-1:
			page_icon(pageCount-4,pageCount,2);
		break;
		case pageCount:
			page_icon(pageCount-4,pageCount,3);
		break;
		default:
			page_icon(pageNum-2,pageNum+2,1);
		break;
	}
}

//下一页
function pageDown(pageNum,pageCount){
	switch(pageNum){
		case 1:
			page_icon(1,5,1);
		break;
		case 2:
			page_icon(1,5,2);
		break;
		case pageCount-1:
			page_icon(pageCount-4,pageCount,4);
		break;
		case pageCount:
		break;
		default:
			page_icon(pageNum-2,pageNum+2,3);
		break;
	}
}

function callback(result){ 
    var pageCount=result.num_pages;
	var total_num=result.total_num;
	$("#total_num").text(total_num);
	$("#totalpage").val(pageCount);
	var curpage=$("#currentpage").val();
	var data=result.list;
	$("#queryList tbody").empty();
	var bg="";
	for(var i=0;i<data.length;i++){
		if(data[i].status == '已完成'){
			bg='success';
		}else{
			bg='warning';
		}
		$("#queryList tbody")
		.append("<tr class='"
		+ bg
		+ "'><td>"
		+ data[i].warndesc
		+ "</td><td style='text-align:center;'>"
		+ data[i].createtime
		+ "</td><td style='text-align:center;'>"
		+ data[i].status
		+ "</td><td style='text-align:center;'><a href='"
		+ data[i].url
		+ "' target='_blank'><img src='/static/img/pageDown.png'></a></td></tr>");
	}
	$("#showpage").text("共 "+pageCount+" 页 "+total_num+" 笔");
	
}




