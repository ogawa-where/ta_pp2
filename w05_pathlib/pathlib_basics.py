#!/usr/bin/env python3
#
# pathlib_basics.py
# 
# [概要]
# pathlibを使った基本的な操作を
# 自作関数で呼び出せるように定義したプログラム．
# 具体的には，
#   ・Pathオブジェクトの作成する
#   ・ディレクトリやファイルを一覧で取得する
#   ・絶対パスを取得する / 名前（ディレクトリ名やファイル名）を取得する
#   ・パスを結合する
#   ・パスが存在しているか確認する
#   ・ディレクトリやファイルを作成 / 削除する
# を定義している．
# なお，ディレクトリやファイルを作成できたことを確認するために
# 削除の関数はすぐに実行しないようにしている．
# main()関数実行後に，作成されたディレクトリとファイルを確認してから，
# reset()関数を呼び出して実行する．
#

from pathlib import Path


def list_dirs_and_files(dir_object):
    # ディレクトリ・ファイルの一覧を取得
    items = list(dir_object.iterdir())
    print(f"{len(items)}個の要素を取得しました．")
    for i, item in enumerate(items):
        print(f"{i+1}番目の要素: {item.name}")
    

def list_includ_subdirs(dir_object):
    # 子ディレクトリ下のファイルを含んで取得
    paths = list(dir_object.glob("**/*"))
    print(f"子ディレクト以下も含めて{len(paths)}個の要素を取得しました．")
    for i, path in enumerate(paths):
        print(f"{i+1}番目の要素: {path.name}")


def check_absolute_path(path_object):
    # 絶対パスを取得する
    abs_path = path_object.resolve()
    print(f"引数に渡されたオブジェクトの絶対パス: \n{abs_path}")


def combine_file_path(dir_object, file_name):
    # ディレクトリパスのオブジェクトにファイル名を結合する
    combined_path = dir_object / file_name

    return combined_path


def make_new_dir(dir_object):
    # ディレクトリを新規作成
    if dir_object.exists() == False:
        dir_object.mkdir(exist_ok=True)
        print(f"新しいディレクトリを作成しました: \n{dir_object}")

    else:
        print(f"{dir_object.name}はすでに存在しています．")


def make_new_file(dir_object, file_name):
    combined_path = combine_file_path(dir_object, file_name)
    # ファイルを新規作成
    if combined_path.exists() == False:
        combined_path.touch()
        print(f"新しいファイルを作成しました: \n{combined_path}")

    else:
        print(f"{combined_path.name}はすでに存在しています．")
        

def del_dir(dir_path):
    # ディレクトリを削除
    if dir_path.exists() == True:
        dir_path.rmdir()
        print(f"{dir_path.name}ディレクトリを削除しました．")

    else:
        print(f"削除対象のディレクトリ({dir_path.name})が存在しません．")

        
def del_file(file_path):
    # ファイルを削除
    if file_path.exists() == True:
        file_path.unlink(missing_ok=True)
        print(f"既存のファイルを削除しました: {file_path}")

    else:
        print(f"削除対象のファイル({file_path.name})が存在しません．")



def main():
    # Pathオブジェクトを作成
    INPUT_DIR_PATH = "./under_the_control_of_pathlib/"
    INPUT_DIR_OBJECT = Path(INPUT_DIR_PATH)

    # 絶対パスを確認した後，ディレクトリ内の要素を取得する処理
    check_absolute_path(INPUT_DIR_OBJECT)
    list_dirs_and_files(INPUT_DIR_OBJECT)
    list_includ_subdirs(INPUT_DIR_OBJECT)

    # Pathオブジェクトを作成
    OUTPUT_DIR_PATH = "./output/"
    OUTPUT_DIR_OBJECT = Path(OUTPUT_DIR_PATH)
    file_name = "sample.py"

    # outputディレクトリを新規作成し，空のPythonファイルも作成する処理
    make_new_dir(OUTPUT_DIR_OBJECT)
    make_new_file(OUTPUT_DIR_OBJECT, file_name)


def reset():
    # main()関数実行後に任意で実行する関数 
    OUTPUT_DIR_PATH = "./output/"
    OUTPUT_DIR_OBJECT = Path(OUTPUT_DIR_PATH)
    file_name = "sample.py"

    del_file(OUTPUT_DIR_OBJECT / file_name)
    del_dir(OUTPUT_DIR_OBJECT)
    

if __name__ == "__main__":
    main()
    #reset()
