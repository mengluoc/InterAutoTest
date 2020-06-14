import os
import yaml


class YamlReader:
    # 初始化，文件是否存在
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('文件不存在')
        self._data = None
        self._data_all = None

    # 单个文档读取
    def data(self):
        if not self._data:
            with open(self.yamlf, "r", encoding="utf-8") as f:
                self._data = yaml.safe_load(f)
                return self._data
        else:
            return self._data

    # 多个文档读取
    def data_all(self):
        if not self._data_all:
            with open(self.yamlf, "r", encoding="utf-8") as f:
                self._data_all = list(yaml.safe_load_all(f))
                return self._data_all
        else:
            return self._data_all