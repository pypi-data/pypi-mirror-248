import os, sys, json, re
from epkernel import BASE
from epkernel.Action import Information


def delete_job(job:str)->None:
    try:
        BASE.job_delete(job)
    except Exception as e:
        print(e)

def create_job(job:str)->bool:
    try:
        openedjob = Information.get_opened_jobs()
        if job in openedjob:
            return False
        for ch in job:
            if u'\u4e00' <= ch <= u'\u9fff':
                return False
        if re.search('((?=[\x20-\x7e]+)[^A-Za-z0-9\_\+\-])',job)!=None or job=='eplib':
            return False
        else:
            ret = json.loads(BASE.job_create(job))['status']
            path = os.path.join(BASE.path,'fontsrc')
            info = os.path.exists(path)
            if info == True:
                load = BASE.load_font(job,path)
            return bool(ret)
    except Exception as e:
        print(e)
        return False
        
def rename_job(src_jobname:str, dst_jobname:str)->bool:
    try:
        openedjob = Information.get_opened_jobs()
        if dst_jobname in openedjob:
            return False
        if json.loads(BASE.is_job_open(src_jobname))['paras']['status']== True:
            # 判断料名中是否有中文
            for ch in dst_jobname:
                if u'\u4e00' <= ch <=u'\u9fff':
                    return False
            # 判断料号中是否有特殊符号
            if re.search('((?=[\x20-\x7e]+)[^A-Za-z0-9\_\+\-])',dst_jobname)!=None or dst_jobname=='eplib':
                return False
            else:
                BASE.job_rename(src_jobname, dst_jobname)
                return True
    except Exception as e:
        print(e)
        return False
#判断指定料号是否打开       
def is_job_open(job:str)->bool:
    try:
        _ret= BASE.is_job_open(job)
        ret =json.loads(_ret)['paras']['status']
        return ret
    except Exception as e:
        print(e)
        return False 

#关闭指定料号(job)并清空内存,若不存在该料号名则不执行返回False值
def close_job(job:str)->bool:
    try:
        data= is_job_open(job)
        if data:
            ret_ =BASE.close_job(job)
            ret= json.loads(ret_)['status']
            return ret
        else:
            print(f'不存在{job}料号名!')
            return False
    except Exception as e:
        print(e) 
    return None

def copy_job(src_job:str,dst_job:str)->bool:
    try:
        opened = is_job_open(dst_job)
        if opened == False:
            create_job(dst_job)
        ret= BASE.copy_job(src_job,dst_job)
        data = json.loads(ret)['paras'][0]
        return data
    except Exception as e:
        print(repr(e))
    return None

def delete_usersymbol(job:str,symbolname:str)->bool:
    try:
        used = BASE.usersymbol_is_used(job,symbolname)
        use = json.loads(used)['paras']['result']
        if use == True:
            return False
        else:
            _ret = BASE.delete_usersymbol(job,symbolname)
            ret = json.loads(_ret)['paras']['result']
            return ret
    except Exception as e:
        print(e)
    return False


def rename_usersymbol(job:str,srcname:str,dstname:str)->bool:
    try:
        for ch in dstname:
            if u'\u4e00' <= ch <=u'\u9fff':
                return False
        if re.search('((?=[\x20-\x7e]+)[^A-Za-z0-9\_\+\-])',dstname)!=None:
            return False
        _ret = BASE.rename_usersymbol(job,srcname,dstname)
        ret = json.loads(_ret)['paras']['result']
        return ret
    except Exception as e:
        print(e)
    return False

def edit_job_attributes(job:str,edit_mode:int,edit_attrname:str,edit_attrvalue:str)->bool:
    try:
        ret = BASE.edit_job_attributes(job,edit_mode,edit_attrname,edit_attrvalue)
        data = json.loads(ret)['status']
        if data == 'true':
            data = True
        else:
            data = False
        return data
    except Exception as e:
        print(e)
        return False

def edit_usersymbol_attributes(job:str,usersymbol_name:str,edit_mode:int,edit_attrname:str,edit_attrvalue:str)->bool:
    try:
        ret = BASE.edit_usersymbol_attributes(job,usersymbol_name,edit_mode,edit_attrname,edit_attrvalue)
        data = json.loads(ret)['status']
        if data == 'true':
            data = True
        else:
            data = False
        return data
    except Exception as e:
        print(e)
        return False




















