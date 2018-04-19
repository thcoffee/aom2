$(function () {
		var today = getNowFormatDate();
		var lastweek = getBeforeWeek(today);
		var lastmonth = getBeforeMonth(today);
		$("#txtBeginDate").val(lastmonth);
		$("#txtEndDate").val(today);
		$.ajax({
			url:"/pps/putdata/",
			data:{
				task:'gettjwarn',
				begindate:lastmonth,
				enddate:today,
			},
			dataType:"json",
			type:"POST",
			success:callback,}
		)
    });
function submit(){
	var begindate=$("#txtBeginDate").val();
	var enddate=$("#txtEndDate").val();
	$.ajax({
		url:"/pps/putdata/",
		data:{
			task:'gettjwarn',
			begindate:begindate,
			enddate:enddate,
		},
		dataType:"json",
		type:"POST",
		success:callback,}
		)
}	
function callback(result){
	var enviname = result.enviname;
	var warntype = result.warntype;
	var warnlevel = result.warnlevel;
	var envnamestr = [];
	var envvalstr = [];
	var typenamestr = [];
	var typevalstr = [];
	var levelnamestr = [];
	var levelvalstr = [];
	for(var i=0;i<enviname.length;i++){
		envnamestr.push(enviname[i].enviname);
		envvalstr.push(enviname[i].count);
	}
	
	for(var i=0;i<warntype.length;i++){
		typenamestr.push(warntype[i].warntype);
		typevalstr.push(warntype[i].count);
	}
	
	for(var i=0;i<warnlevel.length;i++){
		levelnamestr.push(warnlevel[i].warnlevel);
		levelvalstr.push(warnlevel[i].count);
	}
	
	$("#txtBeginDate").calendar({
            controlId: "divDate",                                 // 弹出的日期控件ID，默认: $(this).attr("id") + "Calendar"
            speed: 200,                                           // 三种预定速度之一的字符串("slow", "normal", or "fast")或表示动画时长的毫秒数值(如：1000),默认：200
            complement: true,                                     // 是否显示日期或年空白处的前后月的补充,默认：true
            readonly: true,                                       // 目标对象是否设为只读，默认：true
            upperLimit: new Date(),                               // 日期上限，默认：NaN(不限制)
            lowerLimit: new Date("2011/01/01"),                   // 日期下限，默认：NaN(不限制)
            callback: function () {                             // 点击选择日期后的回调函数
		   }

        });
    $("#txtEndDate").calendar();
	
	// 基于准备好的dom，初始化echarts实例
	var envChart = echarts.init(document.getElementById('enviname'));
	var typeChart = echarts.init(document.getElementById('warntype'));
	var levelChart = echarts.init(document.getElementById('warnlevel'));
	// 指定图表的配置项和数据
	envChart.setOption({
	   title: {
			text: ''
	   },
	   tooltip: {},
	   legend: {
			data: ['报警数量']
	   },
	   xAxis: {
			data: envnamestr
	   },
	   yAxis: {},
	   series: [{
			name: '报警数量',
			type: 'bar',
			data: envvalstr
	   }]
	});

	typeChart.setOption({
	   title: {
			text: ''
	   },
	   tooltip: {},
	   legend: {
			data: ['报警数量']
	   },
	   xAxis: {
			data: typenamestr
	   },
	   yAxis: {},
	   series: [{
			name: '报警数量',
			type: 'bar',
			data: typevalstr
	   }]
	});

	levelChart.setOption({
	   title: {
			text: ''
	   },
	   tooltip: {},
	   legend: {
			data: ['报警数量']
	   },
	   xAxis: {
			data: levelnamestr
	   },
	   yAxis: {},
	   series: [{
			name: '报警数量',
			type: 'bar',
			data: levelvalstr
	   }]
	});
}

function getNowFormatDate() {
	var date = new Date();
	var seperator1 = "-";
	var year = date.getFullYear();
	var month = date.getMonth() + 1;
	var strDate = date.getDate();
	if (month >= 1 && month <= 9) {
		month = "0" + month;
	}

	if (strDate >= 0 && strDate <= 9) {
		strDate = "0" + strDate;
	}
	var currentdate = year + seperator1 + month + seperator1 + strDate;
	return currentdate;
}

//获取指定日期前七天

function getBeforeWeek(d){
	d = new Date(d);
	d = +d - 1000*60*60*24*6;
	d = new Date(d);
	var year = d.getFullYear();
	var mon = d.getMonth()+1;
	var day = d.getDate();
	s = year+"-"+(mon<10?('0'+mon):mon)+"-"+(day<10?('0'+day):day);
return s;
}

//获取指定日期前七天

function getBeforeMonth(d){
	d = new Date(d);
	var year = d.getFullYear();
	var mon = d.getMonth();
	var day = d.getDate();
	s = year+"-"+(mon<10?('0'+mon):mon)+"-"+(day<10?('0'+day):day);
return s;
}




