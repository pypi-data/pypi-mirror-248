import os,sys,re
from epkernel import epcam
import json,math,operator
from datetime import datetime
from decimal import Decimal

path=''

#获取step, layer信息
def get_graphic(job):
    data = {
        'func': 'GET_GRAPHICS',
        'paras': {'job': job}
    }
    return epcam.process(json.dumps(data))

#设置属性筛选
def filter_set_attribute(logic, attribute_list):
    data = {
        'func': 'FILTER_SET_ATR',
        'paras': [{'logic': logic},
                  {'attributes_value': attribute_list}]
    }
    #print(json.dumps(data))
    epcam.process(json.dumps(data))

#根据筛选选择feature
def select_features_by_filter(job, step, layers):
    data = {
            'func': 'SELECT_FEATURES_BY_FILTER',
            'paras': [{'job': job},
                      {'step': step},
                      {'layer': layers}]
        }
    #print(json.dumps(data))
    epcam.process(json.dumps(data))

#feature涨缩
#sel_type : 0 selected 1 all
def resize_global(job, step, layers, sel_type, size):
    data = {
            'func': 'GLOBAL_RESIZE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'sel_type': sel_type},
                      {'size': size},
                      {'corner': False}]
        }
    #print(json.dumps(data))
    epcam.process(json.dumps(data))

#打开料号
def open_job(path, job):
    data = {
        'func': 'OPEN_JOB',
        'paras': [{'path': path},
                  {'job': job}]
    }
    # print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret

#关闭料号
def close_job(job):
    data = {
        'func': 'CLOSE_JOB',
        'paras': 
                  {'jobname': job}
    }
    # print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret

#保存料号
def save_job(job):
    data = {
        'func': 'JOB_SAVE',
        'paras': [{'job': job}]
    }
    #print(json.dumps(data))
    epcam.process(json.dumps(data))

#获取当前层所有的feature的symbol信息
def get_all_features_report(job, step, layer):
    data = {
        'func': 'GET_ALL_FEATURES_REPORT',
        'paras': {'job': job, 
                  'step': step, 
                  'layer': layer}
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret

#获取当前的筛选条件
def get_select_param():
    data = {
        'func': 'GET_SELECT_PARAM',
        'paras': {}
    }
    return epcam.process(json.dumps(data))

#设置新的筛选条件    profile_value//0: all 1: in  2: out
def set_select_param(featuretypes, has_symbols, symbols,  dcode, attributes_flag, attributes_value, 
                        profile_value, use_selection,use_symbol_range=False,symbol_range=[],use_attr_range=False,attr_range=[],
                        exclude_attributes_value=[],exclude_attr_ranges=[],exclude_symbols=[],exclude_symbol_range=[],lines=False,
                        ovals=False,use_length=False,use_angle=False,minlength=0,maxlength=0,minangle=0,maxangle=0):
    data = {
        'func': 'SET_SELECT_PARAM',
        'paras': {'param':{
                  'featuretypes': featuretypes, 
                  'has_symbols': has_symbols, 
                  'symbols': symbols, 
                #   'minline': minline,
                #   'maxline': maxline,
                  'dcode': dcode,
                  'attributes_flag': attributes_flag,
                  'attributes_value': attributes_value,
                  'profile_value': profile_value,
                  'use_selection': use_selection,
                  'use_symbol_range':use_symbol_range,
                  'symbol_range':symbol_range,
                  'use_attr_range':use_attr_range,
                  'attr_range':attr_range,
                  'exclude_attributes_value':exclude_attributes_value,
                  'exclude_attr_ranges':exclude_attr_ranges,
                  'exclude_symbols':exclude_symbols,
                  'exclude_symbol_range':exclude_symbol_range,
                  'lines':lines,
                  'ovals':ovals,
                  'use_length':use_length,
                  'use_angle':use_angle,
                  'minlength':minlength,
                  'maxlength':maxlength,
                  'minangle':minangle,
                  'maxangle':maxangle
                  }
                  }
    }
    #print(json.dumps(data))
    epcam.process(json.dumps(data))

#创建新层
def create_new_layer(job, step, layer, index):
    data = {
        'func': 'CREATE_NEW_LAYER',
        'paras': {'job': job,
                  'step': step, 
                  'layer': layer,
                  'index': index}
    }
    epcam.process(json.dumps(data))

#创建新step
def create_step(jobname, stepname, index):
    data = {
        'func': 'CREATE_STEP',
        'paras': {'jobname': jobname,
                  'stepname': stepname, 
                  'index': index}
    }
    epcam.process(json.dumps(data))

#修改job名
def job_rename(src_jobname, dst_jobname):
    data = {
        'func': 'JOB_RENAME',
        'paras': {'src_jobname': src_jobname,
                  'dst_jobname': dst_jobname }
    }
    epcam.process(json.dumps(data))

#修改matrix信息
def change_matrix(jobname, old_step_index, old_layer_index, new_step_name, new_layer_info):
    data = {
        'func': 'CHANGE_MATRIX',
        'paras': {'jobname': jobname,
                  'old_step_index': old_step_index,
                  'old_layer_index': old_layer_index,
                  'new_step_name': new_step_name,
                  'new_layer_info': new_layer_info}
    }
    epcam.process(json.dumps(data))

#获取matrix信息
def get_matrix(job):
    data = {
        'func': 'GET_MATRIX',
        'paras': {'job': job}
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

#加载layer
def open_layer(job, step, layer):
    data = {
        'func': 'OPEN_LAYER',
        'paras': {'jobname': job,
                  'step': step,
                  'layer': layer}
    }
    epcam.process(json.dumps(data))
    return epcam.process(json.dumps(data))

#copy layer
def copy_layer(jobname, org_layer_index, dst_layer, poi_layer_index):
    data = {
        'func': 'COPY_LAYER',
        'paras': {'jobname': jobname,
                  'org_layer_index': org_layer_index,
                  'dst_layer': dst_layer,
                  'poi_layer_index': poi_layer_index }
    }
    return epcam.process(json.dumps(data))

#删除料号
def job_delete(jobname):
    data = {
        'func': 'JOB_DELETE',
        'paras': {'src_jobname': jobname}
    }
    epcam.process(json.dumps(data))

#删除feature
def sel_delete(job, step, layers):
    data = {
            'func': 'SEL_DELETE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers}]
    }
    epcam.process(json.dumps(data))

#清空选择
def clear_selected_features(job, step, layer):
    data = {
            'func': 'CLEAR_SELECTED_FEATURES',
            'paras': {'job': job,
                      'step': step,
                      'layer': layer}
    }
    #print(json.dumps(data))
    epcam.process(json.dumps(data))

#获取当前层所有选中的feature的symbol信息
def get_selected_features_report(job, step, layer):
    data = {
        'func': 'GET_SELECTED_FEATURES_REPORT',
        'paras': {'job': job, 
                  'step': step, 
                  'layer': layer}
    }
    ret = epcam.process(json.dumps(data))
    return ret

def filter_by_mode(jobname, step, layer, reference_layers, mode, feature_type_ref, symbolflag , symbolnames, 
                    attrflag = -1,attrlogic = 0, attributes = [],use_symbol_range=False,symbol_range=[],
                    use_attr_range=False,attr_range=[],exclude_attributes=[],exclude_attr_range=[],
                    exclude_symbols=[],exclude_symbol_range=[]):
    data = {
        'func': 'FILTER_BY_MODE',
        'paras': {'jobname': jobname, 
                  'step': step, 
                  'layer': layer,
                  'reference_layers': reference_layers, 
                  'mode': mode, 
                  'feature_type_ref': feature_type_ref,
                  'symbolflag': symbolflag, 
                  'symbolnames': symbolnames,
                  'attrflag': attrflag,
                  'attrlogic': attrlogic,
                  'attributes': attributes,
                  'use_symbol_range': use_symbol_range,
                  'symbol_range': symbol_range,
                  'use_attr_range': use_attr_range,
                  'attr_range': attr_range,
                  'exclude_attributes':exclude_attributes,
                  'exclude_attr_ranges':exclude_attr_range,
                  'exclude_symbolnames':exclude_symbols,
                  'exclude_symbol_range':exclude_symbol_range
                  }
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#孔分析
def drill_check(job, step, layers, erf, rout_distance, hole_size, extra_holes, hole_seperation, power_ground_short, missing_hole, 
                npth_to_rout, use_pth, use_npth, use_via, compensated_rout, ranges):
    data = {
        'func': 'DRILL_CHECK',
        'paras': [{'job': job}, 
                  {'step': step}, 
                  {'layers': layers},
                  {'rout_distance': rout_distance}, 
                  {'hole_size': hole_size}, 
                  {'extra_holes': extra_holes},
                  {'hole_seperation': hole_seperation}, 
                  {'power_ground_short': power_ground_short},
                  {'missing_hole': missing_hole},
                  {'npth_to_rout': npth_to_rout},
                  {'use_pth': use_pth},
                  {'use_npth': use_npth},
                  {'use_via': use_via},
                  {'compensated_rout': compensated_rout},
                  {'ranges':ranges}]
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#插入layer
def insert_layer(job, poi_layer_index):
    data = {
            'func': 'LAYER_INSERT',
            'paras': [{'job': job}, 
                      {'poi_layer_index': poi_layer_index}]
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#添加symbol筛选
def filter_set_include_syms(has_symbols, symbols):
    data = {
            'func': 'FILTER_SET_INCLUDE_SYMS',
            'paras': [{'has_symbols': True}, 
                      {'symbols': symbols}]
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#反选
def counter_election(job, step, layer):
    data = {
            'func': 'COUNTER_ELECTION',
            'paras': [{'job': job}, 
                      {'step': step},
                      {'layer': layer}]
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#选中feature
"""selectpolygon :eg.[[0,0],[1,1]]"""
def select_feature(job, step, layer, selectpolygon, featureInfo, margin, clear):
    data = {
            'func': 'SELECT_FEATURE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layer': layer},
                      {'selectpolygon': selectpolygon},
                      {'featureInfo': featureInfo},
                      {'type': margin},#0:单选          1：框选
                      {'clear': clear} #True,False
                      ]
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#修改文字
def change_text(job, step, layers, text, font, x_size, y_size, width, polarity, mirror,angle=0):
    data = {
            'func': 'TEXT_CHANGE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'text': text},
                      {'font': font},
                      {'x_size': x_size},
                      {'y_size': y_size},
                      {'width': width},
                      {'polarity': polarity},
                      {'mirror': mirror},
                      {'angle':angle}
                      ]
        }
    ret = epcam.process(json.dumps(data))
#内外层分析
def signal_layer_check(job, step, layers, erf, pp_spacing, drill2cu, rout2cu, sliver_min, min_pad_overlap, spacing, stubs, 
                        drill, center, rout, smd, size, bottleneck, sliver, pad_connection_check,
                        apply_to, check_missing, use_compensated_rout, sort_spacing, ranges):
    data = {
        'func': 'SIGNAL_LAYER_CHECK',
        'paras': [{'job': job}, 
                  {'step': step}, 
                  {'layers': layers},
                  {'erf': erf},
                  {'pp_spacing': pp_spacing}, 
                  {'drill2cu': drill2cu}, 
                  {'rout2cu': rout2cu},
                  {'sliver_min': sliver_min}, 
                  {'min_pad_overlap': min_pad_overlap},
                  {'spacing': spacing},
                  {'stubs': stubs},
                  {'drill': drill},
                  {'center': center},
                  {'rout': rout},
                  {'smd': smd},
                  {'size': size},
                  {'bottleneck': bottleneck},
                  {'sliver': sliver},
                  {'pad_connection_check': pad_connection_check},
                  {'apply_to': apply_to},
                  {'check_missing': check_missing},
                  {'use_compensated_rout': use_compensated_rout},
                  {'sort_spacing': sort_spacing},
                  {'ranges': ranges}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret

#内外层优化
def signal_layer_DFM(job, step, layers, erf, pth_ar_min, pth_ar_opt, via_ar_min, via_ar_opt, mvia_ar_min, mvia_ar_opt, spacing_min, spacing_opt,
				pad_to_pad_spacing_min, pad_to_pad_spacing_opt, lre_range_fr, lre_range_to, reduction, abs_min, drill_to_cu,
			    apply_to, pads, smds, drills, padup, shave, paddn, rerout, linedn, reshape, padup_can_touch_pad, cut_pad_touch_pad, laser_ar_min,
                laser_ar_opt, buried_min, buried_opt, ranges):
    data = {
        'func': 'SIGNAL_LAYER_DFM',
        'paras': [{'job': job}, 
                  {'step': step}, 
                  {'layers': layers},
                  {'erf': erf},
                  {'pth_ar_min': pth_ar_min}, 
                  {'pth_ar_opt': pth_ar_opt}, 
                  {'via_ar_min': via_ar_min},
                  {'via_ar_opt': via_ar_opt}, 
                  {'mvia_ar_min': mvia_ar_min},
                  {'mvia_ar_opt': mvia_ar_opt},
                  {'spacing_min': spacing_min},
                  {'spacing_opt': spacing_opt},
                  {'pad_to_pad_spacing_min': pad_to_pad_spacing_min},
                  {'pad_to_pad_spacing_opt': pad_to_pad_spacing_opt},
                  {'lre_range_fr': lre_range_fr},
                  {'lre_range_to': lre_range_to},
                  {'reduction': reduction},
                  {'abs_min': abs_min},
                  {'drill_to_cu': drill_to_cu},
                  {'apply_to': apply_to},
                  {'pads': pads},
                  {'smds': smds},
                  {'drills': drills},
                  {'padup': padup},
                  {'shave': shave},
                  {'paddn': paddn},
                  {'rerout': rerout},
                  {'linedn': linedn},
                  {'reshape': reshape},
                  {'padup_can_touch_pad': padup_can_touch_pad},
                  {'cut_pad_touch_pad': cut_pad_touch_pad},
                  {'laser_ar_min': laser_ar_min},
                  {'laser_ar_opt': laser_ar_opt},
                  {'buried_ar_min': buried_min},
                  {'buried_ar_opt': buried_opt},
                  {'ranges': ranges}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))

#打散feature
def sel_break(job, step, layers, sel_type):
    data = {
            'func': 'SEL_BREAK',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'sel_type': sel_type}
                      ]
        }
    #print(json.dumps(data)) 
    ret = epcam.process(json.dumps(data))

#复制Step
def copy_step(job, org_step_index, dst_step, poi_step_index):
    data = {
            'func': 'COPY_STEP',
            'paras': {'jobname': job,
                      'org_step_index': org_step_index,
                      'dst_step': dst_step,
                      'poi_step_index': poi_step_index}                    
        }
    ret = epcam.process(json.dumps(data))
    return ret

#插入step
def insert_step(job, poi_step_index):
    data = {
            'func': 'INSERT_STEP',
            'paras': {'jobname': job, 
                      'poi_step_index': poi_step_index}
    }
    ret = epcam.process(json.dumps(data))

#layer_compare_bmp 
def layer_compare_bmp(jobname1, stepname1, layername1, jobname2, stepname2,layername2, tolerance, grid_size, savepath, suffix, bmp_width, bmp_height):
    data = {
                'func': 'LAYER_COMPARE_BMP',
                'paras': {  'jobname1': jobname1, 
                            'stepname1': stepname1,
                            'layername1': layername1,
                            'jobname2': jobname2,
                            'stepname2': stepname2,
                            'layername2': layername2,
                            'tolerance': tolerance,
                            'grid_size': grid_size,
                            'savepath': savepath,
                            'suffix': suffix,
                            'bmp_width': bmp_width,
                            'bmp_height': bmp_height}
           }      
    ret = epcam.process(json.dumps(data))
    return ret

#泪滴优化
def teardrop_create_DFM(job, step, layers, erf, sel_type, drilled_pads, undrilled_pads, ann_ring_min, drill_size_min, drill_size_max, 
                        cu_spacing, drill_spacing, delete_old_teardrops, apply_to, work_mode, use_arc_tear, arc_angle, bga_pads, 
                        tear_line_width_ratio, ranges):
    data = {
        'func': 'TEARDROP_CREATE_DFM',
        'paras': [{'job': job}, 
                  {'step': step}, 
                  {'layers': layers},
                  {'erf': erf},
                  {'type': sel_type}, 
                  {'drilled_pads': drilled_pads}, 
                  {'undrilled_pads': undrilled_pads},
                  {'ann_ring_min': ann_ring_min}, 
                  {'drill_size_min': drill_size_min},
                  {'drill_size_max': drill_size_max},
                  {'cu_spacing': cu_spacing},
                  {'drill_spacing': drill_spacing},
                  {'delete_old_teardrops': delete_old_teardrops},
                  {'apply_to': apply_to},
                  {'work_mode': work_mode},
                  {'use_arc_tear': use_arc_tear},
                  {'arc_angle': arc_angle},
                  {'bga_pads': bga_pads},
                  {'tear_line_width_ratio': tear_line_width_ratio},
                  {'ranges': ranges}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))

#拼板
def step_repeat(job, parentstep, childsteps):
    data = {
            'func': 'STEP_REPEAT',
            'paras': {'jobname': job, 
                      'parentstep': parentstep,
                      'childsteps': childsteps}
    }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#设置基准点
def set_datum_point(job, stepname, point_x, point_y):
    data = {
            'func': 'SET_DATUM_POINT',
            'paras': {'jobname': job, 
                      'stepname': stepname,
                      'point': {'ix': point_x, 'iy': point_y}}
    }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#获取profile box
def get_profile_box(job, step):
    data = {
            'func': 'PROFILE_BOX',
            'paras': {'job': job, 
                      'step': step}
    }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

#修改feature的叠放顺序
def sel_index(job, step, layers, mode):
    data = {
            'func': 'SEL_INDEX',
            'paras': [{'job': job}, 
                      {'step': step},
                      {'layers': layers},
                      {'mode': mode}]
    }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#新建profile线
def create_profile(jobname, stepname, layername):
    data = {
        'func': 'CREATE_PROFILE',
        'paras': {'jobname': jobname, 
                  'stepname': stepname,
                  'layername': layername}
    }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#添加线
# polarity:1 P 0 N
def add_line(job, step, layers, layer, symbol, start_x, start_y, end_x, end_y, polarity, dcode, attributes):
    data = {
        'func': 'ADD_LINE',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'layer': layer},
                  {'symbol': symbol},
                  {'start_x': start_x},
                  {'start_y': start_y},
                  {'end_x': end_x},
                  {'end_y': end_y},
                  {'polarity': polarity},
                  {'dcode': dcode},
                  {'attributes': attributes}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#跨层复制feature
def sel_copy_other(src_job, src_step, src_layers, dst_layers, invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor):
    data = {
        'func': 'SEL_COPY_OTHER',
        'paras': [{'src_job': src_job},
                  {'src_step': src_step},
                  {'src_layers': src_layers},
                  {'dst_layers': dst_layers},
                  {'invert': invert},
                  {'offset_x': offset_x},
                  {'offset_y': offset_y},
                  {'mirror': mirror},
                  {'resize': resize},
                  {'rotation': rotation},
                  {'x_anchor': x_anchor},
                  {'y_anchor': y_anchor}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

"""
#删除layer
:param     job:
:param     layer_index:
:returns   :
:raises    error:
"""
def delete_layer(job, layer_index):
    data = {
            'func': 'DELETE_LAYER',
            'paras': {'jobname': job,
                      'layer_index': layer_index}                    
        }
    ret = epcam.process(json.dumps(data))

#profile线间新建layer
def create_layer_between_profile(jobname, stepname, new_layername, child_profile_margin):
    data = {
        'func': 'CREATE_LAYER_BETWEEN_PROFILE',
        'paras':  {'jobname': jobname,
                   'stepname': stepname,
                   'new_layername': new_layername,
                   'child_profile_margin': child_profile_margin}
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#添加surface
def add_surface(job, step, layers, layer, polarity, dcode, isround, attributes, points_location):
    data = {
        'func': 'ADD_SURFACE',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'layer': layer},
                  {'polarity': polarity},
                  {'dcode': dcode},
                  {'isround': isround},
                  {'attributes': attributes},
                  {'points_location': points_location}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#区域切割(profile)
def clip_area_use_profile(job, step, layers, clipinside, clipcontour, margin, featuretype):
    data = {
            'func': 'CLIP_AREA_USE_PROFILE',
            'paras': {'job': job,
                      'step': step,
                      'layer': layers,
                      'clipinside': clipinside,
                      'clipcontour': clipcontour,
                      'margin': margin,
                      'featuretype': featuretype,}                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#避铜
def avoid_conductor_DFM_op(jobname, stepname, layernames, erf, coverage_min, coverage_opt, radius_opt, mending_copper_wire, 
                            is_fast, use_global, viadrill2cu, pthdrill2cu):
    data = {
            'func': 'AVOID_CONDUCTOR_DFM_OP',
            'paras': [{'jobname': jobname},
                      {'stepname': stepname},
                      {'layernames': layernames},
                      {'erf': erf},
                      {'coverage_min': coverage_min},
                      {'coverage_opt': coverage_opt},
                      {'radius_opt': radius_opt},
                      {'mending_copper_wire': mending_copper_wire},
                      {'is_fast': is_fast},
                      {'use_global': use_global},
                      {'pthdrill2cu': pthdrill2cu},
                      {'viadrill2cu': viadrill2cu}]                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#去尖角
def remove_sharp_angle(job, step, layers, scope, radius, remove_type, is_round):
    data = {
            'func': 'REMOVE_SHARP_ANGLE',
            'paras': {'para': 
                     {'job': job,
                      'step': step,
                      'layers': layers,
                      'scope': scope,
                      'radius': radius,
                      'type': remove_type,
                      'is_round': is_round}
                      }                  
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#获取当前层所有选中的feature的symbol信息
"""
featureinfo:
type:   1        pad
            2       line
            4       surface
            8       arc
            16      text
            32      barcode
            64      text_plus
            0       unknow
"""
def get_selected_feature_infos(job, step, layer):
    data = {
        'func': 'GET_SELECTED_FEATURE_INFOS',
        'paras': {'jobname': job, 
                  'stepname': step, 
                  'layername': layer}
    }
    ret = epcam.process(json.dumps(data))
    return ret

#获取当前层所有feature的symbol信息
def get_all_feature_infos(job, step, layer):
    data = {
        'func': 'GET_ALL_FEATURE_INFOS',
        'paras': {'jobname': job, 
                  'stepname': step, 
                  'layername': layer}
    }
    ret = epcam.process(json.dumps(data))
    return ret

#防焊层优化
def solder_mask_DFM(job, step, layers, erf, clearance_min, clearance_opt, coverage_min, coverage_opt, bridge_size, 
                    apply_to, use_existing_mask, use_shaves, do_resize, max_oversized_clearance, intersect_width, 
                    cut_surplus_width, cut_surplus_height, is_round, fan_shaved, prevent_vertical_flow_add_sm, 
                    prevent_vertical_flow_del_sm, 
                    drill_clearance_min , drill_clearance_opt , smd_clearance_min,
				    smd_clearance_opt , bga_clearance_min, bga_clearance_opt, add_outline, outline_width, 
                    he_hong_resize_sm_in_surface, resize_gas_sm_no_drill, resize_gas_sm_has_drill, 
                    add_v_cut_sm_size, resize_sm_surface_size, pth_fan_shave, pad_covered_clearance, ranges):
    data = {
            'func': 'SOLDER_MASK_DFM',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'erf': erf},
                      {'clearance_min': clearance_min},
                      {'clearance_opt': clearance_opt},
                      {'coverage_min': coverage_min},
                      {'coverage_opt': coverage_opt},
                      {'bridge_size': bridge_size},
                      {'apply_to': apply_to},
                      {'use_existing_mask': use_existing_mask},
                      {'use_shaves': use_shaves},
                      {'do_resize': do_resize},
                      {'max_oversized_clearance': max_oversized_clearance},
                      {'intersect_width': intersect_width},
                      {'cut_surplus_width': cut_surplus_width},
                      {'cut_surplus_height': cut_surplus_height},
                      {'is_round': is_round},
                      {'fan_shaved': fan_shaved},
                      {'prevent_vertical_flow_add_sm': prevent_vertical_flow_add_sm},
                      {'prevent_vertical_flow_del_sm': prevent_vertical_flow_del_sm},
                      {'drill_clearance_min': drill_clearance_min},
                      {'drill_clearance_opt': drill_clearance_opt},
                      {'smd_clearance_min': smd_clearance_min},
                      {'smd_clearance_opt': smd_clearance_opt},
                      {'bga_clearance_min': bga_clearance_min},
                      {'bga_clearance_opt': bga_clearance_opt},
                      {'add_outline': add_outline},
                      {'outline_width': outline_width},
                      {'he_hong_resize_sm_in_surface': he_hong_resize_sm_in_surface},
                      {'resize_gas_sm_no_drill': resize_gas_sm_no_drill},
                      {'resize_gas_sm_has_drill': resize_gas_sm_has_drill},
                      {'add_v_cut_sm_size': add_v_cut_sm_size},
                      {'resize_sm_surface_size': resize_sm_surface_size},
                      {'pth_fan_shave': pth_fan_shave},
                      {'pad_covered_clearance': pad_covered_clearance},
                      {'ranges': ranges}
                     ]                
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#求一个范围内最小距离
def get_selected_feature_min_spacing(jobname, stepname, layername, search_radium, min_spacing):
    data = {
            'func': 'GET_SELECTED_FEATURE_MIN_SPACING',
            'paras': {
                      'jobname': jobname,
                      'stepname': stepname,
                      'layername': layername,
                      'search_radium': search_radium,
                      'min_spacing': min_spacing
                      }             
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

#移动layer
def move_layer(jobname, org_layer_index, dst_layer_index):
    data = {
            'func': 'MOVE_LAYER_POI',
            'paras': {
                      'jobname': jobname,
                      'org_layer_index': org_layer_index,
                      'dst_layer_index': dst_layer_index,
                      }             
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#contour to pad
def contour2pad(job, step, layers, tol, minsize, maxsize, suffix):
    data = {
            'func': 'CONTOUR2PAD',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'tol': tol},
                      {'minsize': minsize},
                      {'maxsize': maxsize},
                      {'suffix': suffix}
                      ]
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#resize_polyline
def resize_polyline(job, step, layers, size, sel_type):
    data = {
            'func': 'POLYLINE_RESIZE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'size': size},
                      {'sel_type': sel_type},
                      ]
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#求最小公差
def get_min_tolerance(jobname, stepname, layername1, layername2, selectbox):
    data = {
            'func': 'GET_MIN_TOLERANCE',
            'paras': {
                      'jobname': jobname,
                      'stepname': stepname,
                      'layername1': layername1,
                      'layername2': layername2,
                      'selectbox': selectbox
                      }             
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

"""
#删除step
:param     job:
:param     step_index:
:returns   :
:raises    error:
"""
def delete_step(job, step_index):
    data = {
            'func': 'DELETE_STEP',
            'paras': {'jobname': job,
                      'step_index': step_index}                    
        }
    ret = epcam.process(json.dumps(data))
#跨层移动feature
def sel_move_other(src_job, src_step, src_layers, dst_job, dst_step, dst_layer, invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor):
    data = {
        'func': 'SEL_MOVE_OTHER',
        'paras': [{'src_job': src_job},
                  {'src_step': src_step},
                  {'src_layers': src_layers},
                  {'dst_job': dst_job},
                  {'dst_step': dst_step},
                  {'dst_layer': dst_layer},
                  {'invert': invert},
                  {'offset_x': offset_x},
                  {'offset_y': offset_y},
                  {'mirror': mirror},
                  {'resize': resize},
                  {'rotation': rotation},
                  {'x_anchor': x_anchor},
                  {'y_anchor': y_anchor}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#smd_bga pad 优化
def smd_bga_DFM_op(jobname, stepname, layernames, erf, smd_bga_spacing_opt, max_padup_value):
    data = {
            'func': 'SMD_BGA_DFM_OP',
            'paras': [{'jobname': jobname},
                      {'stepname': stepname},
                      {'layernames': layernames},
                      {'erf': erf},
                      {'smd_bga_spacing_opt': smd_bga_spacing_opt},
                      {'max_padup_value': max_padup_value}]                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#load layer
def load_layer(jobname, stepname, layername):
    data = {
            'func': 'LOAD_LAYER',
            'paras': {'jobname': jobname,
                      'stepname': stepname,
                      'layername': layername}                   
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#设置显示模式
def set_display_widths(width):
    data = {
            'func': 'SET_DISPLAY_WIDTHS',
            'paras': [{'width': width}]                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#设置文字显示模式
def set_display_text(disp):
    data = {
            'func': 'SET_DISPLAY_TEXT',
            'paras': [{'disp': disp}]                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#设置单位
def set_units(units):
    data = {
            'func': 'SET_UNITS',
            'paras': [{'units': units}]                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#设置是否显示profile线
def set_display_profile(mode):
    data = {
            'func': 'SET_DISPLAY_PROFILE',
            'paras': [{'mode': mode}]                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#获取显示参数
def get_show_para(mode):
    data = {
            'func': 'SET_DISPLAY_PROFILE',
            'paras': [{'mode': mode}]                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#避npth孔和profile线 优化
def avoid_features_DFM_op(jobname, stepname, layernames, erf, avoid_profile, avoid_profile_size, avoid_npth, avoid_npth_size, 
                            avoid_alone_drill, avoid_alone_drill_size, npth_add_solder_mask, npth_add_solder_mask_size, avoid_v_cut):
    data = {
            'func': 'AVOID_FEATURES_DFM_OP',
            'paras': [{'jobname': jobname},
                      {'stepname': stepname},
                      {'layernames': layernames},
                      {'erf': erf},
                      {'avoid_profile': avoid_profile},
                      {'avoid_profile_size': avoid_profile_size},
                      {'avoid_npth': avoid_npth},
                      {'avoid_npth_size': avoid_npth_size},
                      {'avoid_alone_drill': avoid_alone_drill},
                      {'avoid_alone_drill_size': avoid_alone_drill_size},
                      {'npth_add_solder_mask': npth_add_solder_mask},
                      {'npth_add_solder_mask_size': npth_add_solder_mask_size},
                      {'avoid_v_cut_size': avoid_v_cut}]                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#sliver 优化
def sliver_DFM_op(jobname, stepname, layernames, erf, max_width, max_height):
    data = {
            'func': 'SLIVER_DFM_OP',
            'paras': [{'jobname': jobname},
                      {'stepname': stepname},
                      {'layernames': layernames},
                      {'erf': erf},
                      {'max_width': max_width},
                      {'max_height': max_height}]                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#contourize
def contourize(job, step, layers, accuracy, separate_to_islands, size, mode):
    data = {
            'func': 'CONTOURIZE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'accuracy': accuracy},
                      {'separate_to_islands': separate_to_islands},
                      {'size': size},
                      {'mode': mode},]                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#identify
def file_identify(path):
    data = {
            'func': 'FILE_IDENTIFY',
            'paras': {'pathname': path}                   
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

def set_selection(is_standard, is_clear, all_layers, is_select, inside, exclude):
    data = {
            'func': 'SET_SELECTION',
            'paras': {'sels': {
                      'is_standard': is_standard,
                      'is_clear': is_clear,
                      'all_layers': all_layers,
                      'is_select': is_select,
                      'inside': inside,
                      'exclude': exclude} 
                      }              
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#去除独立pad优化
def NFP_removal_DFM(job, step, layers, erf, isolated, drill_over, duplicate, covered, work_on, pth, pth_pressfit, npth, 
                    via_laser, via, via_photo, remove_undrilled_pads, apply_to, remove_mark_NFP, ranges):
    data = {
            'func': 'NFP_REMOVAL_DFM',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'erf': erf},
                      {'isolated': isolated},
                      {'drill_over': drill_over},
                      {'duplicate': duplicate},
                      {'covered': covered},
                      {'work_on': work_on},
                      {'pth': pth},
                      {'pth_pressfit': pth_pressfit},
                      {'npth': npth},
                      {'via_laser': via_laser},
                      {'via': via},
                      {'via_photo': via_photo},
                      {'remove_undrilled_pads': remove_undrilled_pads},
                      {'apply_to': apply_to},
                      {'remove_mark_NFP': remove_mark_NFP},
                      {'ranges': ranges}]                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#neo削PAD
def New_signal_layer_DFM(job, step, layers, erf, cut_pad_touch_pad, drill_to_cu):
    data = {
        'func': 'NEW_SIGNAL_LAYER_DFM',
        'paras': [{'job': job}, 
                  {'step': step}, 
                  {'layers': layers},
                  {'erf': erf},
                  {'cut_pad_touch_pad': cut_pad_touch_pad},
                  {'drill_to_cu': drill_to_cu}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))

#设置梯形图relationship
def setRelationship(colname, rowname, relation_value, relation_ratio):
    data = {
        'func': 'SETRELATIONSHIP',
        'paras': [{'colname': colname}, 
                  {'rowname': rowname}, 
                  {'relation_value': relation_value},
                  {'relation_ratio': relation_ratio}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))

#获取梯形图relationship
def getRelationship():
    data = {
        'func': 'GETRELATIONSHIP',
        'paras': []
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret

#设置梯形图Introduction
def setIntroduction(attributename, min_resize, min_ring, opt_resize, opt_ring, is_shave):
    data = {
        'func': 'SETINTRODUCTION',
        'paras': [{'attributename': attributename}, 
                  {'min_resize': min_resize}, 
                  {'min_ring': min_ring},
                  {'opt_resize': opt_resize},
                  {'opt_ring': opt_ring},
                  {'is_shave': is_shave}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))

#获取梯形图Introduction
def getIntroduction():
    data = {
        'func': 'GETINTRODUCTION',
        'paras': []
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret


#料号另存为
def save_job_as(job, path):
    data = {
            'func': 'SAVE_JOB_AS',
            'paras': {
                      'job': job,
                      'path': path
                      }             
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

#添加pad
def add_pad(job, step, layers, layer, symbol, location_x, location_y, polarity, dcode, orient,attributes,special_angle=0 ):
    data = {
        'func': 'ADD_PAD',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'layer': layer},
                  {'symbol': symbol},
                  {'location_x': location_x},
                  {'location_y': location_y},
                  {'polarity': polarity},
                  {'dcode': dcode},
                  {'orient': orient},
                  {'attributes': attributes},
                  {'special_angle': special_angle}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#取消选中
def unselect_features(job, step, layer):
    data = {
            'func': 'UNSELECT_FEATURES',
            'paras': {
                      'job': job,
                      'step': step,
                      'layer': layer
                      }             
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

#根据筛选器取消选中
def unselect_features_by_filter(job, step, layers):
    data = {
            'func': 'UNSELECT_FEATURES_BY_FILTER',
            'paras': [
                      {'job': job},
                      {'step': step},
                      {'layer': layers}
                      ]            
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

#dms create job
def DMS_create_job(job):
    data = {
        'func': 'DMS_CREATE_JOB',
        'paras': {'job': job}
                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

def load_job_from_db(job_id, odb_jobname, db_jobname):
    data = {
        'func': 'LOADJOBFROMDB',
        'paras': {'job_id': job_id,
                    'odb_jobname': odb_jobname,
                    'db_jobname': db_jobname }
                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

def login(username, password):
    data = {
        'func': 'LOGIN',
        'paras': {'name': username,
                    'pwd': password }                    
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))
    
# #设置机器人参数
# def setParameter(layer, pa, value):
#     data = {
#         'func': 'SETPARAMETER',
#         'paras': [{'layer': layer}, 
#                   {'pa': pa}, 
#                   {'value': value}]
#     }
#     #print(json.dumps(data))
#     ret = epcam.process(json.dumps(data))

#设置机器人参数
def setParameter(rules):
    data = {
        'func': 'SETPARAMETER',
        'paras': [{'rules': rules}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret

#设置参数(整个料)
def setJobParameter(jobName,rules):
    data = {
        'func': 'SETJOBPARAMETER',
        'paras': {
                      'rules': rules,
                      'jobName': jobName
                      }   
    }
    ret = epcam.process(json.dumps(data))
    return ret

#设置参数(整个料)
def getJobParameter(jobName):
    data = {
        'func': 'GETJOBPARAMETER',
        'paras': {
                      'job': jobName
                      }   
    }
    ret = epcam.process(json.dumps(data))
    return ret

#获取机器人参数
def getParameter():
    data = {
        'func': 'GETPARAMETER',
        'paras': []
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#打开eps文件
def open_eps(job, path):
    data = {
        'func': 'OPEN_EPS',
        'paras': {
                      'job': job,
                      'path': path
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#设置分析结果
def set_layer_checklist(jobName, stepName,layerName,checkList):
    data = {
        'func': 'SET_LAYER_CHECKLIST',
        'paras': {
                      'jobName': jobName,
                      'stepName': stepName,
                      'layerName':layerName,
                      'checkList':checkList
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))
 
#translate
def file_translate(path, job, step, layer, parameters, start_time, end_time, assigned_dcodes, defect_reports):
    data = {
        'func': 'FILE_TRANSLATE',
        'paras': {
                    'path': path,
                    'job': job,
                    'step': step,
                    'layer': layer,
                    'parameters': parameters,
                    'start_time': start_time,
                    'end_time': end_time,
                    'assigned_dcodes': assigned_dcodes,
                    'defect_reports': defect_reports
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#创建料号（无路径）
def job_create(job):
    data = {
        'func': 'JOB_CREATE',
        'paras': {
                    'job': job
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#translate init
def file_translate_init(job):
    data = {
        'func': 'FILE_TRANSLATE_INIT',
        'paras': {
                    'job': job
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#创建料号（有路径）
def create_job(path, job):
    data = {
        'func': 'CREATE_JOB',
        'paras': {
                    'path': path,
                    'job': job
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))
    
#删除料号
def delete_job(job):
    data = {
            'func': 'JOB_DELETE',
            'paras': {
                      'src_jobname': job
                      }             
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

#identify eps
def identify_eps(job, path):
    data = {
            'func': 'IDENTIFY_EPS',
            'paras': {
                      'job': job,
                      'path': path
                      }           
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

def add_outline_drill(job, step, outerline_layer, drill_layer, add_drill_symbolname, move_offset_in_corner, angle_tolerance):
    data = {
        'func': 'ADD_OUTLINE_DRILL',
        'paras': [{'job': job}, 
                  {'step': step}, 
                  {'outerline_layer': outerline_layer},
                  {'drill_layer': drill_layer},
                  {'add_drill_symbolname': add_drill_symbolname},
                  {'move_offset_in_corner': move_offset_in_corner},
                  {'angle_tolerance': angle_tolerance}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))

#get_coupon_single_end_drill_positions
def get_coupon_single_end_drill_positions(xmin, ymin, xmax, ymax, x_margin, y_margin, npth_size, pth_size, pth_ring, avoid_cu_global, clearance, 
                                        pth_to_gnd_drill, min_cu_width, single_lines, differential_lines):
    data = {
        'func': 'GET_COUPON_SINGLE_END_DRILL_POSITIONS',
        'paras': {
                    'xmin': xmin,
                    'ymin': ymin,
                    'xmax': xmax,
                    'ymax': ymax,
                    'x_margin': x_margin,
                    'y_margin': y_margin,
                    'npth_size': npth_size,
                    'pth_size': pth_size,
                    'pth_ring': pth_ring,
                    'avoid_cu_global': avoid_cu_global,
                    'clearance': clearance,
                    'pth_to_gnd_drill': pth_to_gnd_drill,
                    'min_cu_width': min_cu_width,
                    'single_lines': single_lines,
                    'differential_lines': differential_lines
                    }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#index筛选
def select_feature_by_id(job, step, layer, ids):
    data = {
        'func': 'SELECT_FEATURE_BY_ID',
        'paras': {
                    'job': job,
                    'step': step,
                    'layer': layer,
                    'ids': ids
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#设置profile
def set_step_profile(job, step, points):
    data = {
        'func': 'SET_STEP_PROFILE',
        'paras': {
                    'job': job,
                    'step': step,
                    'points': points
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#change symbol
def change_feature_symbols(job, step, layers, symbol, pad_angle):
    data = {
        'func': 'CHANGE_FEATURE_SYMBOLS',
        'paras': {
                    'job': job,
                    'step': step,
                    'layers': layers,
                    'symbol': symbol,
                    'pad_angle': pad_angle
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#clip_area_use_reference
def clip_area_use_reference(jobname, stepname, work_layers, reference_layer, margin, clipcontour, featuretype):
    data = {
        'func': 'CLIP_AREA_USE_REFERENCE',
        'paras': {
                    'jobname': jobname,
                    'stepname': stepname,
                    'work_layer': work_layers,
                    'reference_layer': reference_layer,
                    'margin': margin,
                    'clipcontour': clipcontour,
                    'featuretype': featuretype
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#clip_area_use_manual
def clip_area_use_manual(jobname, stepname, layers, points, margin, clipcontour,clipinside, featuretype):
    data = {
        'func': 'CLIP_AREA_USE_MANUAL',
        'paras': {
                    'job': jobname,
                    'step': stepname,
                    'layers': layers,
                    'points': points,
                    'margin': margin,
                    'clipcontour': clipcontour,
                    'clipinside': clipinside,
                    'featuretype': featuretype
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#line2pad_new
def line2pad_new(job, step, layers):
    data = {
        'func': 'RESHAPE_LINE_TO_PAD_NEW',
        'paras': {
                    'job': job,
                    'step': step,
                    'layers': layers
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))


#pth npth开窗
def npth_and_pth_prepare_op(job, step, sm_clearance, sm_np_clearance, add_sm_pads, add_signal_pads):
    data = {
        'func': 'NPTH_AND_PTH_PREPARE_OP',
        'paras': {
                    'job': job,
                    'step': step,
                    'sm_clearance': sm_clearance,
                    'sm_np_clearance': sm_np_clearance,
                    'add_sm_pads': add_sm_pads,
                    'add_signal_pads': add_signal_pads
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#修改属性
def modify_attributes(job, step, layers, mode, attributes):
    data = {
        'func': 'MODIFY_ATTRIBUTES',
        'paras': {
                    'jobname': job,
                    'stepname': step,
                    'layernames': layers,
                    'mode': mode,
                    'attributes': attributes
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#coupon获取线的坐标
def get_coupon_drill_line_relations(xmin, ymin, xmax, ymax, x_margin, y_margin, npth_size, pth_size, pth_ring, avoid_cu_global, clearance, 
                                        pth_to_gnd_drill, min_cu_width, single_lines, differential_lines, single_group_count, diff_group_count,drill_positions):
    data = {
        'func': 'GET_COUPON_DRILL_LINE_RELATIONS',
        'paras': {
                    'xmin': xmin,
                    'ymin': ymin,
                    'xmax': xmax,
                    'ymax': ymax,
                    'x_margin': x_margin,
                    'y_margin': y_margin,
                    'npth_size': npth_size,
                    'pth_size': pth_size,
                    'pth_ring': pth_ring,
                    'avoid_cu_global': avoid_cu_global,
                    'clearance': clearance,
                    'pth_to_gnd_drill': pth_to_gnd_drill,
                    'min_cu_width': min_cu_width,
                    'single_lines': single_lines,
                    'differential_lines': differential_lines,
                    'single_group_count':single_group_count,
                    'diff_group_count':diff_group_count,
                    'drill_positions': drill_positions                    
                    }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#添加文字
def add_text(job, step, layer, symbol, fontname, text, xsize, ysize, linewidth, location_x, location_y, polarity,
            orient, version, layers, attributes,special_angle=0):
    data = {
        'func': 'ADD_TEXT',
        'paras': [{'job': job},
                  {'step': step},
                  {'layer': layer},
                  {'symbol': symbol},
                  {'fontname': fontname},
                  {'text': text},
                  {'xsize': xsize},
                  {'ysize': ysize},
                  {'linewidth': linewidth},
                  {'location_x': location_x},
                  {'location_y': location_y},
                  {'polarity': polarity},
                  {'orient': orient},
                  {'version': version},
                  {'layers': layers},
                  {'attributes': attributes},
                  {'special_angle': special_angle}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#surface2outline
def surface2outline(job, step, layers, width):
    data = {
            'func': 'SURFACE2OUTLINE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'width': width}
                      ]
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#层别比对
def layer_compare_point(jobname1, stepname1, layername1, jobname2, stepname2, layername2, 
                            tolerance = 22860, mode = True, consider_SR = True, map_layer_resolution = 5080000):
    data = {
            'func': 'LAYER_COMPARE_POINT',
            'paras': {
                        'jobname1': jobname1,
                        'stepname1': stepname1,
                        'layername1': layername1,
                        'jobname2': jobname2,
                        'stepname2': stepname2,
                        'layername2': layername2,
                        'tolerance': tolerance,
                        'global': mode,
                        'consider_SR': consider_SR,
                        'map_layer_resolution': map_layer_resolution, 
                      }                    
            }   
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#获取选中features的box
def get_selected_features_box(job, step, layers):
    data = {
            'func': 'GET_SELECTED_FEATURES_BOX',
            'paras': {
                        'job': job,
                        'step': step,
                        'layers': layers
                      }                    
            }   
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#导出
def layer_export(job, step, layer, _type, filename, gdsdbu, resize, angle, scalingX, scalingY, isReverse,
                    mirror, rotate, scale, profiletop, cw, cutprofile, mirrorpointX, mirrorpointY, rotatepointX,
                    rotatepointY, scalepointX, scalepointY, mirrordirection, cut_polygon,numberFormatL=2,numberFormatR=6,
                    zeros=2,unit=0):
    data = {
            'func': 'LAYER_EXPORT',
            'paras': {
                        'job': job,
                        'step': step,
                        'layer': layer,
                        'type': _type,
                        'filename': filename,
                        'gdsdbu': gdsdbu,
                        'resize': resize,
                        'angle': angle,
                        'scalingX': scalingX,
                        'scalingY': scalingY,
                        'isReverse': isReverse,
                        'mirror': mirror,
                        'rotate': rotate,
                        'scale': scale,
                        'profiletop': profiletop,
                        'cw': cw,
                        'cutprofile': cutprofile,
                        'mirrorpointX': mirrorpointX,
                        'mirrorpointY': mirrorpointY,
                        'rotatepointX': rotatepointX,
                        'rotatepointY': rotatepointY,
                        'scalepointX': scalepointX,
                        'scalepointY': scalepointY,
                        'mirrordirection': mirrordirection,
                        'cut_polygon': cut_polygon,
                        'numberFormatL': numberFormatL,
                        'numberFormatR': numberFormatR,
                        'zeros': zeros,
                        'unit': unit
                      }                    
            }   
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

# def layer_export(job, step, layer, _type, filename):
#     data = {
#             'func': 'LAYER_EXPORT',
#             'paras': {
#                         'job': job,
#                         'step': step,
#                         'layer': layer,
#                         'type': _type,
#                         'filename': filename
#                       }                    
#             }   
#     js = json.dumps(data)
#     print(js)
#     return epcam.process(json.dumps(data))

#获取profile polygon
def get_profile(job, step):
    data = {
            'func': 'GET_PROFILE',
            'paras': {
                        'jobname': job,
                        'stepname': step
                      }                    
            }   
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#将一个料号中某一layer的信息拷贝至另一料号中
def copy_layer_features(src_job, src_step, src_layers, dst_job, dst_step, dst_layers, mode, invert):
    data = {
            'func': 'COPY_LAYER_FEATURES',
            'paras': {
                        'src_job': src_job,
                        'src_step': src_step,
                        'src_layer': src_layers,
                        'dst_job': dst_job,
                        'dst_step': dst_step,
                        'dst_layer': dst_layers,
                        'mode': mode,
                        'invert': invert
                      }                    
            }   
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#层别比对
def layer_compare(jobname1, stepname1, layername1, jobname2, stepname2, layername2, tolerance, mode, consider_SR, 
                    comparison_map_layername, map_layer_resolution):
    data = {
            'func': 'LAYER_COMPARE',
            'paras': {
                        'jobname1': jobname1,
                        'stepname1': stepname1,
                        'layername1': layername1,
                        'jobname2': jobname2,
                        'stepname2': stepname2,
                        'layername2': layername2,
                        'tolerance': tolerance,
                        'global': mode,
                        'consider_SR': consider_SR,
                        'comparison_map_layername': comparison_map_layername,
                        'map_layer_resolution': map_layer_resolution,
                      }                    
            }   
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#图形变换
def transform(jobname,stepname,layername,mode,rotate,scale,mirror_X,mirror_Y,duplicate,datumPoint,angle,xscale,yscale,xoffset,yoffset):
    data = {
            'func': 'TRANSFORM',
            'paras': {
                        'jobname': jobname,
                        'stepname': stepname,
                        'layernames': layername,
                        'mode': mode,
                        'rotate': rotate,
                        'scale': scale,
                        'mirror_X': mirror_X,
                        'mirror_Y': mirror_Y,
                        'duplicate': duplicate,
                        'datumPoint': datumPoint,
                        'angle': angle,
                        'xscale': xscale,
                        'yscale': yscale,
                        'xoffset': xoffset,
                        'yoffset': yoffset
                     }                    
            } 
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

#自动定属性
def auto_classify_attribute(job, step, layers):
    data = {
            'func': 'AUTO_CLASSIFY_ATTRIBUTE',
            'paras': {
                        'job': job,
                        'step': step,
                        'layers': layers
                     }                    
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#自动定属性
def outline2surface(job, step, layers, can_to_pad):
    data = {
            'func': 'RESHAPE_OUTLINE_TO_SURFACE',
            'paras': {
                        'jobname': job,
                        'stepname': step,
                        'layernames': layers,
                        'can_to_pad': can_to_pad,
                     }                    
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#获取料号的usersymbol列表
def get_usersymbol_list(job):
    data = {
            'func': 'RESHAPE_OUTLINE_TO_SURFACE',
            'paras': {
                        'jobname': job
                     }                    
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#ok_step_check
def ok_step_check(result):
    data = {
            'func': 'OK_STEP_CHECK',
            'paras': [{
                        'result': result
                     }]                   
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

def silk_screen_check(job, step, layers, erf, spacing, sm_clearance, rout_clearance, smd_clearance, line_width, pad_clearance, 
                copper_coverage, hole_clearance, apply_to, use_compensated_rout):
    """
    docstring
    """
    data = {
        'func': 'DRILL_CHECK',
        'paras': [{'job': job}, 
                  {'step': step}, 
                  {'layers': layers},
                  {'erf': erf}, 
                  {'spacing': spacing}, 
                  {'sm_clearance': sm_clearance},
                  {'rout_clearance': rout_clearance}, 
                  {'smd_clearance': smd_clearance},
                  {'line_width': line_width},
                  {'pad_clearance': pad_clearance},
                  {'copper_coverage': copper_coverage},
                  {'hole_clearance': hole_clearance},
                  {'apply_to': apply_to},
                  {'use_compensated_rout': use_compensated_rout}]
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#get_step_repeat
def get_step_repeat(job,step):
    data = {
            'func':'GET_STEP_REPEAT',
            'paras':{
                'job':job,
                'step':step
            }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#get_rest_cu//残铜无孔开窗                      单位nm²
def get_rest_cu(job,step,layer,resolution_define,thickness):
    data = {
            'func':'GET_REST_CU',
            'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'or_and':'or',
                'resolution_define':resolution_define,
                'thickness':thickness,
                'holes_slots':True,
                'include_soldermask':False,
                'include_drill':True
            }
    }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

    #get_rest_cu_with_drill//残铜有孔                     单位nm²
def get_rest_cu_with_drill(job,step,layer,resolution_define,thickness):
    data = {
            'func':'GET_REST_CU_WITH_DRILL',
            'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'or_and':'or',
                'resolution_define':resolution_define,
                'thickness':thickness,
                'holes_slots':True,
                'include_soldermask':True,
                'include_drill':True
            }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

    #get_cu_solder_drill//残铜有孔开窗                     单位nm²
def get_cu_solder_drill(job,step,layer,resolution_define,thickness):
    data = {
            'func':'GET_CU_SOLDER_DRILL',
            'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'or_and':'or',
                'resolution_define':resolution_define,
                'thickness':thickness,
                'holes_slots':True,
                'include_soldermask':True,
                'include_drill':True
            }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

    #get_rest_cu_solder//残铜无孔开窗                     单位nm²
def get_rest_cu_solder(job,step,layer,resolution_define,thickness):
    data = {
            'func':'GET_REST_CU_SOLDER',
            'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'or_and':'or',
                'resolution_define':resolution_define,
                'thickness':thickness,
                'holes_slots':True,
                'include_soldermask':True,
                'include_drill':True
            }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

    #get_outlayer_cu//外层残铜有孔开窗                     单位nm²
def get_outlayer_cu(job,step,resolution_define,thickness):
    data = {
            'func':'GET_OUTLAYER_CU',
            'paras':{
                'job':job,
                'step':step,
                'layer':'',
                'or_and':'or',
                'resolution_define':resolution_define,
                'thickness':thickness,
                'holes_slots':True,
                'include_soldermask':True,
                'include_drill':True
            }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

    #get_total_square//计算总面积                    单位nm²
def get_total_square(job,step):
    data = {
            'func':'GET_TOTAL_SQUARE',
            'paras':{
                'job':job,
                'step':step,
                'layer':'',
                'or_and':'or',
                'resolution_define':0,
                'thickness':0,
                'holes_slots':True,
                'include_soldermask':True,
                'include_drill':True
            }
    }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

    #计算选中的feature的面积                     单位nm² 
def get_selected_feature_areas(job,step,layer):
    data = {
            'func':'GET_SELECTED_FEATURE_AREAS',
            'paras':{
                'job':job,
                'step':step,
                'layer':layer,
            }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

    #
def resize_polygon(input_poly,resize_value):
    data = {
            'func':'RESIZE_POLYGON',
            'paras':{
                'input_polygon':input_poly,
                'resize_value':resize_value
            }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))
    
def get_sr_coupon_plan(Panel_Height, Panel_Width, x_margin, y_margin, pannel_left, pannel_bottom,pannel_top,pannel_right,job,pcs_step,
panel_step,coupon_x_margin,coupon_y_margin,coupon_to_set_margin,npth_size,pth_size,pth_ring,avoid_cu_global,clearance,pth_to_gnd_drill,min_cu_width,single_lines,differential_lines):
    data = {
            'func': 'GET_SR_COUPON_PLAN',
            'paras': {
                        'Panel_Height': Panel_Height,
                        'Panel_Width': Panel_Width,
                        'x_margin': x_margin,
                        'y_margin': y_margin,
                        'pannel_left': pannel_left,
                        'pannel_bottom': pannel_bottom,
                        'pannel_top': pannel_top,
                        'pannel_right': pannel_right,
                        'job': job,
                        'pcs_step': pcs_step,
                        'panel_step': panel_step,
                        'coupon_x_margin': coupon_x_margin,
                        'coupon_y_margin': coupon_y_margin,
                        'coupon_to_set_margin': coupon_to_set_margin,
                        'npth_size': npth_size,
                        'pth_size': pth_size,
                        'pth_ring': pth_ring,
                        'avoid_cu_global': avoid_cu_global,
                        'clearance': clearance,
                        'pth_to_gnd_drill': pth_to_gnd_drill,
                        'min_cu_width': min_cu_width,
                        'single_lines': single_lines,
                        'differential_lines': differential_lines
                        }                    
            } 
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

def get_step_repeat(job,step):
    data = {
            'func': 'GET_STEP_REPEAT',
            'paras': {
                        'job': job,
                        'step': step
                        }                    
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

def draw_panel_picture(job,step,layer,path):
    data = {
            'func': 'DRAW_PANEL_PICTURE',
            'paras': {
                        'job': job,
                        'step': step,
                        'layer': layer,
                        'path': path
                        }                    
            } 
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

def get_all_step_repeat_steps(job,step):
    data = {
            'func': 'GET_ALL_STEP_REPEAT_STEPS',
            'paras': {
                        'job': job,
                        'step': step
                        }                    
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

# def fill_profile(job,step,layer,profile_resize,child_profile_resize,avoid_drill_size,fill_by_pattern,symbolname,dx,dy,avoid_drill=True):
#     data = {
#             'func': 'FILL_PROFILE',
#             'paras': {
#                         'job': job,
#                         'step': step,
#                         'layer':layer,
#                         'profile_resize':profile_resize,
#                         'child_profile_resize':child_profile_resize,
#                         'avoid_drill_size':avoid_drill_size,
#                         'fill_by_pattern':fill_by_pattern,  #是否选择自己的symbol填充profile true or false
#                         'symbolname':symbolname,            #fill_by_pattern为false，symbolname填空
#                         'dx':dx,
#                         'dy':dy,
#                         'avoid_drill':avoid_drill
#                         }                    
#             } 
#     js = json.dumps(data)
#     #print(js)
#     return epcam.process(json.dumps(data))

def fill_profile(job,step,layers,step_repeat_nesting,nesting_child_steps,step_margin_x,step_margin_y,max_distance_x,
                 max_distance_y,SR_step_margin_x,SR_step_margin_y,SR_max_distance_x,SR_max_distance_y,avoid_drill,
                 avoid_rout,avoid_feature,polarity):
    data = {
            'func': 'FILL_PROFILE',
            'paras': {
                        'job': job,
                        'step': step,
                        'layers':layers,
                        'step_repeat_nesting':step_repeat_nesting,
                        'nesting_child_steps':nesting_child_steps,
                        'step_margin_x':step_margin_x,
                        'step_margin_y':step_margin_y,  
                        'max_distance_x':max_distance_x,           
                        'max_distance_y':max_distance_y,
                        'SR_step_margin_x':SR_step_margin_x,
                        'SR_step_margin_y':SR_step_margin_y,
                        'SR_max_distance_x':SR_max_distance_x,
                        'SR_max_distance_y':SR_max_distance_y,
                        'avoid_drill':avoid_drill,
                        'avoid_rout':avoid_rout,
                        'avoid_feature':avoid_feature,
                        'polarity':polarity
                        }                    
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))


def use_pattern_fill_contours(jobname,stepname,layername,symbolname,dx,dy,break_partial,cut_primitive,origin_point,outline,outlinewidth,outline_invert,odd_offset = 0,even_offset = 0):
    data = {
            'func': 'USE_PATTERN_FILL_CONTOURS',
            'paras': {
                        'jobname': jobname,
                        'stepname': stepname,
                        'layername':layername,
                        'symbolname':symbolname,
                        'dx':dx,
                        'dy':dy,
                        'break_partial':break_partial,  
                        'cut_primitive':cut_primitive,          
                        'origin_point':origin_point,
                        'outline':outline,
                        'outlinewidth':outlinewidth,
                        'outline_invert':outline_invert,
                        'odd_offset':odd_offset,
                        'even_offset':even_offset
                        }                    
            } 
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

def SL_panel_banding(job):
    data = {
        'func': 'SL_PANEL_BANDING',
        'paras': {
                    'job': job
                    }                    
        } 
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

def negative_layer_to_positive(jobname,stepname,layernames):
    data = {
        'func': 'NEGATIVE_LAYER_TO_POSITIVE',
        'paras': {
                'jobname': jobname,
                'stepname': stepname,
                'layernames': layernames
                }                    
    } 
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

def translate_lines(job,step,layer,op_type,type1,select_edge):
    data = {
        'func': 'TRANSLATE_LINES',
        'paras': {
                'job': job,
                'step': step,
                'layer': layer,
                'op_type': op_type,
                'type': type1,
                'select_edge': select_edge
                }                    
    }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

def is_selected(job,step,layer):
    data = {
        'func': 'IS_SELECTED',
        'paras': {
                'job': job,
                'step': step,
                'layer': layer
                }                    
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#contourize
def reshape_contourize(jobname, stepname, layernames, accuracy, separate_to_islands,max_size, clear_mode):
    data = {
        'func': 'RESHAPE_CONTOURIZE',
        'paras': {
                    'jobname': jobname,
                    'stepname': stepname,
                    '_layernames': layernames,
                    'accuracy': accuracy, #mil 0-2.5
                    'separate_to_islands': separate_to_islands,
                    'max_size': max_size,
                    'clear_mode': clear_mode #int 0
                }   
    }
    return epcam.process(json.dumps(data))

#Guide map 
#sub_kind:sub map 需添加的类型
#panel_kind:panel map 需添加的类型
def run_map(jobname,layername,run_sub,run_panel,sub_kind,panel_kind):
    data = {
        'func': 'RUN_MAP',
        'paras': {
                    'jobname': jobname,
                    'layername': layername,
                    'run_sub': run_sub,
                    'run_panel': run_panel,
                    'sub_kind': sub_kind,
                    'panel_kind': panel_kind
                }   
    }
    return epcam.process(json.dumps(data))

def add_sub_jobname_arrow(jobname,step,layername):
    data = {
        'func': 'ADD_SUB_JOBNAME_ARROW',
        'paras': {
                    'jobname': jobname,
                    'layername': layername,
                    'step': step
                }   
    }
    return epcam.process(json.dumps(data))

def move_select_feature_to_other_step(jobname,stepname,layername,dest_stepname,delete_org):
    data = {
        'func': 'MOVE_SELECT_FEATURE_TO_OTHER_STEP',
        'paras': {
                    'jobname': jobname,
                    'layername': layername,
                    'stepname': stepname,
                    'dest_stepname':dest_stepname,
                    'delete_org':delete_org
                }   
    }
    return epcam.process(json.dumps(data))

def run_edge(job,step,maplayer,is_ol1_top,is_ol2_top,is_smt_top,is_srd_top,is_psa_top,is_laser_top,is_et_top,is_fi_top):
    data = {
        'func': 'RUN_EDGE',
        'paras': {
                    'job': job,
                    'step': step,
                    'maplayer': maplayer,
                    'is_ol1_top':is_ol1_top,
                    'is_ol2_top':is_ol2_top,
                    'is_smt_top':is_smt_top,
                    'is_srd_top':is_srd_top,
                    'is_psa_top':is_psa_top,
                    'is_laser_top':is_laser_top,
                    'is_et_top':is_et_top,
                    'is_fi_top':is_fi_top
                }   
    }
    return epcam.process(json.dumps(data))

#拷贝usersymbol至另一个料号
def copy_usersymbol_to_other_job(job1, job2, symbol1, symbol2):
    data = {
            'func': 'COPY_USERSYMBOL_TO_OTHER_JOB',
            'paras': {
                        'job1': job1,
                        'job2': job2,
                        'symbol1':symbol1,
                        'symbol2':symbol2
                        }                    
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#网格铜 
	# int dx = 0;//横向骨架线距离
	# int dy = 0;//纵向
	# int linewidth = 0;
	# int x_offset = 0;//第一条线的横向偏移
	# int y_offset = 0;//纵向
	# int angle = 0;//(0-45)
def fill_select_feature_by_grid(job,step,layer,dx,dy,linewidth,x_offset,y_offset,angle):
    data = {
            'func': 'FILL_SELECT_FEATURE_BY_GRID',
            'paras': {
                        'job': job,
                        'step': step,
                        'layer':layer,
                        'dx':dx,
                        'dy': dy,
                        'linewidth': linewidth,
                        'x_offset':x_offset,
                        'y_offset':y_offset,
                        'angle':angle
                        }                    
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

def move_selected_features_index(job,step,layers,put_last):
    data = {
            'func': 'MOVE_SELECTED_FEATURES_INDEX',
            'paras': {
                        'jobname': job,
                        'step': step,
                        'layers':layers,
                        'put_last':put_last
                        }                    
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#添加弧
def add_arc(job, step, layers, layer, symbol, start_x, start_y, end_x, end_y, center_x, center_y,cw,polarity, dcode, attributes):
    data = {
        'func': 'ADD_ARC',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'layer': layer},
                  {'symbol': symbol},
                  {'start_x': start_x},
                  {'start_y': start_y},
                  {'end_x': end_x},
                  {'end_y': end_y},
                  {'center_x': center_x},
                  {'center_y': center_y},
                  {'cw': cw},
                  {'polarity': polarity},
                  {'dcode': dcode},
                  {'attributes': attributes}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#整体移动目标层的features jobname, stepname, layername, offset_x, offset_y
def move_same_layer(jobname, stepname, layernames, offset_x, offset_y):
    data = {
            'func': 'MOVE_SAME_LAYER',
            'paras': {
                        'jobname': jobname,
                        'stepname': stepname,
                        'layername':layernames,
                        'offset_x':offset_x,
                        'offset_y':offset_y
                        }                    
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#获取step拼板信息
def get_step_header_infos(job, step):
    data = {
            'func': 'GET_STEP_HEADER_INFOS',
            'paras': {
                        'job': job,
                        'step': step
                        }
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#分类层中的polygon
def classify_polyline(job,step,layer):
    data = {
            'func': 'CLASSIFY_POLYLINE',
            'paras': {
                        'job': job,
                        'step': step,
                        'layer': layer,
                        }
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

def sel_polarity(job,step,layers,polarity,sel_type):
    data = {
        'func': 'SEL_POLARITY',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'polarity': polarity},
                  {'sel_type': sel_type}]
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#Prepare分析
def Prepare_check(job, ranges):
    data = {
        'func': 'PREPARE_CHECK',
        'paras': [{'job': job},
                  {'ranges': ranges}]
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#根据profile创建outline
    """
    layers:[]
    linewidth: 线宽nm
    """
def profile_to_outerline(job, step, layers, linewidth):
    data = {
        'func': 'PROFILE_TO_OUTERLINE',
        'paras': {'job': job,
                  'step': step,
                  'layernames': layers,
                  'linewidth': linewidth}
                  
        }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

    
#防焊分析
def solder_mask_check(job, step, layers, erf, sm_ar, sm_coverage, sm_to_rout, sliver_min, spacing_min, bridge_min, overlap,
                        drill, silver, pads, missing, coverage, spacing, rout, clearance_connection, bridge, apply_to,
                        use_compensated_rout, min_sliver_len, dist2sliver_ratio, apply_range, classify_pad_ar, ranges):
    data = {
        'func': 'SOLDER_MASK_CHECK',
        'paras': [{'job': job}, 
                  {'step': step}, 
                  {'layers': layers},
                  {'erf': erf},
                  {'sm_ar': sm_ar},
                  {'sm_coverage': sm_coverage},
                  {'sm_to_rout': sm_to_rout},
                  {'sliver_min': sliver_min},
                  {'spacing_min': spacing_min},
                  {'bridge_min': bridge_min},
                  {'overlap': overlap},
                  {'drill': drill},
                  {'silver': silver},
                  {'pads': pads},
                  {'missing': missing},
                  {'coverage': coverage},
                  {'spacing': spacing},
                  {'rout': rout},
                  {'clearance_connection': clearance_connection},
                  {'bridge': bridge},
                  {'apply_to': apply_to},
                  {'use_compensated_rout': use_compensated_rout},  
                  {'min_sliver_len': min_sliver_len}, 
                  {'dist2sliver_ratio': dist2sliver_ratio}, 
                  {'apply_range': apply_range},
                  {'classify_pad_ar': classify_pad_ar},    
                  {'ranges' : ranges}]        
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

#select_polyline
    """
    selectpolygon:[{'ix':0,'iy':0}]
    """
def select_polyline(job, step, layer, selectpolygon):
    data = {
        'func': 'SELECT_POLYLINE',
        'paras': {'job': job,
                  'step': step,
                  'layer': layer,
                  'selectpolygon': selectpolygon}
        }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

##flatten_step
def flatten_step(job, step, flatten_layer, dst_layer):
    data = {
        'func': 'FLATTEN_STEP',
        'paras': {'job': job,
                  'step': step,
                  'flatten_layer': flatten_layer,
                  'dst_layer': dst_layer}
                  
        }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

# 钻孔信息
def get_drill_info(job,step,drllayer):
    data = {
        'func': 'GET_DRILL_INFO',
        'paras': {'jobname': job, 
                  'stepname': step, 
                  'layername': drllayer
                  }
                  
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)
    
#清空撤销堆栈
def clear_all_options(job,step):
    data = {
        'func': 'CLEAR_ALL_OPTIONS',
        'paras': {'job': job, 
                  'step': step
                  }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

#identify symbol

def identify_symbol(symbolname):
    data = {
        'func': 'IDENTIFY_SYMBOL',
        'paras': {'content': symbolname    
                  }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

def is_job_open(job):
    data = {
        'func': 'IS_JOB_OPENED',
        'paras': {'jobname': job }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

def use_solid_fill_contours(jobname, stepname, layernames, solid_type, min_brush, use_arcs):
    data = {      
            "func": "USE_SOLID_FILL_CONTOURS",
            "paras":{
                        "jobname":jobname,
                        "stepname":stepname,
                        "_layernames":layernames,
                        "solid_type":solid_type,
                        "min_brush":min_brush,
                        "use_arcs":use_arcs
                        }
            }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

#存储为eps文件
def save_eps(job, path):
    data = {
        'func': 'SAVE_EPS',
        'paras': {
                      'job': job,
                      'path': path
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#导角
def rounding_line_corner(job, step,layers,radius):
    data = {
        'func': 'ROUNDING_LINE_CORNER',
        'paras': {
                      'job': job,
                      'step': step,
                      'layers': layers,
                      'radius': radius
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))
    
def get_rest_cu_rate(job,step,layer,resolution_define,thickness,cu_thickness=0,consider_rout=False):
    data = {
        'func':'GET_REST_CU_RATE',
        'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'or_and':'or',
                'holes_slots':True,
                'include_soldermask':False,
                'include_drill':True,
                'resolution_define':resolution_define,
                'thickness':thickness,
                'cu_thickness':cu_thickness,
                'consider_rout':consider_rout
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

# def get_exposed_area(job,step,layer,mode,drllayers,solderlayer,cu_thickness=0,consider_rout=False):
#     data = {
#         'func':'GET_REST_CU_RATE',
#         'paras':{
#                 'job':job,
#                 'step':step,
#                 'layer':layer,
#                 'or_and':mode,
#                 'holes_slots':True,
#                 'include_soldermask':True,
#                 'include_drill':True,
#                 'multi_mask':False,
#                 'resolution_define':25400,
#                 'thickness':0,
#                 'affect_drill_layers':drllayers,
#                 'mask_layername':solderlayer,
#                 'cu_thickness':cu_thickness,
#                 'consider_rout':consider_rout
#                 }
#             }
#     js = json.dumps(data)
#     # print(js)
#     return epcam.process(json.dumps(data))

def get_exposed_area(job, step, layer, resolution_define, thickness, cu_thickness, consider_rout, mask_layername, mask_layers, 
                     affect_drill_layers , input_num, multi_mask, holes_slots, include_soldermask, include_drill, include_edges,
                     pth_without_pad, or_and ):
    data = {
        'func':'GET_REST_CU_RATE',
        'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'resolution_define':resolution_define,
                'thickness':thickness,
                'cu_thickness':cu_thickness,
                'consider_rout':consider_rout,
                'mask_layername':mask_layername,
                'mask_layers':mask_layers,
                'affect_drill_layers':affect_drill_layers,
                'input_num':input_num,
                'multi_mask':multi_mask,
                'holes_slots':holes_slots,
                'include_soldermask':include_soldermask,
                'include_drill':include_drill,
                'include_edges':include_edges,
                'pth_without_pad':pth_without_pad,
                'or_and':or_and
                }
            }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))


#配置config path
def set_config_path(path):
    data = {
        'func': 'SET_CONFIG_PATH',
        'paras': {
                      'path': path
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#获取layer最小线宽线距的信息
def get_quote_price_info(job,step,layer):
    data = {
        'func': 'GET_QUOTE_PRICE_INFO',
        'paras': {
                    'job': job,
                    'step': step,
                    'layer': layer
                }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#制作分孔图
def drillmap_output(job,step,drilllayer,outlinelayer,outputlayer,unit):
    data = {
        'func': 'DRILLMAP_OUTPUT',
        'paras': {
                    'job': job,
                    'step': step,
                    'drilllayer': drilllayer,
                    'outlinelayer': outlinelayer,
                    'outputlayer': outputlayer,
                    'unit': unit
                }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#获取job内的usersymbol names
def get_special_symbol_names(jobname):
    data = {
        'func': 'GET_SPECIAL_SYMBOL_NAMES',
        'paras': {
                    'jobname': jobname
    }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

def layer_export2(job, step, layer, _type, filename):
    data = {
            'func': 'LAYER_EXPORT',
            'paras': {
                        'job': job,
                        'step': step,
                        'layer': layer,
                        'type': _type,
                        'filename': filename
                      }                    
            }   
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))  

# 合并铜与轮廓线
def merge_cu_edge_lines(jobname, stepname, layernames):
    data = {
        'func': 'MERGE_CU_EDGE_LINES',
        'paras': {
            'jobname': jobname,
            'stepname': stepname,
            'layernames': layernames
        }
    }
    return epcam.process(json.dumps(data))

# 输出drill
def drill2file(job, step, layer,path,isMetric,number_format_l=2,number_format_r=4,
                    zeroes=2,unit=0,tool_unit=1,x_scale=1,y_scale=1,x_anchor=0,y_anchor=0, manufacator = '', tools_order = [], canned_text_mode = 0):
    data = {
        'func': 'DRILL2FILE',
        'paras': {
            'job': job,
            'step': step,
            'layer': layer,
            'path': path,
            'isMetric': isMetric,
            'number_format_l': number_format_l,
            'number_format_r': number_format_r,
            'zeroes': zeroes,
            'unit': unit,
            'tool_unit': tool_unit,
            'x_scale': x_scale,
            'y_scale': y_scale,
            'x_anchor': x_anchor,
            'y_anchor': y_anchor,
            'manufacator': manufacator,
            'tools_order': tools_order,
            'canned_text_mode':canned_text_mode
        }
    }
    return epcam.process(json.dumps(data))

#分类层中的net
def classify_layer_net(job,step,layer):
    data = {
            'func': 'CLASSIFY_LAYER_NET',
            'paras': {
                        'job': job,
                        'step': step,
                        'layer': layer,
                        }
            } 
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

# 设置钻孔信息
def set_drill_info(job,step,drllayer,vecDrillTools):
    data = {
        'func': 'SET_DRILL_INFO',
        'paras': {'jobname': job, 
                  'stepname': step, 
                  'layername': drllayer,
                  'vecDrillTools':vecDrillTools
                  }
                  
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

def add_text_by_drill(jobname, stepname, layername, drill_name, textsize, clear_org_features, toolID_to_text):
    data = {
        'func': 'ADD_TEXT_BY_DRILL',
        'paras': {'jobname': jobname, 
                  'stepname': stepname, 
                  'layername': layername,
                  'drill_name': drill_name,
                  'textsize': textsize,
                  'clear_org_features': clear_org_features,
                  'toolID_to_text':toolID_to_text
                  }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

# 
def create_table(jobname, stepname, layername, clear_org_features, ix, iy, linewidth, rows):
    data = {
        'func': 'CREATE_TABLE',
        'paras': {'jobname': jobname, 
                  'stepname': stepname, 
                  'layername': layername,
                  'clear_org_features':clear_org_features,
                  'ix': ix,
                  'iy': iy,
                  'linewidth': linewidth,
                  'rows': rows
                  }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

#获取当前层feature数
def get_layer_feature_count(jobName, stepName, layerName):
    data = {
        'func': 'GET_LAYER_FEATURE_COUNT',
        'paras': {'jobName': jobName, 
                  'stepName': stepName, 
                  'layerName': layerName}
    }
    return epcam.process(json.dumps(data))

def via_optimization(job,step, move_stack_via, np2laser, rout2laser, np2via, rout2via, pth2via, 
        pth2laser, via2laser, via2via, laser2laser, consider_net, drill2smd, 
            same_netl, same_net_via2laser, same_net_via2via, same_net_laser2laser, vcut2laser, 
                vcut2via, vut_layer):
    data = {
        'func': 'AUTO_MOVE_DRILL_PAD',
        'paras': {
                 'job': job, 
                 'step': step,
                 'move_stack_via': move_stack_via,
                 'np2laser': np2laser,
                 'rout2laser': rout2laser,
                 'np2via': np2via,
                 'rout2via': rout2via,
                 'pth2via': pth2via,
                 'pth2laser': pth2laser,
                 'via2laser': via2laser,
                 'via2via': via2via,
                 'laser2laser': laser2laser,
                 'consider_net': consider_net,
                 'drill2smd': drill2smd,
                 'same_net_via2laser': same_net_via2laser,
                 'same_net_via2via': same_net_via2via,
                 'same_net_laser2laser': same_net_laser2laser,
                 'vcut2laser': vcut2laser,
                 'vcut2via': vcut2via,
                 'vut_layer': vut_layer
                 }
    }
    js = json.dumps(data)
    return epcam.process(js)

#配置sys attr path
def set_sysAttr_path(path):
    data = {
        'func': 'LOAD_SYSATTR',
        'paras': {
                      'path': path
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#配置user attr path
def set_userAttr_path(path):
    data = {
        'func': 'LOAD_USERATTR',
        'paras': {
                      'path': path
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))



def get_opened_jobs():
    data = {
        'func': 'GET_OPENED_JOBS'
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))



def copy_job(src_job,dst_job):
    data = {
        'func': 'COPY_JOB',
        'paras': {
                      'src_job': src_job,
                      'dst_job': dst_job
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))


#pad2line
def pad2line(job, step, layers):
    data = {
        'func': 'RESHAPE_PAD_TO_LINE',
        'paras': {
                    'job': job,
                    'step': step,
                    'layers': layers
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

def show_layer(job, step, layer):
    data = {
        'cmd': 'show_layer',
        'job': job,
        'step': step,
        'layer': layer
    }
    js = json.dumps(data)
    # print(js)
    return epcam.view_cmd(js)


def show_matrix(job):
    data = {
        'cmd': 'show_matrix',
        'job': job
    }
    js = json.dumps(data)
    # print(js)
    return epcam.view_cmd(js)


def has_profile(job, step):
    data = {
        'func': 'HAS_PROFILE',
        'paras': {
                    'job': job,
                    'step': step
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#9.21新增
def get_system_attr_defines():
    data = {
        'func': 'GET_SYSTEM_ATTR_DEFINES',
        'paras': {
                    
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

def get_user_attr_defines():
    data = {
        'func': 'GET_USER_ATTR_DEFINES',
        'paras': {
                    
                      }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))
    
def Dec2Bin(dec):
    temp = []
    result = []
    while dec:
        quo = dec % 2 #取余数
        dec = dec // 2 #商数
        temp.append(quo)
    while temp:
        result.append(temp.pop())
    return result

# 输出rout
def rout2file(job, step, layer,path,number_format_l=2,number_format_r=4,
                    zeroes=2,unit=0,tool_unit=1,x_scale=1,y_scale=1,x_anchor=0,y_anchor=0, partial_order = 0
                    , num_in_x = 0, num_in_y = 0, order_type = 0, serial_no = 0, break_arcs = False):
    data = {
        'func': 'ROUT2FILE',
        'paras': {
            'job': job,
            'step': step,
            'layer': layer,
            'path': path,
            'number_format_l': number_format_l,
            'number_format_r': number_format_r,
            'zeroes': zeroes,
            'unit': unit,
            'tool_unit': tool_unit,
            'x_scale': x_scale,
            'y_scale': y_scale,
            'x_anchor': x_anchor,
            'y_anchor': y_anchor,
            'partial_order': partial_order,
            'num_in_x': num_in_x,
            'num_in_y': num_in_y,
            'order_type': order_type,
            'serial_no': serial_no,
            'break_arcs': break_arcs
        }
    }
    return epcam.process(json.dumps(data))

#20221115
#dxf数据保存至文件
def dxf2file(job,step,layers,savePath):
    '''
    job料是eps时为带后缀全名
    savePath为全路径
    '''
    data = {
        "func":"DXF2FILE",
        "paras":{
            "job":job,
            "step":step,
            "layers":layers,
            "savePath":savePath
        }
    }
    return epcam.process(json.dumps(data))
#MI 20221115
#保存钻带数据
def save_drill_belts(job,step,infoList,copperLayerNum):
    '''
    info中单个obj参数样例
    {
        "drillBeltIndex": 1,
        "drillBeltType": 2,
        "drillLayerName": "drl1-8",
        "drillNumber": 1387,
        "endLayer": 8,
        "startLayer": 1
    }
    job料是eps时为带后缀全名
    '''
    data = {
        "func": "SAVE_DRILL_BELTS",
        "paras":{
            "job":job,
            "drillbelts":{
                "copperLayerNum": copperLayerNum,
                "info":infoList,
                "stepName": step
            }
        }
    }
    return epcam.process(json.dumps(data))
#获取已开料的钻带数据
def get_drill_belts(job):
    '''
    job料是eps时为带后缀全名
    '''
    data = {
        "func":"GET_DRILL_BELTS",
        "paras":{
            "job":job
        }
    }
    return epcam.process(json.dumps(data))
#增加一条钻带数据
def add_drill_belt(job,drillLayerName,startLayer,endLayer,drillBeltType,drillNumber):
    '''
    job料是eps时为带后缀全名
    '''
    data = {
        "func": "ADD_DRILL_BELT",
        "paras": {
            "job": job,
            "params": {
                "drillBeltType": drillBeltType,
                "drillLayerName": drillLayerName,
                "drillNumber": drillNumber,
                "endLayer": endLayer,
                "startLayer": startLayer
            }
        }
    }
    return epcam.process(json.dumps(data))
#删除一条钻带数据
def delete_drill_belt(job,index):
    '''
    job料是eps时为带后缀全名
    '''
    data = {
        "func": "DELETE_DRILL_BELT",
        "paras": {
            "job": job,
            "index":index
        }
    }
    return epcam.process(json.dumps(data))
#修改一条钻带数据
def update_drill_belt(job,index,updateDrillBeltPara):
    '''
    job料是eps时为带后缀全名
    params参数样例，参数可不全给
    {
        "drillBeltIndex": 1,
        "drillBeltType": 2,
        "drillLayerName": "drl1-8",
        "drillNumber": 1387,
        "endLayer": 8,
        "startLayer": 1
    }
    '''
    data = {
        "func": "UPDATE_DRILL_BELT",
        "paras": {
            "job": job,
            "index":index,
            "params": updateDrillBeltPara
        }
    }
    return epcam.process(json.dumps(data))
#清空该资料中钻带数据
def clear_drill_belts(job):
    '''
    job料是eps时为带后缀全名
    '''
    data = {
        "func": "CLEAR_DRILL_BELTS",
        "paras": {
            "job": job
        }
    }
    return epcam.process(json.dumps(data))
#根据已导入的cam资料的孔层信息自动化生成钻带信息
def auto_drill_belts(job,step):
    '''
    job料是eps时为带后缀全名
    '''
    data = {
        "func": "AUTO_DRILL_BELTS",
        "paras": {
            "job": job,
            "step":step
        }
    }
    return epcam.process(json.dumps(data))
#根据资料钻带索引的一条指定钻带,获取cam资料中对应的孔层名
def get_linked_cam_layer(job,index):
    '''
    job料是eps时为带后缀全名
    '''
    data = {
        "func": "GET_LINCKED_CAM_LAYER",
        "paras": {
            "job": job,
            "index":index
        }
    }
    return epcam.process(json.dumps(data))
#保存叠构数据
def save_stackup(job,stackupInfo):
    '''
    job料是eps时为带后缀全名
    stackupSample = {
        "StackUpSegment": [
            {
                "layername": "",
                "materialConductivity": 0.0,
                "materialDielectric": 0.0,
                "materialLossTangent": 0.0,
                "materialName": "",
                "materialThkTolMinus": 0.0,
                "materialThkTolPlus": 0.0,
                "segmentThk": 0.0,
                "segmentType": "COPPER"
            }
        ],
        "symmetryStatus": True,
        "totalThk": 0.0
    }
    '''
    data = {
        "func": "SAVE_STACKUP",
        "paras": {
            "job": job,
            "stackup":stackupInfo
        }
    }
    return epcam.process(json.dumps(data))
#获取资料叠构数据
def get_stackup(job):
    '''
    job料是eps时为带后缀全名
    '''
    data = {
        "func": "GET_STACKUP",
        "paras": {
            "job": job
        }
    }
    return epcam.process(json.dumps(data))
#清空资料中叠构数据
def clear_stackup(job):
    '''
    job料是eps时为带后缀全名
    '''
    data = {
        "func": "CLEAR_STACKUP",
        "paras": {
            "job": job
        }
    }
    return epcam.process(json.dumps(data))
#根据已导入的cam资料的钻带信息自动化生成叠构信息
def auto_stackup(job):
    '''
    job料是eps时为带后缀全名
    '''
    data = {
        "func": "AUTO_STACKUP",
        "paras": {
            "job": job
        }
    }
    return epcam.process(json.dumps(data))
#在资料的叠构信息中增加一层叠构信息
def add_stackup_segment(job,index,stackupParams):
    '''
    job料是eps时为带后缀全名
    {
        "layername": "l1",
        "materialName": "test",
        "segmentType": "PREPREG",
        "layerfunction": 1.1,
        "materialConductivity": 1.1,
        "conductivity_unit": 1.1,
        "materialDielectric": 1.1,
        "materialLossTangent": 1.1,
        "segmentThk": 1.1,
        "materialThkTolPlus": 1.1,
        "materialThkTolMinus": 1.1
    }
    '''
    data = {
        "func": "ADD_STACKUP_SEGMENT",
        "paras": {
            "job": job,
            "index":index,
            "params":stackupParams
        }
    }
    return epcam.process(json.dumps(data))
#删除叠构信息中某层叠构信息
def delete_stackup_segment(job,index):
    '''
    job料是eps时为带后缀全名
    '''
    data = {
        "func": "DELETE_STACKUP_SEGMENT",
        "paras": {
            "job": job,
            "index":index
        }
    }
    return epcam.process(json.dumps(data))
#修改叠构信息中某层叠构信息
def update_stackup_segment(job,index,updateParams):
    '''
    job料是eps时为带后缀全名
    {
        "layername": "l1",
        "materialName": "test",
        "segmentType": "PREPREG",
        "layerfunction": 1.1,
        "materialConductivity": 1.1,
        "conductivity_unit": 1.1,
        "materialDielectric": 1.1,
        "materialLossTangent": 1.1,
        "segmentThk": 1.1,
        "materialThkTolPlus": 1.1,
        "materialThkTolMinus": 1.1
    }
    '''
    data = {
        "func": "UPDATE_STACKUP_SEGMENT",
        "paras": {
            "job": job,
            "index":index,
            "params":updateParams
        }
    }
    return epcam.process(json.dumps(data))

#获取指定孔层下所有详情
def auto_get_drill_info(job,step,layer):
    data = {
        "func": "AUTO_GET_DRILL_INFO",
        "paras": {
            "job": job,
            "step":step,
            "layer":layer
        }
    }
    return epcam.process(json.dumps(data))

#20221129
def output_pdf(job,step,layers,layercolors,outputpath,pdfname,overlap):
    data = {
        "func": "OUTPUT_PDF",
        "paras": {
            "job": job,
            "step":step,
            "layers":layers,
            "layercolors": layercolors,
            "outputpath":outputpath,
            "pdfname":pdfname,
            "overlap":overlap
        }
    }
    return epcam.process(json.dumps(data))

def save_png(job,step,layers,xmin,ymin,xmax,ymax,picpath,picname,backcolor,layercolors):
    data = {
        "func": "OUTPUT_FIXED_PICTURE",
        "paras": {
            "job": job,
            "step":step,
            "layers":layers,
            "xmin":xmin,
            "ymin":ymin,
            "xmax": xmax,
            "ymax":ymax,
            "picpath":picpath,
            "picname":picname,
            "backcolor": backcolor,
            "layercolors":layercolors
        }
    }
    return epcam.process(json.dumps(data))

def getVersion():
    return epcam.getVersion()

def generate_rout_layer(job,step,source_layer,destination_layer,mode):
    data = {
        "func": "GENERATE_ROUT_LAYER",
        "paras": {
            "job": job,
            "step":step,
            "sourceLayer":source_layer,
            "destinationLayer":destination_layer,
            "mode":mode            
        }
    }
    return epcam.process(json.dumps(data))

# 绕pointx,pointy顺时针旋转
def Srotate(angle:int, valuex:int, valuey:int, pointx:int, pointy:int):
    if angle %180 != 0:
        sin = math.sin(math.radians(angle))
        cos = math.sqrt(1-sin**2)
    else:
        cos = math.cos(math.radians(angle))
        sin = math.sqrt(1-cos**2)
    sRotatex = (valuex-pointx)*cos + (valuey-pointy)*sin + pointx
    sRotatey = (valuey-pointy)*cos - (valuex-pointx)*sin + pointy
    return sRotatex,sRotatey
# 坐标平移
def Move(x:int, y:int, delta_x:int, delta_y:int):
    end_x = delta_x+x
    end_y = delta_y+y
    return (end_x, end_y)
# # 水平镜像
# def mirror_y(point_x:int, point_y:int,datum_x:int):
#     dx = point_x-datum_x
#     if dx>0:
#         end_x = datum_x-dx
#     elif dx<0:
#         end_x = datum_x-dx
#     elif dx == 0:
#         end_x = datum_x
#     return (end_x, point_y)

# 水平镜像
def mirror_y(point_x:int, point_y:int,datum_x:int):
    end_x = (datum_x*2)-point_x
    return (end_x, point_y)
# 坐标缩放(sx、sy为缩放系数0-1表示缩小，大于1表示扩大)(px、py为基准点坐标)
def scale(x:float, y:float, sx:float, sy:float, px:float, py:float):
    # x = inch2nm(x)
    # y = inch2nm(y)
    end_x = x*sx + px*(1-sx)
    end_y = y*sy + py*(1-sy)
    # end_x = nm2inch(end_x)
    # end_y = nm2inch(end_y)
    return (end_x, end_y)

def nm2mm(num:float):
    count = float(num/1000000)
    return count

def nm2inch(num:float):
    count = float(num/25400000)
    return count

def inch2mm(num:float):
    count = num*25.4
    return count

def inch2nm(num:float):
    count = num*25400000
    return count
# 数据转换
def data_processing(number:float, number_format_l:int, number_format_r:int, zeroes:int):
    number = str(round(number, number_format_r))
    if ('e' in number) or ('E' in number):
        number = Decimal(float(number))
    d1 = str(number).split(".")[0]
    if d1[0] == '-':
        b = len(d1)-1
        if b != number_format_l:
            d1 = d1.strip('-')
            d1 = d1.zfill(number_format_l)
            d1 = '-'+d1
    else:  
        b = len(d1)
        if zeroes == 1:
            d1 = d1
        else:
            if b != number_format_l:
                d1 = d1.zfill(number_format_l)
    if d1 == '0':
        d1 = ''
    d2 = str(number).split(".")[1]    
    c = len(d2)
    if c > number_format_r:
        d2 = d2[0:number_format_r]
    if zeroes == 0:
        pass
    else:
        if c < number_format_r:
            d2 = d2.ljust(number_format_r, '0')
    return (d1,d2)
# 槽孔数据
def slotLenth( location:dict, unit:bool, angle:float, mirror:bool, number_format_l:int, number_format_r:int, zeroes:int, pointx:float, pointy:float, delta_x:float, delta_y:float, x_scale:float, y_scale:float, x_scale_anchor=0, y_scale_anchor=0):
    xs = location['X1']
    xe = location['X2']
    ys = location['Y1']
    ye = location['Y2']
    if angle !=0:
        xs,ys = Srotate(angle,xs,ys,pointx,pointy)
        xe,ye = Srotate(angle,xe,ye,pointx,pointy)
        xs = round(xs,number_format_r)
        ys = round(ys,number_format_r)
        xe = round(xe,number_format_r)
        ye = round(ye,number_format_r)
    if mirror ==True:
        xs,ys = mirror_y(xs,ys,xs)
        xe,ye = mirror_y(xe,ye,xs)          #根据实际情况修改
    if x_scale != 1 or y_scale != 1:
        xs,ys = scale(xs,ys,x_scale,y_scale,x_scale_anchor,y_scale_anchor)
        xe,ye = scale(xe,ye,x_scale,y_scale,x_scale_anchor,y_scale_anchor)
    if delta_x != 0 or delta_y != 0:
        xs,ys = Move(xs,ys,delta_x,delta_y)
        xe,ye = Move(xe,ye,delta_x,delta_y)
    if unit == False:
        xs = nm2mm(xs)
        ys = nm2mm(ys)
        xe = nm2mm(xe)
        ye = nm2mm(ye)
    elif unit == True:
        xs = nm2inch(xs)
        ys = nm2inch(ys)
        xe = nm2inch(xe)
        ye = nm2inch(ye)
    xs = data_processing(xs,number_format_l,number_format_r,zeroes)
    ys = data_processing(ys,number_format_l,number_format_r,zeroes)
    xe = data_processing(xe,number_format_l,number_format_r,zeroes)
    ye = data_processing(ye,number_format_l,number_format_r,zeroes)
    xs = 'X'+xs[0]+xs[1]
    ys = 'Y'+ys[0]+ys[1]
    xe = 'X'+xe[0]+xe[1]
    ye = 'Y'+ye[0]+ye[1]
    digital = xs+ys+'G85'+xe+ye
    return digital
# 圆孔
def isPad(location:dict, unit:bool, angle:float, mirror:bool, number_format_l:int, number_format_r:int, zeroes:int, pointx:float,pointy:float, delta_x:float, delta_y:float, x_scale:float, y_scale:float, x_scale_anchor=0, y_scale_anchor=0):
    x,y = location['X'],location['Y']
    if angle != 0:
        x,y = Srotate(angle,x,y,pointx,pointy)
        x = round(x,number_format_r)
        y = round(y,number_format_r)
    if mirror ==True:
        x,y = mirror_y(x,y,pointx)                 #根据实际情况修改
    if x_scale != 1 or y_scale != 1:
        x,y = scale(x,y,x_scale,y_scale,x_scale_anchor, y_scale_anchor)
    if delta_x != 0 or delta_y != 0:
        x,y = Move(x,y,delta_x,delta_y)
    if unit == True:
        x = nm2inch(x)
        y = nm2inch(y)
    else:
        x = nm2mm(x)
        y = nm2mm(y)
    x = data_processing(x,number_format_l,number_format_r,zeroes)
    y = data_processing(y,number_format_l,number_format_r,zeroes)
    x = 'X'+x[0]+x[1]
    y = 'Y'+y[0]+y[1]
    xy = x+y
    return xy

#arc2line
def arc2lines(job, step, layers,radius,sel_type):
    data = {
        'func': 'ARC2LINES',
        'paras': [
                    {'job': job},
                    {'step': step},
                    {'layers': layers},
                    {'radius': radius},
                    {'sel_type':sel_type}
        ]  
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))


def save_svg(job, step, layersinfo,savepath):
    data = {
        'func': 'EXPORT_SVG',
        'paras': {'jobName': job,
                  'stepName': step, 
                  'layerNamesInfo': layersinfo,
                  'savePath':savepath
        }
    }
    return epcam.process(json.dumps(data))


def get_all_feature_info(job, step, layer,featuretype=127):
    data = {
        'func': 'GET_ALL_FEATURE_INFO',
        'paras': {'job': job, 
                  'step': step, 
                  'layer': layer,
                  'featureType':featuretype
        }
    }
    return epcam.process(json.dumps(data))

def get_user_symbol_box(job, userSymbolName):
    data = {
        'func': 'GET_USER_SYMBOL_BOX',
        'paras': {'job': job,
                  'userSymbolName': userSymbolName         
        }
    }
    return epcam.process(json.dumps(data))

#extend_slots
def changesize_0_0(angle,size,sin,cos):
    changesize={}
    if angle!=0 and angle!=90:
        xlen=size/2*cos
        ylen=size/2*sin
    else:
        xlen=size/2
        ylen=size/2
    changesize['xlen']=xlen
    changesize['ylen']=ylen
    return changesize

def changesize_0_1(angle,size,sin,cos):
    changesize={}
    if angle!=0 and angle!=90:              
        xlen=size*cos
        ylen=size*sin
    else:
        xlen=size
        ylen=size
    changesize['xlen']=xlen
    changesize['ylen']=ylen
    return changesize

def changesize_1_0(xs,xe,ys,ye,angle,size,sin,cos):
    changesize={}
    height=abs(ye-ys)*25400000
    width=abs(xe-xs)*25400000
    if angle!=0 and angle!=90: 
        lenorg=height/sin
    elif angle==0:
        lenorg=width
    elif angle==90:
        lenorg=height
    if angle!=0 and angle!=90:  
        xlen=(size-lenorg)/2*cos
        ylen=(size-lenorg)/2*sin
    else:
        xlen=(size-lenorg)/2
        ylen=(size-lenorg)/2
    changesize['xlen']=xlen
    changesize['ylen']=ylen
    return changesize

def changesize_1_1(xs,xe,ys,ye,angle,size,sin,cos):
    changesize={}
    height=abs(ye-ys)*25400000
    width=abs(xe-xs)*25400000
    if angle!=0 and angle!=90: 
        lenorg=height/sin
    elif angle==0:
        lenorg=width
    elif angle==90:
        lenorg=height
    if angle!=0 and angle!=90:  
        xlen=(size-lenorg)*cos
        ylen=(size-lenorg)*sin
    else:
        xlen=size-lenorg
        ylen=size-lenorg
    changesize['xlen']=xlen
    changesize['ylen']=ylen
    return changesize

def line_mode_0_0(xlen,ylen,info):
    location={}
    xs=info[0]['XS']
    xe=info[0]['XE']
    ys=info[0]['YS']
    ye=info[0]['YE']
    polarity=info[0]['polarity']
    if polarity=='POS':
        pol=True
    else:
        pol=False
    if xs<xe and ys<ye:
        xsnew=xs*25400000-xlen
        ysnew=ys*25400000-ylen
        xenew=xe*25400000+xlen
        yenew=ye*25400000+ylen
    elif xs<xe and ys>ye:
        xsnew=xs*25400000-xlen
        ysnew=ys*25400000+ylen
        xenew=xe*25400000+xlen
        yenew=ye*25400000-ylen
    elif xs>xe and ys<ye:
        xsnew=xs*25400000+xlen
        ysnew=ys*25400000-ylen
        xenew=xe*25400000-xlen
        yenew=ye*25400000+ylen
    elif xs>xe and ys>ye:
        xsnew=xs*25400000+xlen
        ysnew=ys*25400000+ylen
        xenew=xe*25400000-xlen
        yenew=ye*25400000-ylen
    elif xs==xe and ys<ye:
        xsnew=xs*25400000
        ysnew=ys*25400000-ylen
        xenew=xe*25400000
        yenew=ye*25400000+ylen
    elif xs==xe and ys>ye:
        xsnew=xs*25400000
        ysnew=ys*25400000+ylen
        xenew=xe*25400000
        yenew=ye*25400000-ylen
    elif xs<xe and ys==ye:
        xsnew=xs*25400000-xlen
        ysnew=ys*25400000
        xenew=xe*25400000+xlen
        yenew=ye*25400000
    elif xs>xe and ys==ye:
        xsnew=xs*25400000+xlen
        ysnew=ys*25400000
        xenew=xe*25400000-xlen
        yenew=ye*25400000
    location['xsnew']=xsnew
    location['ysnew']=ysnew
    location['xenew']=xenew
    location['yenew']=yenew
    location['pol']=pol
    return location

def line_mode_0_1(xlen,ylen,info):
    location={}
    xs=info[0]['XS']
    xe=info[0]['XE']
    ys=info[0]['YS']
    ye=info[0]['YE']
    angle=abs(info[0]['angle'])
    symbol=info[0]['symbolname']
    polarity=info[0]['polarity']
    if polarity=='POS':
        pol=True
    else:
        pol=False
    att=info[0]['attributes']
    xx=operator.le(xs,xe)
    yy=operator.le(ys,ye)
    if xx==True and yy==True and angle!=90 and angle!=0:
        xsnew=xs*25400000
        xenew=xe*25400000+xlen
        ysnew=ys*25400000
        yenew=ye*25400000+ylen
    elif xx==True and yy==False and angle!=90 and angle!=0:
        xsnew=xs*25400000
        xenew=xe*25400000+xlen
        ysnew=ys*25400000
        yenew=ye*25400000-ylen
    elif xx==False and yy==True and angle!=90 and angle!=0:
        xsnew=xs*25400000+xlen
        xenew=xe*25400000
        ysnew=ys*25400000-ylen
        yenew=ye*25400000
    elif xx==False and yy==False and angle!=90 and angle!=0:
        xsnew=xs*25400000+xlen
        xenew=xe*25400000
        ysnew=ys*25400000+ylen
        yenew=ye*25400000
    elif xx==True and angle==0:
        xsnew=xs*25400000
        xenew=xe*25400000+xlen
        ysnew=ys*25400000
        yenew=ye*25400000  
    elif xx==False and angle==0:
        xsnew=xs*25400000+xlen
        xenew=xe*25400000
        ysnew=ys*25400000
        yenew=ye*25400000
    elif yy==True and angle==90:
        xsnew=xs*25400000
        xenew=xe*25400000
        ysnew=ys*25400000
        yenew=ye*25400000+ylen
    elif yy==False and angle==90:
        xsnew=xs*25400000
        xenew=xe*25400000
        ysnew=ys*25400000+ylen
        yenew=ye*25400000
    location['xsnew']=xsnew
    location['ysnew']=ysnew
    location['xenew']=xenew
    location['yenew']=yenew
    location['symbol']=symbol
    location['pol']=pol
    location['att']=att
    return location

def line_mode_0_2(xlen,ylen,info):
    location={}
    xs=info[0]['XS']
    xe=info[0]['XE']
    ys=info[0]['YS']
    ye=info[0]['YE']
    angle=abs(info[0]['angle'])
    symbol=info[0]['symbolname']
    polarity=info[0]['polarity']
    if polarity=='POS':
        pol=True
    else:
        pol=False
    att=info[0]['attributes']
    xx=operator.le(xs,xe)
    yy=operator.le(ys,ye)
    if xx==True and yy==True and angle!=90 and angle!=0:
        xsnew=xs*25400000-xlen
        xenew=xe*25400000
        ysnew=ys*25400000-ylen
        yenew=ye*25400000
    elif xx==True and yy==False and angle!=90 and angle!=0:
        xsnew=xs*25400000-xlen
        xenew=xe*25400000
        ysnew=ys*25400000+ylen
        yenew=ye*25400000
    elif xx==False and yy==True and angle!=90 and angle!=0:
        xsnew=xs*25400000
        xenew=xe*25400000-xlen
        ysnew=ys*25400000
        yenew=ye*25400000+ylen
    elif xx==False and yy==False and angle!=90 and angle!=0:
        xsnew=xs*25400000
        xenew=xe*25400000-xlen
        ysnew=ys*25400000
        yenew=ye*25400000-ylen
    elif xx==True and angle==0:
        xsnew=xs*25400000-xlen
        xenew=xe*25400000
        ysnew=ys*25400000
        yenew=ye*25400000  
    elif xx==False and angle==0:
        xsnew=xs*25400000
        xenew=xe*25400000-xlen
        ysnew=ys*25400000
        yenew=ye*25400000
    elif yy==True and angle==90:
        xsnew=xs*25400000
        xenew=xe*25400000
        ysnew=ys*25400000-ylen
        yenew=ye*25400000
    elif yy==False and angle==90:
        xsnew=xs*25400000
        xenew=xe*25400000
        ysnew=ys*25400000
        yenew=ye*25400000-ylen
    location['xsnew']=xsnew
    location['ysnew']=ysnew
    location['xenew']=xenew
    location['yenew']=yenew
    location['symbol']=symbol
    location['pol']=pol
    location['att']=att
    return location

def line_mode_0_3(xlen,ylen,info):
    location={}
    xs=info[0]['XS']
    xe=info[0]['XE']
    ys=info[0]['YS']
    ye=info[0]['YE']
    angle=abs(info[0]['angle'])
    symbol=info[0]['symbolname']
    polarity=info[0]['polarity']
    if polarity=='POS':
        pol=True
    else:
        pol=False
    att=info[0]['attributes']
    
    xx=operator.le(xs,xe)
    yy=operator.le(ys,ye)
    if xx==True and yy==True and angle!=90 and angle!=0:
        xsnew=xs*25400000
        xenew=xe*25400000+xlen
        ysnew=ys*25400000
        yenew=ye*25400000+ylen
    elif xx==True and yy==False and angle!=90 and angle!=0:
        xsnew=xs*25400000
        xenew=xe*25400000+xlen
        ysnew=ys*25400000
        yenew=ye*25400000-ylen
    elif xx==False and yy==True and angle!=90 and angle!=0:
        xsnew=xs*25400000
        xenew=xe*25400000-xlen
        ysnew=ys*25400000
        yenew=ye*25400000+ylen
    elif xx==False and yy==False and angle!=90 and angle!=0:
        xsnew=xs*25400000
        xenew=xe*25400000-xlen
        ysnew=ys*25400000
        yenew=ye*25400000-ylen
    elif xx==True and angle==0:
        xsnew=xs*25400000
        xenew=xe*25400000+xlen
        ysnew=ys*25400000
        yenew=ye*25400000  
    elif xx==False and angle==0:
        xsnew=xs*25400000
        xenew=xe*25400000-xlen
        ysnew=ys*25400000
        yenew=ye*25400000
    elif yy==True and angle==90:
        xsnew=xs*25400000
        xenew=xe*25400000
        ysnew=ys*25400000
        yenew=ye*25400000+ylen
    elif yy==False and angle==90:
        xsnew=xs*25400000
        xenew=xe*25400000
        ysnew=ys*25400000
        yenew=ye*25400000-ylen
    location['xsnew']=xsnew
    location['ysnew']=ysnew
    location['xenew']=xenew
    location['yenew']=yenew
    location['symbol']=symbol
    location['pol']=pol
    location['att']=att
    return location

def line_mode_0_4(xlen,ylen,info):
    location={}
    xs=info[0]['XS']
    xe=info[0]['XE']
    ys=info[0]['YS']
    ye=info[0]['YE']
    angle=abs(info[0]['angle'])
    symbol=info[0]['symbolname']
    polarity=info[0]['polarity']
    if polarity=='POS':
        pol=True
    else:
        pol=False
    att=info[0]['attributes']
    xx=operator.le(xs,xe)
    yy=operator.le(ys,ye)
    if xx==True and yy==True and angle!=90 and angle!=0:
        xsnew=xs*25400000-xlen
        xenew=xe*25400000
        ysnew=ys*25400000-ylen
        yenew=ye*25400000
    elif xx==True and yy==False and angle!=90 and angle!=0:
        xsnew=xs*25400000-xlen
        xenew=xe*25400000
        ysnew=ys*25400000+ylen
        yenew=ye*25400000
    elif xx==False and yy==True and angle!=90 and angle!=0:
        xsnew=xs*25400000+xlen
        xenew=xe*25400000
        ysnew=ys*25400000-ylen
        yenew=ye*25400000
    elif xx==False and yy==False and angle!=90 and angle!=0:
        xsnew=xs*25400000+xlen
        xenew=xe*25400000
        ysnew=ys*25400000+ylen
        yenew=ye*25400000
    elif xx==True and angle==0:
        xsnew=xs*25400000-xlen
        xenew=xe*25400000
        ysnew=ys*25400000
        yenew=ye*25400000  
    elif xx==False and angle==0:
        xsnew=xs*25400000+xlen
        xenew=xe*25400000
        ysnew=ys*25400000
        yenew=ye*25400000
    elif yy==True and angle==90:
        xsnew=xs*25400000
        xenew=xe*25400000
        ysnew=ys*25400000-ylen
        yenew=ye*25400000
    elif yy==False and angle==90:
        xsnew=xs*25400000
        xenew=xe*25400000
        ysnew=ys*25400000+ylen
        yenew=ye*25400000
    location['xsnew']=xsnew
    location['ysnew']=ysnew
    location['xenew']=xenew
    location['yenew']=yenew
    location['symbol']=symbol
    location['pol']=pol
    location['att']=att
    return location

def line_mode_1_0(xlen,ylen,info):
    location={}
    polarity=info[0]['polarity']
    if polarity=='POS':
        pol=True
    else:
        pol=False 
    new=line_mode_0_0(xlen,ylen,info)
    location['xsnew']=new['xsnew']
    location['ysnew']=new['ysnew']
    location['xenew']=new['xenew']
    location['yenew']=new['yenew']
    location['pol']=pol
    return location

def line_mode_1_1(xlen,ylen,info):
    location={}
    polarity=info[0]['polarity']
    if polarity=='POS':
        pol=True
    else:
        pol=False
    new=line_mode_0_1(xlen,ylen,info)
    location['xsnew']=new['xsnew']
    location['ysnew']=new['ysnew']
    location['xenew']=new['xenew']
    location['yenew']=new['yenew']
    location['pol']=pol
    return location

def line_mode_1_2(xlen,ylen,info):
    location={}
    polarity=info[0]['polarity']
    if polarity=='POS':
        pol=True
    else:
        pol=False
    new=line_mode_0_2(xlen,ylen,info)
    location['xsnew']=new['xsnew']
    location['ysnew']=new['ysnew']
    location['xenew']=new['xenew']
    location['yenew']=new['yenew']
    location['pol']=pol
    return location

def line_mode_1_3(xlen,ylen,info):
    location={}
    polarity=info[0]['polarity']
    if polarity=='POS':
        pol=True
    else:
        pol=False
    new=line_mode_0_3(xlen,ylen,info)
    location['xsnew']=new['xsnew']
    location['ysnew']=new['ysnew']
    location['xenew']=new['xenew']
    location['yenew']=new['yenew']
    location['pol']=pol
    return location

def line_mode_1_4(xlen,ylen,info):
    location={}
    polarity=info[0]['polarity']
    if polarity=='POS':
        pol=True
    else:
        pol=False
    new=line_mode_0_4(xlen,ylen,info)
    location['xsnew']=new['xsnew']
    location['ysnew']=new['ysnew']
    location['xenew']=new['xenew']
    location['yenew']=new['yenew']
    location['pol']=pol
    return location

def change_datum_0_0():
    location={}
    location['x']=0
    location['y']=0
    return location

def change_datum_0_1(xsize, ysize, size, sin, cos, sepcial_angle, vertical_angle, angle, mirror):
    location={}
    if 0 < angle < 90 or 180 < angle < 270:
        aa=True
    elif 90 < angle < 180 or 270 < angle < 360:
        aa=False
    if  sepcial_angle == True and vertical_angle == False:
        location['x'] = size/2
        location['y'] = 0
    elif  sepcial_angle == True:
        location['x'] = 0
        location['y'] = size/2
    elif xsize < ysize and mirror == False and aa == True:
        location['x'] = size/2*cos
        location['y'] = size/2*sin
    elif xsize < ysize and mirror == True and aa == True:
        location['x'] = size/2*cos
        location['y'] = -size/2*sin
    elif xsize < ysize and mirror == False and aa == False:
        location['x'] = size/2*cos
        location['y'] = -size/2*sin
    elif xsize < ysize and mirror == True and aa == False:
        location['x'] = size/2*cos
        location['y'] = size/2*sin
    elif xsize > ysize and mirror == False and aa == True:
        location['x'] = size/2*sin
        location['y'] = -size/2*cos
    elif xsize > ysize and mirror == True and aa == True:
        #改
        location['x'] = size/2*sin
        location['y'] = size/2*cos
    elif xsize > ysize and mirror == False and aa == False:
        #改
        location['x'] = size/2*sin
        location['y'] = size/2*cos
    elif xsize > ysize and mirror == True and aa == False:
        #改
        location['x'] = size/2*sin
        location['y'] = -size/2*cos    
    return location

def change_datum_0_2(xsize, ysize, size, sin, cos, sepcial_angle, vertical_angle, angle, mirror):
    location={}
    if 0 < angle < 90 or 180 < angle < 270:
        aa = True
    elif 90 < angle < 180 or 270 < angle < 360:
        aa = False
    if  xsize < ysize and sepcial_angle == True and vertical_angle == False:
        location['x'] = -size/2
        location['y'] = 0
    elif xsize < ysize and sepcial_angle == True:
        location['x'] = 0
        location['y'] = -size/2
    elif xsize>ysize and sepcial_angle == True and vertical_angle == False:
        location['x'] = -size/2
        location['y'] = 0
    elif xsize > ysize and vertical_angle == True:
        location['x'] = 0
        location['y'] = -size/2
    #2023.10.19改
    elif  xsize > ysize and mirror == False and aa == True:
        location['x'] = -size/2*sin
        location['y'] = size/2*cos
    elif  xsize < ysize and mirror == False and aa == True:
        location['x'] = -size/2*cos
        location['y'] = -size/2*sin
    elif xsize > ysize and mirror==True and aa==True:
        location['x'] = -size/2*sin
        location['y'] = -size/2*cos
    elif xsize < ysize and mirror==True and aa==True:
        location['x'] = -size/2*cos
        location['y'] = size/2*sin
    elif xsize < ysize and mirror == False and aa == False:
        location['x'] = -size/2*cos
        location['y'] = size/2*sin
    elif xsize > ysize and mirror == False and aa == False:
        location['x'] = -size/2*sin
        location['y'] = -size/2*cos
    elif xsize > ysize and mirror == True and aa == False:
        location['x'] = -size/2*sin
        location['y'] = size/2*cos
    elif xsize < ysize and mirror == True and aa == False:
        location['x'] = -size/2*cos
        location['y'] = -size/2*sin
    return location

def change_datum_0_3(xsize, ysize, size, sin, cos, angle, mirror, datum):
    location = {}
    if datum == 3:
        i = 1
    elif datum == 4:
        i = -1
    if angle == 0 or angle == 360:
        angle = 0
    if xsize < ysize :
        if angle == 0 :
            location['x'] = 0
            location['y'] = size/2*i
        elif angle == 180 :
            location['x'] = 0
            location['y'] = -size/2*i
        elif angle == 90 :
            location['x'] = size/2*i
            location['y'] = 0
        elif angle == 270 :
            location['x'] = -size/2*i
            location['y'] = 0
        elif 0 <angle < 90 and mirror == False:
            location['x'] = size/2*cos*i
            location['y'] = size/2*sin*i
        elif 0<angle<90 and mirror == True:
            location['x'] = -size/2*cos*i
            location['y'] = size/2*sin*i
        elif 90 < angle < 180 and mirror == False:
            location['x'] = size/2*cos*i
            location['y'] = -size/2*sin*i
        elif 90 < angle < 180 and mirror == True:
            location['x'] = -size/2*cos*i
            location['y'] = -size/2*sin*i
        elif 180 < angle < 270 and mirror == False:
            location['x'] = -size/2*cos*i
            location['y'] = -size/2*sin*i
        elif 180 < angle < 270 and mirror == True:
            location['x'] = size/2*cos*i
            location['y'] = -size/2*sin*i
        elif 270 < angle < 360 and mirror == False:
            location['x'] = -size/2*cos*i
            location['y'] = size/2*sin*i
        elif 270 < angle < 360 and mirror == True:
            location['x'] = size/2*cos*i
            location['y'] = size/2*sin*i
    elif xsize > ysize :
        if angle == 0 :
            location['x'] = size/2*i
            location['y'] = 0
        elif angle == 180 :
            location['x'] = -size/2*i
            location['y'] = 0
        elif angle ==90 :
            location['x'] = 0
            location['y'] = -size/2*i
        elif angle == 270 :
            location['x'] = 0
            location['y'] = size/2*i
        elif 0 < angle < 90 and mirror == False:
            #2023.10.19改(此mode往下所有判断中sin、cos修改)
            location['x'] = size/2*sin*i
            location['y'] = -size/2*cos*i
        elif 0 < angle < 90 and mirror == True:
            location['x'] = size/2*sin*i
            location['y'] = size/2*cos*i
        elif 90 < angle < 180 and mirror == False: 
            location['x'] = -size/2*sin*i
            location['y'] = -size/2*cos*i
        elif 90 < angle < 180 and mirror == True:    
            location['x'] = -size/2*sin*i
            location['y'] = size/2*cos*i
        elif 180 < angle < 270 and mirror == False:           
            location['x'] = -size/2*sin*i
            location['y'] = size/2*cos*i
        elif 180 < angle < 270 and mirror == True:
            location['x'] = -size/2*sin*i
            location['y'] = -size/2*cos*i
        elif 270 < angle < 360 and mirror == False:
            location['x'] = size/2*sin*i
            location['y'] = size/2*cos*i
        elif 270 < angle < 360 and mirror == True:
            location['x'] = size/2*sin*i
            location['y'] = -size/2*cos*i
    return location
       
def change_datum_1_1(xsize, ysize, size, sin, cos, sepcial_angle, vertical_angle, angle, mirror, datum):
    location = {}
    if datum == 1:
        i = 1
    elif datum == 2 :
        i = -1
    if 0 < angle < 90 or 180 < angle < 270:
        aa = 1
    elif 90 < angle < 180 or 270 < angle < 360:
        aa = 2
    if  xsize < ysize and sepcial_angle == True and vertical_angle == False:
        location['x'] = (size-ysize*25400)/2*i
        location['y'] = 0
    elif xsize < ysize and sepcial_angle == True:
        location['x'] = 0
        location['y'] = (size-ysize*25400)/2*i
    elif xsize > ysize and sepcial_angle == True and vertical_angle == False:
        location['x'] = (size-xsize*25400)/2*i
        location['y'] = 0
    elif xsize > ysize and sepcial_angle == True:
        location['x'] = 0
        location['y'] = (size-xsize*25400)/2*i
    elif xsize < ysize and mirror == False and aa == 1:
        location['x'] = (size-ysize*25400)/2*cos*i
        location['y'] = (size-ysize*25400)/2*sin*i
    elif xsize > ysize and mirror == False and aa == 1:
        #2023.10.19改
        location['x'] = (size-xsize*25400)/2*sin*i
        location['y'] = -(size-xsize*25400)/2*cos*i
    elif xsize < ysize and mirror == True and aa == 1:
        location['x'] = (size-ysize*25400)/2*cos*i
        location['y'] = -(size-ysize*25400)/2*sin*i
    elif xsize > ysize and mirror == True and aa == 1:
        #2023.10.19改
        location['x'] = (size-xsize*25400)/2*sin*i
        location['y'] = (size-xsize*25400)/2*cos*i
    elif xsize < ysize and mirror == False and aa == 2:
        location['x'] = (size-ysize*25400)/2*cos*i
        location['y'] = -(size-ysize*25400)/2*sin*i
    elif xsize > ysize and mirror == False and aa == 2:
        #2023.10.19改
        location['x'] = (size-xsize*25400)/2*sin*i
        location['y'] = (size-xsize*25400)/2*cos*i
    elif xsize < ysize and mirror == True and aa == 2:
        location['x'] = (size-ysize*25400)/2*cos*i
        location['y'] = (size-ysize*25400)/2*sin*i
    elif xsize > ysize and mirror == True and aa == 2:
        #2023.10.19改
        location['x'] = (size-xsize*25400)/2*sin*i
        location['y'] = -(size-xsize*25400)/2*cos*i
    return location

def change_datum_1_3(xsize, ysize, size, sin, cos, angle, mirror, datum):
    location = {}
    if datum == 3:
        i = 1
    elif datum == 4:
        i = -1
    if angle == 0 or angle == 360:
        angle = 0
    if xsize < ysize :
        if angle == 0 :
            location['x'] = 0
            location['y'] = (size-ysize*25400)/2*i
        elif angle == 180 :
            location['x'] = 0
            location['y'] = -(size-ysize*25400)/2*i
        elif angle == 90 :
            location['x'] = (size-ysize*25400)/2*i
            location['y'] = 0
        elif angle == 270 :
            location['x'] = -(size-ysize*25400)/2*i
            location['y'] = 0
        elif 0 < angle < 90 and mirror == False:
            location['x'] = (size-ysize*25400)/2*cos*i
            location['y'] = (size-ysize*25400)/2*sin*i
        elif 0 < angle < 90 and mirror == True:
            location['x'] = -(size-ysize*25400)/2*cos*i
            location['y'] = (size-ysize*25400)/2*sin*i
        elif 90 < angle < 180 and mirror == False:
            location['x'] = (size-ysize*25400)/2*cos*i
            location['y'] = -(size-ysize*25400)/2*sin*i
        elif 90 < angle < 180 and mirror == True:
            location['x'] = -(size-ysize*25400)/2*cos*i
            location['y'] = -(size-ysize*25400)/2*sin*i
        elif 180 < angle < 270 and mirror == False:
            location['x'] = -(size-ysize*25400)/2*cos*i
            location['y'] = -(size-ysize*25400)/2*sin*i
        elif 180 < angle < 270 and mirror == True:
            location['x'] = (size-ysize*25400)/2*cos*i
            location['y'] = -(size-ysize*25400)/2*sin*i
        elif 270 < angle < 360 and mirror == False:
            location['x'] = -(size-ysize*25400)/2*cos*i
            location['y'] = (size-ysize*25400)/2*sin*i
        elif 270 < angle < 360 and mirror == True:
            location['x'] = (size-ysize*25400)/2*cos*i
            location['y'] = (size-ysize*25400)/2*sin*i
    elif xsize > ysize :
        if angle == 0 :
            location['x'] = (size-xsize*25400)/2*i
            location['y'] = 0
        elif angle == 180 :
            location['x'] = -(size-xsize*25400)/2*i
            location['y'] = 0
        elif angle == 90 :
            location['x'] = 0
            location['y'] = -(size-xsize*25400)/2*i
        elif angle == 270 :
            location['x'] = 0
            location['y'] = (size-xsize*25400)/2*i
        elif 0 < angle < 90 and mirror == False:
            #2023.10.19改(此mode往下所有判断中sin、cos修改)
            location['x'] = (size-xsize*25400)/2*sin*i
            location['y'] = -(size-xsize*25400)/2*cos*i
        elif 0 < angle < 90 and mirror == True:
            location['x'] = (size-xsize*25400)/2*sin*i
            location['y'] = (size-xsize*25400)/2*cos*i
        elif 90 < angle < 180 and mirror == False:
            location['x'] = -(size-xsize*25400)/2*sin*i
            location['y'] = -(size-xsize*25400)/2*cos*i
        elif 90 < angle < 180 and mirror == True:
            location['x'] = -(size-xsize*25400)/2*sin*i
            location['y'] = (size-xsize*25400)/2*cos*i
        elif 180 < angle < 270 and mirror == False:
            location['x'] = -(size-xsize*25400)/2*sin*i
            location['y'] = (size-xsize*25400)/2*cos*i
        elif 180 < angle < 270 and mirror == True:
            location['x'] = -(size-xsize*25400)/2*sin*i
            location['y'] = -(size-xsize*25400)/2*cos*i
        elif 270 < angle < 360 and mirror == False:
            location['x'] = (size-xsize*25400)/2*sin*i
            location['y'] = (size-xsize*25400)/2*cos*i
        elif 270 < angle < 360 and mirror == True:
            location['x'] = (size-xsize*25400)/2*sin*i
            location['y'] = -(size-xsize*25400)/2*cos*i
    return location 

def oval_mode_0_0(xlen,ylen,sepcial_angle,xsize,ysize):
    location={}
    if  xsize>ysize and sepcial_angle==True:
        xnew=xsize+xlen
        ynew=ysize
    elif xsize>ysize and sepcial_angle==False:
        xnew=xsize+xlen
        ynew=ysize
    elif xsize<ysize and sepcial_angle==True:
        xnew=xsize
        ynew=ysize+ylen
    elif xsize<ysize and sepcial_angle==False:
        xnew=xsize
        ynew=ysize+ylen
    location['xnew']=xnew
    location['ynew']=ynew
    return location

def oval_mode_1_0(xsize,ysize,size):
    location={}
    if xsize>ysize:
        xnew=size/1000000/25.4*1000
        ynew=ysize
    else:
        xnew=xsize
        ynew=size/1000000/25.4*1000
    location['xnew']=xnew
    location['ynew']=ynew  
    return location

def near_hole_splitter(holeSize, holeSpacing,inPoints):
    data = {
        'func': 'NEAR_HOLE_SPLITTER',
        'paras': {'holeSize': holeSize,
                  'holeSpacing': holeSpacing,
                  'inPoints':inPoints
        }
    }
    return epcam.process(json.dumps(data))

def _init():
    global _global_dict
    _global_dict={}

def set_value(key,value):
    _global_dict[key]=value

def get_value(key):
    try:
        return _global_dict[key]
    except:
        print('读取'+key+'失败\r\n')


def refresh_joblist(jobname, stepname):
    data = {
        'func': 'REFRESH_JOBLIST',
        'paras': {
                'jobname': jobname,
                'stepname':stepname
                }   
    }
    #print(json.dumps(data))
    return epcam.uiprocess(json.dumps(data))

    
def close_all_layer(jobname, stepname):
    data = {
        'func': 'CLOSE_ALL_LAYER',
        'paras': {
                'jobname': jobname,
                'stepname':stepname
                }   
    }
    #print(json.dumps(data))
    return epcam.uiprocess(json.dumps(data))

def display_layers(job, step, clayer = '', snaplayer = '', displaylayers = [], affectedlayers = []):
    data = {
        'func': 'DISPLAY_LAYERS',
        'paras': {
                'jobname': job,
                'stepname':step,
                'clayer':clayer,
                'snaplayer':snaplayer,
                'displaylayers':displaylayers,
                'affectedlayers':affectedlayers
                }   
    }
    #print(json.dumps(data))
    return epcam.uiprocess(json.dumps(data))

def set_layer_infos(job,layerInfo,oldAndNewlayerParams):
    data = {
        'func': 'SET_LAYER_INFOS',
        'paras': {
                'job': job,
                'layerInfo':layerInfo,
                'oldAndNewlayerParams': oldAndNewlayerParams
                }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))


def get_fill_param():
    data = {
        'func': 'GET_FILL_PARAM',
        'paras': {
                
                }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

def set_fill_param(fillType,gridParams,patternParams,solidParams):
    data = {
        'func': 'SET_FILL_PARAM',
        'paras': {
                'fillType': fillType,
                'gridParams':gridParams,
                'patternParams': patternParams,
                'solidParams': solidParams
                }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))



def step_flip(job,step):
    data = {
        'func': 'STEP_FLIP',
        'paras': {
                'job': job,
                'step':step
                }   
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

def pcsAnalysis(job, step, path):
    data = {
        'cmd': 'pcsAnalysis',
        'job': job,
        'step': step,
        'path': path
    }  
    return epcam.pcsAnalysis(json.dumps(data))

def read_auto_matrix_rule(path):
    data = {
        'cmd': 'readPathFactoryJson',
        'path': path
    }  
    return epcam.readPathFactoryJson(json.dumps(data))

def read_auto_matrix_template(path):
    data = {
        'cmd': 'readPathTemplateConfigJson',
        'path': path
    }  
    return epcam.readPathTemplateConfigJson(json.dumps(data))

def auto_matrix(nameList):
    data = {
        'cmd': 'getMatchedLayers',
        'NameList': nameList
    }  
    return epcam.getMatchedLayers(json.dumps(data))

def saveNewMatchRule(matchRule, path, ruleName):
    data = {
        'cmd': 'saveNewMatchRule',
        'MatchRule': matchRule,
        'path': path,
        'RuleName': ruleName
    }  
    return epcam.saveNewMatchRule(json.dumps(data))

def getSignalLayers(layerInfos):
    signalLayers = []
    for v in layerInfos:
        if v["type"] == "signal":
            signalLayers.append(v['name'])
    return signalLayers

def typeMatchLayer2LayerInfo(matchLayers, layerInfos, oldList, newList, signalNames = []):
    for vv in matchLayers:
        layerInfo = {}
        layerInfo['type'] = vv['attr']['type']
        layerInfo['name'] = vv['newname']
        layerInfo['context'] = vv['attr']['context']
        layerInfo['polarity'] = vv['attr']['polarity']
        layerInfo['start_name'] = ""
        layerInfo['end_name'] = ""
        layerInfo['old_name'] = vv['oldname']
        layerInfo['row'] = len(layerInfos) + 1
        if vv["LayerType"] == "drill":
            start_index = vv['attr']['startindex']
            end_index = vv['attr']['endindex']
            if (start_index < len(signalNames)) and (end_index < len(signalNames)):
                layerInfo['start_name'] = signalNames[start_index]
                layerInfo['end_name'] = signalNames[end_index]
        #nameMap.append({vv['oldname'] : vv['newname']})
        oldList.append(vv['oldname'])
        newList.append(vv['newname'])
        layerInfos.append(layerInfo)

def matchLayers2LayerInfos(matchLayers):
    layerInfos = []
    oldList = []
    newList = []
    solderPasteTop = []
    silkScreenTop = []
    solderMaskTop = []
    signalTop = []
    signalInner = []
    signalBot = []
    solderMaskBot = []
    silkScreenBot = []
    solderPasteBot = []
    drill = []
    for v in matchLayers:
        if v["LayerType"] == "solder-paste-top":
            solderPasteTop = v['MatchedLayer']
        if v["LayerType"] == "silk-screen-top":
            silkScreenTop = v['MatchedLayer']
        if v["LayerType"] == "solder-mask-top":
            solderMaskTop = v['MatchedLayer']
        if v["LayerType"] == "signal-top":
            signalTop = v['MatchedLayer']
        if v["LayerType"] == "signal-inner":
            signalInner = v['MatchedLayer']
        if v["LayerType"] == "signal-bot":
            signalBot = v['MatchedLayer']
        if v["LayerType"] == "solder-mask-bot":
            solderMaskBot = v['MatchedLayer']
        if v["LayerType"] == "silk-screen-bot":
            silkScreenBot = v['MatchedLayer']
        if v["LayerType"] == "solder-paste-bot":
            solderPasteBot = v['MatchedLayer']
        if v["LayerType"] == "drill":
            drill = v['MatchedLayer']
    typeMatchLayer2LayerInfo(solderPasteTop, layerInfos, oldList, newList)
    typeMatchLayer2LayerInfo(silkScreenTop, layerInfos, oldList, newList)
    typeMatchLayer2LayerInfo(solderMaskTop, layerInfos, oldList, newList)
    typeMatchLayer2LayerInfo(signalTop, layerInfos, oldList, newList)
    typeMatchLayer2LayerInfo(signalInner, layerInfos, oldList, newList)
    typeMatchLayer2LayerInfo(signalBot, layerInfos, oldList, newList)
    typeMatchLayer2LayerInfo(solderMaskBot, layerInfos, oldList, newList)
    typeMatchLayer2LayerInfo(silkScreenBot, layerInfos, oldList, newList)
    typeMatchLayer2LayerInfo(solderPasteBot, layerInfos, oldList, newList)
    signalNames = getSignalLayers(layerInfos)
    typeMatchLayer2LayerInfo(drill, layerInfos, oldList, newList, signalNames)
    return (layerInfos, oldList, newList)

def get_layer_attributes(job,step,layer):
    data = {
        'func': 'GET_LAYER_ATTRIBUTES',
        'paras': {
            'job': job, #string
            'step': step, #string
            'layer': layer #string
        }
    }
    return epcam.process(json.dumps(data))

def edit_layer_attributes(job,step,layer,edit_mode,edit_attr_name,edit_attr_value):
    data = {
        'func': 'EDIT_LAYER_ATTRIBUTES',
        'paras': {
            'job': job, #string
            'step': step, #string
            'layer': layer, #string
            'editMode': edit_mode, #int
            'editAttrName': edit_attr_name,#string
            'editAttrValue': edit_attr_value #string
        }
    }
    return epcam.process(json.dumps(data))

def get_step_attributes(job,step):
    data = {
        'func': 'GET_STEP_ATTRIBUTES',
        'paras': {
            'job': job, #string
            'step': step #string
        }
    }
    return epcam.process(json.dumps(data))

def edit_step_attributes(job,step,edit_mode,edit_attr_name,edit_attr_value):
    data = {
        'func': 'EDIT_STEP_ATTRIBUTES',
        'paras': {
            'job': job, #string
            'step': step, #string
            'editMode': edit_mode, #int
            'editAttrName': edit_attr_name,#string
            'editAttrValue': edit_attr_value #string
        }
    }
    return epcam.process(json.dumps(data))


def change_to_guide_tool(jobname, stepname, type):
    data = {
        'func': 'CHANGE_TO_GUIDE_TOOL',
        'paras': {
                'jobname': jobname,
                'stepname':stepname,
                'type':type
                }   
    }
    #print(json.dumps(data))
    return epcam.uiprocess(json.dumps(data))

def change_to_last_tool(jobname, stepname):
    data = {
        'func': 'CHANGE_TO_LAST_TOOL',
        'paras': {
                'jobname': jobname,
                'stepname':stepname
                }   
    }
    #print(json.dumps(data))
    return epcam.uiprocess(json.dumps(data))

def get_clicked_point(jobname, stepname):
    data = {
        'func': 'GET_CLICKED_POINT',
        'paras': {
                'jobname': jobname,
                'stepname':stepname
                }   
    }
    #print(json.dumps(data))
    return epcam.uiprocess(json.dumps(data))

def get_clicked_box(jobname, stepname):
    data = {
        'func': 'GET_CLICKED_BOX',
        'paras': {
                'jobname': jobname,
                'stepname':stepname
                }   
    }
    #print(json.dumps(data))
    return epcam.uiprocess(json.dumps(data))

def layer_box(job,step,layers):
    data = {
        'func': 'LAYER_BOX',
        'paras': {
            'job': job, 
            'step': step, 
            'layers': layers
        }
    }
    return epcam.process(json.dumps(data))

def check_rout_output(job,step,layer):
    data = {
        'func': 'CHECK_ROUT_OUTPUT',
        'paras': {
            'job': job, 
            'step': step, 
            'sourceLayer': layer
        }
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

def edit_selected_features_attributes(job,step,layer,mode,attributes):
    data = {
        'func': 'EDIT_SELECTED_FEATURES_ATTRIBUTES',
        'paras': {
            'job': job, 
            'step': step, 
            'layer': layer,
            'mode': mode, 
            'attributes': attributes
        }
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

def get_actived_step_info(job):
    data = {
        'func': 'GET_ACTIVED_STEP_INFO',
        'paras': {
            'jobname': job    
                }   
    }
    #print(json.dumps(data))
    return epcam.uiprocess(json.dumps(data))


def add_chain(job,step,layer,chain_number,first_index,comp,is_CCW,add_plunge,toolsize,rout_flag=0,feed=0,speed=0):
    data = {
        'func': 'ADDCHAIN',
        'paras': {
            'job': job, 
            'step': step, 
            'layer': layer,
            'chainNumber': chain_number, 
            'firstIndex': first_index,
            'comp': comp, 
            'isCCW': is_CCW, 
            'addPlunge': add_plunge,
            'toolSize': toolsize,
            'routflag': rout_flag, 
            'feed': feed,
            'speed': speed
        }
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

def get_all_features_report_flattern(job,step,layer):
    data = {
        'func': 'GET_ALL_FEATURES_REPORT_FLATTERN',
        'paras': {
            'job': job, 
            'step': step, 
            'layer': layer       
        }
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))


def select_features_by_net(job,step,layer,vec_dest_layername,use_select_info,selectpolygon):
    data = {
        'func': 'SELECT_FEATURES_BY_NET',
        'paras': {
            'jobname': job, 
            'stepname': step, 
            'layername': layer,  
            'vec_dest_layername': vec_dest_layername, 
            'use_select_info': use_select_info, 
            'selectpolygon': selectpolygon
        }
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

def usersymbol_is_used(job,symbolname):
    data = {
        'func': 'USERSYMBOL_IS_USED',
        'paras': {
            'job': job, 
            'symbolName': symbolname
        }
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

def delete_usersymbol(job,symbolname):
    data = {
        'func': 'DELETE_USERSYMBOL',
        'paras': {
            'job': job, 
            'symbolName': symbolname
        }
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

def rename_usersymbol(job,oldname,newname):
    data = {
        'func': 'RENAME_USERSYMBOL',
        'paras': {
            'job': job, 
            'oldName': oldname,
            'newName': newname
        }
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

def set_symbol_ui_data(oldstr, unit):
    data = {
        'func': 'SET_SYMBOL_UI_DATA',
        'paras': {
                'oldstr': oldstr,
                'unit':unit
                }   
    }
    #print(json.dumps(data))
    return epcam.uiprocess(json.dumps(data))


def uploadFileAny(filePath, remoteFile, bucket = ''):
    data = {
        'cmd': 'uploadFileAny',
        'filePath': filePath,
        'remoteFile': remoteFile,
        'bucket': bucket
    }  
    return epcam.uploadFileAny(json.dumps(data))

def uploadFile_Any(filePath, remoteFile, bucket = ''):
    timestamp = datetime.now().timestamp()
    times = str(timestamp)
    remoteFile = remoteFile + '_' + times
    ret = uploadFileAny(filePath, remoteFile, bucket)
    return json.loads(ret)




def uploadFile_OSS_getUrl(jobname):
    
    epsname=jobname+'.eps'
    outputpath=os.path.dirname(os.path.realpath(__file__))+'/'+'epsoutput+++'
    if  os.path.exists(outputpath):
        print(outputpath)
    else:
        os.mkdir(outputpath)

    savepath=outputpath+'/'+epsname
    setJobParameter(jobname,jobname)
    save_eps(jobname,savepath)
    open_eps('neweps',savepath)
    ret=get_opened_jobs()
    openjobs=json.loads(ret)['paras']
    if 'neweps' not in openjobs:
        return ''
    else:
        epssaved=True
    file_path = savepath
    file_url2=uploadFile_Any(file_path,epsname)['url']
    if epssaved==True:
        os.unlink(savepath)
    return file_url2

def auto_drill_rout_plan(inpoints,exefolderpath,exeruntimes,itertrial,mindist,has_startpoint=False,startpoint={}):
    data = {
        'func': 'AUTO_DRILL_ROUT_PLAN',
        'paras': {
            'inPoints': inpoints, 
            'exeFolderPath': exefolderpath,
            'exeRunTimes': exeruntimes,
            'iterTrial':itertrial,
            'minDist':mindist,
            'hasStartPoint':has_startpoint,
            'startPoint':startpoint
        }
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

def select_features_to_usersymbol(job,step,layer,usersymbol_name,centerx,centery):
    data = {
        'func':'SELECT_FEATURES_TO_USERSYMBOL',
        'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'userSymbolName':usersymbol_name,
                'centerX':centerx,
                'centerY':centery
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

def get_usersymbol_box(job,symbolname):
    data = {
        'func':'GET_USERSYMBOL_BOX',
        'paras':{
                'job':job,
                'symbol_name':symbolname
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

def get_selection():
    data = {
        'func':'GET_SELECTION',
        'paras':{
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

def layer_net_analysis(orig_job,orig_step,work_job,work_step,layers,net_points_type,analysis_type,orig_net_type,work_net_type):
    data = {
        'func':'LAYER_NET_ANALYSIS',
        'paras':{
                'orig_job':orig_job,
                'orig_step':orig_step,
                'work_job':work_job,
                'work_step':work_step,
                'layers':layers,
                'net_points_type':net_points_type,
                'analysis_type':analysis_type,
                'orig_net_type':orig_net_type,
                'work_net_type':work_net_type
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

def net_analysis(orig_job,orig_step,work_job,work_step,layers,net_points_type,analysis_type,orig_net_type,work_net_type):
    data = {
        'func':'NET_ANALYSIS',
        'paras':{
                'orig_job':orig_job,
                'orig_step':orig_step,
                'work_job':work_job,
                'work_step':work_step,
                'layers':layers,
                'net_points_type':net_points_type,
                'analysis_type':analysis_type,
                'orig_net_type':orig_net_type,
                'work_net_type':work_net_type
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

def get_job_attributes(job):
    data = {
        'func':'GET_JOB_ATTRIBUTES',
        'paras':{
                'job':job
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

def get_usersymbol_attributes(job,usersymbol):
    data = {
        'func':'GET_USERSYMBOL_ATTRIBUTES',
        'paras':{
                'job':job,
                'userSymbol':usersymbol
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

def edit_usersymbol_attributes(job,usersymbol_name,edit_mode,edit_attrname,edit_attrvalue):
    data = {
        'func':'EDIT_USERSYMBOL_ATTRIBUTES',
        'paras':{
                'job':job,
                'userSymbolName':usersymbol_name,
                'editMode':edit_mode,
                'editAttrName':edit_attrname,
                'editAttrValue':edit_attrvalue
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

def edit_job_attributes(job,edit_mode,edit_attrname,edit_attrvalue):
    data = {
        'func':'EDIT_JOB_ATTRIBUTES',
        'paras':{
                'job':job,
                'editMode':edit_mode,
                'editAttrName':edit_attrname,
                'editAttrValue':edit_attrvalue
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

def construct_pads(job,step,layer,tolerance):
    data = {
        'func':'CONSTRUCT_PADS',
        'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'tolerance':tolerance
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

def add_tail_drill(job, step, layer, type, mode, split, order, method, distance, distance_t, min_size, max_size, min_hits, size_list ):
    data = {
        'func':'ADD_TAIL_DRILL',
        'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'type':type,
                'mode':mode,
                'split':split,
                'order':order,
                'method':method,
                'distance':distance,
                'distance_t':distance_t,
                'min_size':min_size,
                'max_size':max_size,
                'min_hits':min_hits,
                'size_list':size_list
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

def refresh_all_flip_step(job):
    data = {
        'func':'REFRESH_ALL_FLIP_STEP',
        'paras':{
                'job':job
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

def refresh_flip_step(job, step):
    data = {
        'func':'REFRESH_FLIP_STEP',
        'paras':{
                'job':job,
                'step':step
                }
            }
    js = json.dumps(data)
    # print(js)
    return epcam.process(json.dumps(data))

def split_layer_with_featuretype(job, step, layer):
    data = {
        'func': 'SPLIT_LAYER_WITH_FEATURE_TYPE',
        'paras': {
            'job': job,
            'step': step,
            'layer': layer
        }
    }
    return epcam.process(json.dumps(data))

def split_layer_with_attribute(job, step, layer):
    data = {
        'func': 'SPLIT_LAYER_WITH_ATTRIBUTE',
        'paras': {
            'job': job,
            'step': step,
            'layer': layer
        }
    }
    return epcam.process(json.dumps(data))

def Zero(size:float,accuracy:int):
    try:
        size = str(round(size,accuracy))
        size_l = size.split(".")[0]
        size_r = size.split(".")[1]
        length = len(size_r)
        if length != accuracy:
            size_r = size_r.ljust(accuracy,'0')
            size = size_l+'.'+size_r
        return size
    except Exception as e:
        print(e)

def Deduplication(data):
    ab = []
    THolesize = []
    for b in data:
        THolesize.append(b['iHoleSize'])
    for e in range(0,len(data)):
        if e in ab:
            pass
        else:
            hole = data[e]['iHoleSize']
            if (THolesize.count(hole) != 1) and (data[e]['dType'] != 'TEXT'):
                for t in range(e+1,len(data)):
                    iholesize = data[t]['iHoleSize']
                    if (hole == iholesize) and (data[t]['dType'] != 'TEXT'):
                        (data[e]['vLocations']).extend(data[t]['vLocations'])
                        (data[e]['vLocations_slots']).extend(data[t]['vLocations_slots'])
                        (data[e]['iCount']) = (data[e]['iCount'])+(data[t]['iCount'])
                        ab.append(t)
    data = [n for i, n in enumerate(data) if i not in ab]
    index = 1
    for i in data:
        i['iToolIdx'] = index
        index = index+1
    return data


def delete_splited_layers(job, step, layer):
    data = {
        'func': 'DELETE_SPLITED_LAYERS',
        'paras': {
            'job': job,
            'step': step,
            'layer': layer
        }
    }
    return epcam.process(json.dumps(data)) 

def recovery_splited_layers(job, step, layer):
    data = {
        'func': 'RECOVERY_SPLITED_LAYERS',
        'paras': {
            'job': job,
            'step': step,
            'layer': layer
        }
    }
    return epcam.process(json.dumps(data)) 

def connections(job, step, layers, interaction_type, radius, sel_type, connect_type = 0, blend_type = False):
    data = {
        'func': 'CONNECTIONS',
        'paras': {
            'job': job,
            'step': step,
            'layers': layers,
            'connect_type':connect_type,
            'interaction_type':interaction_type,
            'radius':radius,
            'blend_type':blend_type,
            'sel_type':sel_type
        }
    }
    return epcam.process(json.dumps(data)) 

def get_symbol_name(job, step, layer,points):
    data = {
        'func': 'GET_SYMBOL_NAME',
        'paras': {
            'jobname': job,
            'stepname': step,
            'layername': layer,
            'points':points
        }
    }
    return epcam.process(json.dumps(data)) 

def get_specified_text_infos(job, step, layer,font):
    data = {
        'func': 'GET_SPECIFIED_TEXT_INFOS',
        'paras': {
            'job': job,
            'step': step,
            'layer': layer,
            'font':font
        }
    }
    return epcam.process(json.dumps(data)) 

def undo(job, step):
    data = {
        'func': 'UNDO',
        'paras': {
            'jobname': job,
            'stepname': step
        }
    }
    return epcam.process(json.dumps(data))

def load_font(job, fontfolder):
    data = {
        'func': 'LOAD_FONT',
        'paras': {
            'job': job,
            'fontFolder': fontfolder
        }
    }
    return epcam.process(json.dumps(data))

def get_text_name(job, step, layer, points):
    data = {
        'func': 'GET_TEXT_NAME',
        'paras': {
            'jobname': job,
            'stepname': step,
            'layername': layer,
            'points': points
        }
    }
    return epcam.process(json.dumps(data))

def clean_surface_hole(job, step, layers, maxsize, clearmode):
    data = {
        'func': 'CLEAN_SURFACE_HOLE',
        'paras': {
            'job': job, 
            'step': step,
            'layers': layers,
            'maxSize':maxsize,
            'clearMode':clearmode
        }
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

def holesize2symbol(size):
    try:
        size_inch = "{:.3f}".format(size/25400).rstrip("0").rstrip(".")
        symbol_name = 'r' + str(size_inch)
        return symbol_name
    except Exception as e:
        print(e)
    return False

def job_detailed_copy(src_path, src_job, dst_path, dst_job, include_steps, include_layers, steps, layers):
    data = {
        'func': 'JOB_DETAILED_COPY',
        'paras': {
            'src_path': src_path, 
            'src_jobname': src_job,
            'dst_path': dst_path,
            'dst_jobname':dst_job,
            'include_steps':include_steps,
            'include_layers': include_layers,
            'steps':steps,
            'layers':layers
        }
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

def change_line(job, step, layer, feature_index, start_x, start_y, end_x, end_y):
    data = {
        'func': 'CHANGE_LINE',
        'paras': {
            'job': job, 
            'step': step,
            'layer': layer,
            'feature_index': feature_index,
            'start': {
                'ix': start_x,
                'iy': start_y
            },
            'end': {
                'ix': end_x,
                'iy': end_y
            }
        }
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

def get_rout_feature_info(job, step, layer):
    data = {
        'func': 'GET_ROUT_FEATURE_INFO',
        'paras': {
            'job': job, 
            'step': step,
            'layer': layer
        }
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

#非中文
def check_reg_text_name(textlist):
    pattern = '^[^\u4e00-\u9fa5]{0,}$'
    result = True
    for item in textlist:
        if not re.search(pattern, item):
            result = False
            break     
    return result

#检测非法字符
def check_reg_illegal_charactor(textlist):
    pattern = '((?=[\x20-\x7e]+)[^A-Za-z0-9\_\+\-])'
    result = True
    for item in textlist:
        if  re.search(pattern,item):
            result = False
            break     
    return result