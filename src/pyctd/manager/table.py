from . import table_conf


class Table:
    def __init__(self, sqlalchemy_model, conf):
        """

        :param str name: name of table
        :param conf: configuration of a table from `table_config`
        """
        self.name = sqlalchemy_model.table_suffix
        self.model = sqlalchemy_model
        self.columns_in_file_expected = [x[0] for x in conf['columns']]
        self.columns_in_db = [x[1] for x in conf['columns']]
        self.columns_dict = dict(conf['columns'])
        self.file_name = conf['file_name']
        self.one_to_many = ()
        if 'one_to_many' in conf:
            self.one_to_many = conf['one_to_many']


def get_table_configurations():
    return [Table(sqlalchemy_model, conf) for sqlalchemy_model, conf in table_conf.tables.items()]
