import argparse
import pathlib
import re
import sys

from vodafone_station import VodafoneStation
from vodafone_station.config import Config
from vodafone_station.util import pretty_print

default_config_path = pathlib.Path(pathlib.Path().home(), ".vodafone-station/config.json")


def add_config(parser):
    parser.add_argument('-c', '--config', type=pathlib.Path,
                        required=False,
                        default=default_config_path,
                        help='Path to the configuration file (JSON Format)')


def get_api_names():
    parser = argparse.ArgumentParser(
        add_help=False
    )
    add_config(parser)
    config_path = parser.parse_known_args()[0].config

    if not config_path.exists():
        print(f"No configuration at {config_path.absolute()}. Custom config file can be passed by -c [CONFIG].")
        sys.exit(1)

    config = Config(config_path)
    dont_show_api_key = {"login", "logout"}
    api_names = [
        convert_api_key_to_name(api_key)
        for api_key in config.get_api()
        if api_key not in dont_show_api_key
    ]
    return api_names


__api_regex = re.compile('[A-Z][^A-Z]*')


def convert_api_key_to_name(api_key: str):
    api_key = f"{api_key[0].upper()}{api_key[1:]}"
    api_name_parts = __api_regex.findall(api_key)
    return "_".join([str(api_name_part).lower() for api_name_part in api_name_parts])


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='vodafone-station',
        description='Program to interact with a vodafone station'
    )

    add_config(parser)

    parser.add_argument(
        "-p", "--param",
        required=False,
        nargs=argparse.ZERO_OR_MORE,
        help="Changing values on defined API",
        # action="store"
    )

    parser.add_argument(
        "api",
        type=str,
        choices=get_api_names(),
        help="Function to interact with vodafone station.",
    )

    return parser.parse_args()


def convert_parameter(parameter):
    try:
        return int(parameter)
    except ValueError:
        pass
    try:
        return float(parameter)
    except ValueError:
        pass
    try:
        return parameter.lower() in ['true', '1', 't', 'y', 'yes', 'on']
    except ValueError:
        pass
    try:
        return parameter.lower() in ['false', '0', 'f', 'n', 'no', 'off', '']
    except ValueError:
        pass

    return parameter


def run_func(args):
    func_name = args.api
    parameters = args.param

    if parameters is not None:
        func_name = f"set_{func_name.lower()}"
    else:
        func_name = f"get_{func_name.lower()}"

    config = Config(args.config)
    print("Connecting to vodafone station...")
    vodafone_station = VodafoneStation(config)
    try:
        func = getattr(vodafone_station, func_name)
    except AttributeError:
        print(f"The function {func_name} is not available")
        sys.exit(2)

    print(f"Calling to function {func_name} on vodafone station")
    if parameters is None:
        return pretty_print(func())

    has_no_keyword_args = any(["=" not in parameter for parameter in parameters])
    if has_no_keyword_args and any(["=" in parameter for parameter in parameters]):
        print("The parameters cannot be keyword parameters and positional parameters")
        sys.exit(3)

    if has_no_keyword_args:
        parameters = [convert_parameter(parameter) for parameter in parameters]
        return pretty_print(func(*parameters))

    def get_key(parameter):
        return parameter.split("=")[0]

    def get_value(parameter):
        return convert_parameter(parameter.split("=")[1])

    data = {get_key(parameter): get_value(parameter) for parameter in parameters}
    return pretty_print(func(**data))


def main():
    args = parse_arguments()
    run_func(args)


if __name__ == '__main__':
    main()
