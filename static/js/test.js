
//$(document).ready($.ajax({url:"http://10.68.3.99:8080/pps/putdata/",  
//           data:{'task':'getaut','id':1},
//           dataType:"json",
//           type:"POST",
//           success:dz,
//           }
//    ));   
//
//$(document).ready($.ajax({url:"http://10.68.3.99:8080/pps/putdata/",  
//           data:{'task':'putaud','id':1,'messid':14,'warntaskMsg':'不错','status':0},
//           dataType:"json",
//           type:"POST",
//           success:dz,
//           }
//    ));   
//

$(document).ready($.ajax({url:"http://10.68.3.99:8080/pps/putdata/",  
           data:{'task':'putquerywarn','display_num':5,'page':3},
           dataType:"json",
           type:"POST",
           success:dz,
           }
    ));   



function dz(data){
    //alert('hello');
    var last=JSON.stringify(data);
    alert(last);
}

//function getQueryString(name) {
//    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
//    var reg_rewrite = new RegExp("(^|/)" + name + "/([^/]*)(/|$)", "i");
//    var r = window.location.search.substr(1).match(reg);
//    var q = window.location.pathname.substr(1).match(reg_rewrite);
//    if(r != null){
//        return unescape(r[2]);
//    }else if(q != null){
//        return unescape(q[2]);
//    }else{
//        return null;
//    }
//}
//alert(getQueryString("id")+getQueryString("name"));