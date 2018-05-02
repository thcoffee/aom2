from aom import db
import pymysql
import time

#继承db.opMysqlObj
class opMysqlObj(db.opMysqlObj):

    def __init__(self,**kwages):
         
        db.opMysqlObj.__init__(self,**kwages)
        
    '''
    获取统计信息 
    方法kwage {'begindate':'2018-04-26','enddate':'2018-04-26'}
    '''    
    def getStatistics(self,**kwages):
        if kwages['begindate']!='':
            begindate=kwages['begindate']
        else:
            begindate=time.strftime('%Y-%m-%d', time.localtime(time.time()-(86448*7)))   
        if kwages['enddate']!='':
            enddate=kwages['enddate']+' 23:59:59'
        else:
            enddate=time.strftime('%Y-%m-%d', time.localtime(time.time()) ) 
                      
        sql1="SELECT b.warnname warntype,count FROM(SELECT warntype,COUNT(*) count FROM pps_warntask where createtime <='%s' and  createtime >='%s' GROUP BY warntype ) a LEFT JOIN pps_warntype b ON a.warntype=b.warntype"%(enddate,begindate)
        sql2="SELECT b.enviname,a.count FROM (SELECT enviname,COUNT(*) count FROM pps_warntask where createtime <='%s' and  createtime >='%s' GROUP BY enviname) a  LEFT JOIN pps_envitype b ON a.enviname=b.envitype"%(enddate,begindate)
        sql3="select levelname warnlevel,count FROM (SELECT warnlevel,COUNT(*) count FROM pps_warntask where createtime <='%s' and  createtime >='%s' GROUP BY warnlevel ) a LEFT JOIN pps_warnlevel b ON a.warnlevel=b.level" %(enddate,begindate) 
        return_json={}        
        return_json['warntype']=self.getData(**{'sql':sql1})
        return_json['enviname']=self.getData(**{'sql':sql2})
        return_json['warnlevel']=self.getData(**{'sql':sql3})
        return(return_json)
     
    #获取历史预警信息     
    def getQueryWarn(self,**kwages):
        sql="SELECT CONCAT(substring(warndesc,1,30),'......') warndesc,date_format(createtime,'%Y-%m-%d %H:%i:%s') createtime,case when status=1 then '待处理' when status=2 then '待审核'  when status=3 then '已完成' end status,CONCAT('/pps/querywarninfo/?id=',id) url FROM pps_warntask order by createtime desc LIMIT 0,1000"
        return(self.getData(**{'sql':sql}))
    '''
    排它获取是否存在该预警信息,引入**kwages
    status 填写预警信息对应状态 1待处理 2待审核 3处理完毕
    '''
    def getWarnTaskForUpdate(self,**kwages):
        sql="select a.id,warnid,a.warntype,enviname,warndesc,warnlevel,DATE_FORMAT(createtime, '%Y-%m-%d %H:%i:%s') createtime,DATE_FORMAT(recoverytime, '%Y-%m-%d %H:%i:%s') recoverytime,reason,measure,DATE_FORMAT(writetime, '%Y-%m-%d %H:%i:%s') writetime,status,messid,a.userid,b.auduserid FROM pps_warntask a LEFT JOIN pps_warntype b ON a.warntype=b.warntype where status="+str(kwages['status'])+" and a.id="+str(kwages['id'])+" for update"
        return(self.getData(**{'sql':sql}))
    
    '''
    设置消息状态,引入**kwages  
    fromstatus 从什么状态 (1是未读，2是已读)
    tostatus  变更为什么状态
    messid 消息id
    '''  
    def setMessStatus(self,**kwages):
        sql="update pps_message set status=%s,completetime=now() where status=%s and id=%s"%(kwages['tostatus'],kwages['fromstatus'],kwages['messid'])
        self.putData(**{'sql':sql})
    '''
    新建预警信息审核消息,引入**kwages 
    warntaskMsg  审核意见
    id  warntask的主键id
    userid  用户id
    status  1是同意 2是不同意
    '''
    def createWarnTaskAudMess(self,**kwages):
        sql="insert into pps_warntask_message(createtime,message,wid,uid,status) values(now(),'%s',%s,%s,%s) "%(pymysql.escape_string(kwages['warntaskMsg']),kwages['id'],kwages['userid'],kwages['status'])
        self.putData(**{'sql':sql})
    
    '''
    设置预警信息状态,引入**kwages 
    fromstatus 从什么状态 (1待处理 2待审核 3处理完毕)
    tostatus  变更为什么状态
    id  预警信息主键id
    '''    
    def setWarnTaskStatus(self,**kwages):
        sql="update pps_warntask set status=%s where status=%s and id=%s"%(kwages['tostatus'],kwages['fromstatus'],kwages['id'])
        self.putData(**{'sql':sql})
    '''
    对预警任务设置消息id,引入**kwages 
    lastid 消息id
    id  taskwarn的主键id
    '''
    def setWarnTaskMessId(self,**kwages):
        sql="update pps_warntask set messid=%s where id=%s"%(kwages['lastid'],kwages['id'])
        self.putData(**{'sql':sql})
    '''
    获取所有审核消息 ,引入**kwages 
    id  taskwarn的主键id   
    '''    
    def getWarnTaskAudMessS(self,**kwages):
        sql="SELECT date_format(p.createtime, '%Y-%m-%d %H:%i:%s') createtime,p.message,a.first_name name,CASE WHEN p.status=1 THEN '不同意' ELSE '同意'  END STATUS  FROM pps_warntask_message p LEFT JOIN auth_user a ON p.uid=a.id where wid='"+kwages['id']+"'ORDER BY createtime desc"
        #print(sql)
        return(self.getData(**{'sql':sql}))
    
    '''
    获取审核消息最新的一条 ,引入**kwages 
    id  taskwarn的主键id  
    '''
    def getWarnTaskAudMess(self,**kwages):
        temp={}
        for i in self.getWarnTaskAudMessS(**kwages):
            temp=i
            break
        return(temp)    
    
    '''
    设置预警信息，将原因和预防措施录入    ,引入**kwages 
    reason 原因
    measure  预防措施
    status  状态 (1待处理 2待审核 3处理完毕)
    id taskwarn的主键id  
    '''
    def setWarnTaskInfo(self,**kwages):
        sql="update pps_warntask set reason='%s',measure='%s',writetime=now(),status=%s where status=1 and id=%s"%(pymysql.escape_string(kwages['reason']),pymysql.escape_string(kwages['measure']),kwages['status'],kwages['id'])
        self.putData(**{'sql':sql})
    '''    
    获取预警信息详情  ,引入**kwages 
    userid  用户id
    id  taskwarn的主键id  
    '''
    def getWarnTask(self,**kwages):
        sql="SELECT a.id,warnid,c.warnname warntype,d.enviname,warndesc,b.levelname warnlevel,DATE_FORMAT(createtime, '%Y-%m-%d %H:%i:%s') createtime,DATE_FORMAT(recoverytime, '%Y-%m-%d %H:%i:%s') recoverytime,reason,measure,DATE_FORMAT(writetime, '%Y-%m-%d %H:%i:%s') writetime,STATUS,messid,a.userid FROM pps_warntask a LEFT JOIN  pps_warnlevel b ON a.`warnlevel`=b.level LEFT JOIN pps_warntype c ON a.warntype=c.warntype LEFT JOIN pps_envitype d ON a.enviname=d.envitype WHERE a.userid="+str(kwages['userid'])+" and a.id='"+kwages['id']+"'"
        temp=self.getData(**{'sql':sql})
        if len(temp)>0:
            return(temp[0])
        else:
            return({})
    '''
    获取warntask对用的用户id,引入**kwages 
    id taskwarn的主键id 
    '''
    def getWarnTaskUserid(self,**kwages):
        sql="SELECT userid FROM pps_warntask WHERE  id='"+kwages['id']+"'"
        #print(sql)
        temp=self.getData(**{'sql':sql})
        if len(temp)>0:
            return(temp[0]['userid'])
        else:
            return(0)
    '''
    #获取待处理消息条,引入**kwages 
    userid 用户id
    '''
    def getUndoMess(self,**kwages):
        sql="select activityname,date_format(createtime, '%Y-%m-%d %H:%i:%s') createtime,path from pps_message where status=1 and userid="+str(kwages['userid'])+"  order by createtime desc"
        return(self.getData(**{'sql':sql}))
    
    '''
    获取预警等级名字，输入{'level':2} 返回一个字典{'levelname':'严重'}
     '''    
    def getWarnLevelName(self,**kwages):
        sql="select levelname from pps_warnlevel where level=%s"%(kwages['level'])
        return_json=self.getData(**{'sql':sql})
        if len(return_json)>0:
            return(return_json['levelname'])
        else:
            return({'levelname':'未知'})
            
    def isExistsWarn(self,**kwages):
        sql="select count(*) count from pps_warntask where warnid='%s'"%(kwages['id'])
        if self.getData(**{'sql':sql})[0]['count']>0:
            return(False)
        else:
            return(True)
            
    def getUserid(self,**kwages):
        sql="select userid from pps_warntype where warntype='%s'"%(kwages['type'])
        temp=self.getData(**{'sql':sql})
        if len(temp)>0:
            return(temp[0]['userid'])
        else:
            return(1)
            
    def createWarn(self,**kwages):
        sql="insert into pps_warntask(warnid,warntype,enviname,warndesc,warnlevel,createtime,status,userid)values(%s,'%s','%s','%s','%s',now(),1,%s)"%(kwages['id'],kwages['type'],kwages['evn'],kwages['msg'],str(self.getWarnLevel(**{'levelname':kwages['level']})),kwages['userid'])
        self.putData(**{'sql':sql})   
    
    def getWarnLevel(self,**kwages):
        sql="select level from pps_warnlevel where levelname='%s'"%(kwages['levelname'])
        temp=self.getData(**{'sql':sql})
        if len(temp)>0:
            return(temp[0]['level'])
        else:
            return(5)  

    def createWarnMsg(self,**kwages):
        
        self.createMess(**{'activityname':self.getWarnTypeName(**kwages)+'预警','path':'/pps/dowarn/?id='+kwages['wid'],'userid':kwages['userid']})
        pass   
    
    #设置恢复时间
    def setWarnRecoveryTime(self,**kwages):
        sql="update pps_warntask set recoverytime=now() where warnid=%s" %(kwages['id'])           
        self.putData(**{'sql':sql}) 
        
    #获取预警类型的名字        
    def getWarnTypeName(self,**kwages):
        sql="select warnname from pps_warntype where warntype='%s'"%(kwages['type'])
        temp=self.getData(**{'sql':sql})
        if len(temp)>0:
            return(temp[0]['warnname'])
        else:
            return("未知")
    #获取环境名       
    def getEnviName(self,**kwages):
        sql="select enviname from pps_envitype where envitype='%s'"%(kwages['enviname'])
        temp=self.getData(**{'sql':sql})
        if len(temp)>0:
            return(temp[0]['enviname'])
        else:
            return("未知环境")