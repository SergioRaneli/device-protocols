# -*- coding: utf-8 -*-
import re

KEYWORDS_DESCRIPTIONS = {
    "001": "location information",
    "help me": "SOS alarm",
    "low battery": "low battery alarm",
    "move": "Movement alarm",
    "speed": "Over seed alarm",
    "stockade": "GEO-fence alarm",
    "ac alarm ": "Power off alarm",
    "door alarm": "Door open alarm",
    "sensor alarm": "Shock alarm",
    "acc alarm": "Acc alarm",
    "accident alarm": "accident alarm",
    "bonnet alarm": "bonnet alarm",
    "footbrake alarm": "footbrake alarm",
    "T:": "Temperature alarm",
    "oil": "Fuel alarm",
    "DTC P0001": "diagnostic trouble code:P0001",
    "service": "Vehicle maintenance notification",
    "OBD": "Engine related message",
    "TPMS": "Tyre related message",
}


def get_gps_data_pattern():
    return re.compile(r'imei:'
                      '(?P<imei>\d+),'
                      '(?P<keyword>[^,]+),'
                      '(?P<year>\d{2})/?(?P<month>\d{2})/?(?P<day>\d{2})\s?'
                      '(?P<local_hour>\d{2}):?(?P<local_min>\d{2})(?P<local_sec>\d{2})?,'
                      '[^,]*,'
                      '(?P<gps_signal_status_1>[FL]),'
                      '(?P<utc_hour>\d{2})(?P<utc_min>\d{2})(?P<utc_sec>\d{2})\.(?P<utc_ms>\d+),'
                      '(?P<gps_signal_status_2>[AV]),'
                      '(?P<lat1>\d+)(?P<lat2>\d{2}\.\d+),'
                      '(?P<lat3>[NS])?,'
                      '(?P<lng1>\d+)(?P<lng2>\d{2}\.\d+),'
                      '(?P<lng3>[EW])?,'
                      '(?P<speed>\d+\.?\d*),'
                      '(?P<direction>\d+\.?\d*)?,?'
                      '(?P<altitude>\d+\.?\d*)?,?'
                      '(?P<ext1>[^,]+)?,?'
                      '(?P<ext2>[^,]+)?,?'
                      '(?P<ext3>[^,]+)?,?'
                      '(?P<ext4>[^,]+)?,?'
                      '(?P<ext5>[^,]+)?,?'
                      '.*;')


def get_gps_data_match(string):
    return get_gps_data_pattern().match(string)


def get_obd_data_pattern():
    return re.compile(r'imei:'
                      '(?P<imei>\d+),'
                      '(?P<keyword>OBD),'
                      '(?P<year>\d{2})/?(?P<month>\d{2})/?(?P<day>\d{2})\s?'
                      '(?P<local_hour>\d{2}):?(?P<local_min>\d{2})(?P<local_sec>\d{2})?,'
                      '(?P<accumulative_mileage>[^,]+),'
                      '(?P<instant_fuel>[^,]+),'
                      '(?P<avg_fuel>[^,]+),'
                      '(?P<driving_time>[^,]+),'
                      '(?P<speed>[^,]+),'
                      '(?P<power_load>[^,]+),'
                      '(?P<water_temp>[^,]+),'
                      '(?P<throttle_percentage>[^,]+),'
                      '(?P<engine_speed>[^,]+),'
                      '(?P<battery_voltage>[^,]+),'
                      '(?P<dtc_1>[^,]+)?,?'
                      '(?P<dtc_2>[^,]+)?,?'
                      '(?P<dtc_3>[^,]+)?,?'
                      '(?P<dtc_4>[^,]+)?,?'
                      '.*;')


def get_obd_data_match(string):
    return get_obd_data_pattern().match(string)


def get_tyre_data_pattern():
    return re.compile(r'imei:'
                      '(?P<imei>\d+),'
                      '(?P<keyword>TPMS),'
                      '(?P<year>\d{2})/?(?P<month>\d{2})/?(?P<day>\d{2})\s?'
                      '(?P<local_hour>\d{2}):?(?P<local_min>\d{2})(?P<local_sec>\d{2})?,'
                      '(?P<device_state>[^,]+),'
                      '(?P<num_wheels>[^,]+),'
                      '(?P<left_front_pressure>[^,]+),'
                      '(?P<left_front_temp>[^,]+),'
                      '(?P<left_front_state>[^,]+),'
                      '(?P<right_front_pressure>[^,]+),'
                      '(?P<right_front_temp>[^,]+),'
                      '(?P<right_front_state>[^,]+),'
                      '(?P<left_rear_pressure>[^,]+),'
                      '(?P<left_rear_temp>[^,]+),'
                      '(?P<left_rear_state>[^,]+),'
                      '(?P<right_rear_pressure>[^,]+),'
                      '(?P<right_rear_temp>[^,]+),'
                      '(?P<right_rear_state>[^,]+),?'
                      '.*;')


def get_tyre_data_match(string):
    return get_tyre_data_pattern().match(string)


def get_login_pattern():
    return re.compile(r'^##,imei:(?P<imei>\d+),A;')


def get_login_match(string):
    return get_login_pattern().match(string)


def get_heartbeat_pattern():
    return re.compile(r'^(?P<imei>\d+);')


def get_heartbeat_match(string):
    return get_heartbeat_pattern().match(string)


def get_response(data):
    """
    :param data: string
    :return: dict
    """

    # Auth response
    if get_login_match(data):
        return _create_response(b'LOAD', "login")

    # Heartbeat response
    if get_heartbeat_match(data):
        return _create_response(b'ON', "heartbeat")

    # GPS data response
    if get_gps_data_match(data):
        return _create_response(False, "data", "gps")

    # OBD data response
    if get_obd_data_match(data):
        return _create_response(False, "data", "obd")

    # Tyre data response
    if get_tyre_data_match(data):
        return _create_response(False, "data", "tyre")

    return _create_response(False, "invalid")


def _create_response(message, response_type, sub_response_type=None):
    """
    :param message:
    :param response_type: string
    :param sub_response_type: string
    :return:
    """
    r = {"message": message, "type": response_type}

    if sub_response_type:
        r["sub_type"] = sub_response_type

    return r


def convert_degrees_minutes_to_decimal(degrees, minutes, hemisphere):
    """
    Conversion from MinDec to Decimal Degree
    Given a MinDec (Degrees, Minutes, Decimal Minutes) coordinate such as 79°58.93172W, convert it to a number
    of decimal degrees using the following method:

    - The integer number of degrees is the same (79)
    - The decimal degrees is the decimal minutes divided by 60 (58.93172/60 = ~0.982195)
    - Add the two together (79 + 0.982195= 79.982195)
    - For coordinates in the western (or southern) hemisphere, negate the result.
    - The final result is -79.982195

    :param degrees: number
    :param minutes: number
    :param hemisphere: string
    :return:
    """
    dec = float(degrees)
    dec += float(minutes) / 60.0
    if hemisphere.upper() == 'W' or hemisphere.upper() == 'S':
        dec = -dec

    return round(dec, 12)
