import os
import random
from datetime import datetime
from .utils.FileSystemUtils import assert_is_file, assert_is_dir, winapi_path
import zipfile
from os.path import join, isfile, isdir
import locale
from pathlib import Path


def random_open(directory: str = None,
                file_list: list[str] = None,
                exclude_file_names: list[str] = None,
                program_path: str = "",
                log_file: str = "RandomOpenLog.txt") -> None:
    """
    需求：假设有一个『电影』文件夹，里面有很多没看过的电影，我们想要随机打开一部电影。同理，我们可能想要随机打开一张照片、一个游戏等。

    本函数的作用是使用指定程序随机打开一个某目录下的文件.

    :param directory: 该目录下的所有文件都可能被随机打开.
    :param file_list: 指定需要被随机打开的文件名（文件路径）列表.
    :param exclude_file_names: 如果使用 directory 参数，有一些文件可能不需要被打开.
    :param program_path: 要用哪个程序打开文件.
    :param log_file: 记录过往随机打开的文件.
    """
    if not ((directory is None) ^ (file_list is None)):
        raise Exception("directory and file_name_list cannot be both None, nor can they both have values")

    if directory is not None:
        assert_is_dir(directory)
        files = [join(directory, name) for name in os.listdir(directory)]
        file_list = [name for name in files if isfile(name)]

    if file_list is not None:
        for file in file_list:
            assert_is_file(file)

    if exclude_file_names is None:
        exclude_file_names = []
    exclude_file_names = set(exclude_file_names)

    if program_path != "":
        assert_is_file(program_path)

    # List files, count valid files
    valid_files = [name for name in file_list if os.path.basename(name) not in exclude_file_names]
    valid_num = len(valid_files)

    if valid_num == 0:
        raise Exception("no file to open")

    # random choose one
    index = random.randint(0, valid_num - 1)
    name = valid_files[index]
    print(f'chosen file: {name}')

    with open(log_file, 'a', encoding='utf-8') as log:
        log.write(f"{datetime.now()}\n")
        log.write(f"chosen file: {name}\n")
        log.write("============================\n\n")

    if program_path == "":
        os.system(f'"{name}"')
    else:
        os.system(f'{program_path} "{name}"')

    print("all done")


def walk_while_extract(zip_dir: str,
                       output_dir: str) -> None:
    """
    需求：假设有一个『漫画』文件夹，里面的一级目录是作者名，每个作者目录下都包含了该作者某一期漫画的压缩包。
    我们想要将压缩包和解压后的漫画（通常是多张图片）分别存放。同时，收集每个作者最新的漫画，是一种增量操作。
    这两种操作混合在一起，使得文件管理会非常麻烦。

    本函数的作用是递归遍历 zip_dir，将其中的 zip 压缩包按照相同的相对路径解压到 output_dir 下。解压后，
    两个目录的目录树是一致的。

    已经解压过的 zip 不会重复解压，其判断标准是解压后的文件夹名和压缩文件名相同。

    :param zip_dir: 原始目录
    :param output_dir: 解压目的地
    """
    zip_dir = os.path.abspath(zip_dir)
    output_dir = os.path.abspath(output_dir)

    assert_is_dir(zip_dir)

    extract_count = 0
    ignore_count = 0

    for (root, dirs, files) in os.walk(zip_dir, topdown=True):
        target_dir = join(output_dir, Path(root[len(zip_dir):]).stem)

        existing_dirs = set()
        if isdir(target_dir):
            existing_dirs = set([name.strip() for name in os.listdir(target_dir) if isdir(join(target_dir, name))])

        for file in files:
            file_path = join(root, file)
            simple_name = Path(file).stem.strip()
            if not zipfile.is_zipfile(file_path):
                continue
            # this zip has already been unzipped before
            if simple_name in existing_dirs:
                ignore_count += 1
                continue
            # metadata_encoding should set to the encoding of the OS, otherwise the name of extracted file/dir will
            # be wrongly encoded
            with zipfile.ZipFile(file_path, 'r', metadata_encoding=locale.getpreferredencoding()) as zObj:
                # join: some archives may have files in them directly, instead having a folder with the same name
                # winapi_path: some menga's name is vert long
                # extractall will auto create dirs that do not exist
                zObj.extractall(winapi_path(join(target_dir, simple_name)))
            print(f'extracted: {join(target_dir, file)}')
            extract_count += 1

    print(f'total extracted: {extract_count}')
    print(f'total ignored: {ignore_count}')


def random_open_from_multiple():
    pass
