#!/usr/bin/python
"""Test Platform API 2.0 for thermal sensors"""

import sys
import re

try:
    from platform_test_common import *
except Exception as e:
    if __name__ == '__main__':
        print 'exception {} {}'.format(type(e), e)
        sys.exit(1)
    raise

platforms_dict = {
    'n3248te': {
        'Switch Near Temperature': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Switch Rear Temperature': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Front Panel PHY Temperature': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Near Front Panel Temperature': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Middle Fan Tray Temperature': {
            'model': 'NA',
            'serial': 'NA'
        }
    },

    's5212f': {
        'Port Mid': {
            'model': 'NA',
            'serial': 'NA'
        },
        'NPU Near': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Port Left': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Port Right': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Inlet Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'CPU': {
            'model': 'NA',
            'serial': 'NA'
        }
    },

    's5224f': {
        'CPU On-board': {
            'model': 'NA',
            'serial': 'NA'
        },
        'ASIC On-board': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Left': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Middle': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Right': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Inlet Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU1 Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU2 Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        }
    },

    's5232f': {
        'CPU On-board': {
            'model': 'NA',
            'serial': 'NA'
        },
        'ASIC On-board': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Left': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Middle': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Right': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Inlet Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU1 Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU2 Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        }
    },

    's5248f': {
        'CPU On-board': {
            'model': 'NA',
            'serial': 'NA'
        },
        'ASIC On-board': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Left': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Middle': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Right': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Inlet Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU1 Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU2 Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        }
    },

    's5296f': {
        'PT Middle Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'ASIC On-board': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PT Left Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PT Right Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Inlet Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU1 Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU2 Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU1 Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU2 Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'CPU On-board': {
            'model': 'NA',
            'serial': 'NA'
        }
    },

    's6000': {
        'ASIC On-board': {
            'model': 'NA',
            'serial': 'NA'
        },
        'NIC': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front': {
            'model': 'NA',
            'serial': 'NA'
        },
        'DIMM': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU1-Sensor 1': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU1-Sensor 2': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU2-Sensor 1': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU2-Sensor 2': {
            'model': 'NA',
            'serial': 'NA'
        },
        'CPU Core 0': {
            'model': 'NA',
            'serial': 'NA'
        },
        'CPU Core 1': {
            'model': 'NA',
            'serial': 'NA'
        }
    },

    'z9100': {
        'CPU On-board': {
            'model': 'NA',
            'serial': 'NA'
        },
        'ASIC On-board Rear': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Left': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Right': {
            'model': 'NA',
            'serial': 'NA'
        },
        'CPU Core 0': {
            'model': 'NA',
            'serial': 'NA'
        },
        'CPU Core 1': {
            'model': 'NA',
            'serial': 'NA'
        },
        'CPU Core 2': {
            'model': 'NA',
            'serial': 'NA'
        },
        'CPU Core 3': {
            'model': 'NA',
            'serial': 'NA'
        }
    },

    'z9264f': {
        'CPU On-board': {
            'model': 'NA',
            'serial': 'NA'
        },
        'ASIC On-board': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Left': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Middle': {
            'model': 'NA',
            'serial': 'NA'
        },
        'System Front Right': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Inlet Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU1 Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU2 Airflow Sensor': {
            'model': 'NA',
            'serial': 'NA'
        }
    },

    'z9332f': {
        'CPU On-board': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Baseboard U3': {
            'model': 'NA',
            'serial': 'NA'
        },
        'SW Internal': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Fan U52': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Fan U17': {
            'model': 'NA',
            'serial': 'NA'
        },
        'SW U52': {
            'model': 'NA',
            'serial': 'NA'
        },
        'SW U16': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU1 Inlet': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU1 Hotspot': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU2 Inlet': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU2 Hotspot': {
            'model': 'NA',
            'serial': 'NA'
        },
        'SW U04': {
            'model': 'NA',
            'serial': 'NA'
        },
        'SW U14': {
            'model': 'NA',
            'serial': 'NA'
        },
        'SW U4403': {
            'model': 'NA',
            'serial': 'NA'
        }
    },

    'z9432f': {
        'MB Temp1': {
            'model': 'NA',
            'serial': 'NA'
        },
        'MB Temp2': {
            'model': 'NA',
            'serial': 'NA'
        },
        'MB Temp3': {
            'model': 'NA',
            'serial': 'NA'
        },
        'MB Temp4': {
            'model': 'NA',
            'serial': 'NA'
        },
        'Fanboard Temp': {
            'model': 'NA',
            'serial': 'NA'
        },
        'NPU Mid Temp': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU1 Normal Temp': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU1 Sys Temp': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU1 Chassis Temp': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU2 Normal Temp': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU2 Sys Temp': {
            'model': 'NA',
            'serial': 'NA'
        },
        'PSU2 Chassis Temp': {
            'model': 'NA',
            'serial': 'NA'
        },
        'CPU Temp': {
            'model': 'NA',
            'serial': 'NA'
        },
        'DRAM1 Temp': {
            'model': 'NA',
            'serial': 'NA'
        },
        'DRAM2 Temp': {
            'model': 'NA',
            'serial': 'NA'
        }
    }
}

def check_name(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, str):
        return False
    if methods_results_dict[method] not in platform_dict:
        print_item_mesg(mesg_lvl_err, errid, '{}() unknown or duplicated'.format(method))
        return False
    return True

def check_str(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, str):
        return False
    name_valid, name = method_result_get(methods_results_dict, 'get_name')
    if not name_valid:
        return True
    if name not in platform_dict:
        return False
    expected = platform_dict[name][method[4:]]
    if methods_results_dict[method] != expected:
        print_item_mesg(mesg_lvl_err, errid, '{}() incorrect'.format(method))
        print_mesg(mesg_lvl_info, 'expected {}'.format(expected))
        return False
    return True

def check_positive_float(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, float):
        return False
    if methods_results_dict[method] <= 0.0:
        print_item_mesg(mesg_lvl_err, errid, '{}() invalid'.format(method))
        print_mesg(mesg_lvl_info, 'expected > 0.0')
        return False
    return True

methods_list = (
    ('get_name',                    check_name),
    ('get_presence',                check_bool_warn_if_false),
    ('get_status',                  check_status),
    ('get_model',                   check_str),
    ('get_serial',                  check_str),
    ('get_temperature',             check_positive_float),
    ('get_low_threshold',           check_positive_float),
    ('get_high_threshold',          check_positive_float),
    ('get_low_critical_threshold',  check_positive_float),
    ('get_high_critical_threshold', check_positive_float)
)

def check_set_threshold(errid, sensor, set_method, get_method, threshold_list):
    result = True
    for threshold in threshold_list:
        api_status, api_result = api_wrapper(errid, sensor, set_method, threshold, check_type=bool)
        if not api_status:
            result = False
            continue
        if not api_result:
            print_item_mesg(mesg_lvl_err, errid, '{}({}) failed'.format(set_method, threshold))
            result = False
            continue
        api_status, api_result = api_wrapper(errid, sensor, get_method, check_type=float)
        if not api_status:
            result = False
            continue
        if api_result != threshold:
            print_item_mesg(mesg_lvl_err, errid, '{}() incorrect'.format(get_method))
            print_mesg(mesg_lvl_info, 'expected {}'.format(threshold))
            result = False
    return result

def test_set(errid, sensor):
    pmon_pause()
    result = check_set_threshold(errid, sensor, 'set_high_threshold', 'get_high_threshold', (100.0, 90.0))
    result &= check_set_threshold(errid, sensor, 'set_low_threshold', 'get_low_threshold', (20.0, 10.0))
    pmon_unpause()
    return result

def test(platform):
    test_name_set('thermal_test')
    test_item_set('sensor')
    if platform not in platforms_dict:
        print_mesg(mesg_lvl_err, 'unknown platform {}'.format(platform))
        return False
    platform_dict = dict(platforms_dict[platform])
    chassis = chassis_get()
    if chassis is None:
        return False
    api_status, sensors_list = api_wrapper(None, chassis, 'get_all_thermals', check_type=list)
    if not api_status:
        return False
    result, num_sensors = api_wrapper(None, chassis, 'get_num_thermals', check_type=int)
    if result and num_sensors != len(sensors_list):
        print_mesg(mesg_lvl_err, 'get_num_thermals() not consistent')
        print_mesg(mesg_lvl_info, 'len(get_all_thermals()) = {}'.format(len(sensors_list)))
        result = False
    idx = -1
    for sensor in sensors_list:
        idx += 1
        api_status, sensor_by_idx = api_wrapper(None, chassis, 'get_thermal', idx)
        if api_status:
            if sensor_by_idx is not sensor:
                print_mesg(mesg_lvl_err, 'get_thermal({}) not consistent'.format(idx))
                result = False
        else:
            result = False
        methods_results_dict = {}
        errid = sensor
        name = None
        for method, _ in methods_list:
            api_status, api_result = api_wrapper(errid, sensor, method)
            if not api_status:
                result = False
                continue
            methods_results_dict[method] = api_result
            if method == 'get_name' and api_status:
                errid = api_result
                name = api_result
        for method, func in methods_list:
            if method not in methods_results_dict:
                continue
            result &= func(platform_dict, errid, methods_results_dict, method)
        result &= test_set(errid, sensor)
        if name not in platform_dict:
            continue
        del platform_dict[name]
    if platform_dict:
        print_mesg(mesg_lvl_err, 'platform missing sensors {}'.format(platform_dict.keys()))
    return result

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run Platform API 2.0 test for thermal sensors')
    parser.add_argument('-q', action='store_true', help='Quiet mode, no messages printed')
    parser.add_argument('-v', action='store_true', help='Verbose mode, extra messages printed')
    parser.add_argument('platform', choices=sorted(platforms_dict.keys()), help='Platform to test')
    args = parser.parse_args()
    if args.q:
        mesg_lvl_set(mesg_lvl_none)
    if args.v:
        mesg_lvl_set(mesg_lvl_all)
    sys.exit(0 if test(args.platform) else 1)
