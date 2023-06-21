from PyInstaller.utils.hooks import copy_metadata, collect_data_files

datas = copy_metadata("requests") + collect_data_files("requests")