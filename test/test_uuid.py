from src.database.uuid import UUIDFactory
from uuid import UUID


class TestUUID:
    def test_uuid(self):
        id_generator = UUIDFactory(config={"rootname": "nopnp.org"})
        assert id_generator.create_uuid("root", "users") == UUID("43464a30-cedc-5267-8e78-3c80fec43071")
