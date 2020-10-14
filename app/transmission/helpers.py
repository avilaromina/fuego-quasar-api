import math
import numpy

from .constants import (
    SATELLITES,
    tmp_transmissions,
)


def get_location(distances):
    PA = numpy.array(SATELLITES['kenobi'])
    PB = numpy.array(SATELLITES['skywalker'])
    PC = numpy.array(SATELLITES['sato'])

    try:
        ex = (PB - PA) / (numpy.linalg.norm(PB - PA))
        i = numpy.dot(ex, PC - PA)
        ey = (PC - PA - i * ex) / (numpy.linalg.norm(PC - PA - i * ex))
        d = numpy.linalg.norm(PB - PA)
        j = numpy.dot(ey, PC - PA)

        x = (pow(distances['kenobi'], 2) - pow(distances['skywalker'], 2) + pow(d, 2)) / (2 * d)
        y = (
            (pow(distances['kenobi'], 2) - pow(distances['sato'], 2) + pow(i, 2) + pow(j, 2))
            / (2 * j)
        ) - ((i / j) * x)
        coord = PA + x * ex + y * ey

        return (
            numpy.round(coord, 1)
            if _coordinates_are_valid(coord, distances, SATELLITES)
            else None
        )
    except TypeError:
        pass


def _coordinates_are_valid(coordinates, distances, satellites):
    for sat in satellites.items():
        sat_coord = numpy.array(sat[1])
        if (
            round(
                math.sqrt(
                    (coordinates[0] - sat_coord[0]) ** 2
                    + (coordinates[1] - sat_coord[1]) ** 2
                ),
                1,
            )
            != distances[sat[0]]
        ):
            return False
    return True


def get_message(msg_array):
    try:
        msg_len = min(len(msg) for msg in msg_array)
        if msg_len:
            final_msg = ''
            i = 1
            while i <= msg_len:
                word = None
                for msg in msg_array:
                    if word is not None and msg[-i] != word and msg[-i] != '':
                        return None
                    word = word if msg[-i] == '' else msg[-i]
                final_msg = ' ' + word + final_msg
                i += 1
            return final_msg[1:]
        else:
            return None
    except TypeError:
        pass


def map_distances(msg_list):
    return dict([(msg['name'], msg['distance'])for msg in msg_list])


def set_temp_distances(satellite, distance, message):
    tmp_transmissions[satellite] = (distance, message)


def get_temp_distances(satellites):
    msg = []
    for satellite in satellites:
        msg.append(
            {
                "name": satellite,
                "distance": tmp_transmissions[satellite][0]
                if tmp_transmissions[satellite]
                else None,
                "message": tmp_transmissions[satellite][1]
                if tmp_transmissions[satellite]
                else None,
            }
        )
    return msg


def clear_tmp_distances():
    for satellite in SATELLITES.keys():
        tmp_transmissions[satellite] = None
