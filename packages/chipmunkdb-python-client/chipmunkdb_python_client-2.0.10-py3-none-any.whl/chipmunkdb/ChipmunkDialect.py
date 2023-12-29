from sqlalchemy.dialects import registry
from sqlalchemy.engine import reflection
from sqlalchemy.engine.default import DefaultDialect

from chipmunkdb.ChipmunkConnection import ChipmunkConnection

zeta_dbapi = None

class ChipmunkEngine(object):
    paramstyle = 'qmark'
    Error = BaseException

    def __init__(self, *args, **kwargs):
        pass

    def connect(self, *args, **kwargs):
        return ChipmunkConnection

    def __getattr__(self, item):
        return getattr(zeta_dbapi, item)


class ChipmunkDialect(DefaultDialect):
    # default_paramstyle = 'qmark'
    paramstyle = 'qmark'
    driver = 'chipmunkdb'
    name = 'chipmunkdb'
    hide_parameters = False
    _execution_options= None

    def __init__(self, **kwargs):
        DefaultDialect.__init__(self, **kwargs)


    @reflection.cache
    def execute(self, *args, **kwargs):
        return DefaultDialect.execute(self, *args, **kwargs)

    @classmethod
    def dbapi(cls):
        return ChipmunkEngine

    @classmethod
    def import_dbapi(cls):
        return ChipmunkEngine

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        return [u'table_1', u'table_2', ...]

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        return []

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        return []

    @reflection.cache
    def get_unique_constraints(self, connection, table_name,
                               schema=None, **kw):
        return []

    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, **kw):
        return []

    def get_dialect_cls(self, **kw):
        return ChipmunkDialect

    def raw_connection(self, *args, **kwargs):
        return ChipmunkEngine(*args, **kwargs)

    def connect(self, *args, **kwargs):
        self.dialect = self
        # create a ChipmunkConnection object
        return ChipmunkConnection(engine=self, **kwargs)

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        return []

    def _should_log_info(self):
        return True

    def _should_log_debug(self):
        return True

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        # just an example of the column structure
        result = connection.execute('select * from %s limit 1' % table_name)
        return [{'default': None, 'autoincrement': False, 'type': TEXT, 'name': colname, 'nullable': False} for
                colname, coltype in result.cursor.description]