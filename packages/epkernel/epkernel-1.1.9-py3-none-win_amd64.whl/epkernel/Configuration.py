import os, sys, json,requests,time
from epkernel import Input,epcam,BASE
from epkernel.Action import Information
from epkernel.Edition import Job


def init(path:str): 
    try:
        epcam.init(path)
        BASE.path = path
        v = epcam.getVersion()
        version = v['kernel_id']
        if not version == '1.3.1':
            print("Epkernel与bin包版本不匹配，请谨慎使用")
        else:
            epcam.init_func_maps()
            BASE.set_config_path(path)
            eplibpath = os.path.join(path,'job')
            Input.open_job('EPLIB',eplibpath)
            openedjob = Job.is_job_open('EPLIB')
            if openedjob == False:
                print('EPLIB未打开')
    except Exception as e:
        print(e)
        
        
        
def set_sysattr_path(path:str):
    try:
        BASE.set_sysAttr_path(path)
    except Exception as e:
        print(e)
    return 

def set_userattr_path(path:str):
    try:
        BASE.set_userAttr_path(path)
    except Exception as e:
        print(e)
    return    
    
    
def read_auto_matrix_rule(path:str)->dict:
    try:
        ccc = BASE.read_auto_matrix_rule(path)
        return json.loads(ccc)
    except Exception as e:
        print(e)
        return None

def read_auto_matrix_template(path:str)->dict:
    try:
        ccc = BASE.read_auto_matrix_template(path)
        return json.loads(ccc)
    except Exception as e:
        print(e)
        return None

def add_new_match_rule(layer_infos:list, path:str)->dict:
    try:
        ruleName=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        ret = BASE.saveNewMatchRule(layer_infos,path,ruleName)
        ret = json.loads(ret)
        return ret
    except Exception as e:
        print(e)
    return {}





