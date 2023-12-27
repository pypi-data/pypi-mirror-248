"""Policy Object."""

from requests import Response

from fortigate_api import helpers as h
from fortigate_api.base import Base
from fortigate_api.extended_filters import wrap_efilters
from fortigate_api.types_ import DAny
from fortigate_api.types_ import LDAny, StrInt


class Policy(Base):
    """Policy Object.

    - Web UI: https://hostname/ng/firewall/policy/policy/standard
    - API: https://hostname/api/v2/cmdb/firewall/policy
    - Data: :ref:`Policy.yml`
    """

    def __init__(self, rest):
        """Init Policy Object.

        :param rest: :ref:`Fortigate` REST API connector.
        :type rest: Fortigate
        """
        super().__init__(rest=rest, url_obj="api/v2/cmdb/firewall/policy/", uid_key="policyid")

    # noinspection PyIncorrectDocstring
    @wrap_efilters
    def get(self, **kwargs) -> LDAny:
        """Get fortigate-objects, all or filtered by some of params.

        Need to use only one of params.

        :param uid: Filters fortigate-object by identifier.
            Used to get a single object.
        :type uid: str or int

        :param filter: Filter fortigate-objects by one or multiple :ref:`filtering conditions`.
            Used to get multiple objects.
        :type filter: str or List[str]

        :param efilter: Extended filter: `srcaddr`, `dstaddr` by condition:
            equals `==`, not equals `!=`,  supernets `>=`, subnets `<=`
        :type efilter: str or List[str]

        :return: List of the fortigate-objects.
        :rtype: List[dict]
        """
        return super().get(**kwargs)

    def move(self, uid: StrInt, position: str, neighbor: StrInt) -> Response:
        """Move policy to before/after other neighbor-policy.

        :param uid: Identifier of policy being moved.
        :type uid: str or int

        :param position: "before" or "after" neighbor.
        :type position: str

        :param neighbor: Policy will be moved near to this neighbor-policy.
        :type neighbor: str or int

        :return: Session response.

            - `<Response [200]>` Policy successfully moved,
            - `<Response [400]>` Invalid URL,
            - `<Response [500]>` Policy has not been moved.
        :rtype: requests.Response
        """
        kwargs = {
            "action": "move",
            "username": self.rest.username,
            "secretkey": self.rest.password,
            position: neighbor,
        }
        url = f"{self.url_}{uid}"
        url = h.make_url(url, **kwargs)
        return self.rest.put(url=url, data={})

    def update(self, data: DAny, uid: StrInt = "") -> Response:
        """Update policy-object in the Fortigate.

        :param data: Data of the policy-object.
        :type data: dict

        :param uid:  Policyid of the policy-object,
            taken from the `uid` parameter or from `data["policyid"]`.
        :type uid: str or int

        :return: Session response.

            - `<Response [200]>` Object successfully updated,
            - `<Response [400]>` Invalid URL,
            - `<Response [404]>` Object has not been updated.
        :rtype: requests.Response
        """
        if not uid:
            uid = data.get("policyid") or ""
            if not uid:
                raise ValueError(f"Absent {uid=} and data[\"policyid\"].")
        return self._update(uid=uid, data=data)
