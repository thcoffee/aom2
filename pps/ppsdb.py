from aom import db
import pymysql
import time

class opMysqlObj(db.opMysqlObj):

    def __init__(self,**kwages):
        db.opMysqlObj.__init__(self,**kwages)
        
    #获取统计信息    
    def getStatistics(self,**kwages):
        if kwages['begindate']!='':
            begindate=kwages['begindate']
        else:
            begindate=time.strftime('%Y-%m-%d', time.localtime(time.time()-(86448*7)))   
        if kwages['enddate']!='':
            enddate=kwages['enddate']+' 23:59:59'
        else:
            enddate=time.strftime('%Y-%m-%d', time.localtime(time.time()) ) 
                      
        sql1="SELECT warntype,COUNT(*) count FROM pps_warntask where createtime <='%s' and  createtime >='%s' GROUP BY warntype"%(enddate,begindate)
        sql2="SELECT enviname,COUNT(*) count FROM pps_warntask where createtime <='%s' and  createtime >='%s' GROUP BY enviname"%(enddate,begindate)
        sql3="select levelname warnlevel,count FROM (SELECT warnlevel,COUNT(*) count FROM pps_warntask where createtime <='%s' and  createtime >='%s' GROUP BY warnlevel ) a LEFT JOIN pps_warnlevel b ON a.warnlevel=b.level" %(enddate,begindate) 
        print(kwages,sql1,sql2,sql3)
        return_json={}        
        return_json['warntype']=self.getData(**{'sql':sql1})
        return_json['enviname']=self.getData(**{'sql':sql2})
        return_json['warnlevel']=self.getData(**{'sql':sql3})
        return(return_json)
     
    #获取历史预警信息     
    def getQueryWarn(self,**kwages):
       #print(str(kwages['id']))
        sql="SELECT CONCAT(substring(warndesc,1,30),'......') warndesc,date_format(createtime,'%Y-%m-%d %H:%i:%s') createtime,case when status=1 then '待处理' when status=2 then '待审核'  when status=3 then '已完成' end status,CONCAT('/pps/querywarninfo/?id=',id) url FROM pps_warntask order by createtime desc"
        return(self.getData(**{'sql':sql}))
    
    #排它获取是否存在该预警信息    
    def getWarnTaskForUpdate(self,**kwages):
        sql="select a.id,warnid,a.warntype,enviname,warndesc,warnlevel,DATE_FORMAT(createtime, '%Y-%m-%d %H:%i:%s') createtime,DATE_FORMAT(recoverytime, '%Y-%m-%d %H:%i:%s') recoverytime,reason,measure,DATE_FORMAT(writetime, '%Y-%m-%d %H:%i:%s') writetime,status,messid,a.userid,b.auduserid FROM pps_warntask a LEFT JOIN pps_warntype b ON a.warntype=b.warntype where status="+str(kwages['status'])+" and a.id="+str(kwages['id'])+" for update"
        return(self.getData(**{'sql':sql}))
    
    #设置消息状态    
    def setMessStatus(self,**kwages):
        sql="update pps_message set status=%s,completetime=now() where status=%s and id=%s"%(kwages['tostatus'],kwages['fromstatus'],kwages['messid'])
        self.putData(**{'sql':sql})
    
    #新建预警任务对应的消息
    def createWarnTaskMess(self,**kwages):
        sql="insert into pps_warntask_message(createtime,message,wid,uid,status) values(now(),'%s',%s,%s,%s) "%(pymysql.escape_string(kwages['warntaskMsg']),kwages['id'],kwages['userid'],kwages['status'])
        self.putData(**{'sql':sql})
    
    #设置预警信息状态    
    def setWarnTaskStatus(self,**kwages):
        sql="update pps_warntask set status=%s where status=%s and id=%s"%(kwages['tostatus'],kwages['fromstatus'],kwages['id'])
        self.putData(**{'sql':sql})
    
    #对预警任务设置消息id
    def setWarnTaskMessId(self,**kwages):
        sql="update pps_warntask set messid=%s where id=%s"%(kwages['lastid'],kwages['id'])
        self.putData(**{'sql':sql})
    
    #获取所有审核消息    
    def getWarnTaskMessS(self,**kwages):
        sql="SELECT date_format(p.createtime, '%Y-%m-%d %H:%i:%s') createtime,p.message,a.first_name name,CASE WHEN p.status=1 THEN '不同意' ELSE '同意'  END STATUS  FROM pps_warntask_message p LEFT JOIN auth_user a ON p.uid=a.id where wid='"+kwages['id']+"'ORDER BY createtime desc"
        #print(sql)
        return(self.getData(**{'sql':sql}))
    
    
    #获取审核消息最新的一条
    def getWarnTaskMess(self,**kwages):
        temp={}
        for i in self.getWarnTaskMessS(**kwages):
            temp=i
            break
        return(temp)    
    

    #设置预警信息，将原因和预防措施录入    
    def setWarnTaskInfo(self,**kwages):
        sql="update pps_warntask set reason='%s',measure='%s',writetime=now(),status=%s where status=1 and id=%s"%(pymysql.escape_string(kwages['reason']),pymysql.escape_string(kwages['measure']),kwages['status'],kwages['id'])
        self.putData(**{'sql':sql})
        
    #获取预警信息详情，输入id，获取对应id信息    
    def getWarnTask(self,**kwages):
        sql="SELECT a.id,warnid,warntype,enviname,warndesc,b.levelname warnlevel,DATE_FORMAT(createtime, '%Y-%m-%d %H:%i:%s') createtime,DATE_FORMAT(recoverytime, '%Y-%m-%d %H:%i:%s') recoverytime,reason,measure,DATE_FORMAT(writetime, '%Y-%m-%d %H:%i:%s') writetime,STATUS,messid,userid FROM pps_warntask a LEFT JOIN  pps_warnlevel b ON a.`warnlevel`=b.level WHERE a.userid="+str(kwages['userid'])+" and a.id='"+kwages['id']+"'"
        temp=self.getData(**{'sql':sql})
        if len(temp)>0:
            return(temp[0])
        else:
            return({})
    
    def getWarnTaskUserid(self,**kwages):
        sql="SELECT userid FROM pps_warntask WHERE  id='"+kwages['id']+"'"
        #print(sql)
        temp=self.getData(**{'sql':sql})
        if len(temp)>0:
            return(temp[0]['userid'])
        else:
            return(0)
    #获取待处理消息条
    def getUndoMess(self,**kwages):
        sql="select activityname,date_format(createtime, '%Y-%m-%d %H:%i:%s') createtime,path from pps_message where status=1 and userid="+str(kwages['userid'])+"  order by createtime desc"
        return(self.getData(**{'sql':sql}))
    
    '''
    获取预警等级名字，输入{'level':2} 返回一个字典{'levelname':'严重'}
     '''    
    def getWarnLevelName(self,**kwages):
        sql="select levelname from pps_warnlevel where level=%s"%(kwages['level'])
        return(self.getData(**{'sql':sql})['levelname'])
        