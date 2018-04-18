from aom import db
import pymysql

class opMysqlObj(db.opMysqlObj):

    def __init__(self,**kwages):
        db.opMysqlObj.__init__(self,**kwages)
        
    def getStatistics(self,**kwages):
        sql1="SELECT warntype,COUNT(*) count FROM pps_warntask GROUP BY warntype"
        sql2="SELECT enviname,COUNT(*) count FROM pps_warntask GROUP BY enviname"
        sql3="SELECT warnlevel,COUNT(*) count FROM pps_warntask GROUP BY warnlevel" 
        return_json={}        
        return_json['warntype']=self.getData(**{'sql':sql1})
        return_json['enviname']=self.getData(**{'sql':sql2})
        return_json['warnlevel']=self.getData(**{'sql':sql3})
        return(return_json)
        
    def getQueryWarn(self,**kwages):
       #print(str(kwages['id']))
        sql="SELECT CONCAT(substring(warndesc,1,30),'......') warndesc,date_format(createtime,'%Y-%m-%d %H:%i:%s') createtime,case when status=1 then '待处理' when status=2 then '待审核'  when status=3 then '已完成' end status,CONCAT('/pps/querywarninfo/?id=',id) url FROM pps_warntask order by createtime desc"
        print(sql)
        return(self.getData(**{'sql':sql}))
        
    def getWarnTaskCountForUpdate(self,**kwages):
        sql="select count(*) count from pps_warntask  where status=%s and id=%s for update"%(kwages['status'],kwages['id'])
        print(sql)
        return(self.getData(**{'sql':sql})[0]['count'])
        
    def setMessStatus(self,**kwages):
        sql="update pps_message set status=%s,completetime=now() where status=%s and id=%s"%(kwages['tostatus'],kwages['fromstatus'],kwages['messid'])
        print(sql)
        self.putData(**{'sql':sql})
    
    def createWarnTaskMess(self,**kwages):
        sql="insert into pps_warntask_message(createtime,message,wid,uid,status) values(now(),'%s',%s,1,%s) "%(pymysql.escape_string(kwages['warntaskMsg']),kwages['id'],kwages['status'])
        self.putData(**{'sql':sql})
        
    def setWarnTaskStatus(self,**kwages):
        sql="update pps_warntask set status=%s where status=%s and id=%s"%(kwages['tostatus'],kwages['fromstatus'],kwages['id'])
        self.putData(**{'sql':sql})
    def createMess(self,**kwages):
        sql="insert into  pps_message (createtime,activityname,path,userid,status)values(now(),'%s','%s',%s,1)"%(kwages['activityname'],kwages['path'],kwages['userid'])
        #print(sql)
        self.putData(**{'sql':sql})
        
    def setWarnTaskMessId(self,**kwages):
        sql="update pps_warntask set messid=%s where id=%s"%(kwages['lastid'],kwages['id'])
        self.putData(**{'sql':sql})
        
    def getWarnTaskMessS(self,**kwages):
        sql="SELECT date_format(p.createtime, '%Y-%m-%d %H:%i:%s') createtime,p.message,a.first_name name,CASE WHEN p.status=1 THEN '不同意' ELSE '同意'  END STATUS  FROM pps_warntask_message p LEFT JOIN auth_user a ON p.uid=a.id where wid='"+kwages['id']+"'ORDER BY createtime desc"
        return(self.getData(**{'sql':sql}))
    
    def getWarnTaskMess(self,**kwages):
        temp={}
        for i in self.getWarnTaskMessS(**kwages):
            temp=i
            break
        return(temp)    
        
    def setWarnTaskInfo(self,**kwages):
        sql="update pps_warntask set reason='%s',measure='%s',writetime=now(),status=2 where status=1 and id=%s"%(pymysql.escape_string(kwages['reason']),pymysql.escape_string(kwages['measure']),kwages['id'])
        self.putData(**{'sql':sql})
        
    def getWarnTask(self,**kwages):
        sql="select id,warnid,warntype,enviname,warndesc,warnlevel,date_format(createtime, '%Y-%m-%d %H:%i:%s') createtime,date_format(recoverytime, '%Y-%m-%d %H:%i:%s') recoverytime,reason,measure,date_format(writetime, '%Y-%m-%d %H:%i:%s') writetime,status,messid,userid from pps_warntask where id='"+kwages['id']+"'"
        temp=self.getData(**{'sql':sql})
        if len(temp)>0:
            return(temp[0])
        else:
            return({})
    
    def getUndoMess(self,**kwages):
        sql="select activityname,date_format(createtime, '%Y-%m-%d %H:%i:%s') createtime,path from pps_message where status=1 order by createtime desc"
        return(self.getData(**{'sql':sql}))
        