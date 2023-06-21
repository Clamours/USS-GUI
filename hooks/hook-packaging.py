from PyInstaller.utils.hooks import copy_metadata, collect_data_files

datas = copy_metadata("packaging") + collect_data_files("packaging")