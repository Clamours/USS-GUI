from PyInstaller.utils.hooks import copy_metadata, collect_data_files

datas = copy_metadata("torch.jit") + collect_data_files("torch.jit")