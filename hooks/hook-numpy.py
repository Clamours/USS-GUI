from PyInstaller.utils.hooks import copy_metadata, collect_data_files

datas = copy_metadata("numpy") + collect_data_files("numpy")