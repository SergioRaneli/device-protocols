# -*- coding: utf-8 -*-
from deviceprotocols import gps103


def test_get_login_match():
    data = "##,imei:359586015829802,A;"
    result = gps103.get_login_match(data)
    assert result.group('imei') == "359586015829802"


def test_get_heartbeat_match():
    data = "359586015829802;"
    result = gps103.get_heartbeat_match(data)
    assert result.group('imei') == "359586015829802"


def test_get_gps_data_match():
    data = "imei:359710049100168,move,160712015143,,F,135145.000,A,4339.8602,S,17232.8935,E,0.30,339.24,123.12,0,0,,,;"
    result = gps103.get_gps_data_match(data)
    assert result.group('imei') == "359710049100168"
    assert result.group('keyword') == "move"
    assert result.group('year') == "16"
    assert result.group('month') == "07"
    assert result.group('day') == "12"
    assert result.group('local_hour') == "01"
    assert result.group('local_min') == "51"
    assert result.group('local_sec') == "43"
    assert result.group('gps_signal_status_1') == "F"
    assert result.group('utc_hour') == "13"
    assert result.group('utc_min') == "51"
    assert result.group('utc_sec') == "45"
    assert result.group('utc_ms') == "000"
    assert result.group('gps_signal_status_2') == "A"
    assert result.group('lat1') == "43"
    assert result.group('lat2') == "39.8602"
    assert result.group('lat3') == "S"
    assert result.group('lng1') == "172"
    assert result.group('lng2') == "32.8935"
    assert result.group('lng3') == "E"
    assert result.group('speed') == "0.30"
    assert result.group('direction') == "339.24"
    assert result.group('altitude') == "123.12"
    assert result.group('ext1') == "0"
    assert result.group('ext2') == "0"
    assert result.group('ext3') is None
    assert result.group('ext4') is None


def test_get_obd_data_match():
    data = "imei:359710049100168,OBD,080923192918,12,23,45,67,45,78,54,876,34,56,34,234,656,76;"
    result = gps103.get_obd_data_match(data)
    assert result.group('imei') == "359710049100168"
    assert result.group('keyword') == "OBD"
    assert result.group('year') == "08"
    assert result.group('month') == "09"
    assert result.group('day') == "23"
    assert result.group('local_hour') == "19"
    assert result.group('local_min') == "29"
    assert result.group('local_sec') == "18"
    assert result.group('accumulative_mileage') == "12"
    assert result.group('instant_fuel') == "23"
    assert result.group('avg_fuel') == "45"
    assert result.group('driving_time') == "67"
    assert result.group('speed') == "45"
    assert result.group('power_load') == "78"
    assert result.group('water_temp') == "54"
    assert result.group('throttle_percentage') == "876"
    assert result.group('engine_speed') == "34"
    assert result.group('battery_voltage') == "56"
    assert result.group('dtc_1') == "34"
    assert result.group('dtc_2') == "234"
    assert result.group('dtc_3') == "656"
    assert result.group('dtc_4') == "76"


def test_get_tyre_data_match():
    data = "imei:359710049100168,TPMS,080923192918,12,23,45,67,45,78,54,876,34,56,34,234,656,76;"
    result = gps103.get_tyre_data_match(data)
    assert result.group('imei') == "359710049100168"
    assert result.group('keyword') == "TPMS"
    assert result.group('year') == "08"
    assert result.group('month') == "09"
    assert result.group('day') == "23"
    assert result.group('local_hour') == "19"
    assert result.group('local_min') == "29"
    assert result.group('local_sec') == "18"
    assert result.group('device_state') == "12"
    assert result.group('num_wheels') == "23"
    assert result.group('left_front_pressure') == "45"
    assert result.group('left_front_temp') == "67"
    assert result.group('left_front_state') == "45"
    assert result.group('right_front_pressure') == "78"
    assert result.group('right_front_temp') == "54"
    assert result.group('right_front_state') == "876"
    assert result.group('left_rear_pressure') == "34"
    assert result.group('left_rear_temp') == "56"
    assert result.group('left_rear_state') == "34"
    assert result.group('right_rear_pressure') == "234"
    assert result.group('right_rear_temp') == "656"
    assert result.group('right_rear_state') == "76"


def test_get_response_login_pattern():
    data = "##,imei:359586015829802,A;"
    result = gps103.get_response(data)
    assert result["message"] == b'LOAD'
    assert result["type"] == "login"


def test_get_response_heartbeat_pattern():
    data = "359586015829802;"
    result = gps103.get_response(data)
    assert result["message"] == b'ON'
    assert result["type"] == "heartbeat"


def test_get_response_gps_data_pattern_move():
    data = "imei:359710049100168,move,160712015143,,F,135145.000,A,4339.8602,S,17232.8935,E,0.30,339.24,,0,0,,,;"
    result = gps103.get_response(data)
    assert result["message"] is False
    assert result["type"] == "data"
    assert result["sub_type"] == "gps"


def test_get_response_gps_data_pattern_acc_alarm():
    data = "imei:359710049100168,acc alarm,160712171651,,F,051651.000,A,4339.0694,S,17230.5769,E,52.68,158.86,,1,0,,,;"
    result = gps103.get_response(data)
    assert result["message"] is False
    assert result["type"] == "data"
    assert result["sub_type"] == "gps"


def test_get_response_gps_data_pattern_speed():
    data = "imei:359710049100168,speed,160712171718,,F,051718.000,A,4339.3792,S,17230.8680,E,49.28,129.72,,1,0,,,;"
    result = gps103.get_response(data)
    assert result["message"] is False
    assert result["type"] == "data"
    assert result["sub_type"] == "gps"


def test_get_response_obd_data_pattern():
    data = "imei:359710049100168,OBD,160712171718,12,23,45,67,45,78,54,876,34,56,34,234,656,76,34,54;"
    result = gps103.get_response(data)
    assert result["message"] is False
    assert result["type"] == "data"
    assert result["sub_type"] == "obd"


def test_get_response_tyre_data_pattern():
    data = "imei:359710049100168,TPMS,160712171718,12,23,45,67,45,78,54,876,34,56,34,234,656,76,88;"
    result = gps103.get_response(data)
    print(result)
    assert result["message"] is False
    assert result["type"] == "data"
    assert result["sub_type"] == "tyre"


def test_get_response_invalid_message():
    data = "adasdbfsdwerasinvalid,sdfds;"
    result = gps103.get_response(data)
    assert result["message"] is False
    assert result["type"] == "invalid"


def test_convert_degrees_minutes_to_decimal_south():
    data = "4339.8605"
    hem = "S"
    result = gps103.convert_degrees_minutes_to_decimal(data[0:2], data[2:], hem)
    assert result == -43.664341666667


def test_convert_degrees_minutes_to_decimal_north():
    data = "4339.8605"
    hem = "N"
    result = gps103.convert_degrees_minutes_to_decimal(data[0:2], data[2:], hem)
    assert result == 43.664341666667


def test_convert_degrees_minutes_to_decimal_east():
    data = "17232.8935"
    hem = "E"
    result = gps103.convert_degrees_minutes_to_decimal(data[0:3], data[3:], hem)
    assert result == 172.548225


def test_convert_degrees_minutes_to_decimal_west():
    data = "17232.8935"
    hem = "W"
    result = gps103.convert_degrees_minutes_to_decimal(data[0:3], data[3:], hem)
    assert result == -172.548225

