from flask import Flask 
from flask_cors import *
import typing as t 
from .factory import create_app 
from FAYAAEE .__version__ import VERSION as version 
class FAYAAEE (Flask ):
    _startup_message_printed =False 
    models =[]
    db_config =object ()
    need_register_bp =[]
    def __init__ (OOOO000O0OO0OOOOO ,**OO0O00000OOO000O0 ):
        super ().__init__ (**OO0O00000OOO000O0 )
    def add_models (OOO00O0O0000O000O ,OOOO0O0OO0000O000 :list ):
        OOO00O0O0000O000O .models =OOOO0O0OO0000O000 
    def add_db_config (OO00O00OOOOOOOOO0 ,O0O0O0O0O00OO00O0 :object ):
        OO00O00OOOOOOOOO0 .db_config =O0O0O0O0O00OO00O0 
    def add_blueprints (O00O0OO000000OO00 ,O0OO00000OO00OO00 :list ):
        O00O0OO000000OO00 .need_register_bp =O0OO00000OO00OO00 
    def FAYAAEE_ready (O000OO0OOOOOO0O0O ):
        create_app (O000OO0OOOOOO0O0O ,O000OO0OOOOOO0O0O .models ,O000OO0OOOOOO0O0O .db_config ,"/api",O000OO0OOOOOO0O0O .need_register_bp )
        CORS (O000OO0OOOOOO0O0O ,resources =r'/*')
        O000OO0OOOOOO0O0O ._print_startup_message ()
    def run(
            self,
            host: str | None = None,
            port: int | None = None,
            debug: bool | None = None,
            load_dotenv: bool = True,
            **options: t.Any,
    ) -> None:
        super().run(host, port, debug, load_dotenv, **options)
    def _print_startup_message (O0O00O0O0O0OO0000 ):
        if not getattr (O0O00O0O0O0OO0000 ,'_startup_message_printed',False ):
            O0O00O0O0O0OO0000 ._startup_message_printed =True 
