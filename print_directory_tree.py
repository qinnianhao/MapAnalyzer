import os
 
def print_directory_tree(root_path):
    for root, dirs, files in os.walk(root_path):
        level = root.replace(root_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')
 
# 使用示例
root_path = r'E:\0_GIT\QY130833_MCU_SW\WuLin_QY130833_TC397XP_Tasking\0_Src\ASW'  # 替换为你的目录路径
print_directory_tree(root_path)