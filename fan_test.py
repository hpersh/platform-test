#!/usr/bin/python
"""Test Platform API 2.0 for fans"""

import sys
import re
import time

try:
    from platform_test_common import *
except Exception as e:
    if __name__ == '__main__':
        print 'exception {} {}'.format(type(e), e)
        sys.exit(1)
    raise

platforms_dict = {
    'n3248te': {
        'fans': {
            'names': ['FanTray1', 'FanTray2', 'FanTray3'],
            'skus': (
                {'model': '048M8Y', 'serial': 'TW048M8YDNT00.*$', 'direction': 'exhaust'},
            )
        },
        'psu_fans': {
            'names': ['PSU1 Fan', 'PSU2 Fan'],
            'skus': (
                {'model': 'E PSU', 'serial': 'AC-DC-12V', 'direction': 'exhaust'},
            )
        }
    },

    's5212f': {
        'fans': {
            'names': [
                'FanTray1-Fan1', 'FanTray1-Fan2',
                'FanTray2-Fan1', 'FanTray2-Fan2',
                'FanTray3-Fan1', 'FanTray3-Fan2',
                'FanTray4-Fan1', 'FanTray4-Fan2'
            ],
            'skus': (
                {'model': '0VK93CX01', 'serial': 'CN0VK93CCES00', 'direction': 'exhaust'},
            )
        },
        'psu_fans': {
            'names': ['PSU1 Fan', 'PSU2 Fan'],
            'skus': (
                {'model': '0VK93CX01', 'serial': 'CN0VK93CCES00.*%', 'direction': 'exhaust'},
            )
        }
    },

    's5224f': {
        'fans': {
            'names': [
                'FanTray1-Fan1', 'FanTray1-Fan2',
                'FanTray2-Fan1', 'FanTray2-Fan2',
                'FanTray3-Fan1', 'FanTray3-Fan2',
                'FanTray4-Fan1', 'FanTray4-Fan2'
            ],
            'skus': (
                {'model': '0CNY0XA00', 'serial': 'CN0CNY0XCES00.*$', 'direction': 'CHECK_THIS'},
            )
        },
        'psu_fans': {
            'names': ['PSU1 Fan', 'PSU2 Fan'],
            'skus': (
                {'model': 'CHECK THIS', 'serial': 'CHECK_THIS', 'direction': 'CHECK_THIS'},
            )
        }
    },

    's5232f': {
        'fans': {
            'names': [
                'FanTray1-Fan1', 'FanTray1-Fan2',
                'FanTray2-Fan1', 'FanTray2-Fan2',
                'FanTray3-Fan1', 'FanTray3-Fan2',
                'FanTray4-Fan1', 'FanTray4-Fan2'
            ],
            'skus': (
                {'model': '07R5RFX01', 'serial': 'CN07R5RFCES00.*$', 'direction': 'CHECK_THIS'},
            )
        },
        'psu_fans': {
            'names': ['PSU1 Fan', 'PSU2 Fan'],
            'skus': (
                {'model': 'CHECK THIS', 'serial': 'CHECK_THIS', 'direction': 'CHECK_THIS'},
            )
        }
    },

    's5248f': {
        'fans': {
            'names': [
                'FanTray1-Fan1', 'FanTray1-Fan2',
                'FanTray2-Fan1', 'FanTray2-Fan2',
                'FanTray3-Fan1', 'FanTray3-Fan2',
                'FanTray4-Fan1', 'FanTray4-Fan2'
            ],
            'skus': (
                {'model': '0CNY0XX01', 'serial': 'CN0CNY0XCES00.*$', 'direction': 'CHECK_THIS'},
            )
        },
        'psu_fans': {
            'names': ['PSU1 Fan', 'PSU2 Fan'],
            'skus': (
                {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS$', 'direction': 'CHECK_THIS'},
            )
        }
    },
    
    's5296f': {
        'fans': {
            'names': ['FanTray1-Fan1', 'FanTray2-Fan1', 'FanTray3-Fan1', 'FanTray4-Fan1'],
            'skus': (
                {'model': '00KJKXX01', 'serial': 'CN00KJKXCES00.*$', 'direction': 'intake'},
            )
        },
        'psu_fans': {
            'names': ['PSU1 Fan', 'PSU2 Fan'],
            'skus': (
                {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS', 'direction': 'CHECK_THIS'},
            )
        }
    },

    's6000': {
        'fans': {
            'names': ['FanTray1-Fan1', 'FanTray2-Fan1', 'FanTray3-Fan1', 'FanTray4-Fan1'],
            'skus': (
                {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS', 'direction': 'CHECK_THIS'},
            ),
            'set_methods': ('set_speed', 'set_status_led'),
            'test_speeds': (100, 50)
        },
        'psu_fans': {
            'names': ['PSU1 Fan', 'PSU2 Fan'],
            'skus': (
                {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS', 'direction': 'CHECK_THIS'},
            )
        }
    },

    'z9100': {
        'fans': {
            'names': [
                'FanTray1-Fan1', 'FanTray1-Fan2', 
                'FanTray2-Fan1', 'FanTray2-Fan2', 
                'FanTray3-Fan1', 'FanTray3-Fan2', 
                'FanTray4-Fan1', 'FanTray4-Fan2', 
                'FanTray5-Fan1', 'FanTray5-Fan2'
            ],
            'skus': (
                {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS', 'direction': 'CHECK_THIS'},
            )
        },
        'psu_fans': {
            'names': ['PSU1 Fan', 'PSU2 Fan'],
            'skus': (
                {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS', 'direction': 'CHECK_THIS'},
            )
        }
    },

    'z9264f': {
        'fans': {
            'names': [
                'FanTray1-Fan1', 'FanTray1-Fan2', 
                'FanTray2-Fan1', 'FanTray2-Fan2', 
                'FanTray3-Fan1', 'FanTray3-Fan2', 
                'FanTray4-Fan1', 'FanTray4-Fan2'
            ],
            'skus': (
                {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS', 'direction': 'CHECK_THIS'},
            )
        },
        'psu_fans': {
            'names': ['PSU1 Fan', 'PSU2 Fan'],
            'skus': (
                {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS', 'direction': 'CHECK_THIS'},
            )
        }
    },

    'z9332f': {
        'fans': {
            'names': [
                'FanTray1-Fan1', 'FanTray1-Fan2', 
                'FanTray2-Fan1', 'FanTray2-Fan2', 
                'FanTray3-Fan1', 'FanTray3-Fan2', 
                'FanTray4-Fan1', 'FanTray4-Fan2',
                'FanTray5-Fan1', 'FanTray5-Fan2',
                'FanTray6-Fan1', 'FanTray6-Fan2',
                'FanTray7-Fan1', 'FanTray7-Fan2'
            ],
            'skus': (
                {'model': '210D9', 'serial': 'CN0210D9AVS0097800.*$', 'direction': 'CHECK_THIS'},
            )
        },
        'psu_fans': {
            'names': ['PSU1 Fan', 'PSU2 Fan'],
            'skus': (
                {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS', 'direction': 'CHECK_THIS'},
            )
        }
    },

    'z9432f': {
        'fans': {
            'names': [
                'FanTray1-Fan1', 'FanTray1-Fan2', 
                'FanTray2-Fan1', 'FanTray2-Fan2', 
                'FanTray3-Fan1', 'FanTray3-Fan2', 
                'FanTray4-Fan1', 'FanTray4-Fan2',
                'FanTray5-Fan1', 'FanTray5-Fan2',
                'FanTray6-Fan1', 'FanTray6-Fan2',
                'FanTray7-Fan1', 'FanTray7-Fan2'
            ],
            'skus': (
                {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS', 'direction': 'CHECK_THIS'},
            )
        },
        'psu_fans': {
            'names': ['PSU1 Fan', 'PSU2 Fan'],
            'skus': (
                {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS', 'direction': 'CHECK_THIS'},
            )
        }
    }    
}

def check_name(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, str):
        return False
    if not any([(methods_results_dict[method] in platform_dict[x]['names']) for x in ('fans', 'psu_fans')]):
        print_item_mesg(mesg_lvl_err, errid, '{}() unknown or duplicated'.format(method))
        return False
    return True

def check_direction(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, str):
        return False
    direction = methods_results_dict[method]
    present_valid, present = method_result_get(methods_results_dict, 'get_presence')
    if not present_valid:
        return True
    if present is True and direction not in ('intake', 'exhaust'):
        print_item_mesg(mesg_lvl_err, errid, '{}() incorrect'.format(method))
        print_mesg(mesg_lvl_info, 'expected one of (\'intake\', \'exhaust\')')
        return False
    if present is False and direction != 'NA':
        print_item_mesg(mesg_lvl_err, errid, '{}() incorrect'.format(method))
        print_mesg(mesg_lvl_info, 'expected \'NA\' when absent')
        return False
    return True

def check_speed_pct(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, int):
        return False
    speed = methods_results_dict[method]
    present_valid, present = method_result_get(methods_results_dict, 'get_presence')
    if not present_valid:
        return True
    if present is True and (speed <= 0 or speed > 100):
        print_item_mesg(mesg_lvl_err, errid, '{}() incorrect'.format(method))
        print_mesg(mesg_lvl_info, 'expected in range 1..100 when present')
        return False
    if present is False and speed != 0:
        print_item_mesg(mesg_lvl_err, errid, '{}() incorrect'.format(method))
        print_mesg(mesg_lvl_info, 'expected 0 when absent')
        return False
    return True

def check_sku(skus_list, errid, methods_results_dict, method):
    if methods_results_dict.get('get_presence') is not True:
        print_item_mesg(mesg_lvl_info, errid, 'not present, skipping SKU check')
        return True
    model_valid, model = method_result_get(methods_results_dict, 'get_model')
    serial_valid, serial = method_result_get(methods_results_dict, 'get_serial')
    if not model_valid and not serial_valid:
        print_item_mesg(mesg_lvl_info, errid, 'both model and serial unknown, cannot determine SKU')
        return True
    direction_valid, direction = method_result_get(methods_results_dict, 'get_direction')
    for sku in skus_list:
        if ((not model_valid or model == sku['model'])
            and (not serial_valid or re.match(sku['serial'], serial) is not None)
            ):
            print_item_mesg(mesg_lvl_info, errid, 'matches SKU model {} serial {}'.format(sku['model'], sku['serial']))
            if direction_valid and direction != sku['direction']:
                print_item_mesg(mesg_lvl_err, errid, 'incorrect direction for SKU')
                print_mesg(mesg_lvl_info, 'expected {}'.format(sku['direction']))
                return False
            return True
    print_item_mesg(mesg_lvl_err, errid, 'unknown SKU')
    return False

methods_list = (
    ('get_name',            check_name),
    ('get_presence',        check_bool_warn_if_false),
    ('get_model',           check_non_empty_str_na_if_absent),
    ('get_serial',          check_non_empty_str_na_if_absent),
    ('get_status',          check_status),
    ('get_direction',       check_direction),
    ('get_speed',           check_speed_pct),
    ('get_speed_rpm',       check_positive_int_non_zero_when_present),
    ('get_target_speed',    check_speed_pct),
    ('get_speed_tolerance', check_speed_pct),
    ('get_status_led',      check_status_led)
)

def check_set_speed(fans_dict, errid, fan):
    if 'set_methods' not in fans_dict or 'set_speed' not in fans_dict['set_methods']:
        print_item_mesg(mesg_lvl_info, errid, 'set_speed() not supported')
        return api_wrapper(errid, fan, 'set_speed', 100, check_not_implemented=True)
    print_item_mesg(mesg_lvl_info, errid, 'set_speed() supported')
    api_status, tolerance = api_wrapper(errid, fan, 'get_speed_tolerance', check_type=int)
    if not api_status:
        return False
    for speed in fans_dict['test_speeds']:
        api_status, api_result = api_wrapper(errid, fan, 'set_speed', speed, check_type=bool)
        if not api_status:
            return False
        if not api_result:
            print_item_mesg(mesg_lvl_err, errid, 'set_speed({}) failed'.format(speed))
            return False
        print_item_mesg(mesg_lvl_info, errid, 'waiting for fan to settle...')
        time.sleep(10)
        api_status, api_result = api_wrapper(errid, fan, 'get_target_speed', check_type=int)
        if not api_status:
            return False
        if api_result != speed:
            print_item_mesg(mesg_lvl_err, errid, 'get_target_speed() incorrect')
            print_mesg(mesg_lvl_info, 'expected {}'.format(speed))
            return False
        api_status, api_result = api_wrapper(errid, fan, 'get_speed', check_type=int)
        if not api_status:
            return False
        delta = api_result - speed
        if delta < -tolerance or delta > tolerance:
            print_item_mesg(mesg_lvl_err, errid, 'get_speed() value not within tolerance')
            return False
    return True

def check_set_status_led(fans_dict, errid, fan):
    if 'set_methods' not in fans_dict or 'set_status_led' not in fans_dict['set_methods']:
        print_item_mesg(mesg_lvl_info, errid, 'set_status_led() not supported')
        return api_wrapper(errid, fan, 'set_status_led', 'red', check_not_implemented=True)
    print_item_mesg(mesg_lvl_info, errid, 'set_status_led() supported')
    for color in ('red', 'green'):
        api_status, api_result = api_wrapper(errid, fan, 'set_status_led', color, check_type=bool)
        if not api_status:
            return False
        if not api_result:
            print_item_mesg(mesg_lvl_err, errid, 'set_status_led({}) failed'.format(color))
            return False
        api_status, api_result = api_wrapper(errid, fan, 'get_status_led', check_type=str)
        if not api_status:
            return False
        if api_result != color:
            print_item_mesg(mesg_lvl_err, errid, 'get_status_led() incorrect')
            print_mesg(mesg_lvl_err, 'expected {!r}'.format(color))
            return False
    return True

def test_set(fans_dict, errid, fan):
    pmon_pause()
    result = check_set_speed(fans_dict, errid, fan)
    result &= check_set_status_led(fans_dict, errid, fan)
    pmon_unpause()
    return result

def test(platform):
    test_name_set('fan_test')
    test_item_set('fan')
    if platform not in platforms_dict:
        print_mesg(mesg_lvl_err, 'unknown platform {}'.format(platform))
        return False
    platform_dict = dict(platforms_dict[platform])
    chassis = chassis_get()
    if chassis is None:
        return False
    api_status, fans_list = api_wrapper(None, chassis, 'get_all_fans', check_type=list)
    if not api_status:
        return False
    result, num_fans = api_wrapper(None, chassis, 'get_num_fans', check_type=int)
    if result and num_fans != len(fans_list):
        print_mesg(mesg_lvl_err, 'get_num_fans() not consistent')
        print_mesg(mesg_lvl_info, 'len(get_all_fans()) = {}'.format(len(fans_list)))
        result = False
    api_status, psus_list = api_wrapper(None, chassis, 'get_all_psus', check_type=list)
    if api_status:
        for psu in psus_list:
            api_status, psu_fans = api_wrapper(None, psu, 'get_all_fans', check_type=list)
            if not api_status:
                result = False
                continue
            api_status, num_psu_fans = api_wrapper(None, psu, 'get_num_fans', check_type=int)
            if api_status:
                if num_psu_fans != len(psu_fans):
                    print_mesg(mesg_lvl_err, 'get_num_fans() not consistent')
                    print_mesg(mesg_lvl_info, 'len(get_all_fans()) = {}'.format(len(psu_fans)))
                    result = False
            else:
                result = False
            fans_list += psu_fans
    else:
        result = False    
    for fan in fans_list:
        methods_results_dict = {}
        errid = fan
        name = None
        for method, _ in methods_list:
            api_status, api_result = api_wrapper(errid, fan, method)
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
        if name is None:
            continue
        if name in platform_dict['fans']['names']:
            fans_dict = platform_dict['fans']
        elif name in platform_dict['psu_fans']['names']:
            fans_dict = platform_dict['psu_fans']
        else:
            print_mesg(mesg_lvl_err, 'unknown or invalid name, skipping SKU check')
            result = False
            continue
        result &= check_sku(fans_dict['skus'], errid, methods_results_dict, method)
        result &= test_set(fans_dict, errid, fan)
        fans_dict['names'].remove(name)
    li = platform_dict['fans']['names'] + platform_dict['psu_fans']['names']
    if li:
        print_mesg(mesg_lvl_err, 'missing fans {}'.format(li))
        result = False
    return result

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run Platform API 2.0 test for fans')
    parser.add_argument('-q', action='store_true', help='Quiet mode, no messages printed')
    parser.add_argument('-v', action='store_true', help='Verbose mode, extra messages printed')
    parser.add_argument('platform', choices=sorted(platforms_dict.keys()), help='Platform to test')
    args = parser.parse_args()
    if args.q:
        mesg_lvl_set(mesg_lvl_none)
    if args.v:
        mesg_lvl_set(mesg_lvl_all)
    sys.exit(0 if test(args.platform) else 1)
