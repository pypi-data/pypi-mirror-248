from vodafone_station.vodafone_station_abstract import AbsVodafoneStation as __AbsVodafoneStation


class VodafoneStation(__AbsVodafoneStation):
    def set_upnp(self, new_value):
        return self._post_request(
            path=self.config.get_api_upnp(),
            data={"upnp": new_value}
        )

    def set_wan_ping(self, new_value):
        return self._post_request(
            path=self.config.get_api_wanPing(),
            data={"aps": new_value, "apsv6": new_value}
        )

    def set_firewall(self, new_value):
        new_value = "on" if new_value else "off"
        return self._post_request(
            path=self.config.get_api_firewall(),
            data={"FirewallLevel": new_value, "FirewallLevelV6": new_value, }
        )

    def set_wifi(self, new_value):
        return self._post_request(
            path=self.config.get_api_wifi(),
            data={
                "1[SSIDEnable]": new_value,
                "1[RadioEnable2]": new_value,
                "1[ApplySetting]": "true",
                "2[SSIDEnable]": new_value,
                "2[RadioEnable5]": new_value,
                "2[ApplySetting]": "true",
            }
        )
