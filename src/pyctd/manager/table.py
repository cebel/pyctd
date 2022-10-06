# -*- coding: utf-8 -*-

from . import table_conf
from typing import List, Dict, Tuple


class Table:
    def __init__(self, sqlalchemy_model, conf: table_conf.TableConfig):
        """

        :param str name: name of table
        :param conf: configuration of a table from `table_config`
        """
        self.name: str = sqlalchemy_model.table_suffix
        self.model = sqlalchemy_model
        self.columns_in_file_expected: List[str]  = [x[0] for x in conf.columns]
        self.columns_in_db: List[str] = [x[1] for x in conf.columns]
        self.columns_dict: Dict[str,str] = {x[0]:x[1] for x in conf.columns}
        self.file_name: str = conf.file_name
        self.one_to_many: Tuple[table_conf.OneToManyConfig, ...] = ()
        if conf.one_to_many:
            self.one_to_many = conf.one_to_many


def get_table_configurations():
    return [Table(sqlalchemy_model, conf) for sqlalchemy_model, conf in table_conf.tables.items()]
