import json 
from functools import wraps 
from flasgger import swag_from 
from flask import request ,g ,send_file 
from sqlalchemy import and_ 
from sqlalchemy .orm import class_mapper
from FAYAAEE .extensions import db 
import pandas as pd 
import io 
class AutoUrl :
    def __init__ (O0O0OO00O0OO0O00O ,O0O0O0O0O00OO00O0 ):
        for O0OOOO0O00O0O00O0 in O0O0O0O0O00OO00O0 :
            AutoDB (O0OOOO0O00O0O00O0 ["model"],O0OOOO0O00O0O00O0 ["bp"],O0OOOO0O00O0O00O0 ["url_prefix"])
class AutoDB :
    model ={}
    bp =object 
    url_name =""
    def __init__ (OOO00OOOO0O00O000 ,O00O0OOOO0OO00OOO ,O000O0OO00OO000O0 ,OO00O0OOO0OO0OOO0 ):
        OOO00OOOO0O00O000 .model =O00O0OOOO0OO00OOO 
        OOO00OOOO0O00O000 .bp =O000O0OO00OO000O0 
        OOO00OOOO0O00O000 .url_name =OO00O0OOO0OO0OOO0 
        OOO00OOOO0O00O000 .bp .add_url_rule ('/'+OO00O0OOO0OO0OOO0 +'/get',endpoint =O000O0OO00OO000O0 .name +OO00O0OOO0OO0OOO0 +'get',view_func =OOO00OOOO0O00O000 .get ,methods =['GET'])
        OOO00OOOO0O00O000 .bp .add_url_rule ('/'+OO00O0OOO0OO0OOO0 +'/get_one',endpoint =O000O0OO00OO000O0 .name +OO00O0OOO0OO0OOO0 +'get_one',view_func =OOO00OOOO0O00O000 .get_one ,methods =['GET'])
        OOO00OOOO0O00O000 .bp .add_url_rule ('/'+OO00O0OOO0OO0OOO0 +'/post',endpoint =O000O0OO00OO000O0 .name +OO00O0OOO0OO0OOO0 +'post',view_func =OOO00OOOO0O00O000 .post ,methods =['POST'])
        OOO00OOOO0O00O000 .bp .add_url_rule ('/'+OO00O0OOO0OO0OOO0 +'/delete/<int:one_or_list>/<int:true_del_or_false_del>',endpoint =O000O0OO00OO000O0 .name +OO00O0OOO0OO0OOO0 +'delete',view_func =OOO00OOOO0O00O000 .delete ,methods =['POST'])
        OOO00OOOO0O00O000 .bp .add_url_rule ('/'+OO00O0OOO0OO0OOO0 +'/put',endpoint =O000O0OO00OO000O0 .name +OO00O0OOO0OO0OOO0 +'put',view_func =OOO00OOOO0O00O000 .put ,methods =['POST'])
        OOO00OOOO0O00O000 .bp .add_url_rule ('/'+OO00O0OOO0OO0OOO0 +'/export',endpoint =O000O0OO00OO000O0 .name +OO00O0OOO0OO0OOO0 +'export',view_func =OOO00OOOO0O00O000 .export ,methods =['POST'])
    def list_to_return (O0O0OO00OO0OOO00O ,O00O0OO0O0O0OO000 ):
        ""
        OO00O00O00O00OOOO =[]
        for O0OO0OO0O000O0000 in O00O0OO0O0O0OO000 :
            O0000O0OOOO000OO0 ={}
            for O0O0000000OO0OOOO in class_mapper (O0O0OO00OO0OOO00O .model ).mapped_table .c :
                O0OO000OOOO0O00O0 =str (getattr (O0OO0OO0O000O0000 ,O0O0000000OO0OOOO .name ))
                if O0OO000OOOO0O00O0 !='None':
                    O0000O0OOOO000OO0 [O0O0000000OO0OOOO .name ]=O0OO000OOOO0O00O0 
                else :
                    continue 
            OO00O00O00O00OOOO .append (O0000O0OOOO000OO0 )
        return OO00O00O00O00OOOO 
    def one_to_return (OOOO00OOOOOO0000O ,O000000000OO0OO0O ):
        ""
        OO000O0OOO0OO0O0O ={}
        if O000000000OO0OO0O :
            for OOOOO0000O000000O in class_mapper (OOOO00OOOOOO0000O .model ).mapped_table .c :
                OOO0OOO000OOOO00O =str (getattr (O000000000OO0OO0O ,OOOOO0000O000000O .name ))
                if OOO0OOO000OOOO00O !='None':
                    OO000O0OOO0OO0O0O [OOOOO0000O000000O .name ]=OOO0OOO000OOOO00O 
                else :
                    continue 
            return OO000O0OOO0OO0O0O 
        else :
            return {}
    def check_request_delete (OOOOO00OO0OOOOO0O ):
        @wraps (OOOOO00OO0OOOOO0O )
        def OOOO000OOO00OOOO0 (OOOO0000O0O0000O0 ,*O00OOO00OO0O0O000 ,**O0OO00O000O0OO0O0 ):
            OO000O0000000O00O =request .json 
            for OOOOO0O0O0OO000O0 ,OOOO0OOOO00O0OOOO in OO000O0000000O00O .items ():
                O0000O0000O00O000 =OOOO0000O0O0000O0 .check_parameter_exists (OOOOO0O0O0OO000O0 )
                if not O0000O0000O00O000 :
                    return {'error':'参数错误','code':0 }
            return OOOOO00OO0OOOOO0O (OOOO0000O0O0000O0 ,*O00OOO00OO0O0O000 ,**O0OO00O000O0OO0O0 )
        return OOOO000OOO00OOOO0 
    def check_request_export (O0O000OO0OO0OOO0O ):
        @wraps (O0O000OO0OO0OOO0O )
        def O0OOO0O0000OO000O (O0O0O000O00O0OOOO ,*O0OOO0O00O00O00O0 ,**O0OOO00OOO0OO0O00 ):
            OOOO0OO0O00OOOOO0 =request .json 
            OO0OO0O0O0O000O00 =OOOO0OO0O00OOOOO0 .get ('need_export')
            O0O0OO000O0000000 =OOOO0OO0O00OOOOO0 .get ('condition')
            for OOOOOOOOO00OO0OO0 ,OO0O0O00000000000 in O0O0OO000O0000000 .items ():
                if OOOOOOOOO00OO0OO0 =="_Own"or OOOOOOOOO00OO0OO0 =="_Price":
                    continue 
                OOO000O00OOO0O00O =O0O0O000O00O0OOOO .check_parameter_exists (OOOOOOOOO00OO0OO0 )
                if not OOO000O00OOO0O00O :
                    return {'error':'a参数错误','code':11 }
            for OOOOOOOOO00OO0OO0 ,OO0O0O00000000000 in OO0OO0O0O0O000O00 .items ():
                OOO000O00OOO0O00O =O0O0O000O00O0OOOO .check_parameter_exists (OOOOOOOOO00OO0OO0 )
                if not OOO000O00OOO0O00O :
                    return {'error':'b参数错误','code':10 }
            return O0O000OO0OO0OOO0O (O0O0O000O00O0OOOO ,*O0OOO0O00O00O00O0 ,**O0OOO00OOO0OO0O00 )
        return O0OOO0O0000OO000O 
    def check_request_turn (OOO0O0O0000000OO0 ):
        @wraps (OOO0O0O0000000OO0 )
        def O00O0OOOO0OOOO000 (O00OO0000OO0OOOO0 ,*OO0O0O000OO0O0OOO ,**O000OO0O0O0OOOOOO ):
            O00000O000000OOOO =request .json 
            O00OOO0OO0OO0OOOO =O00000O000000OOOO .get ('need_update')
            O0OO0OO0O0O0OO00O =O00000O000000OOOO .get ('condition')
            for O000OOOOO0OO0OO00 ,OO00O0OO0OOOO0OO0 in O0OO0OO0O0O0OO00O .items ():
                if O000OOOOO0OO0OO00 =="_Own":
                    continue 
                O00O00O0OOO0O0OO0 =O00OO0000OO0OOOO0 .check_parameter_exists (O000OOOOO0OO0OO00 )
                if not O00O00O0OOO0O0OO0 :
                    return {'error':'a参数错误','code':11 }
            for O000OOOOO0OO0OO00 ,OO00O0OO0OOOO0OO0 in O00OOO0OO0OO0OOOO .items ():
                O00O00O0OOO0O0OO0 =O00OO0000OO0OOOO0 .check_parameter_exists (O000OOOOO0OO0OO00 )
                if not O00O00O0OOO0O0OO0 :
                    return {'error':'b参数错误','code':10 }
            return OOO0O0O0000000OO0 (O00OO0000OO0OOOO0 ,*OO0O0O000OO0O0OOO ,**O000OO0O0O0OOOOOO )
        return O00O0OOOO0OOOO000 
    def check_parameter_exists (O0O0O00OO000O0O0O ,OO0000O0O000O0000 ):
        O000O00O0O0000O00 =class_mapper (O0O0O00OO000O0O0O .model )
        return hasattr (O000O00O0O0000O00 .column_attrs ,OO0000O0O000O0000 )
    @swag_from ('swag_config/get.yml')
    def get (OOO0O000O000OO000 ):
        O0OOO000O0OO0OOOO =dict (request .args )
        _OO0O000O0O00OO000 =False 
        if '_Not_Filter'in O0OOO000O0OO0OOOO :
            _OO0O000O0O00OO000 =json .loads (O0OOO000O0OO0OOOO .pop ('_Not_Filter'))
        if '_Own'in O0OOO000O0OO0OOOO :
            O0O00OO00OOO0O00O =O0OOO000O0OO0OOOO .get ('_Own')
            O0OOO000O0OO0OOOO [O0O00OO00OOO0O00O ]=g .username 
            O0OOO000O0OO0OOOO .pop ('_Own')
        if '_Pagination'not in O0OOO000O0OO0OOOO :
            if '_Desc'not in O0OOO000O0OO0OOOO :
                OO00000O000000000 =OOO0O000O000OO000 .model .query .filter_by (is_delete =0 )
            else :
                OO00000O000000000 =OOO0O000O000OO000 .model .query .filter_by (is_delete =0 ).order_by (OOO0O000O000OO000 .model .id .desc ())
                O0OOO000O0OO0OOOO .pop ('_Desc')
            O00O0OOO00O00OO00 =[]
            if '_Search'in O0OOO000O0OO0OOOO :
                OOOO0O0O0OO00O000 =O0OOO000O0OO0OOOO .pop ('_Search')
                O0OOO00OO00OO0OOO =O0OOO000O0OO0OOOO .pop ('_Search_value')
                O00O0OOO00O00OO00 .append (getattr (OOO0O000O000OO000 .model ,OOOO0O0O0OO00O000 ).like ('%'+O0OOO00OO00OO0OOO +'%'))
            for OOOO0O0O0OO00O000 ,O0OOO00OO00OO0OOO in O0OOO000O0OO0OOOO .items ():
                O00O0OOO00O00OO00 .append (getattr (OOO0O000O000OO000 .model ,OOOO0O0O0OO00O000 )==O0OOO00OO00OO0OOO )
            if _OO0O000O0O00OO000 !=False :
                O00O0OOO00O00OO00 .append (getattr (OOO0O000O000OO000 .model ,_OO0O000O0O00OO000 ['key'])!=_OO0O000O0O00OO000 ['value'])
            if O00O0OOO00O00OO00 :
                OO00000O000000000 =OO00000O000000000 .filter (and_ (*O00O0OOO00O00OO00 ))
            OOOOOOOO0000O0000 =OO00000O000000000 .all ()
            return OOO0O000O000OO000 .list_to_return (OOOOOOOO0000O0000 )
        else :
            O0OOO000O0OO0OOOO .pop ('_Pagination')
            OO0OOOOOO00O0OOOO =int (O0OOO000O0OO0OOOO .pop ('page'))
            O0OOOOO0O0O0OOO00 =int (O0OOO000O0OO0OOOO .pop ('per_page'))
            if '_Desc'not in O0OOO000O0OO0OOOO :
                OO00000O000000000 =OOO0O000O000OO000 .model .query .filter_by (is_delete =0 )
            else :
                OO00000O000000000 =OOO0O000O000OO000 .model .query .filter_by (is_delete =0 ).order_by (OOO0O000O000OO000 .model .id .desc ())
                O0OOO000O0OO0OOOO .pop ('_Desc')
            O00O0OOO00O00OO00 =[]
            if '_Search'in O0OOO000O0OO0OOOO :
                OOOO0O0O0OO00O000 =O0OOO000O0OO0OOOO .pop ('_Search')
                O0OOO00OO00OO0OOO =O0OOO000O0OO0OOOO .pop ('_Search_value')
                O00O0OOO00O00OO00 .append (getattr (OOO0O000O000OO000 .model ,OOOO0O0O0OO00O000 ).like ('%'+O0OOO00OO00OO0OOO +'%'))
            for OOOO0O0O0OO00O000 ,O0OOO00OO00OO0OOO in O0OOO000O0OO0OOOO .items ():
                O00O0OOO00O00OO00 .append (getattr (OOO0O000O000OO000 .model ,OOOO0O0O0OO00O000 )==O0OOO00OO00OO0OOO )
            if _OO0O000O0O00OO000 !=False :
                O00O0OOO00O00OO00 .append (getattr (OOO0O000O000OO000 .model ,_OO0O000O0O00OO000 ['key'])!=_OO0O000O0O00OO000 ['value'])
            if O00O0OOO00O00OO00 :
                OO00000O000000000 =OO00000O000000000 .filter (and_ (*O00O0OOO00O00OO00 ))
            OOOOOOOO0000O0000 =OO00000O000000000 .paginate (page =OO0OOOOOO00O0OOOO ,per_page =O0OOOOO0O0O0OOO00 ,error_out =False )
            O0O00OOO0O0O0O0O0 =OOOOOOOO0000O0000 .items 
            O0O00O0OO00000000 =OOOOOOOO0000O0000 .has_next 
            O000OO00O00OOOOOO =OOOOOOOO0000O0000 .has_prev 
            OOOO0OO0O0O0O0OOO =OOOOOOOO0000O0000 .total 
            O000O0O0OOO00O0OO =OOOOOOOO0000O0000 .pages 
            return {'items':OOO0O000O000OO000 .list_to_return (O0O00OOO0O0O0O0O0 ),'has_next':O0O00O0OO00000000 ,'has_prev':O000OO00O00OOOOOO ,'total':OOOO0OO0O0O0O0OOO ,'pages':O000O0O0OOO00O0OO }
    @swag_from ('swag_config/get_one.yml')
    def get_one (OO0OO000OO000O0OO ):
        O0O0OOO000O00O0O0 =dict (request .args )
        if '_Own'in O0O0OOO000O00O0O0 :
            OOOOO0OO0OO00O000 =O0O0OOO000O00O0O0 .get ('_Own')
            O0O0OOO000O00O0O0 [OOOOO0OO0OO00O000 ]=g .username 
            O0O0OOO000O00O0O0 .pop ('_Own')
        OOOO00OO00OOOO0O0 =[]
        OOO0000O000O00O0O =OO0OO000OO000O0OO .model .query .filter_by (is_delete =0 )
        for OOO000OO0OOO00O0O ,OO0OOO00O000O0OOO in O0O0OOO000O00O0O0 .items ():
            OOOO00OO00OOOO0O0 .append (getattr (OO0OO000OO000O0OO .model ,OOO000OO0OOO00O0O )==OO0OOO00O000O0OOO )
        if OOOO00OO00OOOO0O0 :
            OOO0000O000O00O0O =OOO0000O000O00O0O .filter (and_ (*OOOO00OO00OOOO0O0 ))
        O000O0OO00O000OO0 =OOO0000O000O00O0O .first ()
        return OO0OO000OO000O0OO .one_to_return (O000O0OO00O000OO0 )
    @swag_from ('swag_config/post.yml')
    def post (O000OOOO0OOOOO0O0 ):
        O00OO0OO0O000O000 =request .json 
        O0OOO0O0OOO000O0O =O000OOOO0OOOOO0O0 .model ()
        for O0OO000O0OOOO00OO ,OOO00OOO00OOOO0OO in O00OO0OO0O000O000 .items ():
            setattr (O0OOO0O0OOO000O0O ,O0OO000O0OOOO00OO ,OOO00OOO00OOOO0OO )
        try :
            db .session .add (O0OOO0O0OOO000O0O )
            db .session .commit ()
            return {'id':O0OOO0O0OOO000O0O .id ,'code':1 }
        except Exception as OOOO0000OOO00000O :
            print (OOOO0000OOO00000O )
            return {'error':OOOO0000OOO00000O ,'code':-1 }
    @swag_from ('swag_config/delete.yml')
    @check_request_delete 
    def delete (OOOO0O0000OOOOO00 ,OOO0OOO0O00O0OOOO =1 ,O0O0OOOOO0000O0OO =0 ):
        OOOO0O0OO0OOO00OO =request .json 
        O0OO00O0000000O00 =OOOO0O0000OOOOO00 .model .query .filter_by (is_delete =0 )
        O0O0O00O0O0O0O000 =[]
        for O00O0OOOO0OO0O000 ,O000OO0OOOO0OO0OO in OOOO0O0OO0OOO00OO .items ():
            O0O0O00O0O0O0O000 .append (getattr (OOOO0O0000OOOOO00 .model ,O00O0OOOO0OO0O000 )==O000OO0OOOO0OO0OO )
        if O0O0O00O0O0O0O000 :
            O0OO00O0000000O00 =O0OO00O0000000O00 .filter (and_ (*O0O0O00O0O0O0O000 ))
        if len (O0OO00O0000000O00 .all ())>0 :
            if OOO0OOO0O00O0OOOO ==1 :
                if O0O0OOOOO0000O0OO ==0 :
                    O0O0O0O0OO00000O0 =O0OO00O0000000O00 .first ()
                    O0O0O0O0OO00000O0 .is_delete =1 
                else :
                    O0OO00O0000000O00 .delete ()
            else :
                if O0O0OOOOO0000O0OO ==0 :
                    O0OO00O0000000O00 =O0OO00O0000000O00 .all ()
                    for O0O0OOOOOO000O000 in O0OO00O0000000O00 :
                        O0O0OOOOOO000O000 .is_delete =1 
                else :
                    O0OO00O0000000O00 .delete (synchronize_session =False )
            try :
                db .session .commit ()
                return {'code':1 ,'message':'已成功删除'}
            except Exception as OOO000O0O0O000OOO :
                return {'error':OOO000O0O0O000OOO ,'code':-1 }
        else :
            return {'error':'未查询到数据','code':0 }
    @swag_from ('swag_config/put.yml')
    @check_request_turn 
    def put (OOOOO000O0O000OO0 ):
        O00OOOOO0O0O0OO0O =request .json 
        OOOO00O0OOOO0O0O0 =OOOOO000O0O000OO0 .model .query .filter_by (is_delete =0 )
        OOO0O0OOOO0OOO000 =[]
        OOOO0O00O0O0OOO00 =O00OOOOO0O0O0OO0O .get ('need_update')
        O0OO00O000000OOOO =O00OOOOO0O0O0OO0O .get ('condition')
        if '_Own'in O0OO00O000000OOOO :
            O000O0OOOO0000000 =O0OO00O000000OOOO .get ('_Own')
            O0OO00O000000OOOO [O000O0OOOO0000000 ]=g .username 
            O0OO00O000000OOOO .pop ('_Own')
        for OO00000OO0OO00OOO ,OO00OO0OOO0OO0000 in O0OO00O000000OOOO .items ():
            OOO0O0OOOO0OOO000 .append (getattr (OOOOO000O0O000OO0 .model ,OO00000OO0OO00OOO )==OO00OO0OOO0OO0000 )
        if OOO0O0OOOO0OOO000 :
            OOOO00O0OOOO0O0O0 =OOOO00O0OOOO0O0O0 .filter (and_ (*OOO0O0OOOO0OOO000 ))
        if len (OOOO00O0OOOO0O0O0 .all ())>0 :
            for OOO00OOOOO0OO00O0 in OOOO00O0OOOO0O0O0 :
                for OO00000OO0OO00OOO ,OO00OO0OOO0OO0000 in OOOO0O00O0O0OOO00 .items ():
                    setattr (OOO00OOOOO0OO00O0 ,OO00000OO0OO00OOO ,OO00OO0OOO0OO0000 )
            try :
                db .session .commit ()
                return {'code':1 ,'message':'已成功更新','num':len (OOOO00O0OOOO0O0O0 .all ())}
            except Exception as OOO0O0OOOOOOOO00O :
                return {'error':OOO0O0OOOOOOOO00O ,'code':-1 }
        else :
            return {'error':'未查询到匹配数据','code':0 }
    @swag_from ('swag_config/export.yml')
    @check_request_export 
    def export (O00O0O0O00OOO0O0O ):
        OO0000OOOO0OO0OO0 =request .json 
        OOO0O0OOO000OO000 =O00O0O0O00OOO0O0O .model .query .filter_by (is_delete =0 )
        O00O0O0O00000OOOO =[]
        OOO0O0OOOOO0000O0 =OO0000OOOO0OO0OO0 .get ('need_export')
        O00OO0O0000OOO000 =OO0000OOOO0OO0OO0 .get ('condition')
        _OO0O0OOOO0000000O =[]
        if "_Price"in OO0000OOOO0OO0OO0 :
            _OO0O0OOOO0000000O =OO0000OOOO0OO0OO0 .get ('_Price').split (',')
        if '_Own'in O00OO0O0000OOO000 :
            OOO0O00O00OOOOO00 =O00OO0O0000OOO000 .get ('_Own')
            O00OO0O0000OOO000 [OOO0O00O00OOOOO00 ]=g .username 
            O00OO0O0000OOO000 .pop ('_Own')
        for O0OO0OOO00O0OOO0O ,O000O00000OOO0O00 in O00OO0O0000OOO000 .items ():
            O00O0O0O00000OOOO .append (getattr (O00O0O0O00OOO0O0O .model ,O0OO0OOO00O0OOO0O )==O000O00000OOO0O00 )
        if O00O0O0O00000OOOO :
            OOO0O0OOO000OO000 =OOO0O0OOO000OO000 .filter (and_ (*O00O0O0O00000OOOO ))
        OO0O0OO0O0OOOO000 =OOO0O0OOO000OO000 .all ()
        if len (OO0O0OO0O0OOOO000 )>0 :
            try :
                return export_to_excel (OO0O0OO0O0OOOO000 ,OOO0O0OOOOO0000O0 ,_OO0O0OOOO0000000O )
            except Exception as OOO0OO000O000OOOO :
                return {'error':OOO0OO000O000OOOO ,'code':-1 }
        else :
            return {'error':'未查询到匹配数据','code':0 }
def export_to_excel (OO0OOOO0O0O0O0000 ,O0OO0OO0O0O0OOOO0 ,_OO0OO000OOO00OOO0 ):
    O00O0OOO000O00000 =[]
    OOOOO0000OO00OO00 =1 
    for O0OOOO00OO000O0O0 in OO0OOOO0O0O0O0000 :
        O0OOO00O0OOOOOOO0 ={}
        O0OOO00O0OOOOOOO0 .update ({'序号':OOOOO0000OO00OO00 })
        for O000O0O000O0O0OO0 ,OO0O000OOOO00O0OO in O0OO0OO0O0O0OOOO0 .items ():
            if O000O0O000O0O0OO0 in _OO0OO000OOO00OOO0 :
                O0OOO00O0OOOOOOO0 .update ({OO0O000OOOO00O0OO :str ('{:.2f}'.format (getattr (O0OOOO00OO000O0O0 ,O000O0O000O0O0OO0 )/100 ))})
            else :
                O0OOO00O0OOOOOOO0 .update ({OO0O000OOOO00O0OO :str (getattr (O0OOOO00OO000O0O0 ,O000O0O000O0O0OO0 ))})
        O00O0OOO000O00000 .append (O0OOO00O0OOOOOOO0 )
        OOOOO0000OO00OO00 +=1 
    OO0O0O0000O0OO0O0 =pd .DataFrame (O00O0OOO000O00000 )
    O00O00OOOOOO000OO =io .BytesIO ()
    OOOOOOO0000O000O0 =pd .ExcelWriter (O00O00OOOOOO000OO ,engine ='xlsxwriter')
    OO0O0O0000O0OO0O0 .to_excel (OOOOOOO0000O000O0 ,index =False ,sheet_name ='Sheet1')
    OOOOOOO0000O000O0 ._save ()
    O00O00OOOOOO000OO .seek (0 )
    OO0OOOO0O0OO0O000 =send_file (O00O00OOOOOO000OO ,download_name ='exported_data.xlsx',as_attachment =True )
    return OO0OOOO0O0OO0O000 
