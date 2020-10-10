import math
import numpy

from .constants import SATELLITES


def getLocation(dist_array):
    PA = numpy.array(SATELLITES[0])
    PB = numpy.array(SATELLITES[1])
    PC = numpy.array(SATELLITES[2])

    try:
        ex = (PB - PA) / (numpy.linalg.norm(PB - PA))
        i = numpy.dot(ex, PC - PA)
        ey = (PC - PA - i * ex) / (numpy.linalg.norm(PC - PA - i * ex))
        d = numpy.linalg.norm(PB - PA)
        j = numpy.dot(ey, PC - PA)

        x = (pow(dist_array[0], 2) - pow(dist_array[1], 2) + pow(d, 2)) / (2 * d)
        y = (
            (pow(dist_array[0], 2) - pow(dist_array[2], 2) + pow(i, 2) + pow(j, 2))
            / (2 * j)
        ) - ((i / j) * x)
        coord = PA + x * ex + y * ey

        return (
            numpy.round(coord, 1)
            if _coordinates_are_valid(coord, dist_array, SATELLITES)
            else None
        )
    except TypeError:
        pass


def _coordinates_are_valid(coordinates, distances, satellites):
    for sat in satellites:
        sat_coord = numpy.array(sat)
        if (
            round(
                math.sqrt(
                    (coordinates[0] - sat_coord[0]) ** 2
                    + (coordinates[1] - sat_coord[1]) ** 2
                ),
                1,
            )
            != distances[satellites.index(sat)]
        ):
            return False
    return True
