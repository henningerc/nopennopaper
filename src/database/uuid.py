import uuid


class UUIDFactory:
    namespaces = {}
    root_name = ""

    def __init__(self, config):
        UUIDFactory.root_name = config["rootname"]

    @staticmethod
    def create_uuid(namespace_identifier, name):
        if "root" not in UUIDFactory.namespaces.keys():
            UUIDFactory.namespaces["root"] = uuid.uuid5(uuid.NAMESPACE_DNS, UUIDFactory.root_name)

        if namespace_identifier not in UUIDFactory.namespaces.keys():
            UUIDFactory.namespaces[namespace_identifier] = uuid.uuid5(UUIDFactory.namespaces["root"],
                                                                      namespace_identifier)
        return uuid.uuid5(UUIDFactory.namespaces[namespace_identifier], name)
