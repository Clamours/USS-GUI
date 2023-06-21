from PyInstaller.utils.hooks import copy_metadata, collect_data_files

datas = copy_metadata("asyncio") + collect_data_files("asyncio")