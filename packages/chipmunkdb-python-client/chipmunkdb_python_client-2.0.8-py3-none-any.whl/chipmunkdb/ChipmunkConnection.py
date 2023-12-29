
import sqlalchemy as sa
from sqlalchemy.engine import Connection
from sqlalchemy.engine.cursor import CursorResult, ResultFetchStrategy, CursorResultMetaData, ResultMetaData

class ChipmunkCursor(CursorResult):
    description = None
    rowcount = 5
    _metadata = None

    def rowcount(self):
        """
        Return the 'rowcount' for this result.
        """
        return self.rowcount

    def __init__(self, connection, cursor_strategy=ResultFetchStrategy()):
        super(ChipmunkCursor, self).__init__(connection, cursor_strategy, None)
        self._connection = connection


    def execute(self, query, *multiparams, **params):
        """
        Execute a SQL statement construct and return a ResultProxy.
        """
        self._metadata = CursorResultMetaData(self, self.description)
        self._metadata.rowcount = 5

        return ["asd"]

    def close(self):
        """
        Close the cursor.
        """
        pass




class ChipmunkConnection(Connection):
    root_connection = None
    _num_sentinel_cols = 0
    rowcount = -1
    """
    This is the ChipmunkConnection class. It is used to connect to a chipmunkdb.
    We inherit from the sqlalchemy.engine.base.Connection class and implement all of its methods.
    """
    def __init__(self, engine, *args, **kwargs):
        super(ChipmunkConnection, self).__init__(engine, *args)
        self.root_connection = self
        self._session = None

    def _echo(self):
        """
        Return True if the Engine echoing is on.
        """
        pass

    def begin(self):
        """
        Begin a transaction and return a transaction handle.
        """
        pass

    def result_column_struct(self, column):
        """
        Return a DB-API result column structure.
        """
        pass

    def cursor(self):
        return ChipmunkCursor(self)

    def close(self):
        """
        Close this connection.
        """
        pass

    def commit(self):
        """
        Commit the transaction.
        """
        pass

    def connection(self):
        """
        Return a DB-API connection.
        """
        pass

    def create_session(self):
        """
        Return a new Session object.
        """
        pass

    def execute(self, object, *multiparams, **params):
        """
        Execute a SQL expression construct or string statement.
        """
        pass

    def invalidate(self):
        """
        Invalidate the connection.
        """
        pass

    def scalar(self, object, *multiparams, **params):
        """
        Execute a SQL expression construct or string statement and return a scalar result.
        """
        pass

    def transaction(self):
        """
        Return a transaction handle with the current transactional state.
        """
        pass

    def rollback(self):
        """
        Roll back the transaction.
        """
        pass

    def savepoint(self, name=None):
        """
        Return a savepoint handle with the current transactional state.
        """
        pass


