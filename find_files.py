import os, re
import os.path as path

your_directory=r"E:\0_GIT\QY130833_MCU_SW\WuLin_QY130833_TC397XP_Tasking\0_Src\ASW\Feature\slprj\autosar"
# for dirpath, dirnames, filenames in os.walk(your_directory):
#     print("Current directory path: ", dirpath)
#     print("Subdirectories in current directory: ", dirnames)
#     print("Files in current directory: ", filenames)

def find_files(pattern, base='.'):
    """Finds files under base based on pattern
    Walks the filesystem starting at base and 
    returns a list of filenames matching pattern"""

    regex = re.compile(pattern)
    matches = []
    for root, dirs, files in os.walk(base):
        for f in files:
            if regex.match(f):
                matches.append( path.join(root,f) )
    return matches

def find_dirs(pattern, base='.'):
    """Finds directories under base based on pattern
    Walks the filesystem starting at base and 
    returns a list of directory names matching pattern"""

    regex = re.compile(pattern)
    matches = []
    for root, dirs, files in os.walk(base):
        for d in dirs:
            if regex.match(d):
                matches.append( path.join(root,d) )
    return matches

def find_all(pattern, base='.'):
    """Finds files and folders under base based on pattern
    Returns the combined results of find_files and find_dirs"""
    
    matches = find_dirs(pattern,base)
    matches += find_files(pattern,base)
    return matches

def find_all_2(pattern, base='.'):
    """Finds files and folders under base based on pattern.
    Walks the filesystem starting at base and 
    returns a list of file and folder names matching pattern"""

    regex = re.compile(pattern)
    matches = []
    for root, dirs, files in os.walk(base):
        for d in dirs:
            if regex.match(d):
                matches.append( path.join(root,d) )
        for f in files:
            if regex.match(f):
                matches.append( path.join(root,f) )
    return matches

def filter_files(pattern, base='.'):
    """Finds files and folders under base omitting those matching pattern
    Walks the filesystem starting at base and 
    returns a list of file and folder names except those matching pattern"""

    regex = re.compile(pattern)
    matches = []
    for root, dirs, files in os.walk(base):
        for f in files:
            if not regex.match(f):
                matches.append( path.join(root,f) )
    return matches
def apply_to_files(pattern, function, base='.'):
    ''' Apply function to any files matching pattern
    function should take a full file path as an argument
    the return value, if any, will be ignored '''

    regex = re.compile(pattern)
    errors = []
    for root, dirs, files in os.walk(base):
        for f in files:
            if regex.match(f):
                try: function( path.join(root,f) )
                except: errors.append(path.join(root,f))
    return errors

if __name__ == '__main__':
    # pattern = r'Ctrl_LON'
    # path = r'E:\0_GIT\QY130833_MCU_SW\WuLin_QY130833_TC397XP_Tasking\0_Src\ASW\Feature\slprj\autosar'
    # print(find_files(pattern, path))
    # print(find_dirs(pattern, path))
    # print(find_all(pattern, path))
    # print(find_all_2(pattern, path))
    # print(filter_files(pattern, path))
    # print(find_files(pattern, path))
    print('Testing module file_tree.py')
    print("result of find_files('.*')")
    print( find_files('.*') )
    print("result of find_dirs('.*')")
    print( find_dirs('.*') )
    print("result of find_all_1('.*')")
    print( find_all('.*') )
    print("result of find_all_2('.*')")
    print( find_all_2('.*') )
    print("result of filter_files('.*')")
    print( filter_files('.*') )
    print("result of apply_to_files('.*', lambda fn: print(fn.upper())")
    print( apply_to_files('.*', lambda fn: print(fn.upper()) ))
