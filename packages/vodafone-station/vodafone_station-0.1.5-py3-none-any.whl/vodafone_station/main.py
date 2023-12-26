from vodafone_station import VodafoneStation
from vodafone_station import Config
from vodafone_station import pretty_print


def main():
    config = Config("config.json")
    print("Connecting to vodafone station...")
    vodafone_station = VodafoneStation(config)
    print("Calling function...")
    pretty_print(vodafone_station.get_wifi())


if __name__ == '__main__':
    main()
