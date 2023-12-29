#from ctypes import *
import ctypes
import sys
import os
import json

#bin_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin')

# ld_path = os.getenv('LD_LIBRARY_PATH')

#print(epbin_path +  r"\EPCAM_CTYPE.dll")
#dll = ctypes.cdll.LoadLibrary(pp)

#epbin_path = os.getcwd() + r'py\bin"

dll = None
dmsdll = None
vdll = None
uidll = None
# dfmdll = None
matrixdll = None
clouddll = None
bin_path = None

isInit = False

def init(path):

    global dll
    global dmsdll
    global vdll
    global uidll
    # global dfmdll
    global matrixdll
    global clouddll
    global bin_path

    bin_path = path
    os.environ['path'] += (r";" + bin_path)

    dll = ctypes.CDLL(bin_path + r"\EPCAM_CTYPE.dll")
    uidll = ctypes.CDLL(bin_path + r"\EPCAM_UITYPE.dll")
    dmsdll = ctypes.CDLL(bin_path + r"\DMS_CTYPE.dll")
    vdll = ctypes.CDLL(bin_path + r"\Form_View.dll")
    # dfmdll = ctypes.CDLL(bin_path + r"\dfmDataAnalysis.dll")
    matrixdll = ctypes.CDLL(bin_path + r"\AutoMatrix.dll")
    clouddll = ctypes.CDLL(bin_path + r"\AliCloud.dll")

    dll.process.restype =  ctypes.c_char_p
    dll.init_func_map.restype =  ctypes.c_char_p
    dll.init_orig_func_map.restype =  ctypes.c_char_p
    dll.getVersion.restype =  ctypes.c_char_p
    # dll.getVersion.restype =  ctypes.c_char_p
    dll.process.argtypes = [ctypes.c_char_p]
    uidll.process.restype =  ctypes.c_char_p
    uidll.init_ui_func_map.restype =  ctypes.c_char_p
    # uidll.init_orig_func_map.restype =  ctypes.c_char_p
    uidll.process.argtypes = [ctypes.c_char_p]
    vdll.init.argtypes = [ctypes.c_char_p]
    vdll.view_cmd.argtypes = [ctypes.c_char_p]
    dmsdll.init.restype = ctypes.c_char_p
    dmsdll.uploadmongo.restype = ctypes.c_char_p
    dmsdll.getParam.restype = ctypes.c_char_p
    dmsdll.downloadjob.restype = ctypes.c_char_p

    dmsdll.downloadorigin.restype = ctypes.c_char_p
    dmsdll.downloadpre.restype = ctypes.c_char_p
    #cdef extern from"stdio.h":
    #    extern int printf(const char* format, ...)
    dmsdll.upload_robot2mongo.restype = ctypes.c_char_p

    dmsdll.getOrderInfoByJobName.restype = ctypes.c_char_p
    dmsdll.set_robot_status.restype = ctypes.c_int
    dmsdll.epdms_order_status_update.restype = ctypes.c_char_p
    dmsdll.epdms_flow_status_update.restype = ctypes.c_char_p
    dmsdll.get_mongo_fsname.restype = ctypes.c_char_p
    clouddll.uploadFileAny.restype = ctypes.c_char_p
    # dfmdll.pcsAnalysis.restype = ctypes.c_char_p

    matrixdll.readPathFactoryJson.restype = ctypes.c_char_p
    matrixdll.readPathTemplateConfigJson.restype = ctypes.c_char_p
    matrixdll.getMatchedLayers.restype = ctypes.c_char_p
    matrixdll.saveNewMatchRule.restype = ctypes.c_char_p

    # ret = dll.init_func_map()
    # ret = dll.init_orig_func_map()
    # ret = uidll.init_ui_func_map()
    vstring_path = bytes(bin_path, encoding='utf-8')
    vdll.init(vstring_path)

    global isInit
    isInit = True

    # return ret.decode('utf-8')

def init_func_maps():
    ret = dll.init_func_map()
    ret = dll.init_orig_func_map()
    ret = uidll.init_ui_func_map()
    return ret.decode('utf-8')

def set_use_times(times):
    times.encode('utf-8')
    #print(type(json))
    times_str = bytes(times, encoding='utf-8')
    dll.setUseTimes(times_str)

def process(json):
    if isInit == False:
        print('Please init first')
        return

    json.encode('utf-8')
    #print(type(json))
    string_buff = bytes(json, encoding='utf-8')
    #print(type(string_buff), string_buff)
    ret = dll.process(string_buff)
    #print(ret)
    return ret.decode('utf-8')


def view_cmd(vjson):
    string_vjson = bytes(vjson, encoding='utf-8')
    vdll.view_cmd(string_vjson)

def getVersion():
    ret = dll.getVersion()
    ret = ret.decode('utf-8')
    return json.loads(ret)

def uiprocess(json):
    json.encode('utf-8')
    #print(type(json))
    string_buff = bytes(json, encoding='utf-8')
    #print(type(string_buff), string_buff)
    ret = uidll.process(string_buff)
    #print(ret)
    return ret.decode('utf-8')

# def pcsAnalysis(vjson):
#     string_vjson = bytes(vjson, encoding='utf-8')
#     ret = dfmdll.pcsAnalysis(string_vjson)
#     return ret.decode('gbk')

def readPathFactoryJson(vjson):
    string_vjson = bytes(vjson, encoding='utf-8')
    ret = matrixdll.readPathFactoryJson(string_vjson)
    return ret.decode('gbk')

def readPathTemplateConfigJson(vjson):
    string_vjson = bytes(vjson, encoding='utf-8')
    ret = matrixdll.readPathTemplateConfigJson(string_vjson)
    return ret.decode('gbk')

def getMatchedLayers(vjson):
    string_vjson = bytes(vjson, encoding='utf-8')
    ret = matrixdll.getMatchedLayers(string_vjson)
    return ret.decode('gbk')

def saveNewMatchRule(vjson):
    string_vjson = bytes(vjson, encoding='utf-8')
    ret = matrixdll.saveNewMatchRule(string_vjson)
    return ret.decode('gbk')

def get_config_path():
    return bin_path

def uploadFileAny(vjson):
    string_vjson = bytes(vjson, encoding='utf-8')
    ret = clouddll.uploadFileAny(string_vjson)
    return ret.decode('gbk')


