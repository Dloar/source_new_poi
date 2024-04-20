import mpu


def calculate_distance_between_two_points(point_lat1, point_lat2, point_long1, point_long2):
    distance = mpu.haversine_distance((float(point_lat1),
                                       float(point_long1)),
                                      (float(point_lat2),
                                       float(point_long2)))

    return distance