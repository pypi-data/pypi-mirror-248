"""Service Object."""

from fortigate_api.base import Base


class Service(Base):
    """Service Object.

    - Web UI: https://hostname/ng/firewall/service
    - API: https://hostname/api/v2/cmdb/firewall.service/custom
    - Data: :ref:`Service.yml`
    """

    def __init__(self, rest):
        """Init Service Object.

        :param rest: :ref:`Fortigate` REST API connector.
        :type rest: Fortigate
        """
        super().__init__(rest=rest, url_obj="api/v2/cmdb/firewall.service/custom/")
