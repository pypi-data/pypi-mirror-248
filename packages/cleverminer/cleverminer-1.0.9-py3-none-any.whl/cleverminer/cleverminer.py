import sys #line:50
import time #line:51
import copy #line:52
from time import strftime #line:54
from time import gmtime #line:55
import pandas as pd #line:57
import numpy #line:58
from pandas .api .types import CategoricalDtype #line:59
import progressbar #line:61
import re #line:62
class cleverminer :#line:63
    version_string ="1.0.9"#line:65
    def __init__ (O0OO0OOOOO000O0O0 ,**OOOOOO00OO00OO000 ):#line:67
        O0OO0OOOOO000O0O0 ._print_disclaimer ()#line:68
        O0OO0OOOOO000O0O0 .stats ={'total_cnt':0 ,'total_ver':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:77
        O0OO0OOOOO000O0O0 .options ={'max_categories':100 ,'max_rules':None ,'optimizations':True ,'automatic_data_conversions':True ,'progressbar':True ,'keep_df':False }#line:85
        O0OO0OOOOO000O0O0 .df =None #line:86
        O0OO0OOOOO000O0O0 .kwargs =None #line:87
        if len (OOOOOO00OO00OO000 )>0 :#line:88
            O0OO0OOOOO000O0O0 .kwargs =OOOOOO00OO00OO000 #line:89
        O0OO0OOOOO000O0O0 .verbosity ={}#line:90
        O0OO0OOOOO000O0O0 .verbosity ['debug']=False #line:91
        O0OO0OOOOO000O0O0 .verbosity ['print_rules']=False #line:92
        O0OO0OOOOO000O0O0 .verbosity ['print_hashes']=True #line:93
        O0OO0OOOOO000O0O0 .verbosity ['last_hash_time']=0 #line:94
        O0OO0OOOOO000O0O0 .verbosity ['hint']=False #line:95
        if "opts"in OOOOOO00OO00OO000 :#line:96
            O0OO0OOOOO000O0O0 ._set_opts (OOOOOO00OO00OO000 .get ("opts"))#line:97
        if "opts"in OOOOOO00OO00OO000 :#line:98
            if "verbose"in OOOOOO00OO00OO000 .get ('opts'):#line:99
                OO0OO00000O0OOO0O =OOOOOO00OO00OO000 .get ('opts').get ('verbose')#line:100
                if OO0OO00000O0OOO0O .upper ()=='FULL':#line:101
                    O0OO0OOOOO000O0O0 .verbosity ['debug']=True #line:102
                    O0OO0OOOOO000O0O0 .verbosity ['print_rules']=True #line:103
                    O0OO0OOOOO000O0O0 .verbosity ['print_hashes']=False #line:104
                    O0OO0OOOOO000O0O0 .verbosity ['hint']=True #line:105
                    O0OO0OOOOO000O0O0 .options ['progressbar']=False #line:106
                elif OO0OO00000O0OOO0O .upper ()=='RULES':#line:107
                    O0OO0OOOOO000O0O0 .verbosity ['debug']=False #line:108
                    O0OO0OOOOO000O0O0 .verbosity ['print_rules']=True #line:109
                    O0OO0OOOOO000O0O0 .verbosity ['print_hashes']=True #line:110
                    O0OO0OOOOO000O0O0 .verbosity ['hint']=True #line:111
                    O0OO0OOOOO000O0O0 .options ['progressbar']=False #line:112
                elif OO0OO00000O0OOO0O .upper ()=='HINT':#line:113
                    O0OO0OOOOO000O0O0 .verbosity ['debug']=False #line:114
                    O0OO0OOOOO000O0O0 .verbosity ['print_rules']=False #line:115
                    O0OO0OOOOO000O0O0 .verbosity ['print_hashes']=True #line:116
                    O0OO0OOOOO000O0O0 .verbosity ['last_hash_time']=0 #line:117
                    O0OO0OOOOO000O0O0 .verbosity ['hint']=True #line:118
                    O0OO0OOOOO000O0O0 .options ['progressbar']=False #line:119
                elif OO0OO00000O0OOO0O .upper ()=='DEBUG':#line:120
                    O0OO0OOOOO000O0O0 .verbosity ['debug']=True #line:121
                    O0OO0OOOOO000O0O0 .verbosity ['print_rules']=True #line:122
                    O0OO0OOOOO000O0O0 .verbosity ['print_hashes']=True #line:123
                    O0OO0OOOOO000O0O0 .verbosity ['last_hash_time']=0 #line:124
                    O0OO0OOOOO000O0O0 .verbosity ['hint']=True #line:125
                    O0OO0OOOOO000O0O0 .options ['progressbar']=False #line:126
        O0OO0OOOOO000O0O0 ._is_py310 =sys .version_info [0 ]>=4 or (sys .version_info [0 ]>=3 and sys .version_info [1 ]>=10 )#line:127
        if not (O0OO0OOOOO000O0O0 ._is_py310 ):#line:128
            print ("Warning: Python 3.10+ NOT detected. You should upgrade to Python 3.10 or greater to get better performance")#line:129
        else :#line:130
            if (O0OO0OOOOO000O0O0 .verbosity ['debug']):#line:131
                print ("Python 3.10+ detected.")#line:132
        O0OO0OOOOO000O0O0 ._initialized =False #line:133
        O0OO0OOOOO000O0O0 ._init_data ()#line:134
        O0OO0OOOOO000O0O0 ._init_task ()#line:135
        if len (OOOOOO00OO00OO000 )>0 :#line:136
            if "df"in OOOOOO00OO00OO000 :#line:137
                O0OO0OOOOO000O0O0 ._prep_data (OOOOOO00OO00OO000 .get ("df"))#line:138
            else :#line:139
                print ("Missing dataframe. Cannot initialize.")#line:140
                O0OO0OOOOO000O0O0 ._initialized =False #line:141
                return #line:142
            O00000O0OOOOOO0O0 =OOOOOO00OO00OO000 .get ("proc",None )#line:143
            if not (O00000O0OOOOOO0O0 ==None ):#line:144
                O0OO0OOOOO000O0O0 ._calculate (**OOOOOO00OO00OO000 )#line:145
            else :#line:147
                if O0OO0OOOOO000O0O0 .verbosity ['debug']:#line:148
                    print ("INFO: just initialized")#line:149
                O0O0000O000O0000O ={}#line:150
                OO000O00OOOOO0O00 ={}#line:151
                OO000O00OOOOO0O00 ["varname"]=O0OO0OOOOO000O0O0 .data ["varname"]#line:152
                OO000O00OOOOO0O00 ["catnames"]=O0OO0OOOOO000O0O0 .data ["catnames"]#line:153
                O0O0000O000O0000O ["datalabels"]=OO000O00OOOOO0O00 #line:154
                O0OO0OOOOO000O0O0 .result =O0O0000O000O0000O #line:155
        O0OO0OOOOO000O0O0 ._initialized =True #line:157
    def _set_opts (O0OOO0OO0OO0O0OOO ,O0OOO0OO00OO00OO0 ):#line:159
        if "no_optimizations"in O0OOO0OO00OO00OO0 :#line:160
            O0OOO0OO0OO0O0OOO .options ['optimizations']=not (O0OOO0OO00OO00OO0 ['no_optimizations'])#line:161
            print ("No optimization will be made.")#line:162
        if "disable_progressbar"in O0OOO0OO00OO00OO0 :#line:163
            O0OOO0OO0OO0O0OOO .options ['progressbar']=False #line:164
            print ("Progressbar will not be shown.")#line:165
        if "max_rules"in O0OOO0OO00OO00OO0 :#line:166
            O0OOO0OO0OO0O0OOO .options ['max_rules']=O0OOO0OO00OO00OO0 ['max_rules']#line:167
        if "max_categories"in O0OOO0OO00OO00OO0 :#line:168
            O0OOO0OO0OO0O0OOO .options ['max_categories']=O0OOO0OO00OO00OO0 ['max_categories']#line:169
            if O0OOO0OO0OO0O0OOO .verbosity ['debug']==True :#line:170
                print (f"Maximum number of categories set to {O0OOO0OO0OO0O0OOO.options['max_categories']}")#line:171
        if "no_automatic_data_conversions"in O0OOO0OO00OO00OO0 :#line:172
            O0OOO0OO0OO0O0OOO .options ['automatic_data_conversions']=not (O0OOO0OO00OO00OO0 ['no_automatic_data_conversions'])#line:173
            print ("No automatic data conversions will be made.")#line:174
        if "keep_df"in O0OOO0OO00OO00OO0 :#line:175
            O0OOO0OO0OO0O0OOO .options ['keep_df']=O0OOO0OO00OO00OO0 ['keep_df']#line:176
    def _init_data (OO0OOOOOO00O0O0OO ):#line:179
        OO0OOOOOO00O0O0OO .data ={}#line:181
        OO0OOOOOO00O0O0OO .data ["varname"]=[]#line:182
        OO0OOOOOO00O0O0OO .data ["catnames"]=[]#line:183
        OO0OOOOOO00O0O0OO .data ["vtypes"]=[]#line:184
        OO0OOOOOO00O0O0OO .data ["dm"]=[]#line:185
        OO0OOOOOO00O0O0OO .data ["rows_count"]=int (0 )#line:186
        OO0OOOOOO00O0O0OO .data ["data_prepared"]=0 #line:187
    def _init_task (OO0O000000O0O00OO ):#line:189
        if "opts"in OO0O000000O0O00OO .kwargs :#line:191
            OO0O000000O0O00OO ._set_opts (OO0O000000O0O00OO .kwargs .get ("opts"))#line:192
        OO0O000000O0O00OO .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'trace_cedent_asindata':[],'traces':[],'generated_string':'','rule':{},'filter_value':int (0 )}#line:202
        OO0O000000O0O00OO .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:206
        OO0O000000O0O00OO .rulelist =[]#line:207
        OO0O000000O0O00OO .stats ['total_cnt']=0 #line:209
        OO0O000000O0O00OO .stats ['total_valid']=0 #line:210
        OO0O000000O0O00OO .stats ['control_number']=0 #line:211
        OO0O000000O0O00OO .result ={}#line:212
        OO0O000000O0O00OO ._opt_base =None #line:213
        OO0O000000O0O00OO ._opt_relbase =None #line:214
        OO0O000000O0O00OO ._opt_base1 =None #line:215
        OO0O000000O0O00OO ._opt_relbase1 =None #line:216
        OO0O000000O0O00OO ._opt_base2 =None #line:217
        OO0O000000O0O00OO ._opt_relbase2 =None #line:218
        OO0OOO0O0OO00OOO0 =None #line:219
        if not (OO0O000000O0O00OO .kwargs ==None ):#line:220
            OO0OOO0O0OO00OOO0 =OO0O000000O0O00OO .kwargs .get ("quantifiers",None )#line:221
            if not (OO0OOO0O0OO00OOO0 ==None ):#line:222
                for O0000O0OOOO0OOO00 in OO0OOO0O0OO00OOO0 .keys ():#line:223
                    if O0000O0OOOO0OOO00 .upper ()=='BASE':#line:224
                        OO0O000000O0O00OO ._opt_base =OO0OOO0O0OO00OOO0 .get (O0000O0OOOO0OOO00 )#line:225
                    if O0000O0OOOO0OOO00 .upper ()=='RELBASE':#line:226
                        OO0O000000O0O00OO ._opt_relbase =OO0OOO0O0OO00OOO0 .get (O0000O0OOOO0OOO00 )#line:227
                    if (O0000O0OOOO0OOO00 .upper ()=='FRSTBASE')|(O0000O0OOOO0OOO00 .upper ()=='BASE1'):#line:228
                        OO0O000000O0O00OO ._opt_base1 =OO0OOO0O0OO00OOO0 .get (O0000O0OOOO0OOO00 )#line:229
                    if (O0000O0OOOO0OOO00 .upper ()=='SCNDBASE')|(O0000O0OOOO0OOO00 .upper ()=='BASE2'):#line:230
                        OO0O000000O0O00OO ._opt_base2 =OO0OOO0O0OO00OOO0 .get (O0000O0OOOO0OOO00 )#line:231
                    if (O0000O0OOOO0OOO00 .upper ()=='FRSTRELBASE')|(O0000O0OOOO0OOO00 .upper ()=='RELBASE1'):#line:232
                        OO0O000000O0O00OO ._opt_relbase1 =OO0OOO0O0OO00OOO0 .get (O0000O0OOOO0OOO00 )#line:233
                    if (O0000O0OOOO0OOO00 .upper ()=='SCNDRELBASE')|(O0000O0OOOO0OOO00 .upper ()=='RELBASE2'):#line:234
                        OO0O000000O0O00OO ._opt_relbase2 =OO0OOO0O0OO00OOO0 .get (O0000O0OOOO0OOO00 )#line:235
            else :#line:236
                print ("Warning: no quantifiers found. Optimization will not take place (1)")#line:237
        else :#line:238
            print ("Warning: no quantifiers found. Optimization will not take place (2)")#line:239
    def mine (OO00OO0O00O000O0O ,**O00O0000OO00O0000 ):#line:242
        if not (OO00OO0O00O000O0O ._initialized ):#line:243
            print ("Class NOT INITIALIZED. Please call constructor with dataframe first")#line:244
            return #line:245
        OO00OO0O00O000O0O .kwargs =None #line:246
        if len (O00O0000OO00O0000 )>0 :#line:247
            OO00OO0O00O000O0O .kwargs =O00O0000OO00O0000 #line:248
        OO00OO0O00O000O0O ._init_task ()#line:249
        if len (O00O0000OO00O0000 )>0 :#line:250
            O00O0OO00O0000OOO =O00O0000OO00O0000 .get ("proc",None )#line:251
            if not (O00O0OO00O0000OOO ==None ):#line:252
                OO00OO0O00O000O0O ._calc_all (**O00O0000OO00O0000 )#line:253
            else :#line:254
                print ("Rule mining procedure missing")#line:255
    def _get_ver (O00O0O0O0OO000O0O ):#line:258
        return O00O0O0O0OO000O0O .version_string #line:259
    def _print_disclaimer (O0O00O000O000OOOO ):#line:261
        print (f"Cleverminer version {O0O00O000O000OOOO._get_ver()}.")#line:263
    def _automatic_data_conversions (OO000OOO000O000OO ,OO0O00OO0OOO0O0O0 ):#line:269
        print ("Automatically reordering numeric categories ...")#line:270
        for OO00O000000000000 in range (len (OO0O00OO0OOO0O0O0 .columns )):#line:271
            if OO000OOO000O000OO .verbosity ['debug']:#line:272
                print (f"#{OO00O000000000000}: {OO0O00OO0OOO0O0O0.columns[OO00O000000000000]} : {OO0O00OO0OOO0O0O0.dtypes[OO00O000000000000]}.")#line:273
            try :#line:274
                OO0O00OO0OOO0O0O0 [OO0O00OO0OOO0O0O0 .columns [OO00O000000000000 ]]=OO0O00OO0OOO0O0O0 [OO0O00OO0OOO0O0O0 .columns [OO00O000000000000 ]].astype (str ).astype (float )#line:275
                if OO000OOO000O000OO .verbosity ['debug']:#line:276
                    print (f"CONVERTED TO FLOATS #{OO00O000000000000}: {OO0O00OO0OOO0O0O0.columns[OO00O000000000000]} : {OO0O00OO0OOO0O0O0.dtypes[OO00O000000000000]}.")#line:277
                OOO000O00OO0OOOO0 =pd .unique (OO0O00OO0OOO0O0O0 [OO0O00OO0OOO0O0O0 .columns [OO00O000000000000 ]])#line:278
                OOO0O000OO0O00O00 =True #line:279
                for OO000OO0000000O00 in OOO000O00OO0OOOO0 :#line:280
                    if OO000OO0000000O00 %1 !=0 :#line:281
                        OOO0O000OO0O00O00 =False #line:282
                if OOO0O000OO0O00O00 :#line:283
                    OO0O00OO0OOO0O0O0 [OO0O00OO0OOO0O0O0 .columns [OO00O000000000000 ]]=OO0O00OO0OOO0O0O0 [OO0O00OO0OOO0O0O0 .columns [OO00O000000000000 ]].astype (int )#line:284
                    if OO000OOO000O000OO .verbosity ['debug']:#line:285
                        print (f"CONVERTED TO INT #{OO00O000000000000}: {OO0O00OO0OOO0O0O0.columns[OO00O000000000000]} : {OO0O00OO0OOO0O0O0.dtypes[OO00O000000000000]}.")#line:286
                O0O0O0OO000OOO0O0 =pd .unique (OO0O00OO0OOO0O0O0 [OO0O00OO0OOO0O0O0 .columns [OO00O000000000000 ]])#line:287
                O0O00O0OOO00O00O0 =CategoricalDtype (categories =O0O0O0OO000OOO0O0 .sort (),ordered =True )#line:288
                OO0O00OO0OOO0O0O0 [OO0O00OO0OOO0O0O0 .columns [OO00O000000000000 ]]=OO0O00OO0OOO0O0O0 [OO0O00OO0OOO0O0O0 .columns [OO00O000000000000 ]].astype (O0O00O0OOO00O00O0 )#line:289
                if OO000OOO000O000OO .verbosity ['debug']:#line:290
                    print (f"CONVERTED TO CATEGORY #{OO00O000000000000}: {OO0O00OO0OOO0O0O0.columns[OO00O000000000000]} : {OO0O00OO0OOO0O0O0.dtypes[OO00O000000000000]}.")#line:291
            except :#line:293
                if OO000OOO000O000OO .verbosity ['debug']:#line:294
                    print ("...cannot be converted to int")#line:295
                try :#line:296
                    OOOO0OOOO0000000O =OO0O00OO0OOO0O0O0 [OO0O00OO0OOO0O0O0 .columns [OO00O000000000000 ]].unique ()#line:297
                    if OO000OOO000O000OO .verbosity ['debug']:#line:298
                        print (f"Values: {OOOO0OOOO0000000O}")#line:299
                    O00000OO000OO0O00 =True #line:300
                    O0000O0O0OOO000OO =[]#line:301
                    for OO000OO0000000O00 in OOOO0OOOO0000000O :#line:302
                        OOOOO0OO0O00OOOOO =re .findall (r"-?\d+",OO000OO0000000O00 )#line:305
                        if len (OOOOO0OO0O00OOOOO )>0 :#line:307
                            O0000O0O0OOO000OO .append (int (OOOOO0OO0O00OOOOO [0 ]))#line:308
                        else :#line:309
                            O00000OO000OO0O00 =False #line:310
                    if OO000OOO000O000OO .verbosity ['debug']:#line:311
                        print (f"Is ok: {O00000OO000OO0O00}, extracted {O0000O0O0OOO000OO}")#line:312
                    if O00000OO000OO0O00 :#line:313
                        OOOOOO000O0O0O000 =copy .deepcopy (O0000O0O0OOO000OO )#line:314
                        OOOOOO000O0O0O000 .sort ()#line:315
                        O00O00OOOOO00OO0O =[]#line:317
                        for O0OO0OOOO0OOO000O in OOOOOO000O0O0O000 :#line:318
                            OO0O00O0O00OO0O0O =O0000O0O0OOO000OO .index (O0OO0OOOO0OOO000O )#line:319
                            O00O00OOOOO00OO0O .append (OOOO0OOOO0000000O [OO0O00O0O00OO0O0O ])#line:321
                        if OO000OOO000O000OO .verbosity ['debug']:#line:322
                            print (f"Sorted list: {O00O00OOOOO00OO0O}")#line:323
                        O0O00O0OOO00O00O0 =CategoricalDtype (categories =O00O00OOOOO00OO0O ,ordered =True )#line:324
                        OO0O00OO0OOO0O0O0 [OO0O00OO0OOO0O0O0 .columns [OO00O000000000000 ]]=OO0O00OO0OOO0O0O0 [OO0O00OO0OOO0O0O0 .columns [OO00O000000000000 ]].astype (O0O00O0OOO00O00O0 )#line:325
                except :#line:328
                    if OO000OOO000O000OO .verbosity ['debug']:#line:329
                        print ("...cannot extract numbers from all categories")#line:330
    print ("Automatically reordering numeric categories ...done")#line:332
    def _prep_data (O000O0OO0OOO000O0 ,OO0O00OO00O0O00OO ):#line:334
        print ("Starting data preparation ...")#line:335
        O000O0OO0OOO000O0 ._init_data ()#line:336
        O000O0OO0OOO000O0 .stats ['start_prep_time']=time .time ()#line:337
        if O000O0OO0OOO000O0 .options ['automatic_data_conversions']:#line:338
            O000O0OO0OOO000O0 ._automatic_data_conversions (OO0O00OO00O0O00OO )#line:339
        O000O0OO0OOO000O0 .data ["rows_count"]=OO0O00OO00O0O00OO .shape [0 ]#line:340
        for O000O0O0OO0000O0O in OO0O00OO00O0O00OO .select_dtypes (exclude =['category']).columns :#line:341
            OO0O00OO00O0O00OO [O000O0O0OO0000O0O ]=OO0O00OO00O0O00OO [O000O0O0OO0000O0O ].apply (str )#line:342
        try :#line:343
            OO0OOO0000OO00O0O =pd .DataFrame .from_records ([(O0O0OO0O000O0O0O0 ,OO0O00OO00O0O00OO [O0O0OO0O000O0O0O0 ].nunique ())for O0O0OO0O000O0O0O0 in OO0O00OO00O0O00OO .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:345
        except :#line:346
            print ("Error in input data, probably unsupported data type. Will try to scan for column with unsupported type.")#line:347
            O0000OOOO0OO0000O =""#line:348
            try :#line:349
                for O000O0O0OO0000O0O in OO0O00OO00O0O00OO .columns :#line:350
                    O0000OOOO0OO0000O =O000O0O0OO0000O0O #line:351
                    print (f"...column {O000O0O0OO0000O0O} has {int(OO0O00OO00O0O00OO[O000O0O0OO0000O0O].nunique())} values")#line:352
            except :#line:353
                print (f"... detected : column {O0000OOOO0OO0000O} has unsupported type: {type(OO0O00OO00O0O00OO[O000O0O0OO0000O0O])}.")#line:354
                exit (1 )#line:355
            print (f"Error in data profiling - attribute with unsupported type not detected. Please profile attributes manually, only simple attributes are supported.")#line:356
            exit (1 )#line:357
        if O000O0OO0OOO000O0 .verbosity ['hint']:#line:360
            print ("Quick profile of input data: unique value counts are:")#line:361
            print (OO0OOO0000OO00O0O )#line:362
            for O000O0O0OO0000O0O in OO0O00OO00O0O00OO .columns :#line:363
                if OO0O00OO00O0O00OO [O000O0O0OO0000O0O ].nunique ()<O000O0OO0OOO000O0 .options ['max_categories']:#line:364
                    OO0O00OO00O0O00OO [O000O0O0OO0000O0O ]=OO0O00OO00O0O00OO [O000O0O0OO0000O0O ].astype ('category')#line:365
                else :#line:366
                    print (f"WARNING: attribute {O000O0O0OO0000O0O} has more than {O000O0OO0OOO000O0.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:367
                    del OO0O00OO00O0O00OO [O000O0O0OO0000O0O ]#line:368
        for O000O0O0OO0000O0O in OO0O00OO00O0O00OO .columns :#line:370
            if OO0O00OO00O0O00OO [O000O0O0OO0000O0O ].nunique ()>O000O0OO0OOO000O0 .options ['max_categories']:#line:371
                print (f"WARNING: attribute {O000O0O0OO0000O0O} has more than {O000O0OO0OOO000O0.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:372
                del OO0O00OO00O0O00OO [O000O0O0OO0000O0O ]#line:373
        if O000O0OO0OOO000O0 .options ['keep_df']:#line:374
            if O000O0OO0OOO000O0 .verbosity ['debug']:#line:375
                print ("Keeping df.")#line:376
            O000O0OO0OOO000O0 .df =OO0O00OO00O0O00OO #line:377
        print ("Encoding columns into bit-form...")#line:378
        OO00OOO00O0OOOOO0 =0 #line:379
        OOO00OO00O0O00OO0 =0 #line:380
        for OOO0000OO00OO00O0 in OO0O00OO00O0O00OO :#line:381
            if O000O0OO0OOO000O0 .verbosity ['debug']:#line:383
                print ('Column: '+OOO0000OO00OO00O0 )#line:384
            O000O0OO0OOO000O0 .data ["varname"].append (OOO0000OO00OO00O0 )#line:385
            O0OOO0O0000OOOO0O =pd .get_dummies (OO0O00OO00O0O00OO [OOO0000OO00OO00O0 ])#line:386
            OOO0OOOOOO0O0O0O0 =0 #line:387
            if (OO0O00OO00O0O00OO .dtypes [OOO0000OO00OO00O0 ].name =='category'):#line:388
                OOO0OOOOOO0O0O0O0 =1 #line:389
            O000O0OO0OOO000O0 .data ["vtypes"].append (OOO0OOOOOO0O0O0O0 )#line:390
            O0O00OOOOO00O0OO0 =0 #line:393
            O00OO0O0O000O000O =[]#line:394
            O000O00OO0OO0000O =[]#line:395
            for OOOO00OO0OO000O00 in O0OOO0O0000OOOO0O :#line:397
                if O000O0OO0OOO000O0 .verbosity ['debug']:#line:399
                    print ('....category : '+str (OOOO00OO0OO000O00 )+" @ "+str (time .time ()))#line:400
                O00OO0O0O000O000O .append (OOOO00OO0OO000O00 )#line:401
                O0O0OO0O0OO0OO0O0 =int (0 )#line:402
                O00OOOOO0000OOO0O =O0OOO0O0000OOOO0O [OOOO00OO0OO000O00 ].values #line:403
                OO00O0OOOO0O0O00O =numpy .packbits (O00OOOOO0000OOO0O ,bitorder ='little')#line:405
                O0O0OO0O0OO0OO0O0 =int .from_bytes (OO00O0OOOO0O0O00O ,byteorder ='little')#line:406
                O000O00OO0OO0000O .append (O0O0OO0O0OO0OO0O0 )#line:407
                O0O00OOOOO00O0OO0 +=1 #line:425
                OOO00OO00O0O00OO0 +=1 #line:426
            O000O0OO0OOO000O0 .data ["catnames"].append (O00OO0O0O000O000O )#line:428
            O000O0OO0OOO000O0 .data ["dm"].append (O000O00OO0OO0000O )#line:429
        print ("Encoding columns into bit-form...done")#line:431
        if O000O0OO0OOO000O0 .verbosity ['hint']:#line:432
            print (f"List of attributes for analysis is: {O000O0OO0OOO000O0.data['varname']}")#line:433
            print (f"List of category names for individual attributes is : {O000O0OO0OOO000O0.data['catnames']}")#line:434
        if O000O0OO0OOO000O0 .verbosity ['debug']:#line:435
            print (f"List of vtypes is (all should be 1) : {O000O0OO0OOO000O0.data['vtypes']}")#line:436
        O000O0OO0OOO000O0 .data ["data_prepared"]=1 #line:438
        print ("Data preparation finished.")#line:439
        if O000O0OO0OOO000O0 .verbosity ['debug']:#line:440
            print ('Number of variables : '+str (len (O000O0OO0OOO000O0 .data ["dm"])))#line:441
            print ('Total number of categories in all variables : '+str (OOO00OO00O0O00OO0 ))#line:442
        O000O0OO0OOO000O0 .stats ['end_prep_time']=time .time ()#line:443
        if O000O0OO0OOO000O0 .verbosity ['debug']:#line:444
            print ('Time needed for data preparation : ',str (O000O0OO0OOO000O0 .stats ['end_prep_time']-O000O0OO0OOO000O0 .stats ['start_prep_time']))#line:445
    def _bitcount (O0OO0OOO0000OOOOO ,OOO0O00OO0OOOO0O0 ):#line:447
        O0OOOO0OOO0O00O00 =None #line:448
        if (O0OO0OOO0000OOOOO ._is_py310 ):#line:449
            O0OOOO0OOO0O00O00 =OOO0O00OO0OOOO0O0 .bit_count ()#line:450
        else :#line:451
            O0OOOO0OOO0O00O00 =bin (OOO0O00OO0OOOO0O0 ).count ("1")#line:452
        return O0OOOO0OOO0O00O00 #line:453
    def _verifyCF (OO0OO0O00OO000000 ,_OO0O00OOO00000OOO ):#line:456
        O000OOO0000OO000O =OO0OO0O00OO000000 ._bitcount (_OO0O00OOO00000OOO )#line:457
        O0OOOOO0O0OO000O0 =[]#line:458
        OOO00O0OOOOO0O00O =[]#line:459
        O0000OO0OOO000O0O =0 #line:460
        OOO0OO00000OO00OO =0 #line:461
        O0OO0OO00OO0O0OOO =0 #line:462
        OOO0O0O0O0O0O0O0O =0 #line:463
        O00OO0000O00O0OOO =0 #line:464
        O0OOO0O0000OO00OO =0 #line:465
        O00O0O0O0OO00OO00 =0 #line:466
        OO0OO00000O0OOO00 =0 #line:467
        O0O000OOO0O00O00O =0 #line:468
        OOOO000OO0OO0OOOO =None #line:469
        O00OOOOOO0OO0OO00 =None #line:470
        O0O0000O00OOO00OO =None #line:471
        if ('min_step_size'in OO0OO0O00OO000000 .quantifiers ):#line:472
            OOOO000OO0OO0OOOO =OO0OO0O00OO000000 .quantifiers .get ('min_step_size')#line:473
        if ('min_rel_step_size'in OO0OO0O00OO000000 .quantifiers ):#line:474
            O00OOOOOO0OO0OO00 =OO0OO0O00OO000000 .quantifiers .get ('min_rel_step_size')#line:475
            if O00OOOOOO0OO0OO00 >=1 and O00OOOOOO0OO0OO00 <100 :#line:476
                O00OOOOOO0OO0OO00 =O00OOOOOO0OO0OO00 /100 #line:477
        OO0O0OO0O0O0OOO0O =0 #line:478
        OO0O0OOO0O0O0OO00 =0 #line:479
        OOO00OOO0O0OOO000 =[]#line:480
        if ('aad_weights'in OO0OO0O00OO000000 .quantifiers ):#line:481
            OO0O0OO0O0O0OOO0O =1 #line:482
            OO000O0000O0O00O0 =[]#line:483
            OOO00OOO0O0OOO000 =OO0OO0O00OO000000 .quantifiers .get ('aad_weights')#line:484
        O00O0OO00OOOO00OO =OO0OO0O00OO000000 .data ["dm"][OO0OO0O00OO000000 .data ["varname"].index (OO0OO0O00OO000000 .kwargs .get ('target'))]#line:485
        def O00OOO0O0OO0O00OO (OOO000O00OOOOOOOO ,O0000O000O0OOO00O ):#line:486
            O000OO0OOO0OOOO00 =True #line:487
            if (OOO000O00OOOOOOOO >O0000O000O0OOO00O ):#line:488
                if not (OOOO000OO0OO0OOOO is None or OOO000O00OOOOOOOO >=O0000O000O0OOO00O +OOOO000OO0OO0OOOO ):#line:489
                    O000OO0OOO0OOOO00 =False #line:490
                if not (O00OOOOOO0OO0OO00 is None or OOO000O00OOOOOOOO >=O0000O000O0OOO00O *(1 +O00OOOOOO0OO0OO00 )):#line:491
                    O000OO0OOO0OOOO00 =False #line:492
            if (OOO000O00OOOOOOOO <O0000O000O0OOO00O ):#line:493
                if not (OOOO000OO0OO0OOOO is None or OOO000O00OOOOOOOO <=O0000O000O0OOO00O -OOOO000OO0OO0OOOO ):#line:494
                    O000OO0OOO0OOOO00 =False #line:495
                if not (O00OOOOOO0OO0OO00 is None or OOO000O00OOOOOOOO <=O0000O000O0OOO00O *(1 -O00OOOOOO0OO0OO00 )):#line:496
                    O000OO0OOO0OOOO00 =False #line:497
            return O000OO0OOO0OOOO00 #line:498
        for OO00OOOO00O0OO0OO in range (len (O00O0OO00OOOO00OO )):#line:499
            OOO0OO00000OO00OO =O0000OO0OOO000O0O #line:501
            O0000OO0OOO000O0O =OO0OO0O00OO000000 ._bitcount (_OO0O00OOO00000OOO &O00O0OO00OOOO00OO [OO00OOOO00O0OO0OO ])#line:502
            O0OOOOO0O0OO000O0 .append (O0000OO0OOO000O0O )#line:503
            if OO00OOOO00O0OO0OO >0 :#line:504
                if (O0000OO0OOO000O0O >OOO0OO00000OO00OO ):#line:505
                    if (O0OO0OO00OO0O0OOO ==1 )and (O00OOO0O0OO0O00OO (O0000OO0OOO000O0O ,OOO0OO00000OO00OO )):#line:506
                        OO0OO00000O0OOO00 +=1 #line:507
                    else :#line:508
                        if O00OOO0O0OO0O00OO (O0000OO0OOO000O0O ,OOO0OO00000OO00OO ):#line:509
                            OO0OO00000O0OOO00 =1 #line:510
                        else :#line:511
                            OO0OO00000O0OOO00 =0 #line:512
                    if OO0OO00000O0OOO00 >OOO0O0O0O0O0O0O0O :#line:513
                        OOO0O0O0O0O0O0O0O =OO0OO00000O0OOO00 #line:514
                    O0OO0OO00OO0O0OOO =1 #line:515
                    if O00OOO0O0OO0O00OO (O0000OO0OOO000O0O ,OOO0OO00000OO00OO ):#line:516
                        O0OOO0O0000OO00OO +=1 #line:517
                if (O0000OO0OOO000O0O <OOO0OO00000OO00OO ):#line:518
                    if (O0OO0OO00OO0O0OOO ==-1 )and (O00OOO0O0OO0O00OO (O0000OO0OOO000O0O ,OOO0OO00000OO00OO )):#line:519
                        O0O000OOO0O00O00O +=1 #line:520
                    else :#line:521
                        if O00OOO0O0OO0O00OO (O0000OO0OOO000O0O ,OOO0OO00000OO00OO ):#line:522
                            O0O000OOO0O00O00O =1 #line:523
                        else :#line:524
                            O0O000OOO0O00O00O =0 #line:525
                    if O0O000OOO0O00O00O >O00OO0000O00O0OOO :#line:526
                        O00OO0000O00O0OOO =O0O000OOO0O00O00O #line:527
                    O0OO0OO00OO0O0OOO =-1 #line:528
                    if O00OOO0O0OO0O00OO (O0000OO0OOO000O0O ,OOO0OO00000OO00OO ):#line:529
                        O00O0O0O0OO00OO00 +=1 #line:530
                if (O0000OO0OOO000O0O ==OOO0OO00000OO00OO ):#line:531
                    O0OO0OO00OO0O0OOO =0 #line:532
                    O0O000OOO0O00O00O =0 #line:533
                    OO0OO00000O0OOO00 =0 #line:534
            if (OO0O0OO0O0O0OOO0O ):#line:536
                OOO0OOO00OO0000O0 =OO0OO0O00OO000000 ._bitcount (O00O0OO00OOOO00OO [OO00OOOO00O0OO0OO ])#line:537
                OO000O0000O0O00O0 .append (OOO0OOO00OO0000O0 )#line:538
        if (OO0O0OO0O0O0OOO0O &sum (O0OOOOO0O0OO000O0 )>0 ):#line:540
            for OO00OOOO00O0OO0OO in range (len (O00O0OO00OOOO00OO )):#line:541
                if OO000O0000O0O00O0 [OO00OOOO00O0OO0OO ]>0 :#line:542
                    if O0OOOOO0O0OO000O0 [OO00OOOO00O0OO0OO ]/sum (O0OOOOO0O0OO000O0 )>OO000O0000O0O00O0 [OO00OOOO00O0OO0OO ]/sum (OO000O0000O0O00O0 ):#line:544
                        OO0O0OOO0O0O0OO00 +=OOO00OOO0O0OOO000 [OO00OOOO00O0OO0OO ]*((O0OOOOO0O0OO000O0 [OO00OOOO00O0OO0OO ]/sum (O0OOOOO0O0OO000O0 ))/(OO000O0000O0O00O0 [OO00OOOO00O0OO0OO ]/sum (OO000O0000O0O00O0 ))-1 )#line:545
        O0OOOO00000OOOOOO =True #line:548
        for OOOOOO0O0O0OO00OO in OO0OO0O00OO000000 .quantifiers .keys ():#line:549
            if OOOOOO0O0O0OO00OO .upper ()=='BASE':#line:550
                O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )<=O000OOO0000OO000O )#line:551
            if OOOOOO0O0O0OO00OO .upper ()=='RELBASE':#line:552
                O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )<=O000OOO0000OO000O *1.0 /OO0OO0O00OO000000 .data ["rows_count"])#line:553
            if OOOOOO0O0O0OO00OO .upper ()=='S_UP':#line:554
                O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )<=OOO0O0O0O0O0O0O0O )#line:555
            if OOOOOO0O0O0OO00OO .upper ()=='S_DOWN':#line:556
                O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )<=O00OO0000O00O0OOO )#line:557
            if OOOOOO0O0O0OO00OO .upper ()=='S_ANY_UP':#line:558
                O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )<=OOO0O0O0O0O0O0O0O )#line:559
            if OOOOOO0O0O0OO00OO .upper ()=='S_ANY_DOWN':#line:560
                O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )<=O00OO0000O00O0OOO )#line:561
            if OOOOOO0O0O0OO00OO .upper ()=='MAX':#line:562
                O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )<=max (O0OOOOO0O0OO000O0 ))#line:563
            if OOOOOO0O0O0OO00OO .upper ()=='MIN':#line:564
                O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )<=min (O0OOOOO0O0OO000O0 ))#line:565
            if OOOOOO0O0O0OO00OO .upper ()=='RELMAX':#line:566
                if sum (O0OOOOO0O0OO000O0 )>0 :#line:567
                    O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )<=max (O0OOOOO0O0OO000O0 )*1.0 /sum (O0OOOOO0O0OO000O0 ))#line:568
                else :#line:569
                    O0OOOO00000OOOOOO =False #line:570
            if OOOOOO0O0O0OO00OO .upper ()=='RELMAX_LEQ':#line:571
                if sum (O0OOOOO0O0OO000O0 )>0 :#line:572
                    O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )>=max (O0OOOOO0O0OO000O0 )*1.0 /sum (O0OOOOO0O0OO000O0 ))#line:573
                else :#line:574
                    O0OOOO00000OOOOOO =False #line:575
            if OOOOOO0O0O0OO00OO .upper ()=='RELMIN':#line:576
                if sum (O0OOOOO0O0OO000O0 )>0 :#line:577
                    O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )<=min (O0OOOOO0O0OO000O0 )*1.0 /sum (O0OOOOO0O0OO000O0 ))#line:578
                else :#line:579
                    O0OOOO00000OOOOOO =False #line:580
            if OOOOOO0O0O0OO00OO .upper ()=='RELMIN_LEQ':#line:581
                if sum (O0OOOOO0O0OO000O0 )>0 :#line:582
                    O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )>=min (O0OOOOO0O0OO000O0 )*1.0 /sum (O0OOOOO0O0OO000O0 ))#line:583
                else :#line:584
                    O0OOOO00000OOOOOO =False #line:585
            if OOOOOO0O0O0OO00OO .upper ()=='AAD':#line:586
                O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )<=OO0O0OOO0O0O0OO00 )#line:587
            if OOOOOO0O0O0OO00OO .upper ()=='RELRANGE_LEQ':#line:589
                OO0O0OO000OO0000O =OO0OO0O00OO000000 .quantifiers .get (OOOOOO0O0O0OO00OO )#line:590
                if OO0O0OO000OO0000O >=1 and OO0O0OO000OO0000O <100 :#line:591
                    OO0O0OO000OO0000O =OO0O0OO000OO0000O *1.0 /100 #line:592
                OO00OO00OO00OOOO0 =min (O0OOOOO0O0OO000O0 )*1.0 /sum (O0OOOOO0O0OO000O0 )#line:593
                O000OOOO0000OOOOO =max (O0OOOOO0O0OO000O0 )*1.0 /sum (O0OOOOO0O0OO000O0 )#line:594
                O0OOOO00000OOOOOO =O0OOOO00000OOOOOO and (OO0O0OO000OO0000O >=O000OOOO0000OOOOO -OO00OO00OO00OOOO0 )#line:595
        O00OOOO0O0OOO00OO ={}#line:596
        if O0OOOO00000OOOOOO ==True :#line:597
            OO0OO0O00OO000000 .stats ['total_valid']+=1 #line:599
            O00OOOO0O0OOO00OO ["base"]=O000OOO0000OO000O #line:600
            O00OOOO0O0OOO00OO ["rel_base"]=O000OOO0000OO000O *1.0 /OO0OO0O00OO000000 .data ["rows_count"]#line:601
            O00OOOO0O0OOO00OO ["s_up"]=OOO0O0O0O0O0O0O0O #line:602
            O00OOOO0O0OOO00OO ["s_down"]=O00OO0000O00O0OOO #line:603
            O00OOOO0O0OOO00OO ["s_any_up"]=O0OOO0O0000OO00OO #line:604
            O00OOOO0O0OOO00OO ["s_any_down"]=O00O0O0O0OO00OO00 #line:605
            O00OOOO0O0OOO00OO ["max"]=max (O0OOOOO0O0OO000O0 )#line:606
            O00OOOO0O0OOO00OO ["min"]=min (O0OOOOO0O0OO000O0 )#line:607
            if sum (O0OOOOO0O0OO000O0 )>0 :#line:610
                O00OOOO0O0OOO00OO ["rel_max"]=max (O0OOOOO0O0OO000O0 )*1.0 /sum (O0OOOOO0O0OO000O0 )#line:611
                O00OOOO0O0OOO00OO ["rel_min"]=min (O0OOOOO0O0OO000O0 )*1.0 /sum (O0OOOOO0O0OO000O0 )#line:612
            else :#line:613
                O00OOOO0O0OOO00OO ["rel_max"]=0 #line:614
                O00OOOO0O0OOO00OO ["rel_min"]=0 #line:615
            O00OOOO0O0OOO00OO ["hist"]=O0OOOOO0O0OO000O0 #line:616
            if OO0O0OO0O0O0OOO0O :#line:617
                O00OOOO0O0OOO00OO ["aad"]=OO0O0OOO0O0O0OO00 #line:618
                O00OOOO0O0OOO00OO ["hist_full"]=OO000O0000O0O00O0 #line:619
                O00OOOO0O0OOO00OO ["rel_hist"]=[OOOO0O00OOOOO0000 /sum (O0OOOOO0O0OO000O0 )for OOOO0O00OOOOO0000 in O0OOOOO0O0OO000O0 ]#line:620
                O00OOOO0O0OOO00OO ["rel_hist_full"]=[O0O000O0000O00O0O /sum (OO000O0000O0O00O0 )for O0O000O0000O00O0O in OO000O0000O0O00O0 ]#line:621
        return O0OOOO00000OOOOOO ,O00OOOO0O0OOO00OO #line:623
    def _verifyUIC (OOO0OO0OO000OO000 ,_OOO0OO00O0O00OOO0 ):#line:625
        OO00OOOOO0O0O0OOO ={}#line:626
        O00O0O00O0OO0000O =0 #line:627
        for OOOOOOO0O000OO000 in OOO0OO0OO000OO000 .task_actinfo ['cedents']:#line:628
            OO00OOOOO0O0O0OOO [OOOOOOO0O000OO000 ['cedent_type']]=OOOOOOO0O000OO000 ['filter_value']#line:630
            O00O0O00O0OO0000O =O00O0O00O0OO0000O +1 #line:631
        O00OO0O0OOOOOO00O =OOO0OO0OO000OO000 ._bitcount (_OOO0OO00O0O00OOO0 )#line:633
        OO00OOO000O0OOOO0 =[]#line:634
        OO00OO0OOOO00OOO0 =0 #line:635
        OO00O0OOOOOO00OOO =0 #line:636
        O0OOO00000000000O =0 #line:637
        OO0O0O0000OO000O0 =[]#line:638
        O0OOOOO000OOOO000 =[]#line:639
        if ('aad_weights'in OOO0OO0OO000OO000 .quantifiers ):#line:640
            OO0O0O0000OO000O0 =OOO0OO0OO000OO000 .quantifiers .get ('aad_weights')#line:641
            OO00O0OOOOOO00OOO =1 #line:642
        OOOO0OOOO000OO0O0 =OOO0OO0OO000OO000 .data ["dm"][OOO0OO0OO000OO000 .data ["varname"].index (OOO0OO0OO000OO000 .kwargs .get ('target'))]#line:643
        for OO00000O000000OOO in range (len (OOOO0OOOO000OO0O0 )):#line:644
            OOO0O0OOO0O0O00OO =OO00OO0OOOO00OOO0 #line:646
            OO00OO0OOOO00OOO0 =OOO0OO0OO000OO000 ._bitcount (_OOO0OO00O0O00OOO0 &OOOO0OOOO000OO0O0 [OO00000O000000OOO ])#line:647
            OO00OOO000O0OOOO0 .append (OO00OO0OOOO00OOO0 )#line:648
            O000O00O00O000O00 =OOO0OO0OO000OO000 ._bitcount (OO00OOOOO0O0O0OOO ['cond']&OOOO0OOOO000OO0O0 [OO00000O000000OOO ])#line:651
            O0OOOOO000OOOO000 .append (O000O00O00O000O00 )#line:652
        if (OO00O0OOOOOO00OOO &sum (OO00OOO000O0OOOO0 )>0 ):#line:654
            for OO00000O000000OOO in range (len (OOOO0OOOO000OO0O0 )):#line:655
                if O0OOOOO000OOOO000 [OO00000O000000OOO ]>0 :#line:656
                    if OO00OOO000O0OOOO0 [OO00000O000000OOO ]/sum (OO00OOO000O0OOOO0 )>O0OOOOO000OOOO000 [OO00000O000000OOO ]/sum (O0OOOOO000OOOO000 ):#line:658
                        O0OOO00000000000O +=OO0O0O0000OO000O0 [OO00000O000000OOO ]*((OO00OOO000O0OOOO0 [OO00000O000000OOO ]/sum (OO00OOO000O0OOOO0 ))/(O0OOOOO000OOOO000 [OO00000O000000OOO ]/sum (O0OOOOO000OOOO000 ))-1 )#line:659
        OOO0000000O0O00O0 =True #line:662
        for OO0000OOOOO0OOOOO in OOO0OO0OO000OO000 .quantifiers .keys ():#line:663
            if OO0000OOOOO0OOOOO .upper ()=='BASE':#line:664
                OOO0000000O0O00O0 =OOO0000000O0O00O0 and (OOO0OO0OO000OO000 .quantifiers .get (OO0000OOOOO0OOOOO )<=O00OO0O0OOOOOO00O )#line:665
            if OO0000OOOOO0OOOOO .upper ()=='RELBASE':#line:666
                OOO0000000O0O00O0 =OOO0000000O0O00O0 and (OOO0OO0OO000OO000 .quantifiers .get (OO0000OOOOO0OOOOO )<=O00OO0O0OOOOOO00O *1.0 /OOO0OO0OO000OO000 .data ["rows_count"])#line:667
            if OO0000OOOOO0OOOOO .upper ()=='AAD_SCORE':#line:668
                OOO0000000O0O00O0 =OOO0000000O0O00O0 and (OOO0OO0OO000OO000 .quantifiers .get (OO0000OOOOO0OOOOO )<=O0OOO00000000000O )#line:669
        OOOOOOO0OO00OOO00 ={}#line:671
        if OOO0000000O0O00O0 ==True :#line:672
            OOO0OO0OO000OO000 .stats ['total_valid']+=1 #line:674
            OOOOOOO0OO00OOO00 ["base"]=O00OO0O0OOOOOO00O #line:675
            OOOOOOO0OO00OOO00 ["rel_base"]=O00OO0O0OOOOOO00O *1.0 /OOO0OO0OO000OO000 .data ["rows_count"]#line:676
            OOOOOOO0OO00OOO00 ["hist"]=OO00OOO000O0OOOO0 #line:677
            OOOOOOO0OO00OOO00 ["aad_score"]=O0OOO00000000000O #line:679
            OOOOOOO0OO00OOO00 ["hist_cond"]=O0OOOOO000OOOO000 #line:680
            OOOOOOO0OO00OOO00 ["rel_hist"]=[OOO0OOOO0O0O0O00O /sum (OO00OOO000O0OOOO0 )for OOO0OOOO0O0O0O00O in OO00OOO000O0OOOO0 ]#line:681
            OOOOOOO0OO00OOO00 ["rel_hist_cond"]=[O0O00O00OOO00O0O0 /sum (O0OOOOO000OOOO000 )for O0O00O00OOO00O0O0 in O0OOOOO000OOOO000 ]#line:682
        return OOO0000000O0O00O0 ,OOOOOOO0OO00OOO00 #line:684
    def _verify4ft (OOO0OO00O00OOOOOO ,_OO0O00OOOOOOOOO0O ):#line:686
        O00O0O00000OO0O0O ={}#line:687
        OOO00000O00OO00OO =0 #line:688
        for O0OO000O00OOOOO0O in OOO0OO00O00OOOOOO .task_actinfo ['cedents']:#line:689
            O00O0O00000OO0O0O [O0OO000O00OOOOO0O ['cedent_type']]=O0OO000O00OOOOO0O ['filter_value']#line:691
            OOO00000O00OO00OO =OOO00000O00OO00OO +1 #line:692
        OO00000000OOOO0O0 =OOO0OO00O00OOOOOO ._bitcount (O00O0O00000OO0O0O ['ante']&O00O0O00000OO0O0O ['succ']&O00O0O00000OO0O0O ['cond'])#line:694
        O00O0000OO000OO00 =None #line:695
        O00O0000OO000OO00 =0 #line:696
        if OO00000000OOOO0O0 >0 :#line:705
            O00O0000OO000OO00 =OOO0OO00O00OOOOOO ._bitcount (O00O0O00000OO0O0O ['ante']&O00O0O00000OO0O0O ['succ']&O00O0O00000OO0O0O ['cond'])*1.0 /OOO0OO00O00OOOOOO ._bitcount (O00O0O00000OO0O0O ['ante']&O00O0O00000OO0O0O ['cond'])#line:706
        OO00O0OOOO000O000 =1 <<OOO0OO00O00OOOOOO .data ["rows_count"]#line:708
        OOO0OOO0000000O00 =OOO0OO00O00OOOOOO ._bitcount (O00O0O00000OO0O0O ['ante']&O00O0O00000OO0O0O ['succ']&O00O0O00000OO0O0O ['cond'])#line:709
        OO0OOO000O0O0O0O0 =OOO0OO00O00OOOOOO ._bitcount (O00O0O00000OO0O0O ['ante']&~(OO00O0OOOO000O000 |O00O0O00000OO0O0O ['succ'])&O00O0O00000OO0O0O ['cond'])#line:710
        O0OO000O00OOOOO0O =OOO0OO00O00OOOOOO ._bitcount (~(OO00O0OOOO000O000 |O00O0O00000OO0O0O ['ante'])&O00O0O00000OO0O0O ['succ']&O00O0O00000OO0O0O ['cond'])#line:711
        OOO0OOO00OO000O00 =OOO0OO00O00OOOOOO ._bitcount (~(OO00O0OOOO000O000 |O00O0O00000OO0O0O ['ante'])&~(OO00O0OOOO000O000 |O00O0O00000OO0O0O ['succ'])&O00O0O00000OO0O0O ['cond'])#line:712
        OO0O00OOOO0OOO00O =0 #line:713
        if (OOO0OOO0000000O00 +OO0OOO000O0O0O0O0 )*(OOO0OOO0000000O00 +O0OO000O00OOOOO0O )>0 :#line:714
            OO0O00OOOO0OOO00O =OOO0OOO0000000O00 *(OOO0OOO0000000O00 +OO0OOO000O0O0O0O0 +O0OO000O00OOOOO0O +OOO0OOO00OO000O00 )/(OOO0OOO0000000O00 +OO0OOO000O0O0O0O0 )/(OOO0OOO0000000O00 +O0OO000O00OOOOO0O )-1 #line:715
        else :#line:716
            OO0O00OOOO0OOO00O =None #line:717
        OOO00OO0O0OO000O0 =0 #line:718
        if (OOO0OOO0000000O00 +OO0OOO000O0O0O0O0 )*(OOO0OOO0000000O00 +O0OO000O00OOOOO0O )>0 :#line:719
            OOO00OO0O0OO000O0 =1 -OOO0OOO0000000O00 *(OOO0OOO0000000O00 +OO0OOO000O0O0O0O0 +O0OO000O00OOOOO0O +OOO0OOO00OO000O00 )/(OOO0OOO0000000O00 +OO0OOO000O0O0O0O0 )/(OOO0OOO0000000O00 +O0OO000O00OOOOO0O )#line:720
        else :#line:721
            OOO00OO0O0OO000O0 =None #line:722
        O0OO0O0OO0000O0O0 =True #line:723
        for O00OOO000OOO00OO0 in OOO0OO00O00OOOOOO .quantifiers .keys ():#line:724
            if O00OOO000OOO00OO0 .upper ()=='BASE':#line:725
                O0OO0O0OO0000O0O0 =O0OO0O0OO0000O0O0 and (OOO0OO00O00OOOOOO .quantifiers .get (O00OOO000OOO00OO0 )<=OO00000000OOOO0O0 )#line:726
            if O00OOO000OOO00OO0 .upper ()=='RELBASE':#line:727
                O0OO0O0OO0000O0O0 =O0OO0O0OO0000O0O0 and (OOO0OO00O00OOOOOO .quantifiers .get (O00OOO000OOO00OO0 )<=OO00000000OOOO0O0 *1.0 /OOO0OO00O00OOOOOO .data ["rows_count"])#line:728
            if (O00OOO000OOO00OO0 .upper ()=='PIM')or (O00OOO000OOO00OO0 .upper ()=='CONF'):#line:729
                O0OO0O0OO0000O0O0 =O0OO0O0OO0000O0O0 and (OOO0OO00O00OOOOOO .quantifiers .get (O00OOO000OOO00OO0 )<=O00O0000OO000OO00 )#line:730
            if O00OOO000OOO00OO0 .upper ()=='AAD':#line:731
                if OO0O00OOOO0OOO00O !=None :#line:732
                    O0OO0O0OO0000O0O0 =O0OO0O0OO0000O0O0 and (OOO0OO00O00OOOOOO .quantifiers .get (O00OOO000OOO00OO0 )<=OO0O00OOOO0OOO00O )#line:733
                else :#line:734
                    O0OO0O0OO0000O0O0 =False #line:735
            if O00OOO000OOO00OO0 .upper ()=='BAD':#line:736
                if OOO00OO0O0OO000O0 !=None :#line:737
                    O0OO0O0OO0000O0O0 =O0OO0O0OO0000O0O0 and (OOO0OO00O00OOOOOO .quantifiers .get (O00OOO000OOO00OO0 )<=OOO00OO0O0OO000O0 )#line:738
                else :#line:739
                    O0OO0O0OO0000O0O0 =False #line:740
            O0000OO00OOOOO00O ={}#line:741
        if O0OO0O0OO0000O0O0 ==True :#line:742
            OOO0OO00O00OOOOOO .stats ['total_valid']+=1 #line:744
            O0000OO00OOOOO00O ["base"]=OO00000000OOOO0O0 #line:745
            O0000OO00OOOOO00O ["rel_base"]=OO00000000OOOO0O0 *1.0 /OOO0OO00O00OOOOOO .data ["rows_count"]#line:746
            O0000OO00OOOOO00O ["conf"]=O00O0000OO000OO00 #line:747
            O0000OO00OOOOO00O ["aad"]=OO0O00OOOO0OOO00O #line:748
            O0000OO00OOOOO00O ["bad"]=OOO00OO0O0OO000O0 #line:749
            O0000OO00OOOOO00O ["fourfold"]=[OOO0OOO0000000O00 ,OO0OOO000O0O0O0O0 ,O0OO000O00OOOOO0O ,OOO0OOO00OO000O00 ]#line:750
        return O0OO0O0OO0000O0O0 ,O0000OO00OOOOO00O #line:754
    def _verifysd4ft (OOO00OO00000OOO0O ,_O0OO0O0OO0O00O000 ):#line:756
        O0OO000000O0OOO00 ={}#line:757
        OOO0OOO000OOOO0O0 =0 #line:758
        for OO00OO00O00OO0000 in OOO00OO00000OOO0O .task_actinfo ['cedents']:#line:759
            O0OO000000O0OOO00 [OO00OO00O00OO0000 ['cedent_type']]=OO00OO00O00OO0000 ['filter_value']#line:761
            OOO0OOO000OOOO0O0 =OOO0OOO000OOOO0O0 +1 #line:762
        O0O0OO0O00O00OOO0 =OOO00OO00000OOO0O ._bitcount (O0OO000000O0OOO00 ['ante']&O0OO000000O0OOO00 ['succ']&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['frst'])#line:764
        OO0O00OOO0O00OO00 =OOO00OO00000OOO0O ._bitcount (O0OO000000O0OOO00 ['ante']&O0OO000000O0OOO00 ['succ']&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['scnd'])#line:765
        O0O0OO0O00O0OOOO0 =None #line:766
        OO00OOOO00OO0000O =0 #line:767
        O00O00OO0O0O00OOO =0 #line:768
        if O0O0OO0O00O00OOO0 >0 :#line:777
            OO00OOOO00OO0000O =OOO00OO00000OOO0O ._bitcount (O0OO000000O0OOO00 ['ante']&O0OO000000O0OOO00 ['succ']&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['frst'])*1.0 /OOO00OO00000OOO0O ._bitcount (O0OO000000O0OOO00 ['ante']&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['frst'])#line:778
        if OO0O00OOO0O00OO00 >0 :#line:779
            O00O00OO0O0O00OOO =OOO00OO00000OOO0O ._bitcount (O0OO000000O0OOO00 ['ante']&O0OO000000O0OOO00 ['succ']&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['scnd'])*1.0 /OOO00OO00000OOO0O ._bitcount (O0OO000000O0OOO00 ['ante']&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['scnd'])#line:780
        O00OO0OO0OOO0OOO0 =1 <<OOO00OO00000OOO0O .data ["rows_count"]#line:782
        O000OOOOO00O0OOOO =OOO00OO00000OOO0O ._bitcount (O0OO000000O0OOO00 ['ante']&O0OO000000O0OOO00 ['succ']&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['frst'])#line:783
        O0O0000O0000OOO0O =OOO00OO00000OOO0O ._bitcount (O0OO000000O0OOO00 ['ante']&~(O00OO0OO0OOO0OOO0 |O0OO000000O0OOO00 ['succ'])&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['frst'])#line:784
        OO00OOOOOOO0OO00O =OOO00OO00000OOO0O ._bitcount (~(O00OO0OO0OOO0OOO0 |O0OO000000O0OOO00 ['ante'])&O0OO000000O0OOO00 ['succ']&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['frst'])#line:785
        O0OOO000000OO000O =OOO00OO00000OOO0O ._bitcount (~(O00OO0OO0OOO0OOO0 |O0OO000000O0OOO00 ['ante'])&~(O00OO0OO0OOO0OOO0 |O0OO000000O0OOO00 ['succ'])&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['frst'])#line:786
        O000OO0O0OO0O00O0 =OOO00OO00000OOO0O ._bitcount (O0OO000000O0OOO00 ['ante']&O0OO000000O0OOO00 ['succ']&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['scnd'])#line:787
        OOO00OOOO0O0OO0OO =OOO00OO00000OOO0O ._bitcount (O0OO000000O0OOO00 ['ante']&~(O00OO0OO0OOO0OOO0 |O0OO000000O0OOO00 ['succ'])&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['scnd'])#line:788
        O0O00OOO00OO000O0 =OOO00OO00000OOO0O ._bitcount (~(O00OO0OO0OOO0OOO0 |O0OO000000O0OOO00 ['ante'])&O0OO000000O0OOO00 ['succ']&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['scnd'])#line:789
        OOO0O0O00O00OO000 =OOO00OO00000OOO0O ._bitcount (~(O00OO0OO0OOO0OOO0 |O0OO000000O0OOO00 ['ante'])&~(O00OO0OO0OOO0OOO0 |O0OO000000O0OOO00 ['succ'])&O0OO000000O0OOO00 ['cond']&O0OO000000O0OOO00 ['scnd'])#line:790
        O0OOOOO00O0O00000 =True #line:791
        for O0OO00OO000OO0O00 in OOO00OO00000OOO0O .quantifiers .keys ():#line:792
            if (O0OO00OO000OO0O00 .upper ()=='FRSTBASE')|(O0OO00OO000OO0O00 .upper ()=='BASE1'):#line:793
                O0OOOOO00O0O00000 =O0OOOOO00O0O00000 and (OOO00OO00000OOO0O .quantifiers .get (O0OO00OO000OO0O00 )<=O0O0OO0O00O00OOO0 )#line:794
            if (O0OO00OO000OO0O00 .upper ()=='SCNDBASE')|(O0OO00OO000OO0O00 .upper ()=='BASE2'):#line:795
                O0OOOOO00O0O00000 =O0OOOOO00O0O00000 and (OOO00OO00000OOO0O .quantifiers .get (O0OO00OO000OO0O00 )<=OO0O00OOO0O00OO00 )#line:796
            if (O0OO00OO000OO0O00 .upper ()=='FRSTRELBASE')|(O0OO00OO000OO0O00 .upper ()=='RELBASE1'):#line:797
                O0OOOOO00O0O00000 =O0OOOOO00O0O00000 and (OOO00OO00000OOO0O .quantifiers .get (O0OO00OO000OO0O00 )<=O0O0OO0O00O00OOO0 *1.0 /OOO00OO00000OOO0O .data ["rows_count"])#line:798
            if (O0OO00OO000OO0O00 .upper ()=='SCNDRELBASE')|(O0OO00OO000OO0O00 .upper ()=='RELBASE2'):#line:799
                O0OOOOO00O0O00000 =O0OOOOO00O0O00000 and (OOO00OO00000OOO0O .quantifiers .get (O0OO00OO000OO0O00 )<=OO0O00OOO0O00OO00 *1.0 /OOO00OO00000OOO0O .data ["rows_count"])#line:800
            if (O0OO00OO000OO0O00 .upper ()=='FRSTPIM')|(O0OO00OO000OO0O00 .upper ()=='PIM1')|(O0OO00OO000OO0O00 .upper ()=='FRSTCONF')|(O0OO00OO000OO0O00 .upper ()=='CONF1'):#line:801
                O0OOOOO00O0O00000 =O0OOOOO00O0O00000 and (OOO00OO00000OOO0O .quantifiers .get (O0OO00OO000OO0O00 )<=OO00OOOO00OO0000O )#line:802
            if (O0OO00OO000OO0O00 .upper ()=='SCNDPIM')|(O0OO00OO000OO0O00 .upper ()=='PIM2')|(O0OO00OO000OO0O00 .upper ()=='SCNDCONF')|(O0OO00OO000OO0O00 .upper ()=='CONF2'):#line:803
                O0OOOOO00O0O00000 =O0OOOOO00O0O00000 and (OOO00OO00000OOO0O .quantifiers .get (O0OO00OO000OO0O00 )<=O00O00OO0O0O00OOO )#line:804
            if (O0OO00OO000OO0O00 .upper ()=='DELTAPIM')|(O0OO00OO000OO0O00 .upper ()=='DELTACONF'):#line:805
                O0OOOOO00O0O00000 =O0OOOOO00O0O00000 and (OOO00OO00000OOO0O .quantifiers .get (O0OO00OO000OO0O00 )<=OO00OOOO00OO0000O -O00O00OO0O0O00OOO )#line:806
            if (O0OO00OO000OO0O00 .upper ()=='RATIOPIM')|(O0OO00OO000OO0O00 .upper ()=='RATIOCONF'):#line:809
                if (O00O00OO0O0O00OOO >0 ):#line:810
                    O0OOOOO00O0O00000 =O0OOOOO00O0O00000 and (OOO00OO00000OOO0O .quantifiers .get (O0OO00OO000OO0O00 )<=OO00OOOO00OO0000O *1.0 /O00O00OO0O0O00OOO )#line:811
                else :#line:812
                    O0OOOOO00O0O00000 =False #line:813
            if (O0OO00OO000OO0O00 .upper ()=='RATIOPIM_LEQ')|(O0OO00OO000OO0O00 .upper ()=='RATIOCONF_LEQ'):#line:814
                if (O00O00OO0O0O00OOO >0 ):#line:815
                    O0OOOOO00O0O00000 =O0OOOOO00O0O00000 and (OOO00OO00000OOO0O .quantifiers .get (O0OO00OO000OO0O00 )>=OO00OOOO00OO0000O *1.0 /O00O00OO0O0O00OOO )#line:816
                else :#line:817
                    O0OOOOO00O0O00000 =False #line:818
        O0OO000OO00O00000 ={}#line:819
        if O0OOOOO00O0O00000 ==True :#line:820
            OOO00OO00000OOO0O .stats ['total_valid']+=1 #line:822
            O0OO000OO00O00000 ["base1"]=O0O0OO0O00O00OOO0 #line:823
            O0OO000OO00O00000 ["base2"]=OO0O00OOO0O00OO00 #line:824
            O0OO000OO00O00000 ["rel_base1"]=O0O0OO0O00O00OOO0 *1.0 /OOO00OO00000OOO0O .data ["rows_count"]#line:825
            O0OO000OO00O00000 ["rel_base2"]=OO0O00OOO0O00OO00 *1.0 /OOO00OO00000OOO0O .data ["rows_count"]#line:826
            O0OO000OO00O00000 ["conf1"]=OO00OOOO00OO0000O #line:827
            O0OO000OO00O00000 ["conf2"]=O00O00OO0O0O00OOO #line:828
            O0OO000OO00O00000 ["deltaconf"]=OO00OOOO00OO0000O -O00O00OO0O0O00OOO #line:829
            if (O00O00OO0O0O00OOO >0 ):#line:830
                O0OO000OO00O00000 ["ratioconf"]=OO00OOOO00OO0000O *1.0 /O00O00OO0O0O00OOO #line:831
            else :#line:832
                O0OO000OO00O00000 ["ratioconf"]=None #line:833
            O0OO000OO00O00000 ["fourfold1"]=[O000OOOOO00O0OOOO ,O0O0000O0000OOO0O ,OO00OOOOOOO0OO00O ,O0OOO000000OO000O ]#line:834
            O0OO000OO00O00000 ["fourfold2"]=[O000OO0O0OO0O00O0 ,OOO00OOOO0O0OO0OO ,O0O00OOO00OO000O0 ,OOO0O0O00O00OO000 ]#line:835
        return O0OOOOO00O0O00000 ,O0OO000OO00O00000 #line:839
    def _verifynewact4ft (OO0O0O00O0OOOO00O ,_OOO0OO00O0O000O0O ):#line:841
        O00000O0OO00OOO0O ={}#line:842
        for OOO0OOOO0O00OO000 in OO0O0O00O0OOOO00O .task_actinfo ['cedents']:#line:843
            O00000O0OO00OOO0O [OOO0OOOO0O00OO000 ['cedent_type']]=OOO0OOOO0O00OO000 ['filter_value']#line:845
        OO000O0O0O00OO000 =OO0O0O00O0OOOO00O ._bitcount (O00000O0OO00OOO0O ['ante']&O00000O0OO00OOO0O ['succ']&O00000O0OO00OOO0O ['cond'])#line:847
        OOO0000000OO000O0 =OO0O0O00O0OOOO00O ._bitcount (O00000O0OO00OOO0O ['ante']&O00000O0OO00OOO0O ['succ']&O00000O0OO00OOO0O ['cond']&O00000O0OO00OOO0O ['antv']&O00000O0OO00OOO0O ['sucv'])#line:848
        O000O0OO000O00OO0 =None #line:849
        OOO00O0O0O0OOO000 =0 #line:850
        O00000OO000OOO0O0 =0 #line:851
        if OO000O0O0O00OO000 >0 :#line:860
            OOO00O0O0O0OOO000 =OO0O0O00O0OOOO00O ._bitcount (O00000O0OO00OOO0O ['ante']&O00000O0OO00OOO0O ['succ']&O00000O0OO00OOO0O ['cond'])*1.0 /OO0O0O00O0OOOO00O ._bitcount (O00000O0OO00OOO0O ['ante']&O00000O0OO00OOO0O ['cond'])#line:861
        if OOO0000000OO000O0 >0 :#line:862
            O00000OO000OOO0O0 =OO0O0O00O0OOOO00O ._bitcount (O00000O0OO00OOO0O ['ante']&O00000O0OO00OOO0O ['succ']&O00000O0OO00OOO0O ['cond']&O00000O0OO00OOO0O ['antv']&O00000O0OO00OOO0O ['sucv'])*1.0 /OO0O0O00O0OOOO00O ._bitcount (O00000O0OO00OOO0O ['ante']&O00000O0OO00OOO0O ['cond']&O00000O0OO00OOO0O ['antv'])#line:864
        OO0OO0OOO00O0000O =1 <<OO0O0O00O0OOOO00O .rows_count #line:866
        O00000OO0OO000O0O =OO0O0O00O0OOOO00O ._bitcount (O00000O0OO00OOO0O ['ante']&O00000O0OO00OOO0O ['succ']&O00000O0OO00OOO0O ['cond'])#line:867
        O00O000O0O00OOOO0 =OO0O0O00O0OOOO00O ._bitcount (O00000O0OO00OOO0O ['ante']&~(OO0OO0OOO00O0000O |O00000O0OO00OOO0O ['succ'])&O00000O0OO00OOO0O ['cond'])#line:868
        OO0O000O00O000OO0 =OO0O0O00O0OOOO00O ._bitcount (~(OO0OO0OOO00O0000O |O00000O0OO00OOO0O ['ante'])&O00000O0OO00OOO0O ['succ']&O00000O0OO00OOO0O ['cond'])#line:869
        OO000O000O00O000O =OO0O0O00O0OOOO00O ._bitcount (~(OO0OO0OOO00O0000O |O00000O0OO00OOO0O ['ante'])&~(OO0OO0OOO00O0000O |O00000O0OO00OOO0O ['succ'])&O00000O0OO00OOO0O ['cond'])#line:870
        O0OO000O0000O000O =OO0O0O00O0OOOO00O ._bitcount (O00000O0OO00OOO0O ['ante']&O00000O0OO00OOO0O ['succ']&O00000O0OO00OOO0O ['cond']&O00000O0OO00OOO0O ['antv']&O00000O0OO00OOO0O ['sucv'])#line:871
        OO0OO00O000O00O00 =OO0O0O00O0OOOO00O ._bitcount (O00000O0OO00OOO0O ['ante']&~(OO0OO0OOO00O0000O |(O00000O0OO00OOO0O ['succ']&O00000O0OO00OOO0O ['sucv']))&O00000O0OO00OOO0O ['cond'])#line:872
        O000OOOOOOO0O0O00 =OO0O0O00O0OOOO00O ._bitcount (~(OO0OO0OOO00O0000O |(O00000O0OO00OOO0O ['ante']&O00000O0OO00OOO0O ['antv']))&O00000O0OO00OOO0O ['succ']&O00000O0OO00OOO0O ['cond']&O00000O0OO00OOO0O ['sucv'])#line:873
        OOO0O00OOO00OOOO0 =OO0O0O00O0OOOO00O ._bitcount (~(OO0OO0OOO00O0000O |(O00000O0OO00OOO0O ['ante']&O00000O0OO00OOO0O ['antv']))&~(OO0OO0OOO00O0000O |(O00000O0OO00OOO0O ['succ']&O00000O0OO00OOO0O ['sucv']))&O00000O0OO00OOO0O ['cond'])#line:874
        O00O0O00O00OOOOO0 =True #line:875
        for O000O0O0000O0000O in OO0O0O00O0OOOO00O .quantifiers .keys ():#line:876
            if (O000O0O0000O0000O =='PreBase')|(O000O0O0000O0000O =='Base1'):#line:877
                O00O0O00O00OOOOO0 =O00O0O00O00OOOOO0 and (OO0O0O00O0OOOO00O .quantifiers .get (O000O0O0000O0000O )<=OO000O0O0O00OO000 )#line:878
            if (O000O0O0000O0000O =='PostBase')|(O000O0O0000O0000O =='Base2'):#line:879
                O00O0O00O00OOOOO0 =O00O0O00O00OOOOO0 and (OO0O0O00O0OOOO00O .quantifiers .get (O000O0O0000O0000O )<=OOO0000000OO000O0 )#line:880
            if (O000O0O0000O0000O =='PreRelBase')|(O000O0O0000O0000O =='RelBase1'):#line:881
                O00O0O00O00OOOOO0 =O00O0O00O00OOOOO0 and (OO0O0O00O0OOOO00O .quantifiers .get (O000O0O0000O0000O )<=OO000O0O0O00OO000 *1.0 /OO0O0O00O0OOOO00O .data ["rows_count"])#line:882
            if (O000O0O0000O0000O =='PostRelBase')|(O000O0O0000O0000O =='RelBase2'):#line:883
                O00O0O00O00OOOOO0 =O00O0O00O00OOOOO0 and (OO0O0O00O0OOOO00O .quantifiers .get (O000O0O0000O0000O )<=OOO0000000OO000O0 *1.0 /OO0O0O00O0OOOO00O .data ["rows_count"])#line:884
            if (O000O0O0000O0000O =='Prepim')|(O000O0O0000O0000O =='pim1')|(O000O0O0000O0000O =='PreConf')|(O000O0O0000O0000O =='conf1'):#line:885
                O00O0O00O00OOOOO0 =O00O0O00O00OOOOO0 and (OO0O0O00O0OOOO00O .quantifiers .get (O000O0O0000O0000O )<=OOO00O0O0O0OOO000 )#line:886
            if (O000O0O0000O0000O =='Postpim')|(O000O0O0000O0000O =='pim2')|(O000O0O0000O0000O =='PostConf')|(O000O0O0000O0000O =='conf2'):#line:887
                O00O0O00O00OOOOO0 =O00O0O00O00OOOOO0 and (OO0O0O00O0OOOO00O .quantifiers .get (O000O0O0000O0000O )<=O00000OO000OOO0O0 )#line:888
            if (O000O0O0000O0000O =='Deltapim')|(O000O0O0000O0000O =='DeltaConf'):#line:889
                O00O0O00O00OOOOO0 =O00O0O00O00OOOOO0 and (OO0O0O00O0OOOO00O .quantifiers .get (O000O0O0000O0000O )<=OOO00O0O0O0OOO000 -O00000OO000OOO0O0 )#line:890
            if (O000O0O0000O0000O =='Ratiopim')|(O000O0O0000O0000O =='RatioConf'):#line:893
                if (O00000OO000OOO0O0 >0 ):#line:894
                    O00O0O00O00OOOOO0 =O00O0O00O00OOOOO0 and (OO0O0O00O0OOOO00O .quantifiers .get (O000O0O0000O0000O )<=OOO00O0O0O0OOO000 *1.0 /O00000OO000OOO0O0 )#line:895
                else :#line:896
                    O00O0O00O00OOOOO0 =False #line:897
        OOOOOOO00O0OOOO00 ={}#line:898
        if O00O0O00O00OOOOO0 ==True :#line:899
            OO0O0O00O0OOOO00O .stats ['total_valid']+=1 #line:901
            OOOOOOO00O0OOOO00 ["base1"]=OO000O0O0O00OO000 #line:902
            OOOOOOO00O0OOOO00 ["base2"]=OOO0000000OO000O0 #line:903
            OOOOOOO00O0OOOO00 ["rel_base1"]=OO000O0O0O00OO000 *1.0 /OO0O0O00O0OOOO00O .data ["rows_count"]#line:904
            OOOOOOO00O0OOOO00 ["rel_base2"]=OOO0000000OO000O0 *1.0 /OO0O0O00O0OOOO00O .data ["rows_count"]#line:905
            OOOOOOO00O0OOOO00 ["conf1"]=OOO00O0O0O0OOO000 #line:906
            OOOOOOO00O0OOOO00 ["conf2"]=O00000OO000OOO0O0 #line:907
            OOOOOOO00O0OOOO00 ["deltaconf"]=OOO00O0O0O0OOO000 -O00000OO000OOO0O0 #line:908
            if (O00000OO000OOO0O0 >0 ):#line:909
                OOOOOOO00O0OOOO00 ["ratioconf"]=OOO00O0O0O0OOO000 *1.0 /O00000OO000OOO0O0 #line:910
            else :#line:911
                OOOOOOO00O0OOOO00 ["ratioconf"]=None #line:912
            OOOOOOO00O0OOOO00 ["fourfoldpre"]=[O00000OO0OO000O0O ,O00O000O0O00OOOO0 ,OO0O000O00O000OO0 ,OO000O000O00O000O ]#line:913
            OOOOOOO00O0OOOO00 ["fourfoldpost"]=[O0OO000O0000O000O ,OO0OO00O000O00O00 ,O000OOOOOOO0O0O00 ,OOO0O00OOO00OOOO0 ]#line:914
        return O00O0O00O00OOOOO0 ,OOOOOOO00O0OOOO00 #line:916
    def _verifyact4ft (OO0000OO0OO00OO0O ,_O00O0000000O000O0 ):#line:918
        O000O000O0O0OO0OO ={}#line:919
        for O0O0OO0OOOOOO00OO in OO0000OO0OO00OO0O .task_actinfo ['cedents']:#line:920
            O000O000O0O0OO0OO [O0O0OO0OOOOOO00OO ['cedent_type']]=O0O0OO0OOOOOO00OO ['filter_value']#line:922
        OO0OO0O0O00OO00OO =OO0000OO0OO00OO0O ._bitcount (O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['succ']&O000O000O0O0OO0OO ['cond']&O000O000O0O0OO0OO ['antv-']&O000O000O0O0OO0OO ['sucv-'])#line:924
        O000000O00O0O000O =OO0000OO0OO00OO0O ._bitcount (O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['succ']&O000O000O0O0OO0OO ['cond']&O000O000O0O0OO0OO ['antv+']&O000O000O0O0OO0OO ['sucv+'])#line:925
        O0O0OOOO0O00O00OO =None #line:926
        O00O000O000O0O0OO =0 #line:927
        O00OO000OOO00OOO0 =0 #line:928
        if OO0OO0O0O00OO00OO >0 :#line:937
            O00O000O000O0O0OO =OO0000OO0OO00OO0O ._bitcount (O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['succ']&O000O000O0O0OO0OO ['cond']&O000O000O0O0OO0OO ['antv-']&O000O000O0O0OO0OO ['sucv-'])*1.0 /OO0000OO0OO00OO0O ._bitcount (O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['cond']&O000O000O0O0OO0OO ['antv-'])#line:939
        if O000000O00O0O000O >0 :#line:940
            O00OO000OOO00OOO0 =OO0000OO0OO00OO0O ._bitcount (O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['succ']&O000O000O0O0OO0OO ['cond']&O000O000O0O0OO0OO ['antv+']&O000O000O0O0OO0OO ['sucv+'])*1.0 /OO0000OO0OO00OO0O ._bitcount (O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['cond']&O000O000O0O0OO0OO ['antv+'])#line:942
        OO000OOOO000000O0 =1 <<OO0000OO0OO00OO0O .data ["rows_count"]#line:944
        OOOO0O0OO0OO00000 =OO0000OO0OO00OO0O ._bitcount (O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['succ']&O000O000O0O0OO0OO ['cond']&O000O000O0O0OO0OO ['antv-']&O000O000O0O0OO0OO ['sucv-'])#line:945
        O000O00000O0OOO0O =OO0000OO0OO00OO0O ._bitcount (O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['antv-']&~(OO000OOOO000000O0 |(O000O000O0O0OO0OO ['succ']&O000O000O0O0OO0OO ['sucv-']))&O000O000O0O0OO0OO ['cond'])#line:946
        O000OOO0OOOO00000 =OO0000OO0OO00OO0O ._bitcount (~(OO000OOOO000000O0 |(O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['antv-']))&O000O000O0O0OO0OO ['succ']&O000O000O0O0OO0OO ['cond']&O000O000O0O0OO0OO ['sucv-'])#line:947
        O00000O0OOOOOO0OO =OO0000OO0OO00OO0O ._bitcount (~(OO000OOOO000000O0 |(O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['antv-']))&~(OO000OOOO000000O0 |(O000O000O0O0OO0OO ['succ']&O000O000O0O0OO0OO ['sucv-']))&O000O000O0O0OO0OO ['cond'])#line:948
        OOO0O0OO0OOO0OO00 =OO0000OO0OO00OO0O ._bitcount (O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['succ']&O000O000O0O0OO0OO ['cond']&O000O000O0O0OO0OO ['antv+']&O000O000O0O0OO0OO ['sucv+'])#line:949
        OO0O0OO0OOOO00OO0 =OO0000OO0OO00OO0O ._bitcount (O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['antv+']&~(OO000OOOO000000O0 |(O000O000O0O0OO0OO ['succ']&O000O000O0O0OO0OO ['sucv+']))&O000O000O0O0OO0OO ['cond'])#line:950
        O000O00O0O0000OO0 =OO0000OO0OO00OO0O ._bitcount (~(OO000OOOO000000O0 |(O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['antv+']))&O000O000O0O0OO0OO ['succ']&O000O000O0O0OO0OO ['cond']&O000O000O0O0OO0OO ['sucv+'])#line:951
        OO000OOOOO0OO000O =OO0000OO0OO00OO0O ._bitcount (~(OO000OOOO000000O0 |(O000O000O0O0OO0OO ['ante']&O000O000O0O0OO0OO ['antv+']))&~(OO000OOOO000000O0 |(O000O000O0O0OO0OO ['succ']&O000O000O0O0OO0OO ['sucv+']))&O000O000O0O0OO0OO ['cond'])#line:952
        O000O00000O0O0O0O =True #line:953
        for O000000OOO0000000 in OO0000OO0OO00OO0O .quantifiers .keys ():#line:954
            if (O000000OOO0000000 =='PreBase')|(O000000OOO0000000 =='Base1'):#line:955
                O000O00000O0O0O0O =O000O00000O0O0O0O and (OO0000OO0OO00OO0O .quantifiers .get (O000000OOO0000000 )<=OO0OO0O0O00OO00OO )#line:956
            if (O000000OOO0000000 =='PostBase')|(O000000OOO0000000 =='Base2'):#line:957
                O000O00000O0O0O0O =O000O00000O0O0O0O and (OO0000OO0OO00OO0O .quantifiers .get (O000000OOO0000000 )<=O000000O00O0O000O )#line:958
            if (O000000OOO0000000 =='PreRelBase')|(O000000OOO0000000 =='RelBase1'):#line:959
                O000O00000O0O0O0O =O000O00000O0O0O0O and (OO0000OO0OO00OO0O .quantifiers .get (O000000OOO0000000 )<=OO0OO0O0O00OO00OO *1.0 /OO0000OO0OO00OO0O .data ["rows_count"])#line:960
            if (O000000OOO0000000 =='PostRelBase')|(O000000OOO0000000 =='RelBase2'):#line:961
                O000O00000O0O0O0O =O000O00000O0O0O0O and (OO0000OO0OO00OO0O .quantifiers .get (O000000OOO0000000 )<=O000000O00O0O000O *1.0 /OO0000OO0OO00OO0O .data ["rows_count"])#line:962
            if (O000000OOO0000000 =='Prepim')|(O000000OOO0000000 =='pim1')|(O000000OOO0000000 =='PreConf')|(O000000OOO0000000 =='conf1'):#line:963
                O000O00000O0O0O0O =O000O00000O0O0O0O and (OO0000OO0OO00OO0O .quantifiers .get (O000000OOO0000000 )<=O00O000O000O0O0OO )#line:964
            if (O000000OOO0000000 =='Postpim')|(O000000OOO0000000 =='pim2')|(O000000OOO0000000 =='PostConf')|(O000000OOO0000000 =='conf2'):#line:965
                O000O00000O0O0O0O =O000O00000O0O0O0O and (OO0000OO0OO00OO0O .quantifiers .get (O000000OOO0000000 )<=O00OO000OOO00OOO0 )#line:966
            if (O000000OOO0000000 =='Deltapim')|(O000000OOO0000000 =='DeltaConf'):#line:967
                O000O00000O0O0O0O =O000O00000O0O0O0O and (OO0000OO0OO00OO0O .quantifiers .get (O000000OOO0000000 )<=O00O000O000O0O0OO -O00OO000OOO00OOO0 )#line:968
            if (O000000OOO0000000 =='Ratiopim')|(O000000OOO0000000 =='RatioConf'):#line:971
                if (O00O000O000O0O0OO >0 ):#line:972
                    O000O00000O0O0O0O =O000O00000O0O0O0O and (OO0000OO0OO00OO0O .quantifiers .get (O000000OOO0000000 )<=O00OO000OOO00OOO0 *1.0 /O00O000O000O0O0OO )#line:973
                else :#line:974
                    O000O00000O0O0O0O =False #line:975
        O0O0O00O000OOO000 ={}#line:976
        if O000O00000O0O0O0O ==True :#line:977
            OO0000OO0OO00OO0O .stats ['total_valid']+=1 #line:979
            O0O0O00O000OOO000 ["base1"]=OO0OO0O0O00OO00OO #line:980
            O0O0O00O000OOO000 ["base2"]=O000000O00O0O000O #line:981
            O0O0O00O000OOO000 ["rel_base1"]=OO0OO0O0O00OO00OO *1.0 /OO0000OO0OO00OO0O .data ["rows_count"]#line:982
            O0O0O00O000OOO000 ["rel_base2"]=O000000O00O0O000O *1.0 /OO0000OO0OO00OO0O .data ["rows_count"]#line:983
            O0O0O00O000OOO000 ["conf1"]=O00O000O000O0O0OO #line:984
            O0O0O00O000OOO000 ["conf2"]=O00OO000OOO00OOO0 #line:985
            O0O0O00O000OOO000 ["deltaconf"]=O00O000O000O0O0OO -O00OO000OOO00OOO0 #line:986
            if (O00O000O000O0O0OO >0 ):#line:987
                O0O0O00O000OOO000 ["ratioconf"]=O00OO000OOO00OOO0 *1.0 /O00O000O000O0O0OO #line:988
            else :#line:989
                O0O0O00O000OOO000 ["ratioconf"]=None #line:990
            O0O0O00O000OOO000 ["fourfoldpre"]=[OOOO0O0OO0OO00000 ,O000O00000O0OOO0O ,O000OOO0OOOO00000 ,O00000O0OOOOOO0OO ]#line:991
            O0O0O00O000OOO000 ["fourfoldpost"]=[OOO0O0OO0OOO0OO00 ,OO0O0OO0OOOO00OO0 ,O000O00O0O0000OO0 ,OO000OOOOO0OO000O ]#line:992
        return O000O00000O0O0O0O ,O0O0O00O000OOO000 #line:994
    def _verify_opt (OOO0000OO0O000OO0 ,O0OO0OOOOOOOOO0O0 ,O0OOO000O0O00OO00 ):#line:996
        OOO0000OO0O000OO0 .stats ['total_ver']+=1 #line:997
        OOOO0O00O0O000O0O =False #line:998
        if not (O0OO0OOOOOOOOO0O0 ['optim'].get ('only_con')):#line:1001
            return False #line:1002
        if not (OOO0000OO0O000OO0 .options ['optimizations']):#line:1005
            return False #line:1007
        OO0O000OO00O0OOOO ={}#line:1009
        for O00OOO000O000OO0O in OOO0000OO0O000OO0 .task_actinfo ['cedents']:#line:1010
            OO0O000OO00O0OOOO [O00OOO000O000OO0O ['cedent_type']]=O00OOO000O000OO0O ['filter_value']#line:1012
        OOO0000O00000O0O0 =1 <<OOO0000OO0O000OO0 .data ["rows_count"]#line:1014
        OO0OOO0OOOOO0O0OO =OOO0000O00000O0O0 -1 #line:1015
        O0000OO00000O0O00 =""#line:1016
        OO000O0O000000OO0 =0 #line:1017
        if (OO0O000OO00O0OOOO .get ('ante')!=None ):#line:1018
            OO0OOO0OOOOO0O0OO =OO0OOO0OOOOO0O0OO &OO0O000OO00O0OOOO ['ante']#line:1019
        if (OO0O000OO00O0OOOO .get ('succ')!=None ):#line:1020
            OO0OOO0OOOOO0O0OO =OO0OOO0OOOOO0O0OO &OO0O000OO00O0OOOO ['succ']#line:1021
        if (OO0O000OO00O0OOOO .get ('cond')!=None ):#line:1022
            OO0OOO0OOOOO0O0OO =OO0OOO0OOOOO0O0OO &OO0O000OO00O0OOOO ['cond']#line:1023
        OO0OOO0OOOO0OOO0O =None #line:1026
        if (OOO0000OO0O000OO0 .proc =='CFMiner')|(OOO0000OO0O000OO0 .proc =='4ftMiner')|(OOO0000OO0O000OO0 .proc =='UICMiner'):#line:1051
            OOO000OOO0OO000O0 =OOO0000OO0O000OO0 ._bitcount (OO0OOO0OOOOO0O0OO )#line:1052
            if not (OOO0000OO0O000OO0 ._opt_base ==None ):#line:1053
                if not (OOO0000OO0O000OO0 ._opt_base <=OOO000OOO0OO000O0 ):#line:1054
                    OOOO0O00O0O000O0O =True #line:1055
            if not (OOO0000OO0O000OO0 ._opt_relbase ==None ):#line:1057
                if not (OOO0000OO0O000OO0 ._opt_relbase <=OOO000OOO0OO000O0 *1.0 /OOO0000OO0O000OO0 .data ["rows_count"]):#line:1058
                    OOOO0O00O0O000O0O =True #line:1059
        if (OOO0000OO0O000OO0 .proc =='SD4ftMiner'):#line:1061
            OOO000OOO0OO000O0 =OOO0000OO0O000OO0 ._bitcount (OO0OOO0OOOOO0O0OO )#line:1062
            if (not (OOO0000OO0O000OO0 ._opt_base1 ==None ))&(not (OOO0000OO0O000OO0 ._opt_base2 ==None )):#line:1063
                if not (max (OOO0000OO0O000OO0 ._opt_base1 ,OOO0000OO0O000OO0 ._opt_base2 )<=OOO000OOO0OO000O0 ):#line:1064
                    OOOO0O00O0O000O0O =True #line:1066
            if (not (OOO0000OO0O000OO0 ._opt_relbase1 ==None ))&(not (OOO0000OO0O000OO0 ._opt_relbase2 ==None )):#line:1067
                if not (max (OOO0000OO0O000OO0 ._opt_relbase1 ,OOO0000OO0O000OO0 ._opt_relbase2 )<=OOO000OOO0OO000O0 *1.0 /OOO0000OO0O000OO0 .data ["rows_count"]):#line:1068
                    OOOO0O00O0O000O0O =True #line:1069
        return OOOO0O00O0O000O0O #line:1071
        if OOO0000OO0O000OO0 .proc =='CFMiner':#line:1074
            if (O0OOO000O0O00OO00 ['cedent_type']=='cond')&(O0OOO000O0O00OO00 ['defi'].get ('type')=='con'):#line:1075
                OOO000OOO0OO000O0 =bin (OO0O000OO00O0OOOO ['cond']).count ("1")#line:1076
                O0O00O0000O0O00OO =True #line:1077
                for O000OOO0O0O0O0O0O in OOO0000OO0O000OO0 .quantifiers .keys ():#line:1078
                    if O000OOO0O0O0O0O0O =='Base':#line:1079
                        O0O00O0000O0O00OO =O0O00O0000O0O00OO and (OOO0000OO0O000OO0 .quantifiers .get (O000OOO0O0O0O0O0O )<=OOO000OOO0OO000O0 )#line:1080
                        if not (O0O00O0000O0O00OO ):#line:1081
                            print (f"...optimization : base is {OOO000OOO0OO000O0} for {O0OOO000O0O00OO00['generated_string']}")#line:1082
                    if O000OOO0O0O0O0O0O =='RelBase':#line:1083
                        O0O00O0000O0O00OO =O0O00O0000O0O00OO and (OOO0000OO0O000OO0 .quantifiers .get (O000OOO0O0O0O0O0O )<=OOO000OOO0OO000O0 *1.0 /OOO0000OO0O000OO0 .data ["rows_count"])#line:1084
                        if not (O0O00O0000O0O00OO ):#line:1085
                            print (f"...optimization : base is {OOO000OOO0OO000O0} for {O0OOO000O0O00OO00['generated_string']}")#line:1086
                OOOO0O00O0O000O0O =not (O0O00O0000O0O00OO )#line:1087
        elif OOO0000OO0O000OO0 .proc =='4ftMiner':#line:1088
            if (O0OOO000O0O00OO00 ['cedent_type']=='cond')&(O0OOO000O0O00OO00 ['defi'].get ('type')=='con'):#line:1089
                OOO000OOO0OO000O0 =bin (OO0O000OO00O0OOOO ['cond']).count ("1")#line:1090
                O0O00O0000O0O00OO =True #line:1091
                for O000OOO0O0O0O0O0O in OOO0000OO0O000OO0 .quantifiers .keys ():#line:1092
                    if O000OOO0O0O0O0O0O =='Base':#line:1093
                        O0O00O0000O0O00OO =O0O00O0000O0O00OO and (OOO0000OO0O000OO0 .quantifiers .get (O000OOO0O0O0O0O0O )<=OOO000OOO0OO000O0 )#line:1094
                        if not (O0O00O0000O0O00OO ):#line:1095
                            print (f"...optimization : base is {OOO000OOO0OO000O0} for {O0OOO000O0O00OO00['generated_string']}")#line:1096
                    if O000OOO0O0O0O0O0O =='RelBase':#line:1097
                        O0O00O0000O0O00OO =O0O00O0000O0O00OO and (OOO0000OO0O000OO0 .quantifiers .get (O000OOO0O0O0O0O0O )<=OOO000OOO0OO000O0 *1.0 /OOO0000OO0O000OO0 .data ["rows_count"])#line:1098
                        if not (O0O00O0000O0O00OO ):#line:1099
                            print (f"...optimization : base is {OOO000OOO0OO000O0} for {O0OOO000O0O00OO00['generated_string']}")#line:1100
                OOOO0O00O0O000O0O =not (O0O00O0000O0O00OO )#line:1101
            if (O0OOO000O0O00OO00 ['cedent_type']=='ante')&(O0OOO000O0O00OO00 ['defi'].get ('type')=='con'):#line:1102
                OOO000OOO0OO000O0 =bin (OO0O000OO00O0OOOO ['ante']&OO0O000OO00O0OOOO ['cond']).count ("1")#line:1103
                O0O00O0000O0O00OO =True #line:1104
                for O000OOO0O0O0O0O0O in OOO0000OO0O000OO0 .quantifiers .keys ():#line:1105
                    if O000OOO0O0O0O0O0O =='Base':#line:1106
                        O0O00O0000O0O00OO =O0O00O0000O0O00OO and (OOO0000OO0O000OO0 .quantifiers .get (O000OOO0O0O0O0O0O )<=OOO000OOO0OO000O0 )#line:1107
                        if not (O0O00O0000O0O00OO ):#line:1108
                            print (f"...optimization : ANTE: base is {OOO000OOO0OO000O0} for {O0OOO000O0O00OO00['generated_string']}")#line:1109
                    if O000OOO0O0O0O0O0O =='RelBase':#line:1110
                        O0O00O0000O0O00OO =O0O00O0000O0O00OO and (OOO0000OO0O000OO0 .quantifiers .get (O000OOO0O0O0O0O0O )<=OOO000OOO0OO000O0 *1.0 /OOO0000OO0O000OO0 .data ["rows_count"])#line:1111
                        if not (O0O00O0000O0O00OO ):#line:1112
                            print (f"...optimization : ANTE:  base is {OOO000OOO0OO000O0} for {O0OOO000O0O00OO00['generated_string']}")#line:1113
                OOOO0O00O0O000O0O =not (O0O00O0000O0O00OO )#line:1114
            if (O0OOO000O0O00OO00 ['cedent_type']=='succ')&(O0OOO000O0O00OO00 ['defi'].get ('type')=='con'):#line:1115
                OOO000OOO0OO000O0 =bin (OO0O000OO00O0OOOO ['ante']&OO0O000OO00O0OOOO ['cond']&OO0O000OO00O0OOOO ['succ']).count ("1")#line:1116
                OO0OOO0OOOO0OOO0O =0 #line:1117
                if OOO000OOO0OO000O0 >0 :#line:1118
                    OO0OOO0OOOO0OOO0O =bin (OO0O000OO00O0OOOO ['ante']&OO0O000OO00O0OOOO ['succ']&OO0O000OO00O0OOOO ['cond']).count ("1")*1.0 /bin (OO0O000OO00O0OOOO ['ante']&OO0O000OO00O0OOOO ['cond']).count ("1")#line:1119
                OOO0000O00000O0O0 =1 <<OOO0000OO0O000OO0 .data ["rows_count"]#line:1120
                O0OO00O0OO000O000 =bin (OO0O000OO00O0OOOO ['ante']&OO0O000OO00O0OOOO ['succ']&OO0O000OO00O0OOOO ['cond']).count ("1")#line:1121
                OO00O00OOOOOO0OO0 =bin (OO0O000OO00O0OOOO ['ante']&~(OOO0000O00000O0O0 |OO0O000OO00O0OOOO ['succ'])&OO0O000OO00O0OOOO ['cond']).count ("1")#line:1122
                O00OOO000O000OO0O =bin (~(OOO0000O00000O0O0 |OO0O000OO00O0OOOO ['ante'])&OO0O000OO00O0OOOO ['succ']&OO0O000OO00O0OOOO ['cond']).count ("1")#line:1123
                OO00OOOO0O0OO00O0 =bin (~(OOO0000O00000O0O0 |OO0O000OO00O0OOOO ['ante'])&~(OOO0000O00000O0O0 |OO0O000OO00O0OOOO ['succ'])&OO0O000OO00O0OOOO ['cond']).count ("1")#line:1124
                O0O00O0000O0O00OO =True #line:1125
                for O000OOO0O0O0O0O0O in OOO0000OO0O000OO0 .quantifiers .keys ():#line:1126
                    if O000OOO0O0O0O0O0O =='pim':#line:1127
                        O0O00O0000O0O00OO =O0O00O0000O0O00OO and (OOO0000OO0O000OO0 .quantifiers .get (O000OOO0O0O0O0O0O )<=OO0OOO0OOOO0OOO0O )#line:1128
                    if not (O0O00O0000O0O00OO ):#line:1129
                        print (f"...optimization : SUCC:  pim is {OO0OOO0OOOO0OOO0O} for {O0OOO000O0O00OO00['generated_string']}")#line:1130
                    if O000OOO0O0O0O0O0O =='aad':#line:1132
                        if (O0OO00O0OO000O000 +OO00O00OOOOOO0OO0 )*(O0OO00O0OO000O000 +O00OOO000O000OO0O )>0 :#line:1133
                            O0O00O0000O0O00OO =O0O00O0000O0O00OO and (OOO0000OO0O000OO0 .quantifiers .get (O000OOO0O0O0O0O0O )<=O0OO00O0OO000O000 *(O0OO00O0OO000O000 +OO00O00OOOOOO0OO0 +O00OOO000O000OO0O +OO00OOOO0O0OO00O0 )/(O0OO00O0OO000O000 +OO00O00OOOOOO0OO0 )/(O0OO00O0OO000O000 +O00OOO000O000OO0O )-1 )#line:1134
                        else :#line:1135
                            O0O00O0000O0O00OO =False #line:1136
                        if not (O0O00O0000O0O00OO ):#line:1137
                            O0OOO00O00OOO0OOO =O0OO00O0OO000O000 *(O0OO00O0OO000O000 +OO00O00OOOOOO0OO0 +O00OOO000O000OO0O +OO00OOOO0O0OO00O0 )/(O0OO00O0OO000O000 +OO00O00OOOOOO0OO0 )/(O0OO00O0OO000O000 +O00OOO000O000OO0O )-1 #line:1138
                            print (f"...optimization : SUCC:  aad is {O0OOO00O00OOO0OOO} for {O0OOO000O0O00OO00['generated_string']}")#line:1139
                    if O000OOO0O0O0O0O0O =='bad':#line:1140
                        if (O0OO00O0OO000O000 +OO00O00OOOOOO0OO0 )*(O0OO00O0OO000O000 +O00OOO000O000OO0O )>0 :#line:1141
                            O0O00O0000O0O00OO =O0O00O0000O0O00OO and (OOO0000OO0O000OO0 .quantifiers .get (O000OOO0O0O0O0O0O )<=1 -O0OO00O0OO000O000 *(O0OO00O0OO000O000 +OO00O00OOOOOO0OO0 +O00OOO000O000OO0O +OO00OOOO0O0OO00O0 )/(O0OO00O0OO000O000 +OO00O00OOOOOO0OO0 )/(O0OO00O0OO000O000 +O00OOO000O000OO0O ))#line:1142
                        else :#line:1143
                            O0O00O0000O0O00OO =False #line:1144
                        if not (O0O00O0000O0O00OO ):#line:1145
                            OO00000O00OO00O00 =1 -O0OO00O0OO000O000 *(O0OO00O0OO000O000 +OO00O00OOOOOO0OO0 +O00OOO000O000OO0O +OO00OOOO0O0OO00O0 )/(O0OO00O0OO000O000 +OO00O00OOOOOO0OO0 )/(O0OO00O0OO000O000 +O00OOO000O000OO0O )#line:1146
                            print (f"...optimization : SUCC:  bad is {OO00000O00OO00O00} for {O0OOO000O0O00OO00['generated_string']}")#line:1147
                OOOO0O00O0O000O0O =not (O0O00O0000O0O00OO )#line:1148
        if (OOOO0O00O0O000O0O ):#line:1149
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {O0OOO000O0O00OO00['cedent_type']}")#line:1150
        return OOOO0O00O0O000O0O #line:1151
    def _print (OO000OO0O0O0OO000 ,O0OO0OOOO0O0O00O0 ,_OO000O00O000OO00O ,_O0000O00OOOO0OOOO ):#line:1154
        if (len (_OO000O00O000OO00O ))!=len (_O0000O00OOOO0OOOO ):#line:1155
            print ("DIFF IN LEN for following cedent : "+str (len (_OO000O00O000OO00O ))+" vs "+str (len (_O0000O00OOOO0OOOO )))#line:1156
            print ("trace cedent : "+str (_OO000O00O000OO00O )+", traces "+str (_O0000O00OOOO0OOOO ))#line:1157
        OOO00O00O0OOO000O =''#line:1158
        OOOOO0OO0O00O0000 ={}#line:1159
        OO00O00000O00OOO0 =[]#line:1160
        for OOOO0O000OO0OO00O in range (len (_OO000O00O000OO00O )):#line:1161
            O0OOO0OOO0OOO000O =OO000OO0O0O0OO000 .data ["varname"].index (O0OO0OOOO0O0O00O0 ['defi'].get ('attributes')[_OO000O00O000OO00O [OOOO0O000OO0OO00O ]].get ('name'))#line:1162
            OOO00O00O0OOO000O =OOO00O00O0OOO000O +OO000OO0O0O0OO000 .data ["varname"][O0OOO0OOO0OOO000O ]+'('#line:1164
            OO00O00000O00OOO0 .append (O0OOO0OOO0OOO000O )#line:1165
            O00OOO000OOOO0OO0 =[]#line:1166
            for O0OO0OOO00O0O00O0 in _O0000O00OOOO0OOOO [OOOO0O000OO0OO00O ]:#line:1167
                OOO00O00O0OOO000O =OOO00O00O0OOO000O +str (OO000OO0O0O0OO000 .data ["catnames"][O0OOO0OOO0OOO000O ][O0OO0OOO00O0O00O0 ])+" "#line:1168
                O00OOO000OOOO0OO0 .append (str (OO000OO0O0O0OO000 .data ["catnames"][O0OOO0OOO0OOO000O ][O0OO0OOO00O0O00O0 ]))#line:1169
            OOO00O00O0OOO000O =OOO00O00O0OOO000O [:-1 ]+')'#line:1170
            OOOOO0OO0O00O0000 [OO000OO0O0O0OO000 .data ["varname"][O0OOO0OOO0OOO000O ]]=O00OOO000OOOO0OO0 #line:1171
            if OOOO0O000OO0OO00O +1 <len (_OO000O00O000OO00O ):#line:1172
                OOO00O00O0OOO000O =OOO00O00O0OOO000O +' & '#line:1173
        return OOO00O00O0OOO000O ,OOOOO0OO0O00O0000 ,OO00O00000O00OOO0 #line:1177
    def _print_hypo (O0OOO0OO0000000O0 ,OO0O0OOOO000O0O00 ):#line:1179
        O0OOO0OO0000000O0 .print_rule (OO0O0OOOO000O0O00 )#line:1180
    def _print_rule (OO0000O0O0O0O000O ,O000000O00O00000O ):#line:1182
        if OO0000O0O0O0O000O .verbosity ['print_rules']:#line:1183
            print ('Rules info : '+str (O000000O00O00000O ['params']))#line:1184
            for OOO00OO0OO0000O0O in OO0000O0O0O0O000O .task_actinfo ['cedents']:#line:1185
                print (OOO00OO0OO0000O0O ['cedent_type']+' = '+OOO00OO0OO0000O0O ['generated_string'])#line:1186
    def _genvar (OOO0OO000O00000O0 ,O0O00OO0O0000O000 ,OO0OOOOO000000OO0 ,_OOOO0000O0OOOOOOO ,_O00OOO0OOO0O0OOO0 ,_OOO00000O0000000O ,_O0OOO0OO00O0OOO00 ,_OOOOOOOO0O0OOO0O0 ,_OOO0O0OO00O0O0000 ,_OOOO0O0O00O0O00OO ):#line:1188
        _O00O0OO0O00000O0O =0 #line:1189
        if OO0OOOOO000000OO0 ['num_cedent']>0 :#line:1190
            _O00O0OO0O00000O0O =(_OOOO0O0O00O0O00OO -_OOO0O0OO00O0O0000 )/OO0OOOOO000000OO0 ['num_cedent']#line:1191
        for OOO0O0O0O00OOOO0O in range (OO0OOOOO000000OO0 ['num_cedent']):#line:1192
            if len (_OOOO0000O0OOOOOOO )==0 or OOO0O0O0O00OOOO0O >_OOOO0000O0OOOOOOO [-1 ]:#line:1193
                _OOOO0000O0OOOOOOO .append (OOO0O0O0O00OOOO0O )#line:1194
                OOO0O0OOOO00O0O00 =OOO0OO000O00000O0 .data ["varname"].index (OO0OOOOO000000OO0 ['defi'].get ('attributes')[OOO0O0O0O00OOOO0O ].get ('name'))#line:1195
                _O0O0OO00OO00O00OO =OO0OOOOO000000OO0 ['defi'].get ('attributes')[OOO0O0O0O00OOOO0O ].get ('minlen')#line:1196
                _O0O0O0O00O00O000O =OO0OOOOO000000OO0 ['defi'].get ('attributes')[OOO0O0O0O00OOOO0O ].get ('maxlen')#line:1197
                _O00OOO0O0O00000OO =OO0OOOOO000000OO0 ['defi'].get ('attributes')[OOO0O0O0O00OOOO0O ].get ('type')#line:1198
                OO000O00OOOOO000O =len (OOO0OO000O00000O0 .data ["dm"][OOO0O0OOOO00O0O00 ])#line:1199
                _OO00O00OOOOOO000O =[]#line:1200
                _O00OOO0OOO0O0OOO0 .append (_OO00O00OOOOOO000O )#line:1201
                _OOOOO00OOO0OO000O =int (0 )#line:1202
                OOO0OO000O00000O0 ._gencomb (O0O00OO0O0000O000 ,OO0OOOOO000000OO0 ,_OOOO0000O0OOOOOOO ,_O00OOO0OOO0O0OOO0 ,_OO00O00OOOOOO000O ,_OOO00000O0000000O ,_OOOOO00OOO0OO000O ,OO000O00OOOOO000O ,_O00OOO0O0O00000OO ,_O0OOO0OO00O0OOO00 ,_OOOOOOOO0O0OOO0O0 ,_O0O0OO00OO00O00OO ,_O0O0O0O00O00O000O ,_OOO0O0OO00O0O0000 +OOO0O0O0O00OOOO0O *_O00O0OO0O00000O0O ,_OOO0O0OO00O0O0000 +(OOO0O0O0O00OOOO0O +1 )*_O00O0OO0O00000O0O )#line:1203
                _O00OOO0OOO0O0OOO0 .pop ()#line:1204
                _OOOO0000O0OOOOOOO .pop ()#line:1205
    def _gencomb (O00OOOO0OO00OO0O0 ,OO0O0O00000O0O00O ,OOOO00O000O0OO0OO ,_OOO00000O0O0OOOOO ,_OO00O00O0O00O0O00 ,_OO0OO0OO00O0O0000 ,_OO0O00O0OOOO0OOO0 ,_OO0O00OO0000OOOO0 ,OOOOOOOOO0OO0O000 ,_OOO0O000OOO00000O ,_O0OOO0000O0OOOO00 ,_OOOO00OOOOO0O0OO0 ,_O0000OOO0O0O000O0 ,_O0O0000OO0O000O00 ,_OOO00OOO00OOO0O0O ,_O0OOO00O0OO00OOO0 ):#line:1207
        _OO0O0OOO00000000O =[]#line:1208
        if _OOO0O000OOO00000O =="subset":#line:1209
            if len (_OO0OO0OO00O0O0000 )==0 :#line:1210
                _OO0O0OOO00000000O =range (OOOOOOOOO0OO0O000 )#line:1211
            else :#line:1212
                _OO0O0OOO00000000O =range (_OO0OO0OO00O0O0000 [-1 ]+1 ,OOOOOOOOO0OO0O000 )#line:1213
        elif _OOO0O000OOO00000O =="seq":#line:1214
            if len (_OO0OO0OO00O0O0000 )==0 :#line:1215
                _OO0O0OOO00000000O =range (OOOOOOOOO0OO0O000 -_O0000OOO0O0O000O0 +1 )#line:1216
            else :#line:1217
                if _OO0OO0OO00O0O0000 [-1 ]+1 ==OOOOOOOOO0OO0O000 :#line:1218
                    return #line:1219
                O0000OOO000OOOO0O =_OO0OO0OO00O0O0000 [-1 ]+1 #line:1220
                _OO0O0OOO00000000O .append (O0000OOO000OOOO0O )#line:1221
        elif _OOO0O000OOO00000O =="lcut":#line:1222
            if len (_OO0OO0OO00O0O0000 )==0 :#line:1223
                O0000OOO000OOOO0O =0 ;#line:1224
            else :#line:1225
                if _OO0OO0OO00O0O0000 [-1 ]+1 ==OOOOOOOOO0OO0O000 :#line:1226
                    return #line:1227
                O0000OOO000OOOO0O =_OO0OO0OO00O0O0000 [-1 ]+1 #line:1228
            _OO0O0OOO00000000O .append (O0000OOO000OOOO0O )#line:1229
        elif _OOO0O000OOO00000O =="rcut":#line:1230
            if len (_OO0OO0OO00O0O0000 )==0 :#line:1231
                O0000OOO000OOOO0O =OOOOOOOOO0OO0O000 -1 ;#line:1232
            else :#line:1233
                if _OO0OO0OO00O0O0000 [-1 ]==0 :#line:1234
                    return #line:1235
                O0000OOO000OOOO0O =_OO0OO0OO00O0O0000 [-1 ]-1 #line:1236
            _OO0O0OOO00000000O .append (O0000OOO000OOOO0O )#line:1238
        elif _OOO0O000OOO00000O =="one":#line:1239
            if len (_OO0OO0OO00O0O0000 )==0 :#line:1240
                OOO0OOO0O000O000O =O00OOOO0OO00OO0O0 .data ["varname"].index (OOOO00O000O0OO0OO ['defi'].get ('attributes')[_OOO00000O0O0OOOOO [-1 ]].get ('name'))#line:1241
                try :#line:1242
                    O0000OOO000OOOO0O =O00OOOO0OO00OO0O0 .data ["catnames"][OOO0OOO0O000O000O ].index (OOOO00O000O0OO0OO ['defi'].get ('attributes')[_OOO00000O0O0OOOOO [-1 ]].get ('value'))#line:1243
                except :#line:1244
                    print (f"ERROR: attribute '{OOOO00O000O0OO0OO['defi'].get('attributes')[_OOO00000O0O0OOOOO[-1]].get('name')}' has not value '{OOOO00O000O0OO0OO['defi'].get('attributes')[_OOO00000O0O0OOOOO[-1]].get('value')}'")#line:1245
                    exit (1 )#line:1246
                _OO0O0OOO00000000O .append (O0000OOO000OOOO0O )#line:1247
                _O0000OOO0O0O000O0 =1 #line:1248
                _O0O0000OO0O000O00 =1 #line:1249
            else :#line:1250
                print ("DEBUG: one category should not have more categories")#line:1251
                return #line:1252
        else :#line:1253
            print ("Attribute type "+_OOO0O000OOO00000O +" not supported.")#line:1254
            return #line:1255
        if len (_OO0O0OOO00000000O )>0 :#line:1257
            _O0O0OO0OOO00OO0OO =(_O0OOO00O0OO00OOO0 -_OOO00OOO00OOO0O0O )/len (_OO0O0OOO00000000O )#line:1258
        else :#line:1259
            _O0O0OO0OOO00OO0OO =0 #line:1260
        _O00OOOO000O0OO0O0 =0 #line:1262
        for OOO00OO000OOOO0O0 in _OO0O0OOO00000000O :#line:1264
                _OO0OO0OO00O0O0000 .append (OOO00OO000OOOO0O0 )#line:1266
                _OO00O00O0O00O0O00 .pop ()#line:1267
                _OO00O00O0O00O0O00 .append (_OO0OO0OO00O0O0000 )#line:1268
                _OO00O000000OO0OOO =_OO0O00OO0000OOOO0 |O00OOOO0OO00OO0O0 .data ["dm"][O00OOOO0OO00OO0O0 .data ["varname"].index (OOOO00O000O0OO0OO ['defi'].get ('attributes')[_OOO00000O0O0OOOOO [-1 ]].get ('name'))][OOO00OO000OOOO0O0 ]#line:1272
                _O0O000OO0O00O00O0 =1 #line:1274
                if (len (_OOO00000O0O0OOOOO )<_O0OOO0000O0OOOO00 ):#line:1275
                    _O0O000OO0O00O00O0 =-1 #line:1276
                if (len (_OO00O00O0O00O0O00 [-1 ])<_O0000OOO0O0O000O0 ):#line:1278
                    _O0O000OO0O00O00O0 =0 #line:1279
                _O0OO000O000O00O0O =0 #line:1281
                if OOOO00O000O0OO0OO ['defi'].get ('type')=='con':#line:1282
                    _O0OO000O000O00O0O =_OO0O00O0OOOO0OOO0 &_OO00O000000OO0OOO #line:1283
                else :#line:1284
                    _O0OO000O000O00O0O =_OO0O00O0OOOO0OOO0 |_OO00O000000OO0OOO #line:1285
                OOOO00O000O0OO0OO ['trace_cedent']=_OOO00000O0O0OOOOO #line:1286
                OOOO00O000O0OO0OO ['traces']=_OO00O00O0O00O0O00 #line:1287
                O00OOO0OOO0O0000O ,O00000OOOOOOO0OOO ,OOOO000O0OOOO0OOO =O00OOOO0OO00OO0O0 ._print (OOOO00O000O0OO0OO ,_OOO00000O0O0OOOOO ,_OO00O00O0O00O0O00 )#line:1288
                OOOO00O000O0OO0OO ['generated_string']=O00OOO0OOO0O0000O #line:1289
                OOOO00O000O0OO0OO ['rule']=O00000OOOOOOO0OOO #line:1290
                OOOO00O000O0OO0OO ['filter_value']=_O0OO000O000O00O0O #line:1291
                OOOO00O000O0OO0OO ['traces']=copy .deepcopy (_OO00O00O0O00O0O00 )#line:1292
                OOOO00O000O0OO0OO ['trace_cedent']=copy .deepcopy (_OOO00000O0O0OOOOO )#line:1293
                OOOO00O000O0OO0OO ['trace_cedent_asindata']=copy .deepcopy (OOOO000O0OOOO0OOO )#line:1294
                OO0O0O00000O0O00O ['cedents'].append (OOOO00O000O0OO0OO )#line:1296
                O0O0O0OO0000OOOOO =O00OOOO0OO00OO0O0 ._verify_opt (OO0O0O00000O0O00O ,OOOO00O000O0OO0OO )#line:1297
                if not (O0O0O0OO0000OOOOO ):#line:1303
                    if _O0O000OO0O00O00O0 ==1 :#line:1304
                        if len (OO0O0O00000O0O00O ['cedents_to_do'])==len (OO0O0O00000O0O00O ['cedents']):#line:1306
                            if O00OOOO0OO00OO0O0 .proc =='CFMiner':#line:1307
                                O0OO000OOOOOOOO0O ,OOOOO0O0O000OO0O0 =O00OOOO0OO00OO0O0 ._verifyCF (_O0OO000O000O00O0O )#line:1308
                            elif O00OOOO0OO00OO0O0 .proc =='UICMiner':#line:1309
                                O0OO000OOOOOOOO0O ,OOOOO0O0O000OO0O0 =O00OOOO0OO00OO0O0 ._verifyUIC (_O0OO000O000O00O0O )#line:1310
                            elif O00OOOO0OO00OO0O0 .proc =='4ftMiner':#line:1311
                                O0OO000OOOOOOOO0O ,OOOOO0O0O000OO0O0 =O00OOOO0OO00OO0O0 ._verify4ft (_OO00O000000OO0OOO )#line:1312
                            elif O00OOOO0OO00OO0O0 .proc =='SD4ftMiner':#line:1313
                                O0OO000OOOOOOOO0O ,OOOOO0O0O000OO0O0 =O00OOOO0OO00OO0O0 ._verifysd4ft (_OO00O000000OO0OOO )#line:1314
                            elif O00OOOO0OO00OO0O0 .proc =='NewAct4ftMiner':#line:1315
                                O0OO000OOOOOOOO0O ,OOOOO0O0O000OO0O0 =O00OOOO0OO00OO0O0 ._verifynewact4ft (_OO00O000000OO0OOO )#line:1316
                            elif O00OOOO0OO00OO0O0 .proc =='Act4ftMiner':#line:1317
                                O0OO000OOOOOOOO0O ,OOOOO0O0O000OO0O0 =O00OOOO0OO00OO0O0 ._verifyact4ft (_OO00O000000OO0OOO )#line:1318
                            else :#line:1319
                                print ("Unsupported procedure : "+O00OOOO0OO00OO0O0 .proc )#line:1320
                                exit (0 )#line:1321
                            if O0OO000OOOOOOOO0O ==True :#line:1322
                                OO00O0O000000OO0O ={}#line:1323
                                OO00O0O000000OO0O ["rule_id"]=O00OOOO0OO00OO0O0 .stats ['total_valid']#line:1324
                                OO00O0O000000OO0O ["cedents_str"]={}#line:1325
                                OO00O0O000000OO0O ["cedents_struct"]={}#line:1326
                                OO00O0O000000OO0O ['traces']={}#line:1327
                                OO00O0O000000OO0O ['trace_cedent_taskorder']={}#line:1328
                                OO00O0O000000OO0O ['trace_cedent_dataorder']={}#line:1329
                                for O0O0O00OO00O0O00O in OO0O0O00000O0O00O ['cedents']:#line:1330
                                    OO00O0O000000OO0O ['cedents_str'][O0O0O00OO00O0O00O ['cedent_type']]=O0O0O00OO00O0O00O ['generated_string']#line:1332
                                    OO00O0O000000OO0O ['cedents_struct'][O0O0O00OO00O0O00O ['cedent_type']]=O0O0O00OO00O0O00O ['rule']#line:1333
                                    OO00O0O000000OO0O ['traces'][O0O0O00OO00O0O00O ['cedent_type']]=O0O0O00OO00O0O00O ['traces']#line:1334
                                    OO00O0O000000OO0O ['trace_cedent_taskorder'][O0O0O00OO00O0O00O ['cedent_type']]=O0O0O00OO00O0O00O ['trace_cedent']#line:1335
                                    OO00O0O000000OO0O ['trace_cedent_dataorder'][O0O0O00OO00O0O00O ['cedent_type']]=O0O0O00OO00O0O00O ['trace_cedent_asindata']#line:1336
                                OO00O0O000000OO0O ["params"]=OOOOO0O0O000OO0O0 #line:1338
                                O00OOOO0OO00OO0O0 ._print_rule (OO00O0O000000OO0O )#line:1340
                                O00OOOO0OO00OO0O0 .rulelist .append (OO00O0O000000OO0O )#line:1346
                            O00OOOO0OO00OO0O0 .stats ['total_cnt']+=1 #line:1348
                            O00OOOO0OO00OO0O0 .stats ['total_ver']+=1 #line:1349
                    if _O0O000OO0O00O00O0 >=0 :#line:1350
                        if len (OO0O0O00000O0O00O ['cedents_to_do'])>len (OO0O0O00000O0O00O ['cedents']):#line:1351
                            O00OOOO0OO00OO0O0 ._start_cedent (OO0O0O00000O0O00O ,_OOO00OOO00OOO0O0O +_O00OOOO000O0OO0O0 *_O0O0OO0OOO00OO0OO ,_OOO00OOO00OOO0O0O +(_O00OOOO000O0OO0O0 +0.33 )*_O0O0OO0OOO00OO0OO )#line:1352
                    OO0O0O00000O0O00O ['cedents'].pop ()#line:1353
                    if (len (_OOO00000O0O0OOOOO )<_OOOO00OOOOO0O0OO0 ):#line:1354
                        O00OOOO0OO00OO0O0 ._genvar (OO0O0O00000O0O00O ,OOOO00O000O0OO0OO ,_OOO00000O0O0OOOOO ,_OO00O00O0O00O0O00 ,_O0OO000O000O00O0O ,_O0OOO0000O0OOOO00 ,_OOOO00OOOOO0O0OO0 ,_OOO00OOO00OOO0O0O +(_O00OOOO000O0OO0O0 +0.33 )*_O0O0OO0OOO00OO0OO ,_OOO00OOO00OOO0O0O +(_O00OOOO000O0OO0O0 +0.66 )*_O0O0OO0OOO00OO0OO )#line:1355
                else :#line:1356
                    OO0O0O00000O0O00O ['cedents'].pop ()#line:1357
                if len (_OO0OO0OO00O0O0000 )<_O0O0000OO0O000O00 :#line:1358
                    O00OOOO0OO00OO0O0 ._gencomb (OO0O0O00000O0O00O ,OOOO00O000O0OO0OO ,_OOO00000O0O0OOOOO ,_OO00O00O0O00O0O00 ,_OO0OO0OO00O0O0000 ,_OO0O00O0OOOO0OOO0 ,_OO00O000000OO0OOO ,OOOOOOOOO0OO0O000 ,_OOO0O000OOO00000O ,_O0OOO0000O0OOOO00 ,_OOOO00OOOOO0O0OO0 ,_O0000OOO0O0O000O0 ,_O0O0000OO0O000O00 ,_OOO00OOO00OOO0O0O +_O0O0OO0OOO00OO0OO *(_O00OOOO000O0OO0O0 +0.66 ),_OOO00OOO00OOO0O0O +_O0O0OO0OOO00OO0OO *(_O00OOOO000O0OO0O0 +1 ))#line:1359
                _OO0OO0OO00O0O0000 .pop ()#line:1360
                _O00OOOO000O0OO0O0 +=1 #line:1361
                if O00OOOO0OO00OO0O0 .options ['progressbar']:#line:1362
                    O00OOOO0OO00OO0O0 .bar .update (min (100 ,_OOO00OOO00OOO0O0O +_O0O0OO0OOO00OO0OO *_O00OOOO000O0OO0O0 ))#line:1363
    def _start_cedent (OO0O0OO00OOOO00O0 ,O0O0O0O0OOOO0O000 ,_O0OOO0O00O00000OO ,_OOOO0OOO000O000OO ):#line:1366
        if len (O0O0O0O0OOOO0O000 ['cedents_to_do'])>len (O0O0O0O0OOOO0O000 ['cedents']):#line:1367
            _OO0OOO0O00O0OO000 =[]#line:1368
            _O0O0O00O00O0O0OO0 =[]#line:1369
            O0OOO000OO00OO0OO ={}#line:1370
            O0OOO000OO00OO0OO ['cedent_type']=O0O0O0O0OOOO0O000 ['cedents_to_do'][len (O0O0O0O0OOOO0O000 ['cedents'])]#line:1371
            O0O000O0OOO00OOO0 =O0OOO000OO00OO0OO ['cedent_type']#line:1372
            if ((O0O000O0OOO00OOO0 [-1 ]=='-')|(O0O000O0OOO00OOO0 [-1 ]=='+')):#line:1373
                O0O000O0OOO00OOO0 =O0O000O0OOO00OOO0 [:-1 ]#line:1374
            O0OOO000OO00OO0OO ['defi']=OO0O0OO00OOOO00O0 .kwargs .get (O0O000O0OOO00OOO0 )#line:1376
            if (O0OOO000OO00OO0OO ['defi']==None ):#line:1377
                print ("Error getting cedent ",O0OOO000OO00OO0OO ['cedent_type'])#line:1378
            _OOOO0000000OOO000 =int (0 )#line:1379
            O0OOO000OO00OO0OO ['num_cedent']=len (O0OOO000OO00OO0OO ['defi'].get ('attributes'))#line:1386
            if (O0OOO000OO00OO0OO ['defi'].get ('type')=='con'):#line:1387
                _OOOO0000000OOO000 =(1 <<OO0O0OO00OOOO00O0 .data ["rows_count"])-1 #line:1388
            OO0O0OO00OOOO00O0 ._genvar (O0O0O0O0OOOO0O000 ,O0OOO000OO00OO0OO ,_OO0OOO0O00O0OO000 ,_O0O0O00O00O0O0OO0 ,_OOOO0000000OOO000 ,O0OOO000OO00OO0OO ['defi'].get ('minlen'),O0OOO000OO00OO0OO ['defi'].get ('maxlen'),_O0OOO0O00O00000OO ,_OOOO0OOO000O000OO )#line:1389
    def _calc_all (O0000O00000O0OOOO ,**O00OO00OO00OO000O ):#line:1392
        if "df"in O00OO00OO00OO000O :#line:1393
            O0000O00000O0OOOO ._prep_data (O0000O00000O0OOOO .kwargs .get ("df"))#line:1394
        if not (O0000O00000O0OOOO ._initialized ):#line:1395
            print ("ERROR: dataframe is missing and not initialized with dataframe")#line:1396
        else :#line:1397
            O0000O00000O0OOOO ._calculate (**O00OO00OO00OO000O )#line:1398
    def _check_cedents (O0000OO00O000OOOO ,OO0O0O0O000O0OOOO ,**O00000000OO0000O0 ):#line:1400
        OOOO0OO00OO00O000 =True #line:1401
        if (O00000000OO0000O0 .get ('quantifiers',None )==None ):#line:1402
            print (f"Error: missing quantifiers.")#line:1403
            OOOO0OO00OO00O000 =False #line:1404
            return OOOO0OO00OO00O000 #line:1405
        if (type (O00000000OO0000O0 .get ('quantifiers'))!=dict ):#line:1406
            print (f"Error: quantifiers are not dictionary type.")#line:1407
            OOOO0OO00OO00O000 =False #line:1408
            return OOOO0OO00OO00O000 #line:1409
        for OOOO0OOOOO00OOO0O in OO0O0O0O000O0OOOO :#line:1411
            if (O00000000OO0000O0 .get (OOOO0OOOOO00OOO0O ,None )==None ):#line:1412
                print (f"Error: cedent {OOOO0OOOOO00OOO0O} is missing in parameters.")#line:1413
                OOOO0OO00OO00O000 =False #line:1414
                return OOOO0OO00OO00O000 #line:1415
            O0000OOOO0O00OO00 =O00000000OO0000O0 .get (OOOO0OOOOO00OOO0O )#line:1416
            if (O0000OOOO0O00OO00 .get ('minlen'),None )==None :#line:1417
                print (f"Error: cedent {OOOO0OOOOO00OOO0O} has no minimal length specified.")#line:1418
                OOOO0OO00OO00O000 =False #line:1419
                return OOOO0OO00OO00O000 #line:1420
            if not (type (O0000OOOO0O00OO00 .get ('minlen'))is int ):#line:1421
                print (f"Error: cedent {OOOO0OOOOO00OOO0O} has invalid type of minimal length ({type(O0000OOOO0O00OO00.get('minlen'))}).")#line:1422
                OOOO0OO00OO00O000 =False #line:1423
                return OOOO0OO00OO00O000 #line:1424
            if (O0000OOOO0O00OO00 .get ('maxlen'),None )==None :#line:1425
                print (f"Error: cedent {OOOO0OOOOO00OOO0O} has no maximal length specified.")#line:1426
                OOOO0OO00OO00O000 =False #line:1427
                return OOOO0OO00OO00O000 #line:1428
            if not (type (O0000OOOO0O00OO00 .get ('maxlen'))is int ):#line:1429
                print (f"Error: cedent {OOOO0OOOOO00OOO0O} has invalid type of maximal length.")#line:1430
                OOOO0OO00OO00O000 =False #line:1431
                return OOOO0OO00OO00O000 #line:1432
            if (O0000OOOO0O00OO00 .get ('type'),None )==None :#line:1433
                print (f"Error: cedent {OOOO0OOOOO00OOO0O} has no type specified.")#line:1434
                OOOO0OO00OO00O000 =False #line:1435
                return OOOO0OO00OO00O000 #line:1436
            if not ((O0000OOOO0O00OO00 .get ('type'))in (['con','dis'])):#line:1437
                print (f"Error: cedent {OOOO0OOOOO00OOO0O} has invalid type. Allowed values are 'con' and 'dis'.")#line:1438
                OOOO0OO00OO00O000 =False #line:1439
                return OOOO0OO00OO00O000 #line:1440
            if (O0000OOOO0O00OO00 .get ('attributes'),None )==None :#line:1441
                print (f"Error: cedent {OOOO0OOOOO00OOO0O} has no attributes specified.")#line:1442
                OOOO0OO00OO00O000 =False #line:1443
                return OOOO0OO00OO00O000 #line:1444
            for OOOOOO00O0OOO00O0 in O0000OOOO0O00OO00 .get ('attributes'):#line:1445
                if (OOOOOO00O0OOO00O0 .get ('name'),None )==None :#line:1446
                    print (f"Error: cedent {OOOO0OOOOO00OOO0O} / attribute {OOOOOO00O0OOO00O0} has no 'name' attribute specified.")#line:1447
                    OOOO0OO00OO00O000 =False #line:1448
                    return OOOO0OO00OO00O000 #line:1449
                if not ((OOOOOO00O0OOO00O0 .get ('name'))in O0000OO00O000OOOO .data ["varname"]):#line:1450
                    print (f"Error: cedent {OOOO0OOOOO00OOO0O} / attribute {OOOOOO00O0OOO00O0.get('name')} not in variable list. Please check spelling.")#line:1451
                    OOOO0OO00OO00O000 =False #line:1452
                    return OOOO0OO00OO00O000 #line:1453
                if (OOOOOO00O0OOO00O0 .get ('type'),None )==None :#line:1454
                    print (f"Error: cedent {OOOO0OOOOO00OOO0O} / attribute {OOOOOO00O0OOO00O0.get('name')} has no 'type' attribute specified.")#line:1455
                    OOOO0OO00OO00O000 =False #line:1456
                    return OOOO0OO00OO00O000 #line:1457
                if not ((OOOOOO00O0OOO00O0 .get ('type'))in (['rcut','lcut','seq','subset','one'])):#line:1458
                    print (f"Error: cedent {OOOO0OOOOO00OOO0O} / attribute {OOOOOO00O0OOO00O0.get('name')} has unsupported type {OOOOOO00O0OOO00O0.get('type')}. Supported types are 'subset','seq','lcut','rcut','one'.")#line:1459
                    OOOO0OO00OO00O000 =False #line:1460
                    return OOOO0OO00OO00O000 #line:1461
                if (OOOOOO00O0OOO00O0 .get ('minlen'),None )==None :#line:1462
                    print (f"Error: cedent {OOOO0OOOOO00OOO0O} / attribute {OOOOOO00O0OOO00O0.get('name')} has no minimal length specified.")#line:1463
                    OOOO0OO00OO00O000 =False #line:1464
                    return OOOO0OO00OO00O000 #line:1465
                if not (type (OOOOOO00O0OOO00O0 .get ('minlen'))is int ):#line:1466
                    if not (OOOOOO00O0OOO00O0 .get ('type')=='one'):#line:1467
                        print (f"Error: cedent {OOOO0OOOOO00OOO0O} / attribute {OOOOOO00O0OOO00O0.get('name')} has invalid type of minimal length.")#line:1468
                        OOOO0OO00OO00O000 =False #line:1469
                        return OOOO0OO00OO00O000 #line:1470
                if (OOOOOO00O0OOO00O0 .get ('maxlen'),None )==None :#line:1471
                    print (f"Error: cedent {OOOO0OOOOO00OOO0O} / attribute {OOOOOO00O0OOO00O0.get('name')} has no maximal length specified.")#line:1472
                    OOOO0OO00OO00O000 =False #line:1473
                    return OOOO0OO00OO00O000 #line:1474
                if not (type (OOOOOO00O0OOO00O0 .get ('maxlen'))is int ):#line:1475
                    if not (OOOOOO00O0OOO00O0 .get ('type')=='one'):#line:1476
                        print (f"Error: cedent {OOOO0OOOOO00OOO0O} / attribute {OOOOOO00O0OOO00O0.get('name')} has invalid type of maximal length.")#line:1477
                        OOOO0OO00OO00O000 =False #line:1478
                        return OOOO0OO00OO00O000 #line:1479
        return OOOO0OO00OO00O000 #line:1480
    def _calculate (O000O0000OOOOO000 ,**O000OO000OO0OO0OO ):#line:1482
        if O000O0000OOOOO000 .data ["data_prepared"]==0 :#line:1483
            print ("Error: data not prepared")#line:1484
            return #line:1485
        O000O0000OOOOO000 .kwargs =O000OO000OO0OO0OO #line:1486
        O000O0000OOOOO000 .proc =O000OO000OO0OO0OO .get ('proc')#line:1487
        O000O0000OOOOO000 .quantifiers =O000OO000OO0OO0OO .get ('quantifiers')#line:1488
        O000O0000OOOOO000 ._init_task ()#line:1490
        O000O0000OOOOO000 .stats ['start_proc_time']=time .time ()#line:1491
        O000O0000OOOOO000 .task_actinfo ['cedents_to_do']=[]#line:1492
        O000O0000OOOOO000 .task_actinfo ['cedents']=[]#line:1493
        if O000OO000OO0OO0OO .get ("proc")=='UICMiner':#line:1496
            if not (O000O0000OOOOO000 ._check_cedents (['ante'],**O000OO000OO0OO0OO )):#line:1497
                return #line:1498
            _O00OOOOO00OO000O0 =O000OO000OO0OO0OO .get ("cond")#line:1500
            if _O00OOOOO00OO000O0 !=None :#line:1501
                O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1502
            else :#line:1503
                OO00O00OOO0OOO000 =O000O0000OOOOO000 .cedent #line:1504
                OO00O00OOO0OOO000 ['cedent_type']='cond'#line:1505
                OO00O00OOO0OOO000 ['filter_value']=(1 <<O000O0000OOOOO000 .data ["rows_count"])-1 #line:1506
                OO00O00OOO0OOO000 ['generated_string']='---'#line:1507
                O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1509
                O000O0000OOOOO000 .task_actinfo ['cedents'].append (OO00O00OOO0OOO000 )#line:1510
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1511
            if O000OO000OO0OO0OO .get ('target',None )==None :#line:1512
                print ("ERROR: no succedent/target variable defined for UIC Miner")#line:1513
                return #line:1514
            if not (O000OO000OO0OO0OO .get ('target')in O000O0000OOOOO000 .data ["varname"]):#line:1515
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1516
                return #line:1517
            if ("aad_score"in O000O0000OOOOO000 .quantifiers ):#line:1518
                if not ("aad_weights"in O000O0000OOOOO000 .quantifiers ):#line:1519
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1520
                    return #line:1521
                if not (len (O000O0000OOOOO000 .quantifiers .get ("aad_weights"))==len (O000O0000OOOOO000 .data ["dm"][O000O0000OOOOO000 .data ["varname"].index (O000O0000OOOOO000 .kwargs .get ('target'))])):#line:1522
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1523
                    return #line:1524
        elif O000OO000OO0OO0OO .get ("proc")=='CFMiner':#line:1525
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do']=['cond']#line:1526
            if O000OO000OO0OO0OO .get ('target',None )==None :#line:1527
                print ("ERROR: no target variable defined for CF Miner")#line:1528
                return #line:1529
            if not (O000O0000OOOOO000 ._check_cedents (['cond'],**O000OO000OO0OO0OO )):#line:1530
                return #line:1531
            if not (O000OO000OO0OO0OO .get ('target')in O000O0000OOOOO000 .data ["varname"]):#line:1532
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1533
                return #line:1534
            if ("aad"in O000O0000OOOOO000 .quantifiers ):#line:1535
                if not ("aad_weights"in O000O0000OOOOO000 .quantifiers ):#line:1536
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1537
                    return #line:1538
                if not (len (O000O0000OOOOO000 .quantifiers .get ("aad_weights"))==len (O000O0000OOOOO000 .data ["dm"][O000O0000OOOOO000 .data ["varname"].index (O000O0000OOOOO000 .kwargs .get ('target'))])):#line:1539
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1540
                    return #line:1541
        elif O000OO000OO0OO0OO .get ("proc")=='4ftMiner':#line:1544
            if not (O000O0000OOOOO000 ._check_cedents (['ante','succ'],**O000OO000OO0OO0OO )):#line:1545
                return #line:1546
            _O00OOOOO00OO000O0 =O000OO000OO0OO0OO .get ("cond")#line:1548
            if _O00OOOOO00OO000O0 !=None :#line:1549
                O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1550
            else :#line:1551
                OO00O00OOO0OOO000 =O000O0000OOOOO000 .cedent #line:1552
                OO00O00OOO0OOO000 ['cedent_type']='cond'#line:1553
                OO00O00OOO0OOO000 ['filter_value']=(1 <<O000O0000OOOOO000 .data ["rows_count"])-1 #line:1554
                OO00O00OOO0OOO000 ['generated_string']='---'#line:1555
                O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1557
                O000O0000OOOOO000 .task_actinfo ['cedents'].append (OO00O00OOO0OOO000 )#line:1558
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1562
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1563
        elif O000OO000OO0OO0OO .get ("proc")=='NewAct4ftMiner':#line:1564
            _O00OOOOO00OO000O0 =O000OO000OO0OO0OO .get ("cond")#line:1567
            if _O00OOOOO00OO000O0 !=None :#line:1568
                O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1569
            else :#line:1570
                OO00O00OOO0OOO000 =O000O0000OOOOO000 .cedent #line:1571
                OO00O00OOO0OOO000 ['cedent_type']='cond'#line:1572
                OO00O00OOO0OOO000 ['filter_value']=(1 <<O000O0000OOOOO000 .data ["rows_count"])-1 #line:1573
                OO00O00OOO0OOO000 ['generated_string']='---'#line:1574
                print (OO00O00OOO0OOO000 ['filter_value'])#line:1575
                O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1576
                O000O0000OOOOO000 .task_actinfo ['cedents'].append (OO00O00OOO0OOO000 )#line:1577
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('antv')#line:1578
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('sucv')#line:1579
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1580
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1581
        elif O000OO000OO0OO0OO .get ("proc")=='Act4ftMiner':#line:1582
            _O00OOOOO00OO000O0 =O000OO000OO0OO0OO .get ("cond")#line:1585
            if _O00OOOOO00OO000O0 !=None :#line:1586
                O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1587
            else :#line:1588
                OO00O00OOO0OOO000 =O000O0000OOOOO000 .cedent #line:1589
                OO00O00OOO0OOO000 ['cedent_type']='cond'#line:1590
                OO00O00OOO0OOO000 ['filter_value']=(1 <<O000O0000OOOOO000 .data ["rows_count"])-1 #line:1591
                OO00O00OOO0OOO000 ['generated_string']='---'#line:1592
                print (OO00O00OOO0OOO000 ['filter_value'])#line:1593
                O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1594
                O000O0000OOOOO000 .task_actinfo ['cedents'].append (OO00O00OOO0OOO000 )#line:1595
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('antv-')#line:1596
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('antv+')#line:1597
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('sucv-')#line:1598
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('sucv+')#line:1599
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1600
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1601
        elif O000OO000OO0OO0OO .get ("proc")=='SD4ftMiner':#line:1602
            if not (O000O0000OOOOO000 ._check_cedents (['ante','succ','frst','scnd'],**O000OO000OO0OO0OO )):#line:1605
                return #line:1606
            _O00OOOOO00OO000O0 =O000OO000OO0OO0OO .get ("cond")#line:1607
            if _O00OOOOO00OO000O0 !=None :#line:1608
                O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1609
            else :#line:1610
                OO00O00OOO0OOO000 =O000O0000OOOOO000 .cedent #line:1611
                OO00O00OOO0OOO000 ['cedent_type']='cond'#line:1612
                OO00O00OOO0OOO000 ['filter_value']=(1 <<O000O0000OOOOO000 .data ["rows_count"])-1 #line:1613
                OO00O00OOO0OOO000 ['generated_string']='---'#line:1614
                O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1616
                O000O0000OOOOO000 .task_actinfo ['cedents'].append (OO00O00OOO0OOO000 )#line:1617
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('frst')#line:1618
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('scnd')#line:1619
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1620
            O000O0000OOOOO000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1621
        else :#line:1622
            print ("Unsupported procedure")#line:1623
            return #line:1624
        print ("Will go for ",O000OO000OO0OO0OO .get ("proc"))#line:1625
        O000O0000OOOOO000 .task_actinfo ['optim']={}#line:1628
        OOOO0O00O0OOOOOOO =True #line:1629
        for OO00O00000O000OO0 in O000O0000OOOOO000 .task_actinfo ['cedents_to_do']:#line:1630
            try :#line:1631
                OOOO0O000O0OOO0O0 =O000O0000OOOOO000 .kwargs .get (OO00O00000O000OO0 )#line:1632
                if OOOO0O000O0OOO0O0 .get ('type')!='con':#line:1636
                    OOOO0O00O0OOOOOOO =False #line:1637
            except :#line:1639
                OO0O0O00OO00OO000 =1 <2 #line:1640
        if O000O0000OOOOO000 .options ['optimizations']==False :#line:1642
            OOOO0O00O0OOOOOOO =False #line:1643
        O0OOOO0O00OOO0000 ={}#line:1644
        O0OOOO0O00OOO0000 ['only_con']=OOOO0O00O0OOOOOOO #line:1645
        O000O0000OOOOO000 .task_actinfo ['optim']=O0OOOO0O00OOO0000 #line:1646
        print ("Starting to mine rules.")#line:1654
        sys .stdout .flush ()#line:1655
        time .sleep (0.01 )#line:1656
        if O000O0000OOOOO000 .options ['progressbar']:#line:1657
            O0OOO0O0O00O00O0O =[progressbar .Percentage (),progressbar .Bar (),progressbar .Timer ()]#line:1658
            O000O0000OOOOO000 .bar =progressbar .ProgressBar (widgets =O0OOO0O0O00O00O0O ,max_value =100 ,fd =sys .stdout ).start ()#line:1659
            O000O0000OOOOO000 .bar .update (0 )#line:1660
        O000O0000OOOOO000 .progress_lower =0 #line:1661
        O000O0000OOOOO000 .progress_upper =100 #line:1662
        O000O0000OOOOO000 ._start_cedent (O000O0000OOOOO000 .task_actinfo ,O000O0000OOOOO000 .progress_lower ,O000O0000OOOOO000 .progress_upper )#line:1663
        if O000O0000OOOOO000 .options ['progressbar']:#line:1664
            O000O0000OOOOO000 .bar .update (100 )#line:1665
            O000O0000OOOOO000 .bar .finish ()#line:1666
        O000O0000OOOOO000 .stats ['end_proc_time']=time .time ()#line:1668
        print ("Done. Total verifications : "+str (O000O0000OOOOO000 .stats ['total_cnt'])+", rules "+str (O000O0000OOOOO000 .stats ['total_valid'])+", times: prep "+"{:.2f}".format (O000O0000OOOOO000 .stats ['end_prep_time']-O000O0000OOOOO000 .stats ['start_prep_time'])+"sec, processing "+"{:.2f}".format (O000O0000OOOOO000 .stats ['end_proc_time']-O000O0000OOOOO000 .stats ['start_proc_time'])+"sec")#line:1672
        O0O00OOO000O0O0OO ={}#line:1673
        O00OO00OOO0O0O000 ={}#line:1674
        O00OO00OOO0O0O000 ["task_type"]=O000OO000OO0OO0OO .get ('proc')#line:1675
        O00OO00OOO0O0O000 ["target"]=O000OO000OO0OO0OO .get ('target')#line:1677
        O00OO00OOO0O0O000 ["self.quantifiers"]=O000O0000OOOOO000 .quantifiers #line:1678
        if O000OO000OO0OO0OO .get ('cond')!=None :#line:1680
            O00OO00OOO0O0O000 ['cond']=O000OO000OO0OO0OO .get ('cond')#line:1681
        if O000OO000OO0OO0OO .get ('ante')!=None :#line:1682
            O00OO00OOO0O0O000 ['ante']=O000OO000OO0OO0OO .get ('ante')#line:1683
        if O000OO000OO0OO0OO .get ('succ')!=None :#line:1684
            O00OO00OOO0O0O000 ['succ']=O000OO000OO0OO0OO .get ('succ')#line:1685
        if O000OO000OO0OO0OO .get ('opts')!=None :#line:1686
            O00OO00OOO0O0O000 ['opts']=O000OO000OO0OO0OO .get ('opts')#line:1687
        O0O00OOO000O0O0OO ["taskinfo"]=O00OO00OOO0O0O000 #line:1688
        O0OOOO0O00000O0O0 ={}#line:1689
        O0OOOO0O00000O0O0 ["total_verifications"]=O000O0000OOOOO000 .stats ['total_cnt']#line:1690
        O0OOOO0O00000O0O0 ["valid_rules"]=O000O0000OOOOO000 .stats ['total_valid']#line:1691
        O0OOOO0O00000O0O0 ["total_verifications_with_opt"]=O000O0000OOOOO000 .stats ['total_ver']#line:1692
        O0OOOO0O00000O0O0 ["time_prep"]=O000O0000OOOOO000 .stats ['end_prep_time']-O000O0000OOOOO000 .stats ['start_prep_time']#line:1693
        O0OOOO0O00000O0O0 ["time_processing"]=O000O0000OOOOO000 .stats ['end_proc_time']-O000O0000OOOOO000 .stats ['start_proc_time']#line:1694
        O0OOOO0O00000O0O0 ["time_total"]=O000O0000OOOOO000 .stats ['end_prep_time']-O000O0000OOOOO000 .stats ['start_prep_time']+O000O0000OOOOO000 .stats ['end_proc_time']-O000O0000OOOOO000 .stats ['start_proc_time']#line:1695
        O0O00OOO000O0O0OO ["summary_statistics"]=O0OOOO0O00000O0O0 #line:1696
        O0O00OOO000O0O0OO ["rules"]=O000O0000OOOOO000 .rulelist #line:1697
        O0O0O0000O00OO0OO ={}#line:1698
        O0O0O0000O00OO0OO ["varname"]=O000O0000OOOOO000 .data ["varname"]#line:1699
        O0O0O0000O00OO0OO ["catnames"]=O000O0000OOOOO000 .data ["catnames"]#line:1700
        O0O00OOO000O0O0OO ["datalabels"]=O0O0O0000O00OO0OO #line:1701
        O000O0000OOOOO000 .result =O0O00OOO000O0O0OO #line:1702
    def print_summary (OO0000OO0OOOO00OO ):#line:1704
        ""#line:1707
        if not (OO0000OO0OOOO00OO ._is_calculated ()):#line:1708
            print ("ERROR: Task has not been calculated.")#line:1709
            return #line:1710
        print ("")#line:1711
        print ("CleverMiner task processing summary:")#line:1712
        print ("")#line:1713
        print (f"Task type : {OO0000OO0OOOO00OO.result['taskinfo']['task_type']}")#line:1714
        print (f"Number of verifications : {OO0000OO0OOOO00OO.result['summary_statistics']['total_verifications']}")#line:1715
        print (f"Number of rules : {OO0000OO0OOOO00OO.result['summary_statistics']['valid_rules']}")#line:1716
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(OO0000OO0OOOO00OO.result['summary_statistics']['time_total']))}")#line:1717
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(OO0000OO0OOOO00OO.result['summary_statistics']['time_prep']))}")#line:1719
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(OO0000OO0OOOO00OO.result['summary_statistics']['time_processing']))}")#line:1720
        print ("")#line:1721
    def print_hypolist (O0OOOOO00OO00O00O ):#line:1723
        O0OOOOO00OO00O00O .print_rulelist ();#line:1724
    def print_rulelist (OO00O00000000OOO0 ,sortby =None ,storesorted =False ):#line:1726
        if not (OO00O00000000OOO0 ._is_calculated ()):#line:1727
            print ("ERROR: Task has not been calculated.")#line:1728
            return #line:1729
        def O0000OOO00O000O0O (O0OOO0O0O0OOOO000 ):#line:1730
            O0O000O0OO000O000 =O0OOO0O0O0OOOO000 ["params"]#line:1731
            return O0O000O0OO000O000 .get (sortby ,0 )#line:1732
        print ("")#line:1734
        print ("List of rules:")#line:1735
        if OO00O00000000OOO0 .result ['taskinfo']['task_type']=="4ftMiner":#line:1736
            print ("RULEID BASE  CONF  AAD    Rule")#line:1737
        elif OO00O00000000OOO0 .result ['taskinfo']['task_type']=="UICMiner":#line:1738
            print ("RULEID BASE  AAD_SCORE  Rule")#line:1739
        elif OO00O00000000OOO0 .result ['taskinfo']['task_type']=="CFMiner":#line:1740
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:1741
        elif OO00O00000000OOO0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1742
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:1743
        else :#line:1744
            print ("Unsupported task type for rulelist")#line:1745
            return #line:1746
        OOO0O00000O0OO000 =OO00O00000000OOO0 .result ["rules"]#line:1747
        if sortby is not None :#line:1748
            OOO0O00000O0OO000 =sorted (OOO0O00000O0OO000 ,key =O0000OOO00O000O0O ,reverse =True )#line:1749
            if storesorted :#line:1750
                OO00O00000000OOO0 .result ["rules"]=OOO0O00000O0OO000 #line:1751
        for O0000OO0OOOOO0OOO in OOO0O00000O0OO000 :#line:1753
            O00OO0000OO0OO000 ="{:6d}".format (O0000OO0OOOOO0OOO ["rule_id"])#line:1754
            if OO00O00000000OOO0 .result ['taskinfo']['task_type']=="4ftMiner":#line:1755
                O00OO0000OO0OO000 =O00OO0000OO0OO000 +" "+"{:5d}".format (O0000OO0OOOOO0OOO ["params"]["base"])+" "+"{:.3f}".format (O0000OO0OOOOO0OOO ["params"]["conf"])+" "+"{:+.3f}".format (O0000OO0OOOOO0OOO ["params"]["aad"])#line:1757
                O00OO0000OO0OO000 =O00OO0000OO0OO000 +" "+O0000OO0OOOOO0OOO ["cedents_str"]["ante"]+" => "+O0000OO0OOOOO0OOO ["cedents_str"]["succ"]+" | "+O0000OO0OOOOO0OOO ["cedents_str"]["cond"]#line:1758
            elif OO00O00000000OOO0 .result ['taskinfo']['task_type']=="UICMiner":#line:1759
                O00OO0000OO0OO000 =O00OO0000OO0OO000 +" "+"{:5d}".format (O0000OO0OOOOO0OOO ["params"]["base"])+" "+"{:.3f}".format (O0000OO0OOOOO0OOO ["params"]["aad_score"])#line:1760
                O00OO0000OO0OO000 =O00OO0000OO0OO000 +"     "+O0000OO0OOOOO0OOO ["cedents_str"]["ante"]+" => "+OO00O00000000OOO0 .result ['taskinfo']['target']+"(*) | "+O0000OO0OOOOO0OOO ["cedents_str"]["cond"]#line:1761
            elif OO00O00000000OOO0 .result ['taskinfo']['task_type']=="CFMiner":#line:1762
                O00OO0000OO0OO000 =O00OO0000OO0OO000 +" "+"{:5d}".format (O0000OO0OOOOO0OOO ["params"]["base"])+" "+"{:5d}".format (O0000OO0OOOOO0OOO ["params"]["s_up"])+" "+"{:5d}".format (O0000OO0OOOOO0OOO ["params"]["s_down"])#line:1763
                O00OO0000OO0OO000 =O00OO0000OO0OO000 +" "+O0000OO0OOOOO0OOO ["cedents_str"]["cond"]#line:1764
            elif OO00O00000000OOO0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1765
                O00OO0000OO0OO000 =O00OO0000OO0OO000 +" "+"{:5d}".format (O0000OO0OOOOO0OOO ["params"]["base1"])+" "+"{:5d}".format (O0000OO0OOOOO0OOO ["params"]["base2"])+"    "+"{:.3f}".format (O0000OO0OOOOO0OOO ["params"]["ratioconf"])+"    "+"{:+.3f}".format (O0000OO0OOOOO0OOO ["params"]["deltaconf"])#line:1766
                O00OO0000OO0OO000 =O00OO0000OO0OO000 +"  "+O0000OO0OOOOO0OOO ["cedents_str"]["ante"]+" => "+O0000OO0OOOOO0OOO ["cedents_str"]["succ"]+" | "+O0000OO0OOOOO0OOO ["cedents_str"]["cond"]+" : "+O0000OO0OOOOO0OOO ["cedents_str"]["frst"]+" x "+O0000OO0OOOOO0OOO ["cedents_str"]["scnd"]#line:1767
            print (O00OO0000OO0OO000 )#line:1769
        print ("")#line:1770
    def print_hypo (OOOO000O0000O00OO ,OO000O0O0OOOO0000 ):#line:1772
        OOOO000O0000O00OO .print_rule (OO000O0O0OOOO0000 )#line:1773
    def print_rule (O00O0000000OOOO00 ,OOOO0O0000OO00000 ):#line:1776
        if not (O00O0000000OOOO00 ._is_calculated ()):#line:1777
            print ("ERROR: Task has not been calculated.")#line:1778
            return #line:1779
        print ("")#line:1780
        if (OOOO0O0000OO00000 <=len (O00O0000000OOOO00 .result ["rules"])):#line:1781
            if O00O0000000OOOO00 .result ['taskinfo']['task_type']=="4ftMiner":#line:1782
                print ("")#line:1783
                O0O00OOOOO00O000O =O00O0000000OOOO00 .result ["rules"][OOOO0O0000OO00000 -1 ]#line:1784
                print (f"Rule id : {O0O00OOOOO00O000O['rule_id']}")#line:1785
                print ("")#line:1786
                print (f"Base : {'{:5d}'.format(O0O00OOOOO00O000O['params']['base'])}  Relative base : {'{:.3f}'.format(O0O00OOOOO00O000O['params']['rel_base'])}  CONF : {'{:.3f}'.format(O0O00OOOOO00O000O['params']['conf'])}  AAD : {'{:+.3f}'.format(O0O00OOOOO00O000O['params']['aad'])}  BAD : {'{:+.3f}'.format(O0O00OOOOO00O000O['params']['bad'])}")#line:1787
                print ("")#line:1788
                print ("Cedents:")#line:1789
                print (f"  antecedent : {O0O00OOOOO00O000O['cedents_str']['ante']}")#line:1790
                print (f"  succcedent : {O0O00OOOOO00O000O['cedents_str']['succ']}")#line:1791
                print (f"  condition  : {O0O00OOOOO00O000O['cedents_str']['cond']}")#line:1792
                print ("")#line:1793
                print ("Fourfold table")#line:1794
                print (f"    |  S  |  ¬S |")#line:1795
                print (f"----|-----|-----|")#line:1796
                print (f" A  |{'{:5d}'.format(O0O00OOOOO00O000O['params']['fourfold'][0])}|{'{:5d}'.format(O0O00OOOOO00O000O['params']['fourfold'][1])}|")#line:1797
                print (f"----|-----|-----|")#line:1798
                print (f"¬A  |{'{:5d}'.format(O0O00OOOOO00O000O['params']['fourfold'][2])}|{'{:5d}'.format(O0O00OOOOO00O000O['params']['fourfold'][3])}|")#line:1799
                print (f"----|-----|-----|")#line:1800
            elif O00O0000000OOOO00 .result ['taskinfo']['task_type']=="CFMiner":#line:1801
                print ("")#line:1802
                O0O00OOOOO00O000O =O00O0000000OOOO00 .result ["rules"][OOOO0O0000OO00000 -1 ]#line:1803
                print (f"Rule id : {O0O00OOOOO00O000O['rule_id']}")#line:1804
                print ("")#line:1805
                OOO0OOO0OO00O00O0 =""#line:1806
                if ('aad'in O0O00OOOOO00O000O ['params']):#line:1807
                    OOO0OOO0OO00O00O0 ="aad : "+str (O0O00OOOOO00O000O ['params']['aad'])#line:1808
                print (f"Base : {'{:5d}'.format(O0O00OOOOO00O000O['params']['base'])}  Relative base : {'{:.3f}'.format(O0O00OOOOO00O000O['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(O0O00OOOOO00O000O['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(O0O00OOOOO00O000O['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(O0O00OOOOO00O000O['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(O0O00OOOOO00O000O['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(O0O00OOOOO00O000O['params']['max'])}  Histogram minimum : {'{:5d}'.format(O0O00OOOOO00O000O['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(O0O00OOOOO00O000O['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(O0O00OOOOO00O000O['params']['rel_min'])} {OOO0OOO0OO00O00O0}")#line:1810
                print ("")#line:1811
                print (f"Condition  : {O0O00OOOOO00O000O['cedents_str']['cond']}")#line:1812
                print ("")#line:1813
                OOOOO0OOOOOO0O00O =O00O0000000OOOO00 .get_category_names (O00O0000000OOOO00 .result ["taskinfo"]["target"])#line:1814
                print (f"Categories in target variable  {OOOOO0OOOOOO0O00O}")#line:1815
                print (f"Histogram                      {O0O00OOOOO00O000O['params']['hist']}")#line:1816
                if ('aad'in O0O00OOOOO00O000O ['params']):#line:1817
                    print (f"Histogram on full set          {O0O00OOOOO00O000O['params']['hist_full']}")#line:1818
                    print (f"Relative histogram             {O0O00OOOOO00O000O['params']['rel_hist']}")#line:1819
                    print (f"Relative histogram on full set {O0O00OOOOO00O000O['params']['rel_hist_full']}")#line:1820
            elif O00O0000000OOOO00 .result ['taskinfo']['task_type']=="UICMiner":#line:1821
                print ("")#line:1822
                O0O00OOOOO00O000O =O00O0000000OOOO00 .result ["rules"][OOOO0O0000OO00000 -1 ]#line:1823
                print (f"Rule id : {O0O00OOOOO00O000O['rule_id']}")#line:1824
                print ("")#line:1825
                OOO0OOO0OO00O00O0 =""#line:1826
                if ('aad_score'in O0O00OOOOO00O000O ['params']):#line:1827
                    OOO0OOO0OO00O00O0 ="aad score : "+str (O0O00OOOOO00O000O ['params']['aad_score'])#line:1828
                print (f"Base : {'{:5d}'.format(O0O00OOOOO00O000O['params']['base'])}  Relative base : {'{:.3f}'.format(O0O00OOOOO00O000O['params']['rel_base'])}   {OOO0OOO0OO00O00O0}")#line:1830
                print ("")#line:1831
                print (f"Condition  : {O0O00OOOOO00O000O['cedents_str']['cond']}")#line:1832
                print (f"Antecedent : {O0O00OOOOO00O000O['cedents_str']['ante']}")#line:1833
                print ("")#line:1834
                print (f"Histogram                                        {O0O00OOOOO00O000O['params']['hist']}")#line:1835
                if ('aad_score'in O0O00OOOOO00O000O ['params']):#line:1836
                    print (f"Histogram on full set with condition             {O0O00OOOOO00O000O['params']['hist_cond']}")#line:1837
                    print (f"Relative histogram                               {O0O00OOOOO00O000O['params']['rel_hist']}")#line:1838
                    print (f"Relative histogram on full set with condition    {O0O00OOOOO00O000O['params']['rel_hist_cond']}")#line:1839
                OOO0000O00OO000OO =O00O0000000OOOO00 .result ['datalabels']['catnames'][O00O0000000OOOO00 .result ['datalabels']['varname'].index (O00O0000000OOOO00 .result ['taskinfo']['target'])]#line:1840
                print (" ")#line:1842
                print ("Interpretation:")#line:1843
                for OO0000O0OOOOOO0OO in range (len (OOO0000O00OO000OO )):#line:1844
                  O00O00000O0O00000 =0 #line:1845
                  if O0O00OOOOO00O000O ['params']['rel_hist'][OO0000O0OOOOOO0OO ]>0 :#line:1846
                      O00O00000O0O00000 =O0O00OOOOO00O000O ['params']['rel_hist'][OO0000O0OOOOOO0OO ]/O0O00OOOOO00O000O ['params']['rel_hist_cond'][OO0000O0OOOOOO0OO ]#line:1847
                  O0OOOO000OO00OOO0 =''#line:1848
                  if not (O0O00OOOOO00O000O ['cedents_str']['cond']=='---'):#line:1849
                      O0OOOO000OO00OOO0 ="For "+O0O00OOOOO00O000O ['cedents_str']['cond']+": "#line:1850
                  print (f"    {O0OOOO000OO00OOO0}{O00O0000000OOOO00.result['taskinfo']['target']}({OOO0000O00OO000OO[OO0000O0OOOOOO0OO]}) has occurence {'{:.1%}'.format(O0O00OOOOO00O000O['params']['rel_hist_cond'][OO0000O0OOOOOO0OO])}, with antecedent it has occurence {'{:.1%}'.format(O0O00OOOOO00O000O['params']['rel_hist'][OO0000O0OOOOOO0OO])}, that is {'{:.3f}'.format(O00O00000O0O00000)} times more.")#line:1852
            elif O00O0000000OOOO00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1853
                print ("")#line:1854
                O0O00OOOOO00O000O =O00O0000000OOOO00 .result ["rules"][OOOO0O0000OO00000 -1 ]#line:1855
                print (f"Rule id : {O0O00OOOOO00O000O['rule_id']}")#line:1856
                print ("")#line:1857
                print (f"Base1 : {'{:5d}'.format(O0O00OOOOO00O000O['params']['base1'])} Base2 : {'{:5d}'.format(O0O00OOOOO00O000O['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(O0O00OOOOO00O000O['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(O0O00OOOOO00O000O['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(O0O00OOOOO00O000O['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(O0O00OOOOO00O000O['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(O0O00OOOOO00O000O['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(O0O00OOOOO00O000O['params']['ratioconf'])}")#line:1858
                print ("")#line:1859
                print ("Cedents:")#line:1860
                print (f"  antecedent : {O0O00OOOOO00O000O['cedents_str']['ante']}")#line:1861
                print (f"  succcedent : {O0O00OOOOO00O000O['cedents_str']['succ']}")#line:1862
                print (f"  condition  : {O0O00OOOOO00O000O['cedents_str']['cond']}")#line:1863
                print (f"  first set  : {O0O00OOOOO00O000O['cedents_str']['frst']}")#line:1864
                print (f"  second set : {O0O00OOOOO00O000O['cedents_str']['scnd']}")#line:1865
                print ("")#line:1866
                print ("Fourfold tables:")#line:1867
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:1868
                print (f"----|-----|-----|  ----|-----|-----| ")#line:1869
                print (f" A  |{'{:5d}'.format(O0O00OOOOO00O000O['params']['fourfold1'][0])}|{'{:5d}'.format(O0O00OOOOO00O000O['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(O0O00OOOOO00O000O['params']['fourfold2'][0])}|{'{:5d}'.format(O0O00OOOOO00O000O['params']['fourfold2'][1])}|")#line:1870
                print (f"----|-----|-----|  ----|-----|-----|")#line:1871
                print (f"¬A  |{'{:5d}'.format(O0O00OOOOO00O000O['params']['fourfold1'][2])}|{'{:5d}'.format(O0O00OOOOO00O000O['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(O0O00OOOOO00O000O['params']['fourfold2'][2])}|{'{:5d}'.format(O0O00OOOOO00O000O['params']['fourfold2'][3])}|")#line:1872
                print (f"----|-----|-----|  ----|-----|-----|")#line:1873
            else :#line:1874
                print ("Unsupported task type for rule details")#line:1875
            print ("")#line:1879
        else :#line:1880
            print ("No such rule.")#line:1881
    def get_rulecount (OOOO0OO00O0OOO000 ):#line:1883
        if not (OOOO0OO00O0OOO000 ._is_calculated ()):#line:1884
            print ("ERROR: Task has not been calculated.")#line:1885
            return #line:1886
        return len (OOOO0OO00O0OOO000 .result ["rules"])#line:1887
    def get_fourfold (O0OO00O00O00O0O0O ,OOOOO0O0000O0O000 ,order =0 ):#line:1889
        if not (O0OO00O00O00O0O0O ._is_calculated ()):#line:1890
            print ("ERROR: Task has not been calculated.")#line:1891
            return #line:1892
        if (OOOOO0O0000O0O000 <=len (O0OO00O00O00O0O0O .result ["rules"])):#line:1893
            if O0OO00O00O00O0O0O .result ['taskinfo']['task_type']=="4ftMiner":#line:1894
                OO000O00O0OOO0O00 =O0OO00O00O00O0O0O .result ["rules"][OOOOO0O0000O0O000 -1 ]#line:1895
                return OO000O00O0OOO0O00 ['params']['fourfold']#line:1896
            elif O0OO00O00O00O0O0O .result ['taskinfo']['task_type']=="CFMiner":#line:1897
                print ("Error: fourfold for CFMiner is not defined")#line:1898
                return None #line:1899
            elif O0OO00O00O00O0O0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1900
                OO000O00O0OOO0O00 =O0OO00O00O00O0O0O .result ["rules"][OOOOO0O0000O0O000 -1 ]#line:1901
                if order ==1 :#line:1902
                    return OO000O00O0OOO0O00 ['params']['fourfold1']#line:1903
                if order ==2 :#line:1904
                    return OO000O00O0OOO0O00 ['params']['fourfold2']#line:1905
                print ("Error: for SD4ft-Miner, you need to provide order of fourfold table in order= parameter (valid values are 1,2).")#line:1906
                return None #line:1907
            else :#line:1908
                print ("Unsupported task type for rule details")#line:1909
        else :#line:1910
            print ("No such rule.")#line:1911
    def get_hist (OOO000O0O00O000O0 ,O000O000O0OO00OO0 ):#line:1913
        if not (OOO000O0O00O000O0 ._is_calculated ()):#line:1914
            print ("ERROR: Task has not been calculated.")#line:1915
            return #line:1916
        if (O000O000O0OO00OO0 <=len (OOO000O0O00O000O0 .result ["rules"])):#line:1917
            if OOO000O0O00O000O0 .result ['taskinfo']['task_type']=="CFMiner":#line:1918
                OO000OOO000OO000O =OOO000O0O00O000O0 .result ["rules"][O000O000O0OO00OO0 -1 ]#line:1919
                return OO000OOO000OO000O ['params']['hist']#line:1920
            elif OOO000O0O00O000O0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1921
                print ("Error: SD4ft-Miner has no histogram")#line:1922
                return None #line:1923
            elif OOO000O0O00O000O0 .result ['taskinfo']['task_type']=="4ftMiner":#line:1924
                print ("Error: 4ft-Miner has no histogram")#line:1925
                return None #line:1926
            else :#line:1927
                print ("Unsupported task type for rule details")#line:1928
        else :#line:1929
            print ("No such rule.")#line:1930
    def get_hist_cond (OOO000OOO00000OOO ,O000O0OOOO00O0O00 ):#line:1933
        if not (OOO000OOO00000OOO ._is_calculated ()):#line:1934
            print ("ERROR: Task has not been calculated.")#line:1935
            return #line:1936
        if (O000O0OOOO00O0O00 <=len (OOO000OOO00000OOO .result ["rules"])):#line:1937
            if OOO000OOO00000OOO .result ['taskinfo']['task_type']=="UICMiner":#line:1938
                OOO0OOOO00O0O0OO0 =OOO000OOO00000OOO .result ["rules"][O000O0OOOO00O0O00 -1 ]#line:1939
                return OOO0OOOO00O0O0OO0 ['params']['hist_cond']#line:1940
            elif OOO000OOO00000OOO .result ['taskinfo']['task_type']=="CFMiner":#line:1941
                OOO0OOOO00O0O0OO0 =OOO000OOO00000OOO .result ["rules"][O000O0OOOO00O0O00 -1 ]#line:1942
                return OOO0OOOO00O0O0OO0 ['params']['hist']#line:1943
            elif OOO000OOO00000OOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1944
                print ("Error: SD4ft-Miner has no histogram")#line:1945
                return None #line:1946
            elif OOO000OOO00000OOO .result ['taskinfo']['task_type']=="4ftMiner":#line:1947
                print ("Error: 4ft-Miner has no histogram")#line:1948
                return None #line:1949
            else :#line:1950
                print ("Unsupported task type for rule details")#line:1951
        else :#line:1952
            print ("No such rule.")#line:1953
    def get_quantifiers (O000O0OOO0OOOO00O ,OOOO0O000O00OO000 ,order =0 ):#line:1955
        if not (O000O0OOO0OOOO00O ._is_calculated ()):#line:1956
            print ("ERROR: Task has not been calculated.")#line:1957
            return #line:1958
        if (OOOO0O000O00OO000 <=len (O000O0OOO0OOOO00O .result ["rules"])):#line:1959
            OOO000O0OOOOO0OO0 =O000O0OOO0OOOO00O .result ["rules"][OOOO0O000O00OO000 -1 ]#line:1960
            if O000O0OOO0OOOO00O .result ['taskinfo']['task_type']=="4ftMiner":#line:1961
                return OOO000O0OOOOO0OO0 ['params']#line:1962
            elif O000O0OOO0OOOO00O .result ['taskinfo']['task_type']=="CFMiner":#line:1963
                return OOO000O0OOOOO0OO0 ['params']#line:1964
            elif O000O0OOO0OOOO00O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1965
                return OOO000O0OOOOO0OO0 ['params']#line:1966
            else :#line:1967
                print ("Unsupported task type for rule details")#line:1968
        else :#line:1969
            print ("No such rule.")#line:1970
    def get_varlist (OO00O0O0O0OOO0000 ):#line:1972
        return OO00O0O0O0OOO0000 .result ["datalabels"]["varname"]#line:1973
    def get_category_names (O00OOO0OO0OO000OO ,varname =None ,varindex =None ):#line:1975
        O0OO0O000OOOOO0OO =0 #line:1976
        if varindex is not None :#line:1977
            if O0OO0O000OOOOO0OO >=0 &O0OO0O000OOOOO0OO <len (O00OOO0OO0OO000OO .get_varlist ()):#line:1978
                O0OO0O000OOOOO0OO =varindex #line:1979
            else :#line:1980
                print ("Error: no such variable.")#line:1981
                return #line:1982
        if (varname is not None ):#line:1983
            OOOO0OO0OOOOOOO0O =O00OOO0OO0OO000OO .get_varlist ()#line:1984
            O0OO0O000OOOOO0OO =OOOO0OO0OOOOOOO0O .index (varname )#line:1985
            if O0OO0O000OOOOO0OO ==-1 |O0OO0O000OOOOO0OO <0 |O0OO0O000OOOOO0OO >=len (O00OOO0OO0OO000OO .get_varlist ()):#line:1986
                print ("Error: no such variable.")#line:1987
                return #line:1988
        return O00OOO0OO0OO000OO .result ["datalabels"]["catnames"][O0OO0O000OOOOO0OO ]#line:1989
    def print_data_definition (O00OO00000O00OOOO ):#line:1991
        O000O00OO0OOOO000 =O00OO00000O00OOOO .get_varlist ()#line:1992
        for OOO00O0O0000O00OO in O000O00OO0OOOO000 :#line:1993
            O00O0000O00OO0OOO =O00OO00000O00OOOO .get_category_names (OOO00O0O0000O00OO )#line:1994
            O0O0OOO000O00O0OO =""#line:1995
            for O0OO00O0OO00OO000 in O00O0000O00OO0OOO :#line:1996
                O0O0OOO000O00O0OO =O0O0OOO000O00O0OO +str (O0OO00O0OO00OO000 )+" "#line:1997
            O0O0OOO000O00O0OO =O0O0OOO000O00O0OO [:-1 ]#line:1998
            print (f"Variable {OOO00O0O0000O00OO} has {len(O000O00OO0OOOO000)} categories: {O0O0OOO000O00O0OO}")#line:1999
    def _is_calculated (OO00O0OO0O00OO0OO ):#line:2001
        ""#line:2006
        OO000O00O0OOOO000 =False #line:2007
        if 'taskinfo'in OO00O0OO0O00OO0OO .result :#line:2008
            OO000O00O0OOOO000 =True #line:2009
        return OO000O00O0OOOO000 