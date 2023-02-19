import json
import requests
import time
import sonoffcrypto
from zeroconf import Zeroconf


def get_ip_address_as_string(binary_address):
    parts = []
    for i in range(4):
        parts.append(str(int(binary_address.hex()[(i * 2): (i + 1) * 2], 16)))
    return ".".join(parts)


class SonoffMicroSwitch:
    def __init__(
            self,
            device_id,
            api_key
    ) -> None:
        self.device_id = device_id
        self.api_key = api_key
        self.base_url = ""
        self.switch_is_on = None
        self.update()

    def update(self):
        zeroconf = Zeroconf()
        host = f"eWeLink_{self.device_id}._ewelink._tcp.local."
        info = zeroconf.get_service_info(host, host)

        # address and port
        ip_address = get_ip_address_as_string(info.addresses[0])
        self.base_url = f"http://{ip_address}:{info.port}/zeroconf/"

        # current state
        iv = info.properties.get(b"iv")
        data = info.properties.get(b"data1") + info.properties.get(b"data2") + info.properties.get(b"data3") + info.properties.get(b"data4")

        decrypted_data = sonoffcrypto.decrypt(data, iv, self.api_key)
        device_info = json.loads(decrypted_data)
        self.switch_is_on = device_info["switches"][0]["switch"] == "on"

    def send_request(self, action, params):
        http_session = requests.Session()
        http_session.headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "close",
            "Accept": "application/json",
        }

        payload = {
            "deviceid": self.device_id,
            "sequence": str(int(time.time() * 1000)),
        }

        sonoffcrypto.format_encryption_msg(payload, self.api_key, params)

        url = self.base_url + action
        data = json.dumps(payload, separators=(",", ":"))
        response = http_session.post(url, data=data)
        return response.json()

    def is_on(self):
        return self.switch_is_on

    def is_off(self):
        return None if self.switch_is_on is None else not self.switch_is_on

    def turn(self, state):
        params = {
            "switches": [
                {"switch": state, "outlet": 0}
            ]
        }
        response = self.send_request("switches", params)
        if response["error"] == 0:
            self.switch_is_on = state == "on"
            return True
        else:
            return False

    def turn_on(self):
        return self.turn("on")

    def turn_off(self):
        return self.turn("off")

    def toggle(self):
        if self.is_on():
            self.turn_off()
        else:
            self.turn_on()
