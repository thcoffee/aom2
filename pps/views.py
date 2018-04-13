from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator
import traceback
import json
from aom import db
# Create your views here.
@login_required(login_url="/admin/login/") 
def index(request):
    return HttpResponse('''<meta http-equiv="refresh" content="0;url=/pps/undo/">''')

@login_required(login_url="/admin/login/")     
def undo(request):
    return render(request, 'undo.html',{})

@login_required(login_url="/admin/login/")     
def dowarn(request):
    return render(request, 'dowarn.html',{})
    
@login_required(login_url="/admin/login/")     
def review(request):
    return render(request, 'review.html',{})
    	
@csrf_exempt	
def getdata(request):
    return HttpResponse(json.dumps({"name":"liuyanli"}), content_type='application/json')	
	
#@login_required(login_url="/admin/login/") 	
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

def _putAudJson(request):
    try:
        dbcon=db.opMysqlObj(**{'dbname':'default','valueType':'dict'})
        
        sql="update pps_message set status=2,completetime=now() where id=%s"%(request.POST.get('messid'))
        print(sql)
        dbcon.putData(sql=sql)
        
        sql="insert into pps_warntask_message(createtime,message,wid,uid,status) values(now(),'%s',%s,1,%s) "%(request.POST.get('warntaskMsg'),request.POST.get('id'),request.POST.get('status'))
        print(sql)
        dbcon.putData(sql=sql)
        if request.POST.get('status')==1:
            sql="update pps_warntask set status=3 where status=2 and id=%s"%(request.POST.get('id'))
            print(sql)
            dbcon.putData(sql=sql)
        else:
            sql="update pps_warntask set status=1 where status=2 and id=%s"%(request.POST.get('id'))
            print(sql)
            dbcon.putData(sql=sql)
            sql="insert into  pps_message (createtime,activityname,path,userid,status)values(now(),'%s','%s',%s,1)"%('重新处理','/pps/dowarn/?id='+request.POST.get('id'),1)
            print(sql)
            dbcon.putData(sql=sql)
            sql="update pps_warntask set messid=%s where id=%s"%(dbcon.getLaseID()['lastid'],request.POST.get('id'))
            print(sql)
            dbcon.putData(sql=sql)
        dbcon.commit()
        sql="SELECT date_format(p.createtime, '%Y-%m-%d %H:%i:%s') createtime,p.message,a.first_name name,CASE WHEN p.status=1 THEN '不同意' ELSE '同意'  END STATUS  FROM pps_warntask_message p LEFT JOIN auth_user a ON p.uid=a.id where wid='"+request.POST.get('id')+"'ORDER BY createtime "
        warntaskMsg=dbcon.getData(**{'sql':sql}) 
        dbcon.close()
        return_json={'status':'true','warntaskMsg':warntaskMsg}
    except Exception as info: 
        print(traceback.format_exc())
        return_json={'status':'false'}
    return(return_json)    
    
def _putWarnJson(request):
    try:
        dbcon=db.opMysqlObj(**{'dbname':'default','valueType':'dict'})
        sql="update pps_warntask set reason='%s',measure='%s',writetime=now(),status=2 where status=1 and id=%s"%(request.POST.get('reason'),request.POST.get('measure'),request.POST.get('id'))
        print(sql)
        dbcon.putData(sql=sql)
        sql="update pps_message set status=2,completetime=now() where id=%s"%(request.POST.get('messid'))
        dbcon.putData(sql=sql)
        print(sql)
        sql="insert into  pps_message (createtime,activityname,path,userid,status)values(now(),'%s','%s',%s,1)"%('待审核','/pps/review/?id='+request.POST.get('id'),1)
        print(sql)
        dbcon.putData(sql=sql)
        #lastid=dbcon.getLaseID()
       # print(lastid)
        sql="update pps_warntask set messid=%s where id=%s"%(dbcon.getLaseID()['lastid'],request.POST.get('id'))
        print(sql)
        dbcon.putData(sql=sql)
        dbcon.commit()
        dbcon.close()
        return_json={'status':'true'}
    except Exception as info: 
        print(traceback.format_exc())
        return_json={'status':'false'}
    return(return_json)
	
def _getWarnJson(request):
    dbcon=db.opMysqlObj(**{'dbname':'default','valueType':'dict'})
    sql="select id,warnid,warntype,enviname,warndesc,warnlevel,date_format(createtime, '%Y-%m-%d %H:%i:%s') createtime,date_format(recoverytime, '%Y-%m-%d %H:%i:%s') recoverytime,reason,measure,date_format(writetime, '%Y-%m-%d %H:%i:%s') writetime,status,messid,userid from pps_warntask where id='"+request.POST.get('id')+"'"
    
    temp=dbcon.getData(**{'sql':sql})
    
    if len(temp)>0:
        return_json=temp[0]
    else:
        return_json={}
    sql="SELECT date_format(p.createtime, '%Y-%m-%d %H:%i:%s') createtime,p.message,a.first_name name,CASE WHEN p.status=1 THEN '不同意' ELSE '同意'  END STATUS  FROM pps_warntask_message p LEFT JOIN auth_user a ON p.uid=a.id where wid='"+request.POST.get('id')+"'ORDER BY createtime "
    if request.POST.get('task')=='getwarn':
        sql=sql+' desc'

    temp1=dbcon.getData(**{'sql':sql}) 
    if len(temp1)>0:
        if request.POST.get('task')=='getwarn':
            return_json['warntaskMsg']=temp1[0]
        elif request.POST.get('task')=='getaut':
            return_json['warntaskMsg']=temp1
    else:
        if request.POST.get('task')=='getwarn':
            return_json['warntaskMsg']={} 
        elif request.POST.get('task')=='getaut':
            return_json['warntaskMsg']=[]
    print(return_json)    
    return(return_json)
    
def _getUndoJson(request):	
    temp=[]
    for i in range(30):
        temp.append(['预警'+str(i),'2018-01-'+str(i)+' 00:00:00'])
    dbcon=db.opMysqlObj(**{'dbname':'default','valueType':'dict'})	
    temp=dbcon.getData(**{'sql':"select activityname,date_format(createtime, '%Y-%m-%d %H:%i:%s') createtime,path from pps_message where status=1 order by createtime desc"})
    p=_my_pagination(request,temp,request.POST.get('display_num',5))
    return_json={'list':p['list'],'undo_num':len(temp),'num_pages':p['num_pages']}	
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