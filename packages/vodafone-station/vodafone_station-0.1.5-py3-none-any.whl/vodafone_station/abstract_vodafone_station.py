import functools
from abc import ABC

import requests
import requests.cookies

from vodafone_station import util


def get_base_url(config):
    return f"{config.get_protocol()}://{config.get_host()}"


class AbsVodafoneStation(ABC):
    def __init__(self, config):
        self.config = config
        self.BASE_URL = get_base_url(config)
        self.API_PATH = self.config.get_path_api()
        self.ROOT_CERT = self.config.get_root_cert()
        self.session = self.__create_session()
        self.use_base_api = self.config.use_base_api()
        self.__login()

    def __login(self, logout_other_users: bool = None):
        response = self.session.post(
            url=self.get_full_url(self.config.get_api_login()),
            data={"username": self.config.get_username(), "password": "seeksalthash", "logout": logout_other_users},
            verify=self.ROOT_CERT,
        )
        self.session.cookies.set_cookie(requests.cookies.create_cookie("cwd", "No"))

        data_hash = get_res_and_raise_errors(response)
        hashed1 = util.do_pbkdf2_not_coded(self.config.get_password(), data_hash["salt"])
        password = util.do_pbkdf2_not_coded(hashed1, data_hash["saltwebui"])
        try:
            self._post_request(self.config.get_api_login(),
                               {"username": self.config.get_username(), "password": password},
                               csrf=False)
        except ConnectionError as error:
            if self.config.is_always_log_others_out() or "y" in input(
                    "Do you want to logout other users? (y/n)").lower():
                self.__login(True)

        self.get_menu()

    def get_menu(self):
        return self._get_request(self.config.get_api_menu())

    def logout(self):
        self._post_request(
            path=self.config.get_api_logout(),
            data={},
            csrf=False,
        )

    def __del__(self):
        self.logout()

    def get_full_url(self, path):
        return f"{self.BASE_URL}{self.API_PATH if self.use_base_api else ''}{path}"

    def _get_request(self, path):
        response = self.session.get(
            url=self.get_full_url(path),
            verify=self.ROOT_CERT,
        )
        res = get_res_and_raise_errors(response)
        return res

    def _post_request(self, path, data, csrf: bool = True):
        url = self.get_full_url(path)
        headers = {}
        if csrf:
            response = self.session.get(
                url=url,
                headers=headers,
                verify=self.ROOT_CERT,
            )
            res = get_res_and_raise_errors(response)

            csrf_token = res.get("token")
            if csrf_token:
                headers["X-CSRF-TOKEN"] = csrf_token

        response = self.session.post(
            url=url,
            headers=headers,
            data=data,
            verify=self.ROOT_CERT,
        )
        res = get_res_and_raise_errors(response)
        return res

    @staticmethod
    def __create_session():
        session = requests.Session()
        headers = {
            "X-Requested-With": "XMLHttpRequest",
        }
        session.headers.update(headers)
        return session

    def __get_path_from_name(self, name: str) -> str:
        name = name.lower().replace("get_", "").replace("set_", "")
        name_parts = name.split("_")
        name_parts_cap = [str(name).capitalize() if idx > 0 else name for idx, name in enumerate(name_parts)]
        path_var = "".join(name_parts_cap)
        path = getattr(self.config, f"get_api_{path_var}")()
        return path

    def __getattr__(self, name, *args, **kwargs):
        path = self.__get_path_from_name(name)
        if name.startswith("get"):
            return functools.partial(self._get_request, path=path)
        elif name.startswith("set"):
            def wrapper(data):
                return self._post_request(
                    path=path,
                    data=data
                )

            return wrapper


def get_res_and_raise_errors(response):
    response.raise_for_status()
    res = response.json()
    try:
        raise_error_from_res(res)
    except KeyError:
        pass

    try:
        for i in range(10):
            raise_error_from_res(res[str(i)])
    except KeyError:
        pass
    except ConnectionError as error:
        error.res = res

    return res


def raise_error_from_res(res):
    if res["error"] != "error":
        return
    message = res.get("message", f"Error in Response-Body")
    error = ConnectionError(f"{message}")
    error.res = res
    raise error
