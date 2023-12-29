import os, sys, json
from epkernel import epcam, BASE
from epkernel.Action import Information,Selection

def save_eps(job:str, path:str)->bool:
    try:
        filename = os.path.basename(path)
        suffix = os.path.splitext(filename)[1]
        if suffix == '.eps':
            BASE.setJobParameter(job,job)
            BASE.save_eps(job,path)
            return True
        else:
            pass
    except Exception as e:
        print(e)
    return False


def save_gerber( job:str, step:str, layer:str, filename:str,  resize:int=0, angle:float=0, 
                scalingX:float=1, scalingY:float=1, mirror:bool=False, rotate:bool=False, 
                scale:bool=False, cw:bool=False,  mirrorpointX:int=0, mirrorpointY:int=0, 
                rotatepointX:int=0, rotatepointY:int=0, scalepointX:int=0, scalepointY:int=0, 
                mirrorX:bool = False, mirrorY:bool = False, numberFormatL:int=2, 
                numberFormatR:int=6, zeros:int=0, unit:int=0)->bool:
    try:
        _type = 0
        gdsdbu = 0.01
        profiletop = False
        cutprofile = True
        isReverse = False
        cut_polygon = []
        if scalingX == 0:
            scalingX == 1
        if scalingY == 0:
            scalingY == 1
        if mirrorX == True and mirrorY ==True:
            mirrordirection = 'XY'
        elif mirrorX==True and mirrorY ==False:
            mirrordirection = 'Y'
        elif mirrorX==False and mirrorY ==True:
            mirrordirection = 'X'
        else:
            mirrordirection = 'NO'
        _ret = BASE.layer_export(job, step, layer, _type, filename, gdsdbu, resize, angle, scalingX, scalingY, isReverse,
                    mirror, rotate, scale, profiletop, cw, cutprofile, mirrorpointX, mirrorpointY, rotatepointX,
                    rotatepointY, scalepointX, scalepointY, mirrordirection, cut_polygon,numberFormatL,numberFormatR,
                    zeros,unit)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
    return False

def save_excellon2(job:str, step:str, layer:str, path:str, number_format_l:int=2, 
                   number_format_r:int=6, zeroes:int=2, unit:int=0, tool_unit:int=1, 
                   x_scale:float=1, y_scale:float=1, x_anchor:int=0, y_anchor:int=0,canned_text_mode:int=0)->bool:
    try:
        isMetric = unit
        layer_info = Information.get_layer_information(job)
        for i in range(0,len(layer_info)):
            if layer_info[i]['name']==layer and layer_info[i]['context'] == 'board' and layer_info[i]['type'] =='drill':
                BASE.drill2file(job, step, layer,path,isMetric,number_format_l,number_format_r,
                    zeroes,unit,tool_unit,x_scale,y_scale,x_anchor,y_anchor, '',[],canned_text_mode)
                return True
    except Exception as e:
        print(e)
    return False


def save_rout(job:str, step:str, layer:str, path:str, number_format_l:int=2,
              number_format_r:int=6,zeroes:int=2,unit:int=0,tool_unit:int=1,x_scale:float=1,
              y_scale:float=1,x_anchor:int=0,y_anchor:int=0, break_arcs:bool = False)->dict:
    try:
        check = BASE.check_rout_output(job,step,layer)
        info = json.loads(check)['paras']
        errorResult1 = info['checkResult1']['errorResult']
        errorResult2 = info['checkResult2']['errorResult']
        errorResult3 = info['checkResult3']['errorResult']
        error = {}
        for i in errorResult1:
            featureinfo = i['featureInfo']
            if featureinfo != []:
                infos = featureinfo[:3]
                infor = []
                for m in infos:
                    infor.append(m['feature_index'])
                error['featureInfo'] = infor
                error['step'] = i['step']
                error['errorType'] = 0
                error['result'] = False
                break
        if error == {}:
            for j in errorResult2:
                featureinfo = j['featureInfo']
                if featureinfo != []:
                    infos = featureinfo[:3]
                    infor = []
                    for m in infos:
                        infor.append(m['feature_index'])
                    error['featureInfo'] = infor
                    error['step'] = j['step']
                    error['errorType'] = 1
                    error['result'] = False
                    break
        if error == {}:
            for n in errorResult3:
                featureinfo = n['featureInfo']
                if featureinfo != []:
                    infos = featureinfo[:3]
                    infor = []
                    for m in infos:
                        infor.append(m['feature_index'])
                    error['featureInfo'] = infor
                    error['step'] = n['step']
                    error['errorType'] = 2
                    error['result'] = False
                    break
        if error == {}:
            ret = BASE.rout2file(job, step, layer,path,number_format_l,number_format_r,zeroes,unit,tool_unit,x_scale,y_scale,x_anchor,y_anchor, 0, 0, 0, 0, 0, break_arcs)
            if 'status' in ret:
                ret = {'result':False,'errorType':3}
            else:
                ret = json.loads(ret)['paras']
                if ret == True:
                    ret = {'result':True}
                else:
                    ret = {'result':False,'errorType':3}
            return ret
        else:
            return error
    except Exception as e:
        print(e)
    return {}


def save_job(job:str,path:str)->bool:
    try:
        layers = Information.get_layers(job)
        steps = Information.get_steps(job)
        for step in steps:
            for layer in layers:
                BASE.load_layer(job,step,layer)
        BASE.save_job_as(job,path)
        return True
    except Exception as e:
        print(e)
    return False


def save_dxf(job:str,step:str,layers:list,savePath:str)->bool:
    try:
        _ret = BASE.dxf2file(job,step,layers,savePath)
        ret = json.loads(_ret)['paras']['result']
        return ret
    except Exception as e:
        print(e)
    return False

def save_pdf(job:str, step:str, layers:list, layercolors:list, outputpath:str, overlap:bool)->bool:
    try:
        (outputpath,pdfname) = os.path.split(outputpath)
        layer_sum = len(layers)
        colors_sum = len(layercolors)
        b = True
        if layer_sum != colors_sum:
            b = False
        else:
            for i in range(0,colors_sum):
                color = layercolors[i]
                if len(color) !=4:
                    b = False
                    break
        if b == True:
            _ret = BASE.output_pdf(job,step,layers,layercolors,outputpath,pdfname,overlap)
            ret = json.loads(_ret)['status']
            if ret == 'true':
                ret = True
            else:
                ret = False
            return ret
    except Exception as e:
        print(e)
    return False

def save_png(job:str, step:str, layers:list, xmin:int, ymin:int, xmax:int, ymax:int, picpath:str, backcolor:list, layercolors:list)->bool:
    try:
        (picpath,picname) = os.path.split(picpath)
        layer_sum = len(layers)
        color_sum = len(layercolors)
        back_sum = len(backcolor)
        b = True
        if  back_sum != 4:
            b = False
        else:
            if layer_sum != color_sum:
                b = False
            else:
                for i in range(0,color_sum):
                    color = layercolors[i]
                    if len(color) != 4:
                        b = False
                        break
        if b == True:
            _ret = BASE.save_png(job,step,layers,xmin,ymin,xmax,ymax,picpath,picname,backcolor,layercolors)
            ret = json.loads(_ret)['status']
            if ret == 'true':
                ret = True
            else:
                ret = False
            return ret
    except Exception as e:
        print(e)
    return False

# 输出文件
def save_drill(data:list,filename:str, unit:bool=True, tool_unit:bool=False, 
               number_format_l:int=2, number_format_r:int=6, zeroes:int=2, 
               x_scale:float=1, y_scale:float=1, x_anchor:int=0, y_anchor:int=0,combined:bool=False,
               accuracy:int = 3,job:str = '',panel_step :str= '',layer:str='',tail_step:str = '',
               mode:int = 0, distance :int= 0,distance_t:int=0,min_size:int=0,
               max_size:int=0, min_hits:int=0, x_scale_anchor:int=0, y_scale_anchor:int=0, x_origin:int=0, 
               y_origin:int=0, showG:bool=False, desc:list=[])->bool:
  try:
    if combined == True:
        data = BASE.Deduplication(data)         #合刀接口，不合text中的信息
    size_list = []              #添加尾孔时的刀径信息
    toolsize = []               #刀径表的信息
    tool = []                   #不包含dType为TEXT时的刀径列表
    text = []                   #合刀且扩孔时扩孔的信息
    text_dict= []               #dType为text时的整体输出时的信息
    locat_list=[]               #dType为text时的打散输出时的信息
    text_list = []              #dType为text时所有的孔径大小
    reaming = []                #扩孔的iToolSize
    reaming_index = []          #combined、isNibble均为True且扩孔的iToolSize不唯一时记录index
    for i in data:
        if i['dType'] == 'TEXT':        #整理dType为text时的输出信息及刀径列表
            text_dict.clear()
            locat_list.clear()
            text_list.clear()
            ret = BASE.get_specified_text_infos(job,panel_step,layer,'canned_57')
            paras = json.loads(ret)['paras']
            if paras == []:
                infos57 = []
            else:
                infos57 = paras['result']
            ret = BASE.get_specified_text_infos(job,panel_step,layer,'canned_67')
            paras67 = json.loads(ret)['paras']
            if paras67 == []:
                infos67 = []
            else:
                infos67 = paras67['result']
            infos = infos57+infos67
            for variables in infos:
                featureinfo = variables['featureInfo']
                points = variables['points']
                holesize = featureinfo['linewidth']
                if (featureinfo['angle'] == 0 or featureinfo['angle']==270) and (featureinfo['mirror']==False):
                    if(featureinfo['angle']) == 0:
                        title = 'M97'
                        featurex = (BASE.inch2nm(featureinfo['X']))+(holesize/2)
                        featurey = (BASE.inch2nm(featureinfo['Y']))+(holesize/2)
                    elif (featureinfo['angle']) == 270:
                        title = 'M98'
                        featurex = (BASE.inch2nm(featureinfo['X']))-(holesize/2)
                        featurey = (BASE.inch2nm(featureinfo['Y']))+(holesize/2)
                    pointes = {}
                    pointes['X'] = featurex
                    pointes['Y'] = featurey
                    locations = BASE.isPad(pointes, unit, 0, False, number_format_l, number_format_r, zeroes, x_anchor, y_anchor, x_origin, y_origin, x_scale, y_scale, x_scale_anchor, y_scale_anchor)
                    feature_dict = {}
                    feature_dict['text'] = featureinfo['realtext']          # feature的文本信息
                    feature_dict['iHoleSize'] = holesize                    # 刀径
                    feature_dict['title'] = title                           # 对应角度的机器码
                    feature_dict['location'] = locations                    # feature的具体坐标
                    text_dict.append(feature_dict)  
                    text_list.append(holesize)
                else:
                    for point in points:
                        if unit == True:
                            locationx = BASE.nm2inch(point['point']['ix'])
                            locationy = BASE.nm2inch(point['point']['iy'])
                        else:
                            locationx = BASE.nm2mm(point['point']['ix'])
                            locationy = BASE.nm2mm(point['point']['iy'])
                        locationx,locationy = BASE.Move(locationx, locationy, x_origin, y_origin,)
                        locationx = BASE.data_processing(locationx,number_format_l,number_format_r,zeroes)
                        locationy = BASE.data_processing(locationy,number_format_l,number_format_r,zeroes)
                        locationdata = 'X'+locationx[0]+locationx[1]+'Y'+locationy[0]+locationy[1]
                        point_dict = {}
                        point_dict['iHoleSize'] = holesize
                        point_dict['point'] = locationdata
                        locat_list.append(point_dict)
                        text_list.append(holesize)
            text_list = [i for n,i in enumerate(text_list) if i not in text_list[:n]]
            size_list = size_list+text_list
            toolsize = toolsize+text_list
        else:           #dType不为text时的刀径列表
            if min_size == 0 and max_size == 0:
                if min_hits == 0 or i['iCount']>min_hits:
                    if i['isNibble'] == False:
                        size_list.append(i['iHoleSize'])
                    elif i['isNibble'] == True:
                        size_list.append(i['iToolSize'])
            elif min_size<i['iHoleSize'] <max_size:
                if min_hits == 0 or i['iCount']>min_hits:
                    if i['isNibble'] == False:
                        size_list.append(i['iHoleSize'])
                    elif i['isNibble'] == True:
                        size_list.append(i['iToolSize'])
            if i['isNibble'] == False:  
                toolsize.append(i['iHoleSize'])
                tool.append(i['iHoleSize'])
            else:           #扩孔时的刀径表
                toolsize.append(i['iToolSize'])
                tool.append(i['iToolSize'])
        
        if combined == True and i['isNibble'] == True and (toolsize.count(i['iToolSize']) != 1):      #添加扩孔并合刀时的坐标信息
            locations = i['vLocations']
            for pad in locations:
                xy = BASE.isPad(pad,unit,0,False,number_format_l, number_format_r, zeroes, x_anchor, y_anchor, x_origin, y_origin, x_scale, y_scale, x_scale_anchor, y_scale_anchor)
                holesize = i['iHoleSize']
                if unit == True:
                    holesize = BASE.nm2inch(holesize)
                else:
                    holesize = BASE.nm2mm(holesize)
                holesize = BASE.data_processing(holesize,number_format_l,number_format_r,zeroes)
                lenth = xy+'G84X'+holesize[0]+holesize[1]
                size_dict = {}
                size_dict['iToolSize'] = i['iToolSize']
                size_dict['lenth'] = lenth
                text.append(size_dict)
            reaming.append(i['iToolSize'])
            reaming_index.append(i['iToolIdx'])
    for t in range(len(data)-1,-1,-1):
        if data[t]['iToolIdx'] in reaming_index:
            data.pop(t)
    if text_list != [] and combined == True:
        for aa in text_list:
            if aa in tool:
                text_list.remove(aa)
    if combined == True:
        sizelist = [i for n,i in enumerate(size_list) if i not in size_list[:n]]
        toolsize = [i for n,i in enumerate(toolsize) if i not in toolsize[:n]]
    else:
        sizelist = size_list
    ret = BASE.add_tail_drill(job,tail_step,layer,0,mode,0,0,0,distance,distance_t,
                        min_size,max_size,min_hits,sizelist)
    if 'true' in ret:               #添加尾孔成功后的尾孔孔径和坐标
        info = Information.get_drill_info(job,tail_step,layer)
        point = Information.get_datum_point(job,tail_step)
        sr = Information.get_sr_step_info(job,panel_step) 
        wk_data = [] 
        for sr_step in sr:
            if sr_step['NAME'] == tail_step:
                X = sr_step['X']
                Y = sr_step['Y']
                angle = sr_step['ANGLE']
                mirror = sr_step['MIRROR']
                for drill in info:
                    for location in drill['vLocations']:
                        delta_x = (X - point['x_datum']) + (x_origin)
                        delta_y = (Y - point['y_datum']) + (y_origin)
                        pad = BASE.isPad(location,unit,angle,mirror,number_format_l,number_format_r,zeroes,point['x_datum'],point['y_datum'],delta_x,delta_y,x_scale,y_scale, x_scale_anchor, y_scale_anchor)
                        locations = {}
                        locations['iHoleSize'] = drill['iHoleSize']
                        locations['data'] = pad
                        wk_data.append(locations)
    else:
        wk_data = []
    file = open(filename, 'w', encoding = 'utf-8')      #指定路径新建文件并打开文件，写入头文件
    file.write('M48'+'\n')
    if desc != []:
        for p in desc:
            file.write(p + '\n')
    else:
        if unit == True:
            file.write('INCH')
        else:
            file.write('METRIC')
        if zeroes == 0:
            file.write(',LZ'+'\n')
        elif zeroes == 1:
            file.write(',TZ'+'\n')
        else:
            file.write('\n')
        file.write(';FILE_FORMAT='+str(number_format_l)+':'+str(number_format_r)+'\n')
    sum = 1
    for n in toolsize:              #输出刀径表
        to = str(sum).rjust(2,'0')
        if tool_unit == True:
            size_mm = BASE.nm2inch(n)
        else:
            size_mm =BASE.nm2mm(n)
        size = BASE.Zero(size_mm,accuracy)
        content = 'T'+to+'C'+size
        file.write(content+'\n')
        sum = sum+1
    file.write('%'+'\n')
    if showG == True:
        file.write('G93')
        if x_origin != 0 or y_origin != 0:
            if unit == True:
                origin_x = BASE.nm2inch(x_origin)
                origin_y = BASE.nm2inch(y_origin)
            else:
                origin_x = BASE.nm2mm(x_origin)
                origin_y = BASE.nm2mm(y_origin)
            orig_x = BASE.data_processing(origin_x, number_format_l, number_format_r, zeroes)
            orig_y = BASE.data_processing(origin_y, number_format_l, number_format_r, zeroes)
            origx = orig_x[0] + orig_x[1]
            lenx = origx.count('0')
            holeformat = number_format_l + number_format_r
            if lenx == holeformat:
                origx = '0'
            origy = orig_y[0] + orig_y[1]
            leny = origy.count('0')
            if leny == holeformat:
                origy = '0'
            orig = 'X' + origx + 'Y' + origy
            file.write(orig + '\n')
        else:
            file.write('X0Y0' + '\n')
    if unit == True:
        x_anchor = BASE.nm2inch(x_anchor)
        y_anchor = BASE.nm2inch(y_anchor)
    else:
        x_anchor = BASE.nm2mm(x_anchor)
        y_anchor = BASE.nm2mm(y_anchor)  
    weikong = []
    number = 1
    featuretext = []
    datapass = []
    for finishsize in toolsize:
        to = str(number).rjust(2,'0')
        part = 'T'+to
        file.write(part+'\n')
        for i in data:                  #输出坐标点信息
            if (i['iHoleSize'] == finishsize) and (i not in datapass):                
                location = i['vLocations']
                vLocations_slots = i['vLocations_slots']
                if (mode == 0 or mode == 1) and (wk_data != []):
                    for wk in wk_data:
                        if (wk['iHoleSize'] == i['iHoleSize'] or wk['iHoleSize'] == i['iToolSize']) and (wk['data'] not in weikong):
                            work = wk['data']
                            file.write(work+'\n')
                            weikong.append(work)
                            break
                if combined == True:
                    for feature in text_dict:
                        if (feature['iHoleSize'] == i['iHoleSize']) and (feature not in featuretext):
                            file.write(feature['title']+','+feature['text']+'\n')
                            file.write(feature['location']+'\n')
                            featuretext.append(feature)
                    for datum in locat_list:
                        if datum['iHoleSize'] == i['iHoleSize']:
                            file.write(datum['point']+'\n')
                    if i['iHoleSize'] in reaming:
                        for part in text:
                            if (part['iToolSize'] == i['iHoleSize']) or (part['iToolSize'] == i['iToolSize']):
                                file.write(part['lenth']+'\n')
                if combined == False and i['dType'] == 'TEXT':
                    for feature in text_dict:
                        if (feature['iHoleSize'] == i['iHoleSize']) and (feature not in featuretext):
                            file.write(feature['title']+','+feature['text']+'\n')
                            file.write(feature['location']+'\n')
                            featuretext.append(feature)
                if i['dType'] != 'TEXT':
                    for pad in location:
                        if i['isNibble'] == True:
                            xy = BASE.isPad(pad,unit,0,False,number_format_l, number_format_r, zeroes, x_anchor, y_anchor, x_origin, y_origin, x_scale, y_scale, x_scale_anchor, y_scale_anchor)
                            holesize = i['iHoleSize']
                            if unit == True:
                                holesize = BASE.nm2inch(holesize)
                            else:
                                holesize = BASE.nm2mm(holesize)
                            holesize = BASE.data_processing(holesize,number_format_l,number_format_r,zeroes)
                            lenth = xy+'G84X'+holesize[0]+holesize[1]
                            file.write(lenth+'\n')
                        elif i['isNibble'] == False and i['dType'] != 'TEXT':
                            xy = BASE.isPad(pad, unit, 0, False, number_format_l, number_format_r, zeroes, x_anchor, y_anchor, x_origin, y_origin, x_scale, y_scale, x_scale_anchor, y_scale_anchor)
                            file.write(xy+'\n')
                    for j in vLocations_slots:
                        digital = BASE.slotLenth(j, unit, 0, False, number_format_l, number_format_r, zeroes, x_anchor, y_anchor, x_origin, y_origin, x_scale, y_scale, x_scale_anchor, y_scale_anchor)
                        file.write(digital+'\n')
                datapass.append(i)
                if (mode == 0 or mode == 2) and (wk_data != []):
                    for wk in wk_data:
                        if (wk['iHoleSize'] == i['iHoleSize'] or wk['iHoleSize'] == i['iToolSize']) and (wk['data'] not in weikong):
                            work = wk['data']
                            file.write(work+'\n')
                            weikong.append(work)
                            break
                if combined == False:
                    break
        number+=1
    file.write('M30')
    file.close()
    print("保存文件成功")
    return True
  except Exception as e:
    print(e)
  return False


def save_gds(job:str, step:str, layer:str, filename:str, gdsdbu:float)->bool:
    try:
        _type = 1
        resize = 0
        angle = 0
        scalingX = 1
        scalingY = 1
        isReverse = False
        mirror = False
        rotate = False
        scale = False
        profiletop =False
        cw = False
        cutprofile =   True
        mirrorpointX = 0
        mirrorpointY = 0
        rotatepointX = 0
        rotatepointY = 0
        scalepointX = 0
        scalepointY = 0
        mirrordirection = 'X'
        cut_polygon = []
        numberFormatL = 2
        numberFormatR = 6
        zeros = 0
        unit = 0
        _ret = BASE.layer_export(job, step, layer, _type, filename, gdsdbu, resize, angle, scalingX, scalingY, isReverse,
                    mirror, rotate, scale, profiletop, cw, cutprofile, mirrorpointX, mirrorpointY, rotatepointX,
                    rotatepointY, scalepointX, scalepointY, mirrordirection, cut_polygon,numberFormatL,numberFormatR,
                    zeros,unit)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
    return False

def save_svg(job:str, step:str, layersinfo:dict, savepath:str)->bool:
    try:
        exist = os.path.exists(savepath)
        if exist:
            layersinfo = [layersinfo]
            ret = BASE.save_svg(job, step, layersinfo,savepath)
            if 'status' in ret :
                return False
            else:
                data = json.loads(ret)['paras']['result']
                if data == None:
                    return False
                else:
                    return True
        else:
            return False
    except Exception as e:
        print(e)
    return False

