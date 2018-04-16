from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator
import traceback
import json
import time
from . import ppsdb
# Create your views here.

#首页
@login_required(login_url="/admin/login/") 
def index(request):
    return HttpResponse('''<meta http-equiv="refresh" content="0;url=/pps/undo/">''')

#待处理消息
@login_required(login_url="/admin/login/")     
def undo(request):
    return render(request, 'undo.html',{})

#处理预警消息
@login_required(login_url="/admin/login/")     
def dowarn(request):
    return render(request, 'dowarn.html',{})

#审核    
@login_required(login_url="/admin/login/")     
def review(request):
    return render(request, 'review.html',{})
 
@login_required(login_url="/admin/login/")      
@csrf_exempt	
def getdata(request):
    return HttpResponse(json.dumps({"name":"liuyanli"}), content_type='application/json')	
	
@login_required(login_url="/admin/login/") 	
@csrf_exempt		
def putdata(request):
    #print(request.POST.get('task'))
    if request.POST.get('task')=='test':
        return HttpResponse(json.dumps({"name":"liuyanli"}), content_type='application/json')	
    elif request.POST.get('task')=='getundo':	
        return HttpResponse(json.dumps(_getUndoJson(request)), content_type='application/json')	
    elif request.POST.get('task')=='getwarn':
        return HttpResponse(json.dumps(_getWarnJson(request)), content_type='application/json')
    elif request.POST.get('task')=='getaut':
        return HttpResponse(json.dumps(_getWarnJson(request)), content_type='application/json')
    elif request.POST.get('task')=='putwarn':
        return HttpResponse(json.dumps(_putWarnJson(request)), content_type='application/json') 
    elif request.POST.get('task')=='putaud':
        return HttpResponse(json.dumps(_putAudJson(request)), content_type='application/json') 
    else:
        return HttpResponse(json.dumps({"name":"liuyanli"}), content_type='application/json')
		
def test(request):
    return render(request, 'test.html',{'id':'hell'})


#获取审批页面信息    
def _putAudJson(request):
    try:
        dbcon=ppsdb.opMysqlObj(**{'dbname':'default','valueType':'dict'})
        warnTaskCount=dbcon.getWarnTaskCountForUpdate(**{'id':request.POST.get('id',0),'status':2})
        if warnTaskCount!=0:
            dbcon.setMessStatus(**{'fromstatus':1,'tostatus':2,'messid':request.POST.get('messid')})
            dbcon.createWarnTaskMess(**{'warntaskMsg':request.POST.get('warntaskMsg'),'id':request.POST.get('id',0),'status':request.POST.get('status')})
            if request.POST.get('status')=='1':
                dbcon.setWarnTaskStatus(**{'fromstatus':2,'tostatus':3,'id':request.POST.get('id',0)})
            else:
                dbcon.setWarnTaskStatus(**{'fromstatus':2,'tostatus':1,'id':request.POST.get('id',0)})
                dbcon.createMess(**{'activityname':'重新处理','path':'/pps/dowarn/?id='+request.POST.get('id'),'userid':1})
                dbcon.setWarnTaskMessId(**{'lastid':dbcon.getLaseID()['lastid'],'id':request.POST.get('id',0)})
            dbcon.commit()
            warntaskMsg=dbcon.getWarnTaskMessS(**{'id':request.POST.get('id',0)})
            dbcon.close()
            return_json={'status':'true','warntaskMsg':warntaskMsg}
        else:
            dbcon.commit()
            dbcon.close()
            return_json={'status':'false','warntaskMsg':[]}
            
    except Exception as info: 
        print(traceback.format_exc())
        return_json={'status':'false','warntaskMsg':[]}
    print(return_json)
    return(return_json)    



#提交处理预警信息表单信息    
def _putWarnJson(request):
    try:
        dbcon=ppsdb.opMysqlObj(**{'dbname':'default','valueType':'dict'})
        warnTaskCount=dbcon.getWarnTaskCountForUpdate(**{'id':request.POST.get('id'),'status':1})
        if warnTaskCount!=0:
            dbcon.setWarnTaskInfo(**{'reason':request.POST.get('reason'),'measure':request.POST.get('measure'),'id':request.POST.get('id')})
            dbcon.setMessStatus(**{'fromstatus':1,'tostatus':2,'messid':request.POST.get('messid')})
            dbcon.createMess(**{'activityname':'待审核','path':'/pps/review/?id='+request.POST.get('id'),'userid':1})
            dbcon.setWarnTaskMessId(**{'lastid':dbcon.getLaseID()['lastid'],'id':request.POST.get('id')})
        dbcon.commit()
        dbcon.close()
        return_json={'status':'true'}
    except Exception as info: 
        print(traceback.format_exc())
        return_json={'status':'false'}
    return(return_json)


#获取处理预警信息表单信息
def _getWarnJson(request):
    dbcon=ppsdb.opMysqlObj(**{'dbname':'default','valueType':'dict'})
    return_json=dbcon.getWarnTask(**{'id':request.POST.get('id')})
    if request.POST.get('task')=='getwarn':
        return_json['warntaskMsg']=dbcon.getWarnTaskMess(**{'id':request.POST.get('id')})
    elif request.POST.get('task')=='getaut':
        return_json['warntaskMsg']=dbcon.getWarnTaskMessS(**{'id':request.POST.get('id')})
    print(return_json)    
    return(return_json)


#获取未处理消息

def _getUndoJson(request):	
    dbcon=ppsdb.opMysqlObj(**{'dbname':'default','valueType':'dict'})	
    undoList=dbcon.getUndoMess(**{})
    p=_my_pagination(request,undoList,request.POST.get('display_num',5))
    return_json={'list':p['list'],'undo_num':len(undoList),'num_pages':p['num_pages']}	
    print(return_json)
    return(return_json)
	
#分页
def _my_pagination(request, queryset, display_amount=10, after_range_num = 5,bevor_range_num = 4):
    #按参数分页
    paginator = Paginator(queryset, display_amount)
    try:
        #得到request中的page参数
        page =int(request.POST.get('page'))      
    except:
        #默认为1
        page = 1
    #页码超出范围指向1    
    if page <1 or page >  paginator.num_pages:
        page=1        
    try:
        #尝试获得分页列表
        objects = paginator.page(page)
    #如果页数不存在
    except EmptyPage:
        #获得最后一页
        objects = paginator.page(paginator.num_pages)
    #如果不是一个整数
    except:
        #获得第一页
        objects = paginator.page(1)
    #根据参数配置导航显示范围
    if page >=after_range_num and paginator.num_pages-page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    elif page >= after_range_num and page >paginator.num_pages-after_range_num:
        page_range = paginator.page_range[-(after_range_num+bevor_range_num):]
    else:
        page_range = paginator.page_range[0:bevor_range_num+bevor_range_num+1]
    return ({'list':list(objects),'num_pages':paginator.num_pages})