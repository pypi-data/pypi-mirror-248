import datetime
from pathlib import Path
import os
import shutil
import compileall


def package(root_path="./", reserve_one=False):
    """
    编译根目录下的包括子目录里的所有py文件成pyc文件到新的文件夹下
    如果只保留一份文件，请将需编译的目录备份，因为本程序会清空该源文件夹
    :param root_path: 需编译的目录
    :param reserve_one: 是否只保留一个目录
    :return:
    """
    root = Path(root_path)

    # 先删除根目录下的pyc文件和__pycache__文件夹
    for src_file in root.rglob("*.pyc"):
        os.remove(src_file)
    for src_file in root.rglob("__pycache__"):
        os.rmdir(src_file)

    current_day = datetime.date.today()  # 当前日期
    edition = "1.0"  # 设置版本号

    dest = Path(root.parent / f"{root.name}_{edition}.{'001'}_beta_{current_day}")  # 目标文件夹名称

    if os.path.exists(dest):
        shutil.rmtree(dest)

    shutil.copytree(root, dest)

    compileall.compile_dir(root, force=True)  # 将项目下的py都编译成pyc文件

    for src_file in root.glob("**/*.pyc"):  # 遍历所有pyc文件
        relative_path = src_file.relative_to(root)  # pyc文件对应模块文件夹名称
        dest_folder = dest / str(relative_path.parent.parent)  # 在目标文件夹下创建同名模块文件夹
        os.makedirs(dest_folder, exist_ok=True)
        dest_file = dest_folder / (src_file.stem.rsplit(".", 1)[0] + src_file.suffix)  # 创建同名文件
        print(f"install {relative_path}")
        shutil.copyfile(src_file, dest_file)  # 将pyc文件复制到同名文件

    # 清除源py文件
    for src_file in dest.rglob("*.py"):
        os.remove(src_file)

    # 清除源目录文件
    if reserve_one:
        if os.path.exists(root):
            shutil.rmtree(root)
        dest.rename(root)


if __name__ == '__main__':
    package(root_path="./", reserve_one=False)

    # 会清空源文件夹，记得备份，适合上线部署，删除源代码，防止泄露
    # package(root_path="./test_project/",reserve_one=True