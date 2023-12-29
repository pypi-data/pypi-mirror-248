import os, sys, json
from epkernel import BASE
import math
from epkernel.Edition import Layers,Matrix,Job
from epkernel.Action import Selection, Information


#将指定层中选中的feature拷贝至目标层，若无选中feature则将指定层资料整层拷贝
def copy2other_layer(src_job:str, src_step:str, src_layer:str, dst_layer:str, invert:bool, offset_x:int, 
                     offset_y:int, mirror:int, resize:float, rotation:float, x_anchor:float, y_anchor:float):
    try:
        BASE.sel_copy_other(src_job, src_step, [src_layer], [dst_layer], invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor)
    except Exception as e:
        print(e)
    return None

def delete_feature(job:str, step:str, layers:list):
    try:
        BASE.sel_delete(job, step, layers)
    except Exception as e:
        print(e)
    return 0

def change_text(job:str, step:str, layers:list, text:str, font:str, x_size:int, y_size:int, width:int, polarity:bool, mirror:int,angle:int=0)->None:
    try:
        if polarity==True:
            polarity=1
        else:
            polarity=-1
        BASE.change_text(job, step, layers, text, font, x_size, y_size, width, polarity, mirror,angle)
    except Exception as e:
        print(e)
    return 0

def break_features(job:str, step:str, layers:list, type:int):
    try:
        BASE.sel_break(job, step, layers, type)
    except Exception as e:
            print(e)
    return 0

def add_line(job:str, step:str, layers:list, symbol:str, start_x:int, start_y:int, end_x:int, end_y:int, polarity:bool, attributes:list)->None:
    try:
        layer = ''
        if len(layers) > 0:
            layer = layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=-1
        BASE.add_line(job, step, layers, layer, symbol, start_x, start_y, end_x, end_y, polarity, 0, attributes)
    except Exception as e:
        print(e)
    return 0
    
def hierarchy_edit(job:str, step:str, layers:list, mode:int):
    try:
        BASE.sel_index(job, step, layers, mode)
    except Exception as e:
        print(e)
    return 0

def add_surface(job:str, step:str, layers:list, polarity:bool, attributes:list, points_location:list)->None:
    try:
        layer = ''
        if len(layers)> 0:
            layer = layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=-1
        BASE.add_surface(job, step, layers, layer, polarity, 0, False, attributes, points_location)
    except Exception as e:
        print(e)
    return ''

def add_round_surface(job:str, step:str, layers:list, polarity:bool, attributes:list,center_x:int,center_y:int,radius:int)->None:
    try:
        layer = ''
        if len(layers)> 0:
            layer = layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=-1
        point2_x = center_x + radius
        point2_y = center_y
        points_location = [[point2_x, point2_y],[center_x, center_y]]
        BASE.add_surface(job, step, layers, layer, polarity, 0, True, attributes, points_location)
    except Exception as e:
        print(e)
    return '' 

def contour2pad(job:str, step:str, layers:list, tol:float, minsize:float, maxsize:float, suffix:str):
    try:
        BASE.contour2pad(job, step, layers, tol, minsize, maxsize, suffix)
    except Exception as e:
        print(e)
    return ''

def resize_polyline(job:str, step:str, layers:list, size:float, sel_type:bool):
    try:
        BASE.resize_polyline(job, step, layers, size, sel_type)
    except Exception as e:
        print(e)
    return ''

def contourize(job:str, step:str, layers:list, accuracy:int, separate_to_islands:bool, size:int, mode:int):
    try:
        mode = mode+1
        BASE.contourize(job, step, layers, accuracy, separate_to_islands, size, mode)
    except Exception as e:
        print(e)
    return ''

def add_pad(job:str, step:str, layers:list, symbol:str, location_x:int, location_y:int, polarity:bool, orient:int, attributes:list,special_angle:float=0)->None:
    try:
        layer=''
        if len(layers)>0:
            layer=layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=-1
        check = Information.identify_symbol(symbol)
        if not check:
            usesymbol_list = Information.get_usersymbol_list(job)
            if symbol not in usesymbol_list:
                aa=Job.is_job_open('eplib')
                if aa:
                    copy_usersymbol_to_other_job('eplib',job, symbol, symbol)
        BASE.add_pad(job, step, layers, layer, symbol, location_x, location_y, polarity, 0, orient,attributes,special_angle)
    except Exception as e:
        print(e)
    return ''

def change_feature_symbols(job:str, step:str, layers:list, symbol:str,pad_angle:bool = False):
    try:
        check = True
        for layer in layers:
            feature = Information.has_selected_features(job,step,layer)
            if feature == True:
                info = Information.get_selected_features_infos(job,step,layer)
            else:
                info = Information.get_all_features_info(job,step,layer)
            for data in info:
                attributes = data['attributes']
                attr = str(attributes)
                if ('.rout_chain' in attr) and (data['type'] == 2 or data['type'] == 8):
                    check = False
                    break
            if check == False:
                break
        if check == True:
            BASE.change_feature_symbols(job, step, layers, symbol, pad_angle)
    except Exception as e:
        print(e)
    return 0

#将指定料号的step下的指定层的所有feature信息拷贝至目标料号的step下的对应层中
def copy_features2dstjob(src_job:str, src_step:str, src_layer:str, dst_job:str, dst_step:str, dst_layer:str, mode:bool, invert:bool)->None:
    try:
        BASE.copy_layer_features(src_job, src_step, [src_layer], dst_job, dst_step, [dst_layer], mode, invert)
    except Exception as e:
        print(e)
    return ''
    
def create_profile(job:str, step:str, layer:str):
    try:
        BASE.create_profile(job, step, layer)
    except Exception as e:
        print(e)
    return None

def step_repeat(job:str, parent_step:str, child_steps:list):
    """
    #拼板
    :param     parentstep: panel
    :param     childsteps: 拼入panel的step
    :returns    :
    :raise error:
    """
    try:
        BASE.step_repeat(job, parent_step, child_steps)
    except Exception as e:
        print(e)
    return 0

def surface_repair(job:str, step:str, layers:list, scope:int, radius:int, remove_type:int, is_round:bool):
    try:
        BASE.remove_sharp_angle(job, step, layers, scope, radius, remove_type, is_round)
    except Exception as e:
        print(e)
    return 

def surface2outline(job:str, step:str, layers:list, width:float):
    try:
        BASE.surface2outline(job, step, layers, width)
    except Exception as e:
        print(e)
    return 

def line2pad(job:str, step:str, layers:list):
    try:
        BASE.line2pad_new(job, step, layers)
    except Exception as e:
        print(e)
    return 

def modify_attributes(job:str, step:str, layers:list, mode:int, attributes:list):
    try:
        if mode == 3 or mode == 2:
            for layer in layers:
                BASE.edit_selected_features_attributes(job, step, layer, mode, attributes)
        else:
            BASE.modify_attributes(job,step,layers,mode,attributes)
    except Exception as e:
        print(e)
    return 

def use_pattern_fill_contours(job:str,step:str,layer:str,symbolname:str,dx:int,dy:int,break_partial:bool,cut_primitive:bool,origin_point:bool,outline:bool,outlinewidth:float = 0,outline_invert:bool = False,odd_offset:int = 0,even_offset:int = 0):
    try:
        if 0 < dx < 2540000000 and 0 < dy < 2540000000:
            BASE.use_pattern_fill_contours(job,step,layer,symbolname,dx,dy,break_partial,cut_primitive,origin_point,outline,outlinewidth,outline_invert,odd_offset,even_offset)
    except Exception as e:
        print(e)
    return 

def add_arc(job:str, step:str, layers:list, symbol:str, start_x:int, start_y:int, end_x:int, end_y:int, center_x:int, center_y:int,cw:bool,polarity:bool, attributes:list)->None:
    try:
        layer=''
        if len(layers)>0:
            layer=layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=-1
        dcode = 0
        BASE.add_arc(job, step, layers, layer, symbol, start_x, start_y, end_x, end_y, center_x, center_y,cw,polarity, dcode, attributes)
    except Exception as e:
        print(e)
    return None

def layer_compare(job1:str, step1:str, layer1:str, job2:str, step2:str, layer2:str, tol:int, isGlobal:bool, consider_SR:bool, comparison_map_layername:str, map_layer_resolution:int)->None:
    try:
        BASE.layer_compare(job1, step1, layer1, job2, step2, layer2, tol, isGlobal, consider_SR, comparison_map_layername, map_layer_resolution)
    except Exception as e:
        print(e)
    return None

def add_text(job:str, step:str, layers:list, fontname:str, text:str, xsize:int, ysize:int, linewidth:int, location_x:int, location_y:int,polarity:bool,orient:int,  attributes:list,special_angle:float=0)->None:
    try:
        layer = ''
        if len(layers)>0:
            layer = layers[0]
        if polarity == True:
            polarity = 1
        else:
            polarity = -1
        BASE.add_text(job, step, layer, '',fontname, text, xsize, ysize, linewidth, location_x, location_y, polarity,orient, 0, layers, attributes,special_angle)
    except Exception as e:
        print(e)
    return ''     

def change_polarity(job:str,step:str,layers:list,polarity:int,type:int)->bool:
    try:
        sel_type = type
        _ret = BASE.sel_polarity(job, step, layers, polarity, sel_type)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
        return False

def fill_profile(job:str, step:str, layers:list, fill_type:int=0 ,step_repeat_nesting:bool=True, nesting_child_steps:list=[], step_margin_x:int=0,
                 step_margin_y:int=0, max_distance_x:int=0, max_distance_y:int=0,SR_step_margin_x:int=0,SR_step_margin_y:int=0,
                 SR_max_distance_x:int=0,SR_max_distance_y:int=0,avoid_drill:int=0,avoid_rout:int=0,avoid_feature:int=0,
                 polarity:bool=True)->bool:
    try:
        info = Information.get_fill_param()
        patternParams = info['patternParams']
        solidParams = info['solidParams']
        gridParams = info['gridParams']
        symbol = patternParams['symbolName']
        BASE.set_fill_param(fill_type,gridParams,patternParams,solidParams)
        check = False
        if fill_type == 2:
            if 0 < gridParams['dx'] < 2540000000 and 0 < gridParams['dy'] < 2540000000:
                check = True
        elif fill_type == 3:
            if 0 < patternParams['dx'] < 2540000000 and 0 < patternParams['dy'] < 2540000000:
                check = True
            identify = Information.identify_symbol(symbol)
            if not identify:
                usersymbol_list = Information.get_usersymbol_list(job)
                if symbol not in usersymbol_list:
                    aa = Job.is_job_open('eplib')
                    if aa:
                        copy_usersymbol_to_other_job('eplib', job, symbol, symbol)
        elif fill_type == 1:
            if  10 < solidParams['minBrush'] < 2540000000:
                check = True
        if check == True or fill_type == 0:
            t =Information.get_usersymbol_list(job)
            _ret = BASE.fill_profile(job,step,layers,step_repeat_nesting,nesting_child_steps,step_margin_x,step_margin_y,
                                    max_distance_x,max_distance_y,SR_step_margin_x,SR_step_margin_y,SR_max_distance_x,
                                    SR_max_distance_y,avoid_drill,avoid_rout,avoid_feature,polarity)
            ret = json.loads(_ret)['result']
            return ret
    except Exception as e:
        print(e)
    return False

def resize_global(job:str, step:str, layers:list, type:int, size:int):
    try:
        sel_type = type
        BASE.resize_global(job, step, layers, sel_type, size)
    except Exception as e:
        print(e)
    return None

def use_line_fill_contours(job:str,step:str,layer:str,dx:int,dy:int,linewidth:int,x_offset:int,y_offset:int,angle:int):
    try:
        if 0 < dx < 2540000000 and 0 < dy < 2540000000:
            BASE.fill_select_feature_by_grid(job,step,layer,dx,dy,linewidth,x_offset,y_offset,angle)
    except Exception as e:
        print(e)
    return None

def move2same_layer(job:str, step:str, layers:list, offset_x:int, offset_y:int):
    try:
        jobname = job
        stepname = step
        layernames = layers
        BASE.move_same_layer(jobname, stepname, layernames, offset_x, offset_y)
    except Exception as e:
        print(e)
    return None

def clip_area_use_reference(job:str, step:str, layers:list, reference_layer:str, margin:float, clipcontour:bool, text:bool,surface:bool,arc:bool,line:bool,pad:bool):
    try:
        jobname = job
        stepname = step
        work_layers = layers
        positive = True
        negative = True
        featuretype_sum = 0
        featuretype_list= [positive,negative,text,surface,arc,line,pad]
        for index in range(len(featuretype_list)):
            if featuretype_list[index]==True:
                featuretype_list[index]=len(featuretype_list)-index-1
            else:
                featuretype_list[index]=None
        for type_ in featuretype_list:
            if type_!=None:
                featuretype_sum += math.pow(2,type_)
        BASE.clip_area_use_reference(jobname, stepname, work_layers, reference_layer, margin, clipcontour, featuretype_sum)
    except Exception as e:
        print(e)
    return None

def clip_area_use_manual(job:str, step:str, layers:list, points:list, margin:float,  clipcontour:bool, clipinside:bool, text:bool, surface:bool, arc:bool, line:bool, pad:bool):
    try:
        jobname = job
        stepname = step
        positive = True
        negative = True
        featuretype_sum = 0
        featuretype_list= [positive,negative,text,surface,arc,line,pad]
        for index in range(len(featuretype_list)):
            if featuretype_list[index]==True:
                featuretype_list[index]=len(featuretype_list)-index-1
            else:
                featuretype_list[index]=None
        for type_ in featuretype_list:
            if type_!=None:
                featuretype_sum += math.pow(2,type_)
        for i in layers:
            layer = i
            BASE.load_layer(job,step,layer)
        BASE.clip_area_use_manual(jobname, stepname, layers, points, margin, clipcontour,clipinside, featuretype_sum)
    except Exception as e:
        print(e)
    return None

def clip_area_use_profile(job:str, step:str, layers:list,  clipinside:bool, clipcontour:bool, margin:float, text:bool, surface:bool, arc:bool, line:bool, pad:bool):
    try:
        positive = True
        negative = True
        featuretype_sum = 0
        featuretype_list= [positive,negative,text,surface,arc,line,pad]
        for index in range(len(featuretype_list)):
            if featuretype_list[index]==True:
                featuretype_list[index]=len(featuretype_list)-index-1
            else:
                featuretype_list[index]=None
        for type_ in featuretype_list:
            if type_!=None:
                featuretype_sum += math.pow(2,type_)
        for i in layers:
            layer = i
            BASE.load_layer(job,step,layer)
        BASE.clip_area_use_profile(job, step, layers, clipinside, clipcontour, margin, featuretype_sum)
    except Exception as e:
        print(e)
    return None

def transform_features(job:str,step:str,layer:str,mode:int,rotate:bool,scale:bool,mirror_X:bool,mirror_Y:bool,duplicate:bool,datumPoint:dict,angle:float,xscale:float,yscale:float,xoffset:int,yoffset:int):
    try:
        jobname = job
        stepname = step
        layername = layer
        BASE.transform(jobname,stepname,layername,mode,rotate,scale,mirror_X,mirror_Y,duplicate,datumPoint,angle,xscale,yscale,xoffset,yoffset)
    except Exception as e:
        print(e)
    return None

def rounding_line_corner(job:str, step:str, layers:list, radius:int):
    try:
        BASE.rounding_line_corner(job,step,layers,radius)
    except Exception as e:
        print(e)
    return 

def flatten_step(job:str, step:str ,flatten_layer:str, dst_layer:str)->bool:
    try:
        layers = Information.get_layers(job)
        ret = BASE.get_all_step_repeat_steps(job,step)
        steps = json.loads(ret)['steps']
        if steps != None:
            for i in range(0,len(layers)):
                for j in range(0,len(layers)):
                    if layers[i] == dst_layer and layers[j] == flatten_layer:
                        _ret = BASE.flatten_step(job,step,flatten_layer,dst_layer)
                        ret = json.loads(_ret)['status']
                        if ret =='true':
                            ret = True
                        else:
                            ret = False
                        return ret
        else:
            pass
    except Exception as e:
        print(e)
    return False

def layer_compare_point(job1:str, step1:str, layer1:str, job2:str, step2:str, layer2:str, tol:int = 22860,isGlobal:bool = True,consider_SR:bool = True, map_layer_resolution:int = 5080000)->list:
    try:
        tolerance = tol
        mode = isGlobal
        point = BASE.layer_compare_point(job1, step1, layer1, job2, step2, layer2, tolerance, mode, consider_SR, map_layer_resolution)
        points = json.loads(point)['result']
        return points
    except Exception as e:
        print(e)
    return [] 

def profile_to_outline(job:str, step:str, layers:list, linewidth:int):
    try:
        BASE.profile_to_outerline(job,step,layers,linewidth)
    except Exception as e:
        print(e)
    return None

def arc2lines(job:str, step:str, layers:list, radius:float, sel_type:bool):
    try:
        if sel_type == True:
            sel_type = 0
        else:
            sel_type = 1
        BASE.arc2lines(job,step,layers,radius,sel_type)
    except Exception as e:
        print(e)
    return None

def extend_slots(job:str, step:str, layers:list, mode:int, datum:int, size:int):
    try:
        if mode ==1 and size <0:
            return False
        
        all_layers=layers
        for layer in all_layers:
            lineindex = []
            ovalindex = []
            ret=Information.has_selected_features(job, step, layer)
            if ret == False:
                Selection.set_featuretype_filter(True, True, False, False, False, True, True) 
                Selection.select_features_by_filter(job, step, [layer])
            select_info = Information.get_selected_features_infos(job, step, layer)
            for item in select_info:
                if item['type'] == 2:
                    lineindex.append(item['feature_index'])
                elif item['type'] == 1 and item['symbolname'][0:4] =='oval':
                    ovalindex.append(item['feature_index'])
                
            if len(lineindex) == 0 and len(ovalindex) == 0:
                return False
        #对feature做处理
        #line处理
            if len(lineindex) != 0:
                for line_id in lineindex:
                    Selection.clear_select(job, step, layer)
                    Selection.reset_select_filter()
                    Selection.select_feature_by_id(job, step, layer, [line_id])           
                    info=Information.get_selected_features_infos(job, step, layer)
                    xs=info[0]['XS']
                    xe=info[0]['XE']
                    ys=info[0]['YS']
                    ye=info[0]['YE']
                    angle=abs(info[0]['angle'])
                    sin = math.sin(math.radians(angle))
                    cos = math.cos(math.radians(angle))
                    ##判断缩短值是否小于原本长度
                    check=True
                    if angle==0:
                        orglen=abs(xe-xs)*25400000
                    elif angle==90:
                        orglen=abs(ye-ys)*25400000
                    else:
                        orglen=abs(xe-xs)*25400000/cos
                    if size<0 and abs(size)>=orglen:
                        check=False
                    if check==True:
                        if mode==0 and datum==0:
                            xlen=BASE.changesize_0_0(angle,size,sin,cos)['xlen']
                            ylen=BASE.changesize_0_0(angle,size,sin,cos)['ylen']
                            location=BASE.line_mode_0_0(xlen,ylen,info)
                        if mode==0 and datum==1:
                            xlen=BASE.changesize_0_1(angle,size,sin,cos)['xlen']
                            ylen=BASE.changesize_0_1(angle,size,sin,cos)['ylen']
                            location=BASE.line_mode_0_1(xlen,ylen,info)
                        if mode==0 and datum==2:
                            xlen=BASE.changesize_0_1(angle,size,sin,cos)['xlen']
                            ylen=BASE.changesize_0_1(angle,size,sin,cos)['ylen']
                            location=BASE.line_mode_0_2(xlen,ylen,info)
                        if mode==0 and datum==3:
                            xlen=BASE.changesize_0_1(angle,size,sin,cos)['xlen']
                            ylen=BASE.changesize_0_1(angle,size,sin,cos)['ylen']
                            location=BASE.line_mode_0_3(xlen,ylen,info)
                        if mode==0 and datum==4:
                            xlen=BASE.changesize_0_1(angle,size,sin,cos)['xlen']
                            ylen=BASE.changesize_0_1(angle,size,sin,cos)['ylen']
                            location=BASE.line_mode_0_4(xlen,ylen,info)
                        if mode==1 and datum==0:
                            xlen=BASE.changesize_1_0(xs,xe,ys,ye,angle,size,sin,cos)['xlen']
                            ylen=BASE.changesize_1_0(xs,xe,ys,ye,angle,size,sin,cos)['ylen']
                            location=BASE.line_mode_1_0(xlen,ylen,info)
                        if mode==1 and datum==1:
                            xlen=BASE.changesize_1_1(xs,xe,ys,ye,angle,size,sin,cos)['xlen']
                            ylen=BASE.changesize_1_1(xs,xe,ys,ye,angle,size,sin,cos)['ylen']
                            location=BASE.line_mode_1_1(xlen,ylen,info)
                        if mode==1 and datum==2:
                            xlen=BASE.changesize_1_1(xs,xe,ys,ye,angle,size,sin,cos)['xlen']
                            ylen=BASE.changesize_1_1(xs,xe,ys,ye,angle,size,sin,cos)['ylen']
                            location=BASE.line_mode_1_2(xlen,ylen,info)
                        if mode==1 and datum==3:
                            xlen=BASE.changesize_1_1(xs,xe,ys,ye,angle,size,sin,cos)['xlen']
                            ylen=BASE.changesize_1_1(xs,xe,ys,ye,angle,size,sin,cos)['ylen']
                            location=BASE.line_mode_1_3(xlen,ylen,info)
                        if mode==1 and datum==4:
                            xlen=BASE.changesize_1_1(xs,xe,ys,ye,angle,size,sin,cos)['xlen']
                            ylen=BASE.changesize_1_1(xs,xe,ys,ye,angle,size,sin,cos)['ylen']
                            location=BASE.line_mode_1_4(xlen,ylen,info)
                    
                        xsnew=location['xsnew']
                        ysnew=location['ysnew']
                        xenew=location['xenew']
                        yenew=location['yenew']
                       
                        BASE.change_line(job, step, layer , line_id, xsnew,ysnew,xenew,yenew)
                   
        #oval处理
            if len(ovalindex) != 0:
                for oval_id in ovalindex:
                    Selection.reset_select_filter()
                    Selection.clear_select(job, step, layer)
                    Selection.select_feature_by_id(job, step, layer, [oval_id])
                    info=Information.get_selected_features_infos(job,step,layer)
                    mirror=info[0]['mirror']
                    sym=info[0]['symbolname'].strip('oval').split('x',1)
                    xsize=float(sym[0])
                    ysize=float(sym[1]) 
                    angle=info[0]['angle']
                    sepcial_angle=False
                    vertical_angle =False
                    if angle==0 or angle==180 or angle==360 or angle==90 or angle==270 :
                        anglenew=0
                        sepcial_angle=True 
                    elif 0 < angle < 90 or 180 < angle < 270:
                        anglenew = 90 - angle % 90
                        sepcial_angle = False
                    elif 90 < angle < 180 or 270 < angle < 360:
                        anglenew = angle%90
                        sepcial_angle = False
                    #2023.10.19改
                    aa = 0
                    if angle == 0 or angle == 180 or angle == 360:
                        aa = 180
                    elif angle == 90 or angle == 270 :
                        aa = 90
                    if xsize < ysize and aa == 180:
                        vertical_angle=True                  
                    elif xsize > ysize and aa == 90:
                        vertical_angle=True
                    if xsize<ysize:
                        orglen=ysize*25400
                    else:
                        orglen=xsize*25400
                    check=True
                    if size<0 and abs(size)>=orglen:
                        check=False
                    xlen=size/1000000/25.4*1000
                    ylen=size/1000000/25.4*1000
                    sin = math.sin(math.radians(anglenew))
                    cos = math.cos(math.radians(anglenew))
                    if check==True:
                        if mode==0 and datum==0:
                            location=BASE.change_datum_0_0()
                            info=BASE.oval_mode_0_0(xlen,ylen,sepcial_angle,xsize,ysize)
                        if mode==0 and datum==1:
                            location=BASE.change_datum_0_1(xsize,ysize,size,sin,cos,sepcial_angle,vertical_angle,angle,mirror)
                            info=BASE.oval_mode_0_0(xlen,ylen,sepcial_angle,xsize,ysize)
                        if mode==0 and datum==2:
                            location=BASE.change_datum_0_2(xsize,ysize,size,sin,cos,sepcial_angle,vertical_angle,angle,mirror)
                            info=BASE.oval_mode_0_0(xlen,ylen,sepcial_angle,xsize,ysize)
                        if mode==0 and datum==3:
                            location=BASE.change_datum_0_3(xsize,ysize,size,sin,cos,angle,mirror,datum)
                            info=BASE.oval_mode_0_0(xlen,ylen,sepcial_angle,xsize,ysize)
                        if mode==0 and datum==4:
                            location=BASE.change_datum_0_3(xsize,ysize,size,sin,cos,angle,mirror,datum)
                            info=BASE.oval_mode_0_0(xlen,ylen,sepcial_angle,xsize,ysize)
                        if mode==1 and datum==0:
                            location=BASE.change_datum_0_0()
                            info=BASE.oval_mode_1_0(xsize,ysize,size)
                        if mode==1 and datum==1:
                            location=BASE.change_datum_1_1(xsize,ysize,size,sin,cos,sepcial_angle,vertical_angle,angle,mirror,datum)
                            info=BASE.oval_mode_1_0(xsize,ysize,size)
                        if mode==1 and datum==2:
                            location=BASE.change_datum_1_1(xsize,ysize,size,sin,cos,sepcial_angle,vertical_angle,angle,mirror,datum)
                            info=BASE.oval_mode_1_0(xsize,ysize,size)
                        if mode==1 and datum==3:
                            location=BASE.change_datum_1_3(xsize,ysize,size,sin,cos,angle,mirror,datum)
                            info=BASE.oval_mode_1_0(xsize,ysize,size)
                        if mode==1 and datum==4:
                            location=BASE.change_datum_1_3(xsize,ysize,size,sin,cos,angle,mirror,datum)
                            info=BASE.oval_mode_1_0(xsize,ysize,size)
                        offsetx=location['x']
                        offsety=location['y']
                        xnew=info['xnew']
                        ynew=info['ynew']
                        symbolname='oval'+str(xnew)+'x'+str(ynew)
                        change_feature_symbols(job, step, [layer], symbolname)
                        Selection.select_feature_by_id(job, step, layer, [oval_id])
                        move2same_layer(job, step, [layer], offsetx, offsety)
    except Exception as e:
            print(e)
    return None

def near_hole_splitter(holeSize:int, holeSpacing:int,inPoints:list)->list:
    try:
        for i in inPoints:
            i['ix'] = i['X']
            i['iy'] = i['Y']
            del i['X']
            del i['Y']
        ret = BASE.near_hole_splitter(holeSize,holeSpacing,inPoints)
        ret = json.loads(ret)['paras']
        for j in ret:
            j['X'] = j['ix']
            j['Y'] = j['iy']
            del j['ix']
            del j['iy']
        return ret
    except Exception as e:
        print(e)
    return []

def outline2surface(job:str, step:str, layers:list, to_pad:bool):
    try:
        BASE.outline2surface(job,step,layers,to_pad)
    except Exception as e:
        print(e)
    return None

#将指定料号指定层中选中的feature移动至目标料号下的目标层中，
def move2other_layer(src_job:str, src_step:str, src_layers:list, dst_job:str, dst_step:str, dst_layer:str, invert:bool, offset_x:int, offset_y:int, mirror:int, resize:float, rotation:float, x_anchor:float, y_anchor:float)->None:
    try:
        BASE.sel_move_other(src_job, src_step, src_layers, dst_job, dst_step, dst_layer, invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor)
    except Exception as e:
        print(e)

def copy_usersymbol_to_other_job(job1:str, job2:str, symbol1:str, symbol2:str):
    try:
        BASE.copy_usersymbol_to_other_job(job1,job2,symbol1,symbol2)
    except Exception as e:
        print(e)

def set_fill_grid_param(angle:int, dx:int, dy:int, linewidth:int, xoffset:int, yoffset:int):
    try:
        ret = Information.get_fill_param()
        fillType = 2
        patternParams = ret['patternParams']
        solidParams = ret['solidParams']
        gridParams = ret['gridParams']
        gridParams['angle'] = angle
        gridParams['dx'] = dx
        gridParams['dy'] = dy
        gridParams['lineWidth'] = linewidth
        gridParams['xOffset'] = xoffset
        gridParams['yOffset'] = yoffset
        BASE.set_fill_param(fillType,gridParams,patternParams,solidParams)
    except Exception as e:
        print(e)

def set_fill_pattern_param(symbolname:str, break_partial:bool, cut_primitive:bool, dx:int, dy:int, origin_point:bool, outline:bool, outline_invert:bool=False,outline_width:int=0,even_offset:int=0,odd_offset:int=0,angle:int = 0):
    try:
        ret = Information.get_fill_param()
        fillType = 3
        patternParams = ret['patternParams']
        solidParams = ret['solidParams']
        gridParams = ret['gridParams']
        patternParams['breakPartial'] = break_partial
        patternParams['cutPrimitive'] = cut_primitive
        patternParams['dx'] = dx
        patternParams['dy'] = dy
        patternParams['evenOffset'] = even_offset
        patternParams['oddOffset'] = odd_offset
        patternParams['originPoint'] = origin_point
        patternParams['outline'] = outline
        patternParams['outlineInvert'] = outline_invert
        patternParams['outlineWidth'] = outline_width
        patternParams['symbolName'] = symbolname
        patternParams['angle'] = angle
        BASE.set_fill_param(fillType,gridParams,patternParams,solidParams)
    except Exception as e:
        print(e)

def set_fill_solid_param(solid_type:bool=True,min_brush:int=25400,use_arcs:bool=False):
    try:
        ret = Information.get_fill_param()
        fillType = 0
        if solid_type:
            fillType = 1
        patternParams = ret['patternParams']
        solidParams = ret['solidParams']
        gridParams = ret['gridParams']
        solidParams['minBrush'] = min_brush
        solidParams['solidType'] = solid_type
        solidParams['useArcs'] = use_arcs
        BASE.set_fill_param(fillType,gridParams,patternParams,solidParams)
    except Exception as e:
        print(e)

def fill_contours(job:str,step:str,layer:str,type:int):
    try:
        ret = BASE.get_fill_param()
        param = json.loads(ret)['paras']
        if type == 0:
            minBrush = param['solidParams']['minBrush']
            useArcs = param['solidParams']['useArcs']
            use_solid_fill_contours(job,step,[layer],minBrush,useArcs)
        elif type == 1:
            angle = param['gridParams']['angle']
            dx = param['gridParams']['dx']
            dy = param['gridParams']['dy']
            lineWidth = param['gridParams']['lineWidth']
            xOffset = param['gridParams']['xOffset']
            yOffset = param['gridParams']['yOffset']
            use_line_fill_contours(job,step,layer,dx,dy,lineWidth,xOffset,yOffset,angle)
        elif type == 2:
            breakPartial = param['patternParams']['breakPartial']
            cutPrimitive = param['patternParams']['cutPrimitive']
            dx = param['patternParams']['dx']
            dy = param['patternParams']['dy']
            evenOffset = param['patternParams']['evenOffset']
            oddOffset = param['patternParams']['oddOffset']
            originPoint = param['patternParams']['originPoint']
            outline = param['patternParams']['outline']
            outlineInvert = param['patternParams']['outlineInvert']
            outlineWidth = param['patternParams']['outlineWidth']
            symbolName = param['patternParams']['symbolName']
            use_pattern_fill_contours(job,step,layer,symbolName,dx,dy,breakPartial,cutPrimitive,originPoint,outline,outlineWidth,outlineInvert,oddOffset,evenOffset)
    except Exception as e:
        print(e)

def use_solid_fill_contours(job:str, step:str, layers:list, min_brush:int, use_arcs:bool=False):
    try:
        if 10 < min_brush < 2540000000:
            BASE.use_solid_fill_contours(job,step,layers,True,min_brush,use_arcs)
    except Exception as e:
        print(e)

def add_chain(job:str,step:str,layer:str,chain_number:int,first_index:int,comp:int,keep_direction:bool,
              add_plunge:bool,toolsize:float,rout_flag:float = 0,feed:float = 0,speed:float = 0):
    try:
        if comp == 0:
            comp = 'None'
        elif comp == 1:
            comp = 'Left'
        elif comp == 2:
            comp = 'Right'
        BASE.add_chain(job,step,layer,chain_number,first_index,comp,keep_direction,add_plunge,toolsize,rout_flag,feed,speed)
    except Exception as e:
        print(e)

def pad2line(job:str,step:str,layers:list):
    try:
        BASE.pad2line(job,step,layers)
    except Exception as e:
        print(e)

def generate_rout_layer(job:str,step:str,srcLayer:str,disLayer:str,mode:int)->bool:
    try:
        data = Information.get_layer_information(job)
        for i in data:
            if i['context'] == 'board' and i['type'] == 'rout' and i['name'] == srcLayer:
                info = BASE.generate_rout_layer(job,step,srcLayer,disLayer,mode)
                ret = json.loads(info)['status']
                if ret == 'true':
                    ret = True
                else:
                    ret = False
                return ret
    except Exception as e:
        print(e)
    return False

def clean_surface_hole(job:str, step:str, layers:list, maxsize:int, clearmode:int):
    try:
        mode = clearmode+1
        BASE.clean_surface_hole(job, step, layers, maxsize, mode)
    except Exception as e:
        print(e)

