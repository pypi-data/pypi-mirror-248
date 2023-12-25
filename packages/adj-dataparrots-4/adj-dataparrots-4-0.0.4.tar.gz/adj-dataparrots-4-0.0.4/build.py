import os
import shutil
import compileall
import sys

base_path = os.path.dirname(os.path.realpath(__file__))
_, project_name = os.path.split(base_path)
dest_path = os.path.join(base_path, 'releases', f'{project_name}')
exclude_list = ('releases', '.git', 'logs', '.gitignore', 'migrations', 'accesstoken.json', 'issues.txt', 'sample questions.txt', 'todo.txt')
 
def clear_dest_dir(path):
    if os.path.exists(path):
        dir_list = os.listdir(path)
        for e in dir_list:
            full_path = os.path.join(path, e)
            if os.path.isdir(full_path):
                clear_dest_dir(full_path)
            else:
                print(f'Removing {full_path}')
                os.remove(full_path)

def clear_source_dir(path):
    dir_list = os.listdir(path)
    for e in dir_list:
        if e not in exclude_list:
            full_path = os.path.join(path, e)
            if os.path.isdir(full_path) and e == '__pycache__':
                pyc_list = os.listdir(full_path)
                for f in pyc_list:
                    print(f'Removing: {os.path.join(full_path, f)}')
                    os.remove(os.path.join(full_path, f))
            elif os.path.isdir(full_path):
                clear_source_dir(full_path)
            else:                    
                pass
                
def walk_dir(path):
    dir_list = os.listdir(path)
    for e in dir_list:
        if e not in exclude_list:
            full_path = os.path.join(path, e)
            if os.path.isdir(full_path) and e == '__pycache__':
                dest_full_path = dest_path + path[len(base_path):]
                pyc_list = os.listdir(full_path)
                for f in pyc_list:
                    print(f)
                    d = f.split('.')
                    d = d[0] + '.' + d[2]
                    print(f'Copying: {os.path.join(full_path, f)} to: {os.path.join(dest_full_path, d)}')
                    shutil.copy(os.path.join(full_path, f), os.path.join(dest_full_path, d))
            elif os.path.isdir(full_path):
                dest_full_path = dest_path + full_path[len(base_path):]
                print(f'creating directory: {dest_full_path}')
                os.makedirs(dest_full_path, exist_ok=True)
                walk_dir(full_path)
            else:                    
                dest_full_path = dest_path + full_path[len(base_path):]
                if dest_full_path[-3:] != '.py':
                    print(f'Copying: {full_path} to: {dest_full_path}')
                    shutil.copy(full_path, dest_full_path)

if __name__ == "__main__":
    print(len(sys.argv))
    
    if len(sys.argv) < 2:
        print("please include version!")
    else:
        dest_path += '_' +sys.argv[1]
        print(f'Project Name: {project_name}, Base Dir: {base_path}, Target Dir: {dest_path}')
        print(f'Exclusion List: {exclude_list}')

        print(f'Clearing: {dest_path}')
        clear_dest_dir(dest_path)
        
        print(f'Clearing: {base_path}')
        #clear_source_dir(base_path)
        
        #compileall.compile_dir(base_path)        
        
        os.makedirs(dest_path, exist_ok=True)
        walk_dir(base_path)
