$(function () {
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
    });
	
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
		data: ["ERP正式机","电商正式机","ERP测试机","电商测试机","山西正式机"]
   },
   yAxis: {},
   series: [{
		name: '报警数量',
		type: 'bar',
		data: ["11","22","33","4","25"]
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
		data: ["中间件","数据库","主机"]
   },
   yAxis: {},
   series: [{
		name: '报警数量',
		type: 'bar',
		data: ["11","22","33"]
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
		data: ["灾难","严重","一般严重","一般"]
   },
   yAxis: {},
   series: [{
		name: '报警数量',
		type: 'bar',
		data: ["11","22","33","4"]
   }]
});


