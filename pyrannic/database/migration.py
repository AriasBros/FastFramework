from pyrannic.contracts.database.migration import MigrationInterface
from pyrannic.contracts.database.schema import SchemaInterface


class Migration(MigrationInterface):
    schema: SchemaInterface

    def __init__(self, schema: SchemaInterface):
        self.schema = schema
