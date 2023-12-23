import os
dir = os.path.abspath(os.path.dirname(__file__))

dir_metro = os.path.join(dir, "metro")
dir_metro_net40 = os.path.join(dir_metro, "net40")

libs = {}

if os.path.exists(dir_metro_net40):
    for lib in os.listdir(dir_metro_net40):
        path = os.path.join(dir_metro_net40, lib)
        if os.path.isfile(path):
            if os.path.splitext(path)[1] == ".dll":  # 判断文件扩展名是否为“.dll”
                libs[lib] = path

from aquareflog import Debug
Debug(f"MetroFramework Library Files {libs}")