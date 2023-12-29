

from sqlalchemy.dialects import registry

registry.register("chipmunkdb", "chipmunkdb.ChipmunkDialect", "ChipmunkDialect")