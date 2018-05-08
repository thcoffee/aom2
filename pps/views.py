from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib import auth
from aom import custom
from . import ppsdb
import traceback
import simplejson
import json
import time
import sys
import logging
logger = logging.getLogger("django")
#logger = logging.getLogger(__name__)
# Create your views here.

#页面访问权限验证妆饰器
def _auth_page(view): 
    
    #自动登录方法
    def aauth(request, *args, **kwargs): 
        #登录动作
        user = authenticate(username=request.GET.get('empNo',''), password='tcxt'+request.GET.get('empNo',''))
        if user is not None:
            login(request, user)
        return view(request, *args, **kwargs)

    #主方法
    def main(request, *args, **kwargs)  :  
        #判断是否登录了
        if request.user.is_authenticated: 
            #如果登录了直接访问对应方法
            return view(request, *args, **kwargs)          
        else:
            #如果没有登录运行aauth
            return aauth(request, *args, **kwargs)   
            
    return main



#首页 

@_auth_page 
def index(request):
    return HttpResponse('''<meta http-equiv="refresh" content="0;url=/pps/undo/">''')

#待处理消息
#@_auth_page  
@login_required(login_url="/admin/login/")   
def undo(request):
    return render(request, 'undo.html',{})

#处理预警消息
@login_required(login_url="/admin/login/")   
def dowarn(request):
    return render(request, 'dowarn.html',{})

#查看预警列表信息
@login_required(login_url="/admin/login/")  
def querywarn(request):
    return render(request, 'querywarn.html',{})


#查看预警信息
@login_required(login_url="/admin/login/")  
def querywarninfo(request):
    return render(request, 'querywarninfo.html',{})

#审核    
@login_required(login_url="/admin/login/")     
def review(request):
    return render(request, 'review.html',{})

#统计
@login_required(login_url="/admin/login/")  
def tjwarn(request):
    return render(request, 'tjwarn.html',{})

#ajax获取入口    
@csrf_exempt
@login_required(login_url="/admin/login/")     	
def getdata(request):
    return HttpResponse(json.dumps({"name":"liuyanli"}), content_type='application/json')	
	
#ajax提交入口
@csrf_exempt
@login_required(login_url="/admin/login/")  		
def putdata(request):
    try:
        if request.POST.get('task')=='test':
            return HttpResponse(json.dumps({"name":"liuyanli"}), content_type='application/json')	
        #获取待处理消息    
        elif request.POST.get('task')=='getundo':	
            return HttpResponse(json.dumps(_getUndoJson(request)), content_type='application/json')	
        #获取预警信息    
        elif request.POST.get('task')=='getwarn':
            return HttpResponse(json.dumps(_getWarnJson(request)), content_type='application/json')
        #获取审计信息    
        elif request.POST.get('task')=='getaut':
            return HttpResponse(json.dumps(_getWarnJson(request)), content_type='application/json')
        #提交预警信息处理    
        elif request.POST.get('task')=='putwarn':
            return HttpResponse(json.dumps(_putWarnJson(request)), content_type='application/json') 
        #提交审核信息    
        elif request.POST.get('task')=='putaud':
            return HttpResponse(json.dumps(_putAudJson(request)), content_type='application/json') 
        #提交请求获取预警信息查询    
        elif request.POST.get('task')=='putquerywarn':
            return HttpResponse(json.dumps(_getQueryWarn(request)), content_type='application/json') 
        #获取预警信息查询详细内容    
        elif request.POST.get('task')=='getquerywarninfo':
            return HttpResponse(json.dumps(_getWarnJson(request)), content_type='application/json') 
        #获取统计信息    
        elif request.POST.get('task')=='gettjwarn':
            return HttpResponse(json.dumps(_getTjwarn(request)), content_type='application/json')     
        else:
            return HttpResponse(json.dumps({"name":"liuyanli"}), content_type='application/json')
    except Exception as info:
        logger.error(traceback.format_exc())
@csrf_exempt		
def test(request):
    print(a)
    try:
        print(simplejson.loads(request.body))
        #print(a)
        return_json={'a':'b'}
        return HttpResponse(json.dumps({"name":"liuyanli"}),content_type='application/json')
    except Exception as info: 
        print(traceback.format_exc())
        return HttpResponse(json.dumps({"msg":"error","content":str(traceback.format_exc())}),content_type='application/json')
    #return render(request, 'test.html',{'id':'hell'})

#获取统计信息
def _getTjwarn(request):
    dbcon=ppsdb.opMysqlObj(**{'dbname':'default','valueType':'dict'})
    return_json=dbcon.getStatistics(**{'begindate':request.POST.get('begindate'),'enddate':request.POST.get('enddate')})
    return(return_json)  

#获取警告记录    
def _getQueryWarn(request):
    temp=[]
    for i in range(123):
        temp.append({'warndesc':'预警'+str(i),'createtime':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+(86448*i))),'status':'完成','url':'/pps/querywarninfo/?id='+str(i)})
    dbcon=ppsdb.opMysqlObj(**{'dbname':'default','valueType':'dict'})
    temp=dbcon.getQueryWarn(**{'id':request.POST.get('id')})
    p=custom._my_pagination(request,temp,request.POST.get('display_num',5))
    return_json={'list':p['list'],'total_num':len(temp),'num_pages':p['num_pages']}   
    return(return_json)
    
#获取审批页面信息    
def _putAudJson(request):
    try:
        dbcon=ppsdb.opMysqlObj(**{'dbname':'default','valueType':'dict'})
        #排它锁查看是否有该条信息
        warnTaskCount=dbcon.getWarnTaskForUpdate(**{'id':request.POST.get('id',0),'status':2})
        #如果有该条信息
        if len(warnTaskCount)!=0:
            #将消息状态变更为已处理
            #dbcon.setMessStatus(**{'fromstatus':1,'tostatus':2,'messid':request.POST.get('messid')})
            for i in dbcon.getMessageId(**{'wid':request.POST.get('id')}) :           
                dbcon.setMessStatus(**{'fromstatus':1,'tostatus':2,'messid':i['mid']}) 
            #创建一条审核意见
            dbcon.createWarnTaskAudMess(**{'warntaskMsg':request.POST.get('warntaskMsg'),'id':request.POST.get('id',0),'status':request.POST.get('status'),'userid':request.user.id})
            #如果同意
            if request.POST.get('status')=='1':
                #将预警信息标注为以处理完毕
                dbcon.setWarnTaskStatus(**{'fromstatus':2,'tostatus':3,'id':request.POST.get('id',0)})
            else:
                #不同意将预警信息状态从待审核变更为待处理
                dbcon.setWarnTaskStatus(**{'fromstatus':2,'tostatus':1,'id':request.POST.get('id',0)})
                #给处理人重新发消息
                dbcon.createMess(**{'activityname':'重新处理','path':'/pps/dowarn/?id='+request.POST.get('id'),'userid':dbcon.getWarnTaskUserid(**{'id':request.POST.get('id',0)})})
                #更新预警信息对应的消息id
                #dbcon.setWarnTaskMessId(**{'lastid':dbcon.getLaseID(),'id':request.POST.get('id',0)})
                dbcon.create_warntask_w2m(**{'wid':request.POST.get('id'),'mid':str(dbcon.getLaseID())})
            dbcon.commit()
            #获取预警信息对应的审核意见
            warntaskMsg=dbcon.getWarnTaskAudMessS(**{'id':request.POST.get('id',0)})
            dbcon.close()
            return_json={'status':'true','warntaskMsg':warntaskMsg}
        else:
            dbcon.commit()
            dbcon.close()
            return_json={'status':'false','warntaskMsg':[]}
            
    except Exception as info:
        print(traceback.format_exc())
        return_json={'status':'false','warntaskMsg':[]}
    return(return_json)    



#提交处理预警信息表单信息    
def _putWarnJson(request):
    try:
        dbcon=ppsdb.opMysqlObj(**{'dbname':'default','valueType':'dict'})
        #排它锁查看是否有该条信息
        warnTaskCount=dbcon.getWarnTaskForUpdate(**{'id':request.POST.get('id'),'status':1})
        #如果有该条信息
        if len(warnTaskCount)!=0:
            #如果预警级别小于3级
            for i in dbcon.getMessageId(**{'wid':request.POST.get('id')}) :           
                dbcon.setMessStatus(**{'fromstatus':1,'tostatus':2,'messid':i['mid']})  
                
            if warnTaskCount[0]['warnlevel']<3:
                #预警信息变为待审核
                dbcon.setWarnTaskInfo(**{'reason':request.POST.get('reason'),'measure':request.POST.get('measure'),'id':request.POST.get('id'),'status':2,'userid':request.user.id})
                #发出待审核消息
                dbcon.createMess(**{'activityname':'待审核','path':'/pps/review/?id='+request.POST.get('id'),'userid':warnTaskCount[0]['auduserid']})   
                #将将待审核消息id写入预警信息中。
                dbcon.create_warntask_w2m(**{'wid':request.POST.get('id'),'mid':str(dbcon.getLaseID())})
            else:
                #否则直接将预警信息变更问以处理完毕。
                dbcon.setWarnTaskInfo(**{'reason':request.POST.get('reason'),'measure':request.POST.get('measure'),'id':request.POST.get('id'),'status':3})
            #将消息状态设置为已读。
             
                         
        dbcon.commit()
        dbcon.close()
        return_json={'status':'true'}
    except Exception as info: 
        logger.error(traceback.format_exc())
        return_json={'status':'false'}
    return(return_json)


#获取处理预警信息表单信息
def _getWarnJson(request):
    dbcon=ppsdb.opMysqlObj(**{'dbname':'default','valueType':'dict'})
    #如果是处理警告信息页面 或者是查询预警信息详细页面 
    if request.POST.get('task')=='getwarn' :
        return_json=dbcon.getWarnTask(**{'id':request.POST.get('id'),'userid':request.user.id})
        return_json['warntaskMsg']=dbcon.getWarnTaskAudMess(**{'id':request.POST.get('id')})
    #如果是审核信息页面
    elif request.POST.get('task')=='getquerywarninfo':
        userid=dbcon.getWarnTaskUserid(**{'id':request.POST.get('id')})
        return_json=dbcon.getWarnTask(**{'id':request.POST.get('id'),'userid':userid})
        return_json['warntaskMsg']=dbcon.getWarnTaskAudMess(**{'id':request.POST.get('id')})
    elif request.POST.get('task')=='getaut':
        userid=dbcon.getWarnTaskUserid(**{'id':request.POST.get('id')})
        return_json=dbcon.getWarnTask(**{'id':request.POST.get('id'),'userid':userid})
        return_json['warntaskMsg']=dbcon.getWarnTaskAudMessS(**{'id':request.POST.get('id')})    
    return(return_json)


#获取未处理消息

def _getUndoJson(request):	
    dbcon=ppsdb.opMysqlObj(**{'dbname':'default','valueType':'dict'})	
    #获取对应用户的未处理消息
    undoList=dbcon.getUndoMess(**{'userid':request.user.id})
    #分页处理
    p=custom._my_pagination(request,undoList,request.POST.get('display_num',5))
    return_json={'list':p['list'],'undo_num':len(undoList),'num_pages':p['num_pages']}	
    return(return_json)
	

