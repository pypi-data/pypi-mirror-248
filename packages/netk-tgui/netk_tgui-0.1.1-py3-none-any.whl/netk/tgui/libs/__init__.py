from os import path, listdir

path_tgui_libs = path.abspath(path.dirname(__file__))
path_tgui_libs_themes = path.join(path_tgui_libs, "themes")
path_tgui_libs_babyblue_theme = path.join(path_tgui_libs_themes, "BabyBlue.txt")
path_tgui_libs_black_theme = path.join(path_tgui_libs_themes, "Black.txt")
path_tgui_libs_nano_theme = path.join(path_tgui_libs_themes, "NanoGui.style")
path_tgui_libs_sunvalley_light_theme = path.join(path_tgui_libs_themes, "SunValley", "Light", "Theme.txt")
path_tgui_libs_sunvalley_dark_theme = path.join(path_tgui_libs_themes, "SunValley", "Dark", "Theme.txt")
path_tgui_libs_transparent_grey_theme = path.join(path_tgui_libs_themes, "TransparentGrey.txt")

libs = {}

if path.exists(path_tgui_libs):
    for lib in listdir(path_tgui_libs):
        _path = path.join(path_tgui_libs, lib)
        if path.isfile(_path):
            if path.splitext(_path)[1] == ".dll":  # 判断文件扩展名是否为“.dll”
                libs[lib] = _path

"""from sys import platform

if platform == "win32":
    if path.exists(path_tgui_libs_win32_x64):
        for lib in listdir(path_tgui_libs_win32_x64):
            _path = path.join(path_tgui_libs_win32_x64, lib)
            if path.isfile(_path):
                if path.splitext(_path)[1] == ".dll":  # 判断文件扩展名是否为“.dll”
                    libs[lib] = _path

print(libs)"""