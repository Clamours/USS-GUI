from PyInstaller.utils.hooks import copy_metadata, collect_data_files

datas = copy_metadata("tokenizers") + collect_data_files("tokenizers")