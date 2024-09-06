import os
import re
import pandas as pd  # 导入 pandas 库
import numpy as np
from find_files import find_files

def Add_FilePath(df,dir):
    df['p0'] = np.nan
    df['p1'] = np.nan
    df['p2'] = np.nan
    df['p3'] = np.nan
    df['p4'] = np.nan
    df['p5'] = np.nan
    df['p6'] = np.nan
    for i in range(len(df)):
        try:
            filename=find_files(df.loc[i, '[in] File'],dir)
            print(filename)
            paths=filename[0].split('\\')
            for j in range(len(paths)):
                if j>6:break
                title = 'p'+str(j)
                df.loc[i, title] = paths[j]
        except:
            pass
    return df

def delete_files_by_extensions(root_dir, extensions):
    """
    删除指定目录下的所有子目录及文件，这些文件具有特定的扩展名。
    参数:
    root_dir: 要清理的目录的根目录。
    extensions: 要删除的文件的扩展名列表。
    """
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(tuple(extensions)):
                os.remove(os.path.join(root, file))

def pos_process(excel_file, excel_file_out, debug_path):
    # Step 1、Sheet1处理，将16进制转换易读的kb bytes数。
    df1 = pd.read_excel(excel_file, sheet_name='sheet1')
    df1['Code(Kb)'] = np.nan
    df1['Data(Kb)'] = np.nan
    df1['Reserved(Kb)'] = np.nan
    df1['Free(Kb)'] = np.nan
    df1['Total(Kb)'] = np.nan
    try:
        df1['Code(Kb)'] = df1['Code'].apply(lambda x: int(x, base=16))/1024
        df1['Data(Kb)'] = df1['Data'].apply(lambda x: int(x, base=16))/1024
        df1['Reserved(Kb)'] = df1['Reserved'].apply(lambda x: int(x, base=16))/1024
        df1['Free(Kb)'] = df1['Free'].apply(lambda x: int(x, base=16))/1024
        df1['Total(Kb)'] = df1['Total'].apply(lambda x: int(x, base=16))/1024
    except:
        pass

    # Step 2、Sheet2处理，将16进制转换易读的kb bytes数，获取Section的类型。    
    df2 = pd.read_excel(excel_file, sheet_name='sheet2')
    df2['Section'] = np.any
    df2['Size'] = np.nan

    for i in range(len(df2)):
        try:
            df2.loc[i, 'Section'] = re.split(r'[;,. ]', df2.loc[i, '[out] Section'])[1]
        except:
            pass
        try:
            df2.loc[i, 'Size'] = int(df2.loc[i, '[out] Size (MAU)'],16)/1024
        except:
            pass

    # Step 3、删除Debug中除*.o外的文件，节省Step4的耗时。
    directory_path = debug_path
    extensions_to_delete = ['.d', '.opt', '.src','.mk']
    delete_files_by_extensions(directory_path, extensions_to_delete)

    # Step 4、分析、增加文件的路径，方便筛选、透析，耗时很长。
    df2 = Add_FilePath(df2, debug_path)

    # Step 5、写入excel表
    with pd.ExcelWriter(excel_file_out, engine='openpyxl') as writer:
        df1.to_excel(writer, sheet_name='sheet1', index=False)  # 写入第一个 Sheet
        df2.to_excel(writer, sheet_name='sheet2', index=False)  # 写入第二个 Sheet

if __name__ == '__main__':
    excel_file = r'WuLin_QY130833_TC397XP_Tasking_20240905142326.xlsx'
    excel_file_out = r'multiple_sheets_example.xlsx'  # 设定输出的文件名
    debug_path = r'.\Debug'
    pos_process(excel_file,excel_file_out,debug_path)

