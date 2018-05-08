from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import traceback
import simplejson
import json
import logging
from . import ppsdb
logger = logging.getLogger("django")
@csrf_exempt
def api(request):
    try:
        logger.info(simplejson.loads(request.body))
        postJson=simplejson.loads(request.body)
        if postJson['task']=='warntask':
            return HttpResponse(json.dumps(_puttask(**{'postJson':postJson})),content_type='application/json')
        else:
            return HttpResponse(json.dumps({"msg":"unKnow"}),content_type='application/json')
    except Exception as info: 
        logger.error(traceback.format_exc())
        return HttpResponse(json.dumps({"msg":"error","content":str(traceback.format_exc())}),content_type='application/json')
        
        
def _puttask(**kwages):
    task=kwages['postJson']['data']
    dbcon=ppsdb.opMysqlObj(**{'dbname':'default','valueType':'dict'})
    if dbcon.isExistsWarn(**task):     
        dbcon.createWarn(**task)
        task['wid']=str(dbcon.getLaseID())
        for i in dbcon.getUserid(**task):
            task['userid']=i['userid']
            dbcon.createWarnMsg(**task)
            dbcon.create_warntask_w2m(**{'wid':task['wid'],'mid':str(dbcon.getLaseID())})            
        #dbcon.setWarnTaskMessId(**{'lastid':str(dbcon.getLaseID()),'id':task['wid']})
    else:
        dbcon.setWarnRecoveryTime(**task)
    dbcon.commit()
    dbcon.close()