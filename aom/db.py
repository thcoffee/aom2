import pymysql
from django.conf import settings
class opMysqlObj(object):
    def __init__(self,**kwages):
        self.databases=kwages['dbname']
        if 'valueType' in  kwages:
            self.valueType=kwages['valueType']
        else:    
            self.valueType='list'
        self._getdb()
        pass
        
    def _getdb(self):
        temp=settings.DATABASES[self.databases]
        temp2={}
        temp2['user'],temp2['password'],temp2['host'],temp2['database'],temp2['port']=temp['USER'],temp['PASSWORD'],temp['HOST'],temp['NAME'],int(temp['PORT'])
        temp2['charset']='utf8'
        if self.valueType=='dict':
            temp2['cursorclass']=pymysql.cursors.DictCursor
        #print(temp2)
        self.db=pymysql.connect(**temp2)
    
    def getLaseID(self):
        return(self.getData(**{'sql':'SELECT LAST_INSERT_ID() lastid'})[0])
    
    def getData(self,**kwages):     
        cur=self.db.cursor()
        cur.execute(kwages['sql'])
        return(cur.fetchall())
        
    def commit(self):
        self.db.commit()    
        
    def putData(self,**kwages):
        cur=self.db.cursor() 
        cur.execute(kwages['sql'])
        
    def close(self):
        self.db.close()
    
