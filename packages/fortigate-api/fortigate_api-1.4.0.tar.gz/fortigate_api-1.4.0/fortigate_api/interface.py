"""Interface Object."""

from fortigate_api import helpers as h
from fortigate_api.base import Base
from fortigate_api.types_ import LDAny


class Interface(Base):
    """Interface Object.

    - Web UI: https://hostname/ng/interface
    - API: https://hostname/api/v2/cmdb/system/interface
    - Data: :ref:`Interface.yml`
    """

    def __init__(self, rest):
        """Init Interface Object.

        :param rest: :ref:`Fortigate` REST API connector.
        :type rest: Fortigate
        """
        super().__init__(rest=rest, url_obj="api/v2/cmdb/system/interface/")

    # noinspection PyIncorrectDocstring
    def get(self, **kwargs) -> LDAny:
        """Get interface-objects in specified vdom, all or filtered by some of params.

        :param str uid: Filters interface-object by unique identifier.
            Used to get a single object.

        :param filter: Filter fortigate-objects by one or multiple :ref:`filtering conditions`.
            Used to get multiple objects.
        :type filter: str or List[str]

        :param bool all: Gets all interface-objects from all vdom.

        :return: List of interface-objects.
        :rtype: List[dict]
        """
        if kwargs.get("all"):
            h.pop_quoted(key="all", data=kwargs)
            return super().get(**kwargs)
        interfaces = super().get(**kwargs)
        interfaces = [d for d in interfaces if d["vdom"] == self.rest.vdom]
        return interfaces
