from PyInstaller.utils.hooks import copy_metadata, collect_data_files

datas = copy_metadata("filelock") + collect_data_files("filelock")