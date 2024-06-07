import c104
import random
import time
import json
import argparse

def on_step_command(point: c104.Point, previous_state: dict, message: c104.IncomingMessage) -> c104.ResponseState:
    """ handle incoming regulating step command
    """
    print("{0} STEP COMMAND on IOA: {1}, new: {2}, prev: {3}, cot: {4}, quality: {5}".format(point.type, point.io_address, point.value, previous_state, message.cot, point.quality))

    if point.value == c104.Step.LOWER:
        # do something
        return c104.ResponseState.SUCCESS

    if point.value == c104.Step.HIGHER:
        # do something
        return c104.ResponseState.SUCCESS

    return c104.ResponseState.FAILURE


def before_transmit(point: c104.Point) -> None:
    """ update point value before transmission
    """
    point.value = random.random() * 100
    print("{0} BEFORE TRANSMIT on IOA: {1}".format(point.type, point.io_address))

def add_station_points_from_json(json_data, station):
    """
    Adds points to a station from a given JSON.

    :param json_data: A dictionary representing the JSON data containing point information.
    :param station: The station object to which points need to be added.
    """
    # Iterate over the datapoints in the JSON
    for datapoint in json_data['exchanged_data']['datapoints']:
        # Iterate over protocols for each datapoint
        for protocol in datapoint['protocols']:
            if protocol['name'] == 'iec104':
                # Extract the address part after the dash
                address = protocol['address'].split('-')[1]
                
                # Get the point type from the typeid attribute
                #typeid = getattr(c104.Type, protocol['typeid'], None)
                
                if typeid:
                    # Add the point to the station
                    point = station.add_point(io_address=int(address), type=c104.Type.M_ME_NA_1, report_ms=10000)
                    point.on_before_auto_transmit(callable=before_transmit)
                    point.on_before_read(callable=before_transmit)

def main():
    # datapoints configuration preparation
    parser = argparse.ArgumentParser(description='Parse JSON for datapoints.')
    parser.add_argument('input_file', help='The input JSON file path')

    args = parser.parse_args()

    # Reading JSON file
    with open(args.input_file, 'r') as file:
        json_data = json.load(file)

    
    # server and station preparation
    server = c104.Server(ip="0.0.0.0", port=2404)
    station = server.add_station(common_address=11509)

    # monitoring point preparation
    #point = station.add_point(io_address=11, type=c104.Type.M_ME_NC_1, report_ms=15000)
    add_station_points_from_json(json_data, station)

    # command point preparation
    command = station.add_point(io_address=12, type=c104.Type.C_RC_TA_1)
    command.on_receive(callable=on_step_command)

    # start
    server.start()

    while not server.has_active_connections:
        print("Waiting for connection")
        time.sleep(1)

    time.sleep(1)

    c = 0
    while server.has_open_connections and c<30:
        c += 1
        print("Keep alive until disconnected")
        time.sleep(1)


if __name__ == "__main__":
    c104.set_debug_mode(c104.Debug.Server)
    main()
    time.sleep(1)
