from epkernel import BASE,epcam
from tkinter import *
from tkinter.font import *
import os,sys,json

def refresh_joblist(job:str, step:str):
  try:
    BASE.refresh_joblist(job,step)
  except Exception as e:
    print(e)

def close_all_layer(job:str, step:str):
  try:
    BASE.close_all_layer(job,step)
  except Exception as e:
    print(e)

def display_layers(job:str, step:str, clayer:str = '',snaplayer:str = '', displaylayers:list = [], affectedlayers:list = []):
  try:
    BASE.display_layers(job, step, clayer, snaplayer, displaylayers, affectedlayers)
  except Exception as e:
    print(e)

def change_to_guide_tool(job:str, step:str, type:int=0):
  try:
    BASE.change_to_guide_tool(job, step, type)
  except Exception as e:
    print(e)

def change_to_last_tool(job:str, step:str):
  try:
    BASE.change_to_last_tool(job, step)
  except Exception as e:
    print(e)

def get_clicked_point(job:str, step:str)->dict:
  try:
    point = BASE.get_clicked_point(job, step)
    point = json.loads(point)['paras']
    return point
  except Exception as e:
    print(e)
    return None

def get_clicked_box(job:str, step:str)->dict:
  try:
    box = BASE.get_clicked_box(job, step)
    box = json.loads(box)['paras']
    return box
  except Exception as e:
    print(e)
    return None

def change_to_point_tool(job:str, step:str, tips:str = '')->dict:
  try:
    def on_tool_clicked():
        change_to_guide_tool(job, step, 1)
    def on_ctn_clicked():
        change_to_guide_tool(job, step, 1)
        ret = get_clicked_point(job, step)
        return_str.append(ret)
        change_to_last_tool(job, step)
        root_window.destroy()
    # -*- coding:utf-8 -*-
    # 调用Tk()创建主窗口
    return_str = []
    if tips == '':
        tips = '请单击选择合适的坐标'
    change_to_guide_tool(job, step, 1)
    root_window = Tk(baseName = '提示')
    root_window.transient()
    root_window.attributes('-topmost', 'true')
    root_window.resizable(0, 0)
    # 给主窗口起一个名字，也就是窗口的名字
    root_window.title('Guide提示')
    main_frame = Frame(root_window, bg = 'yellow')
    main_frame.place(relwidth=1, relheight=1)
    cfg_path = epcam.get_config_path()
    if cfg_path != None:
      logo_path = os.path.join(os.path.join(cfg_path, 'Resources'), 'logo.ico')
      if os.path.exists(logo_path):
        root_window.iconbitmap(logo_path)
    root_window.geometry('330x100+234+45')
    fontStyle = Font(size = 18)
    tips_lb = Label(main_frame, text = tips, borderwidth=2, font = fontStyle, fg='red', bg='yellow')
    # lb_width = tips_lb.
    tool_btn = Button(main_frame, text = '工具', bg = 'cyan', command = on_tool_clicked)
    ctn_btn = Button(main_frame, text = '继续', command = on_ctn_clicked, bg = 'lime')
    tips_lb.place(x=10, y=26)
    tool_btn.place(x=275, y = 26, width=50, height = 30)
    ctn_btn.place(x=115, y = 65, width=100, height = 30)
    #开启主循环，让窗口处于显示状态
    root_window.mainloop()
    return return_str
  except Exception as e:
    print(e)
    return {}

def change_to_box_tool(job:str, step:str, tips:str = '')->dict:
  try:
    def on_tool_clicked():
        change_to_guide_tool(job, step, 0)
    def on_ctn_clicked():
        change_to_guide_tool(job, step, 0)
        ret = get_clicked_box(job, step)
        return_str.append(ret)
        change_to_last_tool(job, step)
        root_window.destroy()
    # -*- coding:utf-8 -*-
    # 调用Tk()创建主窗口
    return_str = []
    if tips == '':
        tips = '请框选合适的位置'
    change_to_guide_tool(job, step, 0)
    root_window = Tk(baseName = '提示')
    root_window.attributes('-topmost', 'true')
    root_window.resizable(False, False)
    # 给主窗口起一个名字，也就是窗口的名字
    root_window.title('Guide提示')
    main_frame = Frame(root_window, bg = 'yellow')
    main_frame.place(relwidth=1, relheight=1)
    cfg_path = epcam.get_config_path()
    if cfg_path != None:
      logo_path = os.path.join(os.path.join(cfg_path, 'Resources'), 'logo.ico')
      if os.path.exists(logo_path):
        root_window.iconbitmap(logo_path)
    root_window.geometry('330x100+234+45')
    fontStyle = Font(size = 18)
    tips_lb = Label(main_frame, text = tips, borderwidth=2, font = fontStyle, fg='red', bg='yellow', anchor=CENTER)
    # lb_width = tips_lb.
    tool_btn = Button(main_frame, text = '工具', bg = 'cyan', command = on_tool_clicked)
    ctn_btn = Button(main_frame, text = '继续', command = on_ctn_clicked, bg = 'lime')
    tips_lb.place(x=10, y=26)
    tool_btn.place(x=275, y = 26, width=50, height = 30)
    ctn_btn.place(x=115, y = 65, width=100, height = 30)
    #开启主循环，让窗口处于显示状态
    root_window.mainloop()
    return return_str
  except Exception as e:
    print(e)
    return {}

def get_active_step(job:str)->str:
  try:
    ret = BASE.get_actived_step_info(job)
    ret = json.loads(ret)['paras']['step']
    return ret
  except Exception as e:
    print(e)
    return ''

def get_work_layer(job:str)->str:
  try:
    ret = BASE.get_actived_step_info(job)
    ret = json.loads(ret)['paras']['c_layer']
    return ret
  except Exception as e:
    print(e)
    return ''

def get_affected_layers(job:str)->list:
  try:
    ret = BASE.get_actived_step_info(job)
    ret = json.loads(ret)['paras']['affect_layers']
    return ret
  except Exception as e:
    print(e)
    return []





