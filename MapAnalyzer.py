import os
import xlwt
import time
from tkinter.filedialog import askopenfilename
from pos_process import pos_process

memory_list = []
section_list = []

def read_mapfile(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines

def split_line(data):
    data = [i.split('|') for i in data]
    return data

def pre_process(path, memory_list,section_list):
    rawfile = read_mapfile(path)
    rawlist =split_line(rawfile)
    counter = 0
    for item in rawlist:
        if len(item) == 8:
            item = [i.strip() for i in item] #去除前后空格
            # item.pop(0) SS
            if item[1] != '': # 剔除无效行
                if counter == 0:
                    memory_list.append(item)
                else:
                    section_list.append(item)
                if item[1] == 'Total':
                    counter= counter+1             
    return

def write_excel(path, list1,list2):
    wb = xlwt.Workbook()
    ws1 = wb.add_sheet('sheet1')
    ws2 = wb.add_sheet('sheet2')
    ws3 = wb.add_sheet('sheet3')
    ws4 = wb.add_sheet('sheet4')

    for i in range(len(list1)):
        for j in range(len(list1[i])):
            ws1.write(i, j, list1[i][j])
    for i in range(len(list2)):
        for j in range(len(list2[i])):
            ws2.write(i, j, list2[i][j])
    wb.save(path) 
         
if __name__ == '__main__':
    print("请选择Tasking编译器生成的*.map文件：")
    map_path = askopenfilename(title="选择文件", filetypes=[("map文件", "*.map")])
    print(map_path)
    f = os.path.basename(map_path).split(".")[0]+'_'+ time.strftime('%Y%m%d%H%M%S')
    file_pre = f+'_pre.xlsx'
    file_pos = f+'_pos.xlsx'

    print("预处理...")
    pre_process(map_path, memory_list, section_list)
    write_excel(file_pre, memory_list, section_list)
    print('预处理完成,生成：'+ file_pre)

    print('后处理...')
    pos_process(file_pre, file_pos, os.path.dirname(map_path))
    print('后处理完成,生成：'+ file_pos)
