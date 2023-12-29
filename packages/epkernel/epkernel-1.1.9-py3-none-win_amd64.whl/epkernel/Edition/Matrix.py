import os, sys, json
from epkernel import BASE
from epkernel.Edition import Layers
from epkernel.Action import Selection, Information


# 拷贝Layer
def copy_layer(job:str, old_layer_name:str) :
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        src_layername=[]
        src_layername= Information.get_layers(job)
        if old_layer_name in src_layername:
            for i in range(0, len(layer_infos)):         
                if layer_infos[i]['name'] == old_layer_name:
                    old_layer_index = i + 1
        else:
            print('e')
            return 0
        dst_layer = ''
        # 新建空layer
        create_layer(job, 'jbz')
        ret2 = BASE.copy_layer(job, old_layer_index,
                               dst_layer, len(layer_infos) + 1)
        data2 = json.loads(ret2)
        new_layer = data2['paras']['newname']
        # 删除新层
        delete_layer(job, 'jbz')
        return new_layer
    except Exception as e:
        print(e)
        print('123456')
    return ''

# 创建layer
def create_layer(job:str, layer:str, row_index:int=-1):
    try:
        text = BASE.check_reg_text_name(layer)
        charactor = BASE.check_reg_illegal_charactor(layer)
        if text == True and charactor == True:
            step = ''  # 在所有层创建
            BASE.create_new_layer(job, step, layer, row_index)
    except Exception as e:
        print(e)

# 删除layer
def delete_layer(job:str, layername:str):
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == layername:
                layer_index = i + 1
                BASE.delete_layer(job, layer_index)
                break
    except Exception as e:
        print(e)
    return 0

# 创建step
def create_step(job:str, step:str, col_index:int=-1):
    try:
        text = BASE.check_reg_text_name(step)
        charactor = BASE.check_reg_illegal_charactor(step)
        if text == True and charactor == True:
            BASE.create_step(job, step, col_index)
    except Exception as e:
        print(e)

def change_matrix_row(job:str, layer:str, context:str, type:str, layername:str, polarity:bool = True):
    """
    #修改指定层别信息,若修改后信息与原层别一致，则此函数不执行
    :param     jobname:
    :param     layer:
    :param     context:
    :returns   :
    :raises    error:
    """
    try:
        text = BASE.check_reg_text_name(layername)
        charactor = BASE.check_reg_illegal_charactor(layername)
        if text == True and charactor == True:
            ret = BASE.get_matrix(job)
            data = json.loads(ret)
            layer_infos = data['paras']['info']
            if polarity == True:
                polarity = 'positive'
            else:
                polarity = 'negative'
            for i in range(0, len(layer_infos)):
                if layer_infos[i]['name'] == layer:
                    layer_index = i + 1
                    layer_infos[i]['context'] = context
                    layer_infos[i]['type'] = type
                    layer_infos[i]['name'] = layername
                    layer_infos[i]['polarity'] = polarity
            BASE.change_matrix(job, -1, layer_index, '',
                            layer_infos[layer_index-1])
    except Exception as e:
        print(e)
    return 0

def change_matrix_column(job:str, src_name:str, dst_name:str):
    try:
        text = BASE.check_reg_text_name(dst_name)
        charactor = BASE.check_reg_illegal_charactor(dst_name)
        if text == True and charactor == True:
            ret = BASE.get_matrix(job)
            data = json.loads(ret)
            step_infos = data['paras']['steps']
            old_step_index = step_infos.index(src_name) + 1
            old_layer_index = -1
            new_layer_info = ''
            BASE.change_matrix(job, old_step_index,
                            old_layer_index, dst_name, new_layer_info)
    except Exception as e:
        print(e)

def delete_step(job:str, step:str):
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        for i in range(0, len(step_infos)):
            if step_infos[i] == step:
                step_index = i + 1
        BASE.delete_step(job, step_index)
    except Exception as e:
        print(e)
    return 0

def copy_step(job:str, src_step_name:str)->str:
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        if src_step_name in step_infos:
            for i in range(0, len(step_infos)):
                if step_infos[i] == src_step_name:
                    old_step_index = i + 1
            dst_step = ''
            # 新建空
            create_step(job, 'jbz') 
            ret= Information.get_steps(job)
            ret2 = BASE.copy_step(job, old_step_index,
                                dst_step, len(step_infos)+1)
            data2 = json.loads(ret2)
            new_step = data2['paras']['newname']
            # 删除新层
            delete_step(job, 'jbz')
        return new_step
    except Exception as e:
        print(e)
    return ''

#备份多层（覆盖）(需备份层无选中feature)
def backup_layer(job:str, step:str, layers:list, suffix:str):
    try:
        layer_list = Information.get_layers(job)
        for layer in layers:
            new_layer = layer + suffix
            if new_layer not in layer_list:
                create_layer(job, new_layer)
            else:
                BASE.clear_selected_features(job, step, new_layer)
                Selection.reverse_select(job, step, new_layer) 
                Layers.delete_feature(job, step, [new_layer])  
                BASE.clear_selected_features(job, step, new_layer)
            Layers.copy2other_layer(job, step, layer, new_layer, False, 0, 0, 0, 0, 0, 0, 0)
    except Exception as e:
        print(e)
        return None

def move_layer(job:str, org_layer_index:int, dst_layer_index:int):
    try:
        jobname = job
        BASE.move_layer(jobname, org_layer_index, dst_layer_index)
    except Exception as e:
        print(e)
        return None

def set_layer_infos(job:str, layerInfos:list, oldList:list, newList:list)->bool:
    try:
        if not len(oldList) == len(newList):
            return False
        if not len(oldList) == len(layerInfos):
            return False
        if len(oldList) == 0:
            return False
        nameMap = []
        for i in range(len(oldList)):
            nameMap.append({oldList[i] : newList[i]})
        ret = BASE.set_layer_infos(job, layerInfos, nameMap)
        ret = json.loads(ret)
        if 'status' in ret:
            if ret['status'] == 'true':
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print(e)
        return False

def auto_matrix(job:str)->tuple:
    try:
        #获取所有层别名
        nameList = Information.get_layers(job)
        vv = BASE.auto_matrix(nameList)
        nn = json.loads(vv)
        ret = json.loads(nn['msg'])
        if ret == '':
            return ([], [], [])
        #将匹配结果转为set_layer_infos需要的数据结构
        bbb = BASE.matchLayers2LayerInfos(ret)
        layerInfos = bbb[0]
        oldList = bbb[1]
        newList = bbb[2]

        #加入将未匹配成功的层
        for v in layerInfos:
            nameList.remove(v["old_name"])
        
        vIndex = 1
        for vv in nameList:
            layerInfo = {}
            layerInfo['type'] = 'document'
            layerInfo['name'] = vv
            layerInfo['context'] = 'misc'
            layerInfo['polarity'] = 'positive'
            layerInfo['start_name'] = ""
            layerInfo['end_name'] = ""
            layerInfo['old_name'] = vv
            layerInfo['row'] = len(layerInfos) + vIndex
            layerInfos.append(layerInfo)
            #nameMap.append({vv : vv})
            oldList.append(vv)
            newList.append(vv)
        return (layerInfos, oldList, newList)
    except Exception as e:
        print(e)
        return ([], [], [])

def create_flip(job:str, step:str)->bool:
    try:
        _ret = BASE.step_flip(job,step)
        ret = json.loads(_ret)['paras']['result']
        return ret
    except Exception as e:
        print(e)
        return False

def edit_step_attributes(job:str, step:str, edit_mode:int, edit_attr_name:str, edit_attr_value:str)->bool:
    try:
        _ret = BASE.edit_step_attributes(job,step,edit_mode,edit_attr_name,edit_attr_value)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
        return False

def edit_layer_attributes(job:str, step:str, layer:str, edit_mode:int, edit_attr_name:str, edit_attr_value:str)->bool:
    try:
        _ret = BASE.edit_layer_attributes(job,step,layer,edit_mode,edit_attr_name,edit_attr_value)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
        return False

def change_drill_cross(job:str, layer:str, start_name:str, end_name:str):
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == layer:
                layer_index = i + 1
                layer_infos[i]['start_name'] = start_name
                layer_infos[i]['end_name'] = end_name
        BASE.change_matrix(job, -1, layer_index, '', layer_infos[layer_index-1])
    except Exception as e:
        print(e)
    return 0

def refresh_flip_step(job:str, steps:list=[])->bool:
    try:
        if steps == []:
            info = BASE.refresh_all_flip_step(job)
            data = json.loads(info)['status']
            if data == 'true':
                data = True
            else:
                data = False
        else:
            flip = []
            for step in steps:
                info = BASE.refresh_flip_step(job,step)
                ret = json.loads(info)['result']
                flip.append(ret)
            if False in flip:
                data = False
            else:
                data = True
        return data
    except Exception as e:
        print(e)
    return False















