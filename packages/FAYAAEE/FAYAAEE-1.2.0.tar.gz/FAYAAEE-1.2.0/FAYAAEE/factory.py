from flask import Flask 
from FAYAAEE .extensions import db 
from FAYAAEE .FaabJWT import JWT 
from flasgger import Swagger 
import inspect 
from FAYAAEE .FaabFunction import AutoUrl 
def get_variable_name (O0OO00OO00OO0OOO0 ):
    O0O00000OO0O00O00 =inspect .currentframe ().f_back 
    for O0OO000O00O00O0O0 ,OO0OO0OO0OOOO00OO in O0O00000OO0O00O00 .f_locals .items ():
        if OO0OO0OO0OOOO00OO is O0OO00OO00OO0OOO0 :
            return O0OO000O00O00O0O0 
    return None 
def create_app (OO0OOOOOOOOOOO00O ,O0OOO00O000O000OO ,O0O0O0O000O0O0O0O ,OO00OOO0OO00OO000 :str |None ='/api',O0OO000O00OOO0O00 =None ):
    OO0OOOOOOOOOOO00O .config .from_object (O0O0O0O000O0O0O0O )
    if len (O0OO000O00OOO0O00 )>0 :
        for OOOO0OO00O0000O00 in O0OO000O00OOO0O00 :
            OO0OOOOOOOOOOO00O .register_blueprint (OOOO0OO00O0000O00 ,url_prefix =OO00OOO0OO00OO000 +'/'+OOOO0OO00O0000O00 .name )
    for O0OO0O0OO0O00000O in O0OOO00O000O000OO :
        AutoUrl (O0OO0O0OO0O00000O )
        OO0OOOOOOOOOOO00O .register_blueprint (O0OO0O0OO0O00000O [0 ]["bp"],url_prefix =OO00OOO0OO00OO000 +'/'+O0OO0O0OO0O00000O [0 ]["bp"].name )
    OO0OOOOOOOOOOO00O .register_blueprint (JWT )
    db .init_app (OO0OOOOOOOOOOO00O )
    O00000OO00O00OOO0 =Swagger .DEFAULT_CONFIG 
    O00000OO00O00OOO0 ['title']='FAYAAEE'
    O00000OO00O00OOO0 ['description']='由FAYAAEE自动生成的API文档'
    O00000OO00O00OOO0 ['version']='1.0.0'
    Swagger (OO0OOOOOOOOOOO00O ,config =O00000OO00O00OOO0 )
    with OO0OOOOOOOOOOO00O .app_context ():
        db .create_all ()
    return OO0OOOOOOOOOOO00O 
