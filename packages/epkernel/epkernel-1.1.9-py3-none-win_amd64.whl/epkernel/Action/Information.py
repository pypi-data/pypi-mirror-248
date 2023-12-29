import os, sys, json, math
from epkernel import epcam, BASE

def check_matrix_info(job:str, step:str='', layers:list=[])->bool:
    try:
        if isinstance(job, str) and isinstance(step, str) and isinstance(layers, list):
            open_jobs = get_opened_jobs()
            if job in open_jobs: 
                if step == '' and layers == []:
                    return False
                step_lst= get_steps(job)
                layer_lst = get_layers(job)
                if step!='':
                    if step not in step_lst:
                        print('step不存在')
                        return False
                if layers!=[]:
                    for layer in layers:
                        if layer not in layer_lst:
                            print(layer + ' 不存在')
                            return False
            else:
                print(f'{job}:未打开,请查找原因!')
                return False
        else:
            print("请检查填写的参数类型!")
            return False
    except Exception as e:
        return False
        print(e)
    return True

def has_selected_features(job:str,step:str,layer:str)->bool:
    try:
        ret = BASE.is_selected(job,step,layer)
        ret = json.loads(ret)
        if 'result' in ret:
            return ret['result']
        return False
    except Exception as e:
        print(e)
    return False

def get_drill_layers(job:str)->list:
    """
    #获取孔层layer名
    :param     job:
    :param     step:
    :return    drill_list:孔层名列表
    :raises    error:
    """
    try:
        ret = BASE.get_graphic(job)
        data = json.loads(ret)
        drill_list = []
        layer_info = data['paras']['info']
        for i in range(0, len(layer_info)):
            if layer_info[i]['type'] == 'drill' and layer_info[i]['context'] == 'board':
                drill_list.append(layer_info[i]['name'])
        return drill_list
    except Exception as e:
        print(e)
    return []

def get_inner_layers(job:str)->list:
    """
    #获取内层layer_list
    :param     job:
    :returns   inner_layer_list:内层layername列表
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                board_layer_list.append(layer_info[i]['name'])      
        if len(board_layer_list) <= 2:
            print('no inner layer!')
            return []
        else:
            board_layer_list.pop(-1)
            board_layer_list.pop(0)
            inner_layer_list = board_layer_list
        return inner_layer_list
    except Exception as e:
        print(e)
    return []

def get_board_layers(job:str)->list:
    try:
        ret = BASE.get_graphic(job)
        data = json.loads(ret)
        layer_list = []
        layer_info = data['paras']['info']
        if len(layer_info):
            for i in range(0, len(layer_info)):
                if layer_info[i]['context'] == 'board':
                    layer_list.append(layer_info[i]['name'])
        return layer_list
    except Exception as e:
        print(e)
        #sys.exit(0)
    return ''

def get_soldermask_layers(job:str)->list:
    """
    #获取防焊层list
    :param     job:
    :param     step:
    :returns   solder_mask_list:
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        solder_mask_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'solder_mask':
                solder_mask_list.append(layer_info[i]['name'])      
        return solder_mask_list
    except Exception as e:
        print(e)
    return ''

def get_signal_layers(job:str)->list:
    """
    #获取内外层layer 名
    :param     job:
    :returns   inner_layer_list:内层layername列表
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                board_layer_list.append(layer_info[i]['name'])
        return board_layer_list
    except Exception as e:
        print(e)
    return []

def get_outer_layers(job:str)->list:
    """
    #获取外层list
    :param     job:
    :returns   outter_layer_list:外层layername列表
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        index_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                index_list.append(i)
        if index_list == []:
            print("no signal layer")
            return []
        for j in range(min(index_list),max(index_list)+1):
            board_layer_list.append(layer_info[j]['name'])
        outter_layer_list = []
        outter_layer_list.append(board_layer_list[0])
        if len(board_layer_list) == 1:
            return outter_layer_list
        outter_layer_list.append(board_layer_list[-1])
        return outter_layer_list
    except Exception as e:
        print(e)
    return ''

def get_silkscreen_layers(job:str)->list:
    """
    #获取丝印层layer_list      
    :param     job: 
    :returns   layer_list:丝印层layername列表     
    :raises    error:    
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        layer_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'silk_screen':
                layer_list.append(layer_info[i]['name'])
        if len(layer_list) < 1:
            print("can't find silk_screen-layer!")
        return layer_list
    except Exception as e:
        print(e)
    return ''

#获取layer profile polygon
def get_profile(job:str, step:str)->list:
    try:
        _ret = BASE.get_profile(job, step)
        ret = json.loads(_ret)['points']
        return ret
    except Exception as e:
        print(e)
    return []

def get_layer_feature_count(job:str, step:str, layer:str)->int:
    try:
        ret = BASE.get_layer_feature_count(job, step, layer)
        ret = json.loads(ret)
        if 'featureNum' in ret:
            return int(ret['featureNum'])
        return -1
    except Exception as e:
        print(e)
    return -1

def get_steps(job:str)->list:
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        steps = data['paras']['steps']
        return steps
    except Exception as e:
        print(e)
    return []

def get_layers(job:str)->list:
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        layer_list = []
        for i in range(0, len(layer_infos)):
            layer_list.append(layer_infos[i]['name'])
        return layer_list
    except Exception as e:
        print(e)
    return []

def get_usersymbol_list(job:str)->list:
    try:
        ret = BASE.get_special_symbol_names(job)
        data = json.loads(ret)
        user_list = data['paras']
        return user_list
    except Exception as e:
        print(e)
    return []

def get_profile_box(job:str, step:str)->dict:  
    try:
        #转成小写
        job= job.lower()
        step= step.lower()
        info= check_matrix_info(job, step)
        if info:
            ret_= BASE.has_profile(job,step)
            data_= json.loads(ret_)['result']
            if data_:
                ret = BASE.get_profile_box(job, step)
                data = json.loads(ret)
                box = data['paras']
                profile_box = {}
                profile_box['xmax'] = box['Xmax']
                profile_box['xmin'] = box['Xmin']
                profile_box['ymax'] = box['Ymax']
                profile_box['ymin'] = box['Ymin']
                return profile_box
            print('没有profile!')
            return {}
        return None
    except Exception as e:
        print(e)
    return None

#获取拼版中最小和最大坐标
def get_inner_profile_box(job:str,step:str)->dict:
    try:
        repeat_infos=BASE.get_step_repeat(job,step)    #获取拼板信息
        repeat_infos=json.loads(repeat_infos)
        repeat_infos=repeat_infos['result']
        xminlist=[]
        yminlist=[]
        xmaxlist=[]
        ymaxlist=[]
        for repeat_info in repeat_infos:
            repeat_infox=repeat_info['X']
            repeat_infoy=repeat_info['Y']
            set_box=get_profile_box(job, repeat_info['NAME'])
            datum_x=json.loads(BASE.get_step_header_infos(job, repeat_info['NAME']))['x_datum']
            datum_y=json.loads(BASE.get_step_header_infos(job, repeat_info['NAME']))['y_datum']
            x_offset = repeat_infox - datum_x
            y_offset = repeat_infoy - datum_y
            pts=[]
            pts.append([set_box['xmin']+x_offset,set_box['ymin']+y_offset])
            pts.append([set_box['xmin']+x_offset,set_box['ymax']+y_offset])
            pts.append([set_box['xmax']+x_offset,set_box['ymax']+y_offset])
            pts.append([set_box['xmax']+x_offset,set_box['ymin']+y_offset])
            width=set_box['xmax']-set_box['xmin']
            height=set_box['ymax']-set_box['ymin']
            if repeat_info['MIRROR']:
                pts.clear()
                pts.append([set_box['xmin']+x_offset-width,set_box['ymin']+y_offset])
                pts.append([set_box['xmin']+x_offset-width,set_box['ymax']+y_offset])
                pts.append([set_box['xmin']+x_offset,set_box['ymax']+y_offset])
                pts.append([set_box['xmin']+x_offset,set_box['ymin']+y_offset])

            if repeat_info['ANGLE']!=0:
                value = math.acos(-1) / 180
                ratio = -1 * repeat_info['ANGLE'] * value
                if repeat_info['MIRROR']:
                    ratio = -1 * (360-repeat_info['ANGLE']) * value
                for pt in pts:
                    a = pt[0]
                    b = pt[1]
                    pt[0]=(a - repeat_infox)*math.cos(ratio) - (b - repeat_infoy)*math.sin(ratio) + repeat_infox
                    pt[1]=(a - repeat_infox)*math.sin(ratio) + (b - repeat_infoy)*math.cos(ratio) + repeat_infoy
            allx=[]
            ally=[]
            for pt in pts:
                allx.append(pt[0])
                ally.append(pt[1])
            allx.sort()
            ally.sort()
            xmin=allx[0]
            ymin=ally[0]
            set_length=allx[-1]-allx[0]
            set_width=ally[-1]-ally[0]    
            length= (repeat_info['NX']-1)*repeat_info['DX']+set_length
            width = (repeat_info['NY']-1)*repeat_info['DY']+set_width
            xmax=xmin+length
            ymax=ymin+width
            xminlist.append(xmin)
            yminlist.append(ymin)
            xmaxlist.append(xmax)
            ymaxlist.append(ymax)
        xminlist.sort()
        yminlist.sort()
        xmaxlist.sort(reverse=True)
        ymaxlist.sort(reverse=True)
        gSRxmin=xminlist[0]
        gSRymin=yminlist[0]
        gSRxmax=xmaxlist[0]
        gSRymax=ymaxlist[0]
        gSRxcenter = (gSRxmax-gSRxmin)/2
        gSRycenter = (gSRymax-gSRymin)/2
        infos={}
        infos['xmin']=gSRxmin
        infos['ymin']=gSRymin
        infos['xmax']=gSRxmax
        infos['ymax']=gSRymax
        infos['xcenter'] = gSRxcenter
        infos['ycenter'] = gSRycenter
        return infos
    except Exception as e:
        print(e)
    return {}

def get_selected_features_box(job:str, step:str, layers:list)->dict:
    try:
        job= job.lower()
        step= step.lower()
        for layer in range(len(layers)):
            layers[layer] = layers[layer].lower()
        info= check_matrix_info(job, step,layers)
        if info:                
            ret = BASE.get_selected_features_box(job, step, layers)
            data = json.loads(ret)
            features_box=[]
            for value in data.values():
                features_box.append(value)
            if len(set(features_box))==1:
                print("No features are selected!")
                return {}
            else:
                return data
        return None
    except Exception as e:
        print(e)
    return None


def get_rest_cu_rate(job:str,step:str,layer:str,thickness:int,cu_thickness:int = 0,consider_rout:bool = False)->float:
    try:
        resolution_define = 1000
        ret = BASE.get_rest_cu_rate(job,step,layer,resolution_define,thickness,cu_thickness,consider_rout)
        cu_t = json.loads(ret)['result']
        data = float(cu_t.split('/')[1])/100
        return data
    except Exception as e:
        print(e)
        return -1
       
def get_opened_jobs()->list:
    try:
        ret= BASE.get_opened_jobs()
        data= json.loads(ret)
        if 'paras' in data:
            return data['paras']
        else:
            return []
    except Exception as e:
        print(repr(e))
        return None

#获取选中feature的坐标,symbolname,极性, 角度, 是否镜像
def get_selected_features_infos(job:str, step:str, layer:str)->list:
    try:
        ret = BASE.get_selected_feature_infos(job, step, layer)
        data = json.loads(ret)
        featureinfos = []
        if data['paras'] != False:
            return data['paras']
    except Exception as e:
        print(e)
    return None

def get_selected_features_count(job:str, step:str, layer:str = '')->int:
    try:
        if layer != '':
            count_sum=0
            features_count = get_selected_features_infos(job,step,layer)
            if features_count!=None:
                count_sum = len(features_count)
            else:
                count_sum = 0
            return count_sum
        else:
            sum = 0
            layers = get_layers(job)
            for i in layers:
                feature_count = get_selected_features_infos(job,step,i)
                if feature_count !=None:
                    count = len(feature_count)
                else:
                    count = 0
                sum = sum+count
            return sum
    except Exception as e:
        print(e)
    return None

#获取当前状态下筛选器的筛选状态
def get_select_param()->dict:
    try:
        featuretype_list= ['positive','negative','text','surface','arc','line','pad']
        ret= BASE.get_select_param()
        data = json.loads(ret)
        if data['paras']!=False:
            infos= data['paras']['param']
            featuretypes= infos['featuretypes']
            result= BASE.Dec2Bin(featuretypes)
            if len(result)!=7 and featuretypes>32:
                result.reverse()
                result_new= result
                result_new.append(0)
                result_new.reverse()
            else:
                result_new=result
            bool_lst=[]
            for value in result_new:
                if value==1:
                    bool_lst.append(True)
                else:
                    bool_lst.append(False)
            new_lst = dict(zip(featuretype_list, bool_lst))
            infos['featuretypes']=new_lst
            return infos
    except Exception as e:
        print(repr(e))
    return None

def get_system_attr_defines()->list:
    try:
        ret = BASE.get_system_attr_defines()
        data = json.loads(ret)
        if data['paras'] != False:
            return data['paras']
    except Exception as e:
        print(e)
    return None

def get_user_attr_defines()->list:
    try:
        ret = BASE.get_user_attr_defines()
        data = json.loads(ret)
        if data['paras'] != False:
            return data['paras']
    except Exception as e:
        print(e)
    return None

def get_powerground_layers(job:str)->list:
    try:
        ret = BASE.get_graphic(job)
        data = json.loads(ret)
        power_ground_list = []
        layer_info = data['paras']['info']
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'power_ground':
                power_ground_list.append(layer_info[i]['name'])
        if len(power_ground_list)<1:
            print("can't find power_ground-layers!")
            return []
        return power_ground_list
    except Exception as e:
        print(e)
    return None

def get_layer_info(job:str,context:str,type:list)->list:
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        layer_list =[]
        for i in range(0,len(layer_infos)):
            for j in range(len(type)):
                if layer_infos[i]['context'] ==context and layer_infos[i]['type']==type[j]:
                    layer_dict = {}
                    layer_dict['name'] = layer_infos[i]['name']
                    layer_dict['context'] = layer_infos[i]['context']
                    layer_dict['type'] = layer_infos[i]['type']
                    layer_dict['start_name'] = layer_infos[i]['start_name']
                    layer_dict['end_name'] = layer_infos[i]['end_name']
                    layer_dict['polarity'] = layer_infos[i]['polarity']
                    layer_list.append(layer_dict)
        return layer_list
    except Exception as e:
        print(e)
    return []

def get_sr_step_info(job:str,step:str)->list:
    try:
        ret = BASE.get_step_repeat(job,step)
        data = json.loads(ret)
        step_info = data['result']
        step_list = []
        for i in range(0,len(step_info)):
            step_dict = {}
            name= step_info[i]['NAME'].lower()
            step_dict['NAME'] = name
            step_dict['X'] = step_info[i]['X']
            step_dict['Y'] = step_info[i]['Y']
            step_dict['DX'] = step_info[i]['DX']
            step_dict['DY'] = step_info[i]['DY']
            step_dict['NX'] = step_info[i]['NX']
            step_dict['NY'] = step_info[i]['NY']
            step_dict['ANGLE'] = step_info[i]['ANGLE']
            step_dict['MIRROR'] = step_info[i]['MIRROR']
            step_list.append(step_dict)
        for n in step_list:
            stepname = n['NAME']
            angle = n['ANGLE']
            mirror = n['MIRROR']
            dx = n['DX']
            dy = n['DY']
            nx = n['NX']
            ny = n['NY']
            sx = n['X']
            sy = n['Y']
            point = get_datum_point(job,stepname)
            box = get_profile_box(job,stepname)
            x_datum = point['x_datum']
            y_datum = point['y_datum']   
            xMax = box['xmax']
            xMin = box['xmin']
            yMax = box['ymax']
            yMin = box['ymin']          
            delta_x = sx - x_datum
            delta_y = sy - y_datum          #子step在panel中的相对位置
            Minx,Miny = BASE.Srotate(angle,xMin,yMin,x_datum,y_datum)
            Maxx,Maxy = BASE.Srotate(angle,xMax,yMax,x_datum,y_datum)
            maxx = Maxx+delta_x
            maxy = Maxy+delta_y
            minx = Minx+delta_x
            miny = Miny+delta_y             
            if mirror == True:
                minx,miny = BASE.mirror_y(minx,miny,sx)
                maxx,maxy = BASE.mirror_y(maxx,maxy,sx)       #子step的box坐标先旋转后平移镜像
            Max_x = max([maxx,minx])
            Max_y = max([maxy,miny])
            Min_x = min([maxx,minx])
            Min_y = min([maxy,miny])
            max_x = Max_x+dx*(nx-1)
            max_y = Max_y+dy*(ny-1)         #根据nx、ny阵列获得整体box坐标
            n['xmin'] = Min_x
            n['ymin'] = Min_y
            n['xmax'] = max_x
            n['ymax'] = max_y
        return step_list
    except Exception as e:
        print(e)
    return []

def get_sub_steps_name(job:str,step:str)->list:
    try:
        ret = BASE.get_all_step_repeat_steps(job,step)
        data = json.loads(ret)
        step_list =data['steps']
        if step_list == None:
            return []
        return step_list
    except Exception as e:
        print(e)
    return []        

def get_layer_information(job:str)->list:
    try:
        _ret = BASE.get_matrix(job)
        data = json.loads(_ret)
        ret = []
        ret = data['paras']['info']
        signal_list = []
        for j in range(0,len(ret)):
            if ret[j]['context'] == 'board' and ret[j]['type'] == 'signal' or ret[j]['type'] == 'power_ground':
                signal_list.append(j)  
        b = len(signal_list)
        if signal_list != []:
            if b == 1:
                begin = min(signal_list)
                end = max(signal_list)
                ret[signal_list[0]]['side'] = 'none'
                ret[signal_list[0]]['foil_side'] = 'none'
                b_list = []
            elif b == 2:
                begin = min(signal_list)
                end = max(signal_list)
                b_list = []
            else:
                b_list = signal_list[1:(b-1)]
                begin = min(b_list)
                end = max(b_list)
            for i in range(0,len(ret)):
                if ret[i]['context'] == 'misc':
                    ret[i]['side'] = 'none'
                    ret[i]['foil_side'] = 'none'
                elif ret[i]['context'] == 'board' and ret[i]['type'] != 'signal' and ret[i]['type'] != 'power_ground':
                    if i < begin:
                        if ret[i]['type'] == 'silk_screen' or ret[i]['type'] == 'solder_mask' or ret[i]['type'] == 'solder_paste':
                            ret[i]['side'] = 'top'
                        else:
                            ret[i]['side'] = 'none'
                    elif i > end:
                        if ret[i]['type'] == 'silk_screen' or ret[i]['type'] == 'solder_mask' or ret[i]['type'] == 'solder_paste':
                            ret[i]['side'] = 'bottom'
                        else:
                            ret[i]['side'] = 'none' 
                    ret[i]['foil_side'] = 'none'
            if b != 1:
                ret[signal_list[0]]['side'] = 'top'
                ret[signal_list[0]]['foil_side'] = 'top'
                ret[signal_list[-1]]['side'] = 'bottom'
                ret[signal_list[-1]]['foil_side'] = 'bottom'
                if b_list != []:
                    if len(b_list) % 2  == 0:
                        for m in range(begin,end,2):
                            ret[m]['side'] = 'inner'
                            ret[m]['foil_side'] = 'top'
                            m += 1
                            ret[m]['side'] = 'inner'
                            ret[m]['foil_side'] = 'bottom'
                    else:
                        for n in range(begin,end,2):
                            ret[n]['side'] = 'inner'
                            ret[n]['foil_side'] = 'top'
                            n += 1
                            ret[n]['side'] = 'inner'
                            ret[n]['foil_side'] = 'bottom'  
                        ret[end]['side'] = 'inner'
                        ret[end]['foil_side'] = 'top'
        else:
            for t in ret:
                t['side'] = 'none'
                t['foil_side'] = 'none'
        return ret
    except Exception as e:
        print(e)
    return []

def get_all_selected_features_count(job:str, step:str)->int:
    try:
        sum = 0
        layers = get_layers(job)
        feature_list = []
        feature_dict = {}
        for i in layers:
            layer = i
            ret = has_selected_features(job,step,layer)
            if ret ==True:
                count = get_selected_features_count(job,step,layer)
                sum = sum+count
            else:
                count = 0
            # feature_dict = {}
            feature_dict[layer] = count
        feature_list.append(feature_dict)
        feature_list.append(sum)
        return feature_list
    except Exception as e:
        print(e)
    return None

def get_drill_info(job:str, step:str, layer:str,combine_slot:bool=False)->list:
    try:
        layer_info = get_layer_information(job)
        for i in range(0,len(layer_info)):
            if layer_info[i]['name']==layer and layer_info[i]['type'] =='drill':
                data = BASE.get_drill_info(job, step, layer)
                data = json.loads(data)['paras']['vecDrillTools']
                info = json.loads(BASE.set_drill_info(job,step,layer,data))['status']
                if info == 'true':
                    _ret = BASE.auto_get_drill_info(job,step,layer)
                    data = json.loads(_ret)['result']['data']['drills']
                    for i in data:
                        if i['dType'] == 'TEXT':
                            i['isText'] = True
                        else:
                            i['isText'] = False
                        i['isNibble'] = False
                        i['iToolSize'] = i['iHoleSize']
        if combine_slot == True:
            ab = []
            for e in range(0,len(data)):
                if e in ab:
                    pass
                else:
                    if data[e]['vLocations_slots'] != []:
                        type = data[e]['dType']
                        hole = data[e]['iHoleSize']
                        data[e]['iSlotLenth'] = (data[e]['iCount'])*(data[e]['iSlotLenth'])
                        for t in range(e+1, len(data)):
                            if data[t]['vLocations_slots'] != [] and data[t]['dType'] == type and data[t]['iHoleSize'] == hole:
                                locations = data[e]['vLocations_slots']
                                number = data[t]['iCount']
                                length = number*(data[t]['iSlotLenth'])
                                icount = (data[e]['iCount'])+number
                                locations.extend(data[t]['vLocations_slots'])
                                slotlenth = (data[e]['iSlotLenth'])+length
                                data[e]['iCount'] = icount
                                data[e]['iSlotLenth'] = slotlenth
                                data[e]['vLocations_slots'] = locations
                                ab.append(t)
            data = [n for i, n in enumerate(data) if i not in ab]
            index = 1
            for i in data:
                i['iToolIdx'] = index
                index = index+1
        return data
    except Exception as e:
        print(e)
    return []

def has_profile(job:str, step:str)->bool:
    try:
        _ret = BASE.has_profile(job, step)
        ret = json.loads(_ret)['result']
        return ret
    except Exception as e:
        print(e)
    return False

def get_all_symbol_info(job:str, step:str, layer:str,sr:bool = False)->dict:
    try:
        BASE.load_layer(job, step, layer)
        if sr == False:
            _ret = BASE.get_all_features_report(job,step,layer)
            ret = json.loads(_ret)['paras']
        else:
            _ret = BASE.get_all_features_report_flattern(job,step,layer)
            ret = json.loads(_ret)['paras']
        return ret
    except Exception as e:
        print(e)
    return {}

def get_layer_report(job:str, layer:str)->dict:
    try:
        aa =BASE.get_matrix(job)
        ret = json.loads(aa)['paras']['info']
        signal_list = []
        solder_list = []
        silk_list = []
        j = 0
        for j in range(0,len(ret)):
            if ret[j]['context'] =='board'and ret[j]['type'] == 'signal':
                signal_list.append(ret[j]['row'])
            elif ret[j]['context'] =='board'and ret[j]['type'] == 'solder_mask':
                solder_list.append(ret[j]['row'])
            elif ret[j]['context'] =='board'and ret[j]['type'] == 'silk_screen':
                silk_list.append(ret[j]['row'])
        b = len(signal_list)
        b_list = signal_list[1:(b-1)]
        for i in range(0,len(ret)):
            if ret[i]['name'] == layer:
                index = ret[i]['row']
                layer_dict = {}
                layer_dict['context'] = ret[i]['context']
                layer_dict['type'] = ret[i]['type']
                if index == signal_list[0]:
                    layer_dict['location'] = "outer_top"
                elif index == signal_list[-1]:
                    layer_dict['location'] = "outer_bottom"
                elif (index in b_list):
                    layer_dict['location'] = 'inner'
                elif (index in solder_list):
                    l1 = abs(signal_list[0]-index) 
                    l2 = abs(signal_list[-1]-index) 
                    if l1<l2:
                        layer_dict['location'] = 'top'
                    elif l1>l2:
                        layer_dict['location'] = 'bottom'
                elif (index in silk_list):
                    l1 = abs(signal_list[0]-index)
                    l2 = abs(signal_list[-1]-index)
                    if l1<l2:
                        layer_dict['location'] = 'top'
                    elif l1>l2:
                        layer_dict['location'] = 'bottom'
                else:
                    layer_dict['location'] = 'none'
        return layer_dict
    except Exception as e:
        print(e)
    return {}

def get_outerlayer_closest_soldermask(job:str, layer:str)->str:
    try:
        ret  = BASE.get_matrix(job)
        ret = json.loads(ret)['paras']['info']
        signal_list = []
        for i in range(0,len(ret)):
            if ret[i]['name'] ==layer and ret[i]['type'] == 'solder_mask' and ret[i]['context'] == 'board':
                index = ret[i]['row']
                break
        for n in range(0,len(ret)):
            if ret[n]['context'] =='board'and ret[n]['type'] == 'signal':
                signal_list.append(ret[n]['row'])
        l1 = abs(signal_list[0]-index)
        l2 = abs(signal_list[-1]-index)
        if l1<l2:
            top = signal_list[0]
        elif l1>l2:
            top = signal_list[-1]
        for m in range(0,len(ret)):
            if ret[m]['row'] == top:
                name = ret[m]['name']
                break
        return name
    except Exception as e:
        print(e)
    return ''

def get_soldermask_closest_signal(job:str, layer:str)->str:
    try:
        ret  = BASE.get_matrix(job)
        ret = json.loads(ret)['paras']['info']
        silk_list = []
        for i in range(0,len(ret)):
            if ret[i]['name'] ==layer and ret[i]['context'] == 'board' and ret[i]['type'] == 'signal':
                index = ret[i]['row']
                break
        for n in range(0,len(ret)):
            if ret[n]['context'] =='board'and ret[n]['type'] == 'solder_mask':
                silk_dict = {}
                silk_dict['row'] = ret[n]['row']
                silk_dict['name'] = ret[n]['name']
                silk_list.append(silk_dict)
        datum = []
        b = []
        for m in silk_list:
            d = abs(m['row']-index)
            b.append(d)
            silk = {}
            silk['name'] = m['name']
            silk['delta'] = d
            datum.append(silk)
        a = min(b)
        for o in datum:
            delta = o['delta']
            if a == delta:
                layername = o['name']
        return layername
    except Exception as e:
        print(e)
    return ''

def get_drill_cross(job:str, layer:str)->list:
    try:
        ret = BASE.get_matrix(job)
        ret = json.loads(ret)['paras']['info']
        layer_list = []
        drill_list=[]
        for i in range(0,len(ret)):
            if ret[i]['name'] ==layer and ret[i]['type'] == 'drill' and ret[i]['context'] == 'board':
                start = ret[i]['start_name']
                end = ret[i]['end_name']
                break
        for n in range(0,len(ret)):
            if ret[n]['name'] == start or ret[n]['name'] == end:
                drill_list.append(ret[n]['row'])
                name_list = list(range(math.ceil(drill_list[0]), math.floor(drill_list[-1]) + 1))
        for m in range(0,len(ret)):
            b = ret[m]['row']
            if b in name_list:
                if ret[m]['type'] == 'signal' or ret[m]['type'] == 'power_ground':
                    layer_dict = {}
                    layer_dict['name'] = ret[m]['name']
                    layer_dict['index'] = ret[m]['row']
                    layer_list.append(layer_dict)
        return layer_list
    except Exception as e:
        print(e)
    return []

def get_rout_cross(job:str, layer:str)->list:
    try:
        ret = BASE.get_matrix(job)
        ret = json.loads(ret)['paras']['info']
        layer_list = []
        rout_list=[]
        for i in range(0,len(ret)):
            if ret[i]['name'] ==layer and ret[i]['context'] == 'board' and ret[i]['type'] == 'rout':
                start = ret[i]['start_name']
                end = ret[i]['end_name']
                break
        for n in range(0,len(ret)):
            if ret[n]['name'] == start or ret[n]['name'] == end:
                rout_list.append(ret[n]['row'])
                name_list = list(range(math.ceil(rout_list[0]), math.floor(rout_list[-1]) + 1))
        for m in range(0,len(ret)):
            b = ret[m]['row']
            if b in name_list:
                if ret[m]['type'] == 'signal' or ret[m]['type'] == 'power_ground':
                    layer_dict = {}
                    layer_dict['name'] = ret[m]['name']
                    layer_dict['index'] = ret[m]['row']
                    layer_list.append(layer_dict)
        return layer_list
    except Exception as e:
        print(e)
    return []

def get_datum_point(job:str, step:str)->dict:
    try:
        ret = check_matrix_info(job,step,[])
        if ret == True:
            data = BASE.get_step_header_infos(job,step)
            data = json.loads(data)
            point_dict = {}
            point_dict['x_datum'] = data['x_datum']
            point_dict['y_datum'] = data['y_datum']
            return point_dict
        else:
            return None
    except Exception as e:
        print(e)
    return None

def get_sub_step_info(job:str, step:str)->list:
    try:
        data = get_sr_step_info(job,step)
        datum_point = []
        # 获取panel中所有pcs、set的基准点坐标，旋转角度、是否镜像
        for s in data:
            nx = s['NX']
            ny = s['NY']
            dx = s['DX']
            dy = s['DY']
            angle = s['ANGLE']
            mirror = s['MIRROR']
            step1 = s['NAME']
            sx = s['X']
            sy = s['Y']
            for n in range(0,nx):
                for m in range(0,ny):
                    point = {}
                    point['X'] = sx
                    point['Y'] = sy
                    point['angle'] = angle
                    point['name'] = step1
                    point['mirror'] = mirror
                    datum_point.append(point)
                    sy = sy+dy
                sx = sx+dx
                sy = sy-(dy*ny)
            info1 = get_sr_step_info(job,step1)
            if info1 != []:
                for b in info1:
                    for i in range(0,1):
                        step2 = b['NAME']
                        nx1 = b['NX']
                        ny1 = b['NY']
                        sx1 = b['X']
                        sy1 = b['Y']
                        dx1 = b['DX']
                        dy1 = b['DY']
                        angle1 = b['ANGLE']
                        mirror1 = b['MIRROR']
                        if mirror == True and mirror1 == True:
                            mir = False
                        elif mirror == False and mirror1 == False:
                            mir = False
                        else:
                            mir = True
                        ang = angle+angle1
                        if ang >= 360:
                            ang = ang-360
                        datum_point1 = []
                        for n in range(0,nx1):
                            for m in range(0,ny1):
                                point = {}
                                point['X'] = sx1
                                point['Y'] = sy1
                                point['angle'] = ang
                                point['name'] = step2
                                point['mirror'] = mir
                                datum_point1.append(point)
                                sy1 = sy1+dy1
                            sx1 = sx1+dx1
                            sy1 = sy1-(dy1*ny1)
                    point = get_datum_point(job,step1)
                    pointx = point['x_datum']
                    pointy = point['y_datum']
                    delta_x = (s['X'])-pointx
                    delta_y = (s['Y'])-pointy
                    if angle != 0:
                        for p in datum_point1:
                            x = p['X']
                            y = p['Y']
                            x,y = BASE.Srotate(angle,x,y,pointx,pointy)
                            p['X'] = x
                            p['Y'] = y
                    if delta_x != 0 or delta_y != 0:
                        for n in datum_point1:
                            x = n['X']
                            y = n['Y']
                            x,y = BASE.Move(x,y,delta_x,delta_y)     
                            n['X'] = x
                            n['Y'] = y   
                    if mirror == True:
                        for p in datum_point1:
                            x = p['X']
                            y = p['Y']
                            p['X'] = -x
                            p['Y'] = y
                    datum_point2 = []
                    for l in datum_point1:
                        ex = l['X']
                        ey = l['Y']
                        for n in range(0,nx):
                            for m in range(0,ny):
                                point = {}
                                point['X'] = ex
                                point['Y'] = ey
                                point['angle'] = ang
                                point['name'] = step2
                                point['mirror'] = mir
                                datum_point2.append(point)
                                ey = ey+dy
                            ex = ex+dx
                            ey = ey-(dy*ny)
                    datum_point = datum_point+datum_point2
        panel_box = []
        for t in datum_point:
            stepname = t['name'] 
            mir = t['mirror']
            px = t['X']
            py = t['Y']     #edit在panel中基准点的坐标
            an = t['angle']    #edit在panel中的旋转角度
            datum = get_datum_point(job,stepname)             
            p_x = datum['x_datum']
            p_y = datum['y_datum']                 #edit本身的基准点坐标
            set_box = get_profile_box(job,stepname)
            set_minx = set_box['xmin']
            set_miny = set_box['ymin']
            set_maxx = set_box['xmax']
            set_maxy = set_box['ymax']               #edit的profile_box
            delta_x = px-p_x
            delta_y = py-p_y
            minx = set_minx
            miny = set_miny
            maxx = set_maxx
            maxy = set_maxy
            if an != 0:
                minx,miny = BASE.Srotate(an,set_minx,set_miny,p_x,p_y)
                maxx,maxy = BASE.Srotate(an,set_maxx,set_maxy,p_x,p_y)
            if delta_x != 0 or delta_y != 0:
                minx,miny = BASE.Move(minx,miny,delta_x,delta_y)
                maxx,maxy = BASE.Move(maxx,maxy,delta_x,delta_y)
            if mir == True:
                minx,miny = BASE.mirror_y(minx,miny,px)
                maxx,maxy = BASE.mirror_y(maxx,maxy,px)
            x_list = [minx,maxx]
            y_list = [miny,maxy]
            xmin = min(x_list)
            ymin = min(y_list)
            xmax = max(x_list)
            ymax = max(y_list)
            # px = BASE.nm2inch(px)
            # py = BASE.nm2inch(py)
            # xmin = BASE.nm2inch(xmin)
            # ymin = BASE.nm2inch(ymin)
            # xmax = BASE.nm2inch(xmax)
            # ymax = BASE.nm2inch(ymax)
            box_dict = {}
            box_dict['epREPEATstep'] = stepname
            box_dict['epREPEATxa'] = px
            box_dict['epREPEATya'] = py
            box_dict['epREPEATangle'] = an
            box_dict['epREPEATmirror'] = mir
            box_dict['epREPEATxmin'] = xmin
            box_dict['epREPEATymin'] = ymin
            box_dict['epREPEATxmax'] = xmax
            box_dict['epREPEATymax'] = ymax
            panel_box.append(box_dict)
        return panel_box
    except Exception as e:
        print(e)
    return []

def get_selected_symbol_info(job:str, step:str, layer:str)->dict:
    try:
        ret = BASE.get_selected_features_report(job, step, layer)
        ret = json.loads(ret)['paras']
        return ret
    except Exception as e:
        print(e)
    return {}

def get_all_features_info(job:str ,step:str, layer:str)->list:
    try:
        ret = BASE.get_all_feature_info(job,step,layer,127)
        ret = json.loads(ret)['paras']
        return ret
    except Exception as e:
        print(e)
    return []

def get_user_symbol_box(job:str, user_symbol_name:str)->dict:
    try:
        data = BASE.get_usersymbol_box(job,user_symbol_name)
        ret = json.loads(data)['paras']
        deltax = ret['xmax']-ret['xmin']
        deltay = ret['ymax']-ret['ymin']
        ret['height'] = deltay
        ret['width'] = deltax
        return ret
    except Exception as e:
        print(e)
    return []

def get_fill_param()->dict:
    try:
        _ret = BASE.get_fill_param()
        ret = json.loads(_ret)['paras']
        return ret
    except Exception as e:
        print(e)
        return {}

def get_layer_attributes(job:str, step:str,layer:str)->dict:
    try:
        _ret = BASE.get_layer_attributes(job,step,layer)
        ret = json.loads(_ret)['paras']
        return ret
    except Exception as e:
        print(e)
        return []

def get_step_attributes(job:str, step:str)->dict:
    try:
        _ret = BASE.get_step_attributes(job,step)
        ret = json.loads(_ret)['paras']
        return ret
    except Exception as e:
        print(e)
        return {}

def check_rout_output(job:str, step:str, layer:str)->dict:
    try:
        layersinfo = get_layer_information(job)
        for info in layersinfo:
            if info['name'] == layer and info['type'] == 'rout' and info['context'] == 'board':
                _ret = BASE.check_rout_output(job,step,layer)
                ret = json.loads(_ret)['paras']
                return ret
    except Exception as e:
        print(e)
    return {}

def identify_symbol(symbolname:str)->bool:
    try:
        _ret = BASE.identify_symbol(symbolname)
        ret = json.loads(_ret)['result']
        return ret
    except Exception as e:
        print(e)
    return False


def get_exposed_area(job:str, step:str, layer_param:dict, 
                     affect_drill_layers:list, resolution_define:int, thickness:int, cu_thickness:float,
                     multi_mask:bool, holes_slots:bool, include_soldermask:bool, include_drill:bool, 
                     include_edges:bool, pth_without_pad:bool, mode:int,consider_rout:bool)->float:
    try:
        if mode == 0:
            or_and = 'and'
        elif mode == 1:
            or_and = 'or'
        number = len(layer_param.keys())
        result = {}
        va = 0
        for param in layer_param.keys():
            mask_layers = layer_param[param]
            if len(mask_layers) == 1:
                mask_layername = mask_layers[0]
                mask_layers = []
            else:
                mask_layername = ''
            ret = BASE.get_exposed_area(job, step, param, resolution_define, thickness, cu_thickness, 
                            consider_rout, mask_layername, mask_layers, affect_drill_layers, 
                            number, multi_mask, holes_slots, include_soldermask, include_drill, 
                            include_edges, pth_without_pad, or_and)
            ret = json.loads(ret)['result']
            data = float(ret.split('/')[0])
            data = round((data*645.16),4)
            result[param] = data
            va += data
        result['sum'] = va
        return result
    except Exception as e:
        print(e)
        return {}

def get_cu_area(job:str,step:str,layer:str,cu_thickness=0,consider_rout=False)->float:
    try:
        ret = BASE.get_rest_cu_rate(job,step,layer,25400,0,cu_thickness,consider_rout)
        ret = json.loads(ret)['result']
        data = float(ret.split('/')[0])
        data = round((data*645.16),4)
        return data
    except Exception as e:
        print(e)
        return 0


def get_selection()->dict:
    try:
        ret = BASE.get_selection()
        data = json.loads(ret)['paras']
        return data
    except Exception as e:
        print(e)
        return {}

def get_job_attributes(job:str)->dict:
    try:
        data = BASE.get_job_attributes(job)
        ret = json.loads(data)['paras']
        return ret
    except Exception as e:
        print(e)
        return {}

def get_usersymbol_attributes(job:str,usersymbol:str)->dict:
    try:
        ret = BASE.get_usersymbol_attributes(job,usersymbol)
        data = json.loads(ret)['paras']
        return data
    except Exception as e:
        print(e)
        return {}

def change_symbolname_unit(oldstr:str, unit:int)->str:
    try:
        data = BASE.set_symbol_ui_data(oldstr, unit)
        info = json.loads(data)['paras']['result']
        if info == True:
            ret = json.loads(data)['paras']['new_str']
        else:
            ret = ''
        return ret
    except Exception as e:
        print(e)
    return ''

def get_origin_point(job:str, step:str)->dict:
    try:
        check = check_matrix_info(job,step,[])
        if check == True:
            data = BASE.get_step_header_infos(job,step)
            data = json.loads(data)
            point_dict = {}
            point_dict['x_origin'] = data['x_origin']
            point_dict['y_origin'] = data['y_origin']
            return point_dict
        else:
            return {}
    except Exception as e:
        print(e)
    return {}
















    
    