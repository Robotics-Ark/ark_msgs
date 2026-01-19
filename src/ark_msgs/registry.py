from ark.registry import Registry
from google.protobuf.message import Message


class ArkMsgsRegistry(Registry):

    def register_item(self, item: type[Message]):
        name = item.DESCRIPTOR.full_name
        return super().register_item(name, item)


msgs = ArkMsgsRegistry()
