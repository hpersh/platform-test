#!/usr/bin/python
"""Test Platform API 2.0 for components"""

import sys
import re

try:
    from platform_test_common import *
except Exception as e:
    if __name__ == '__main__':
        print 'exception {} {}'.format(type(e), e)
        sys.exit(1)
    raise

re_bios_vers      = '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+-[0-9]+$'
re_cpld_fpga_vers = '[0-9]+\.[0-9]+$'
re_bmc_vers       = '[0-9]+\.[0-9]+$'

platforms_dict = {
    'n3248te': {
        'BIOS': {
            'desc': 'Performs initialization of hardware components during booting',
            'vers': re_bios_vers
        },
        'CPU CPLD': {
            'desc': 'Used for managing the CPU power sequence and CPU states',
            'vers': re_cpld_fpga_vers
        },
        'SYS CPLD': {
            'desc': 'Used for managing FAN, PSU, SFP modules (1-48) SFP Plus modules (49-62)',
            'vers': re_cpld_fpga_vers
        }
    },

    's5212f': {
        'BIOS': {
            'desc': 'Performs initialization of hardware components during booting',
            'vers': re_bios_vers
        },
        'FPGA': {
            'desc': 'Used for managing the system LEDs',
            'vers': re_cpld_fpga_vers
        },
        'BMC': {
            'desc': 'Platform management controller for on-board temperature '
                    'monitoring, in-chassis power, Fan and LED control',
            'vers': re_bmc_vers
        },
        'System CPLD': {
            'desc': 'Used for managing the CPU power sequence and CPU states',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 1': {
            'desc': 'CHECK THIS -- Used for managing SFP28/QSFP28 port transceivers (SFP28 1-24, QSFP28 1-4)',
            'vers': re_cpld_fpga_vers
        }
    },

    's5224f': {
        'BIOS': {
            'desc': 'Performs initialization of hardware components during booting',
            'vers': re_bios_vers
        },
        'FPGA': {
            'desc': 'Used for managing the system LEDs',
            'vers': re_cpld_fpga_vers
        },
        'BMC': {
            'desc': 'Platform management controller for on-board temperature '
                    'monitoring, in-chassis power, Fan and LED control',
            'vers': re_bmc_vers
        },
        'System CPLD': {
            'desc': 'Used for managing the CPU power sequence and CPU states',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 1': {
            'desc': 'Used for managing SFP28/QSFP28 port transceivers (SFP28 1-24, QSFP28 1-4)',
            'vers': re_cpld_fpga_vers
        }
    },

    's5232f': {
        'BIOS': {
            'desc': 'Performs initialization of hardware components during booting',
            'vers': re_bios_vers
        },
        'FPGA': {
            'desc': 'Used for managing the system LEDs',
            'vers': re_cpld_fpga_vers
        },
        'BMC': {
            'desc': 'Platform management controller for on-board temperature '
                    'monitoring, in-chassis power, Fan and LED control',
            'vers': re_bmc_vers             
        },
        'System CPLD': {
            'desc': 'Used for managing the CPU power sequence and CPU states',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 1': {
            'desc': 'Used for managing SFP28/QSFP28 port transceivers (SFP28 1-24, QSFP28 1-4)',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 2': {
            'desc': 'CHECK THIS --Used for managing SFP28/QSFP28 port transceivers (SFP28 25-48, QSFP28 5-8)',
            'vers': re_cpld_fpga_vers
        }
    },

    's5248f': {
        'BIOS': {
            'desc': 'Performs initialization of hardware components during booting',
            'vers': re_bios_vers
        },
        'FPGA': {
            'desc': 'Used for managing the system LEDs',
            'vers': re_cpld_fpga_vers
        },
        'BMC': {
            'desc': 'Platform management controller for on-board temperature '
                    'monitoring, in-chassis power, Fan and LED control',
            'vers': re_bmc_vers
        },
        'System CPLD': {
            'desc': 'Used for managing the CPU power sequence and CPU states',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 1': {
            'desc': 'Used for managing SFP28/QSFP28 port transceivers (SFP28 1-24, QSFP28 1-4)',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 2': {
            'desc': 'Used for managing SFP28/QSFP28 port transceivers (SFP28 25-48, QSFP28 5-8)',
            'vers': re_cpld_fpga_vers
        }
    },

    's5296f': {
        'BIOS': {
            'desc': 'Performs initialization of hardware components during booting',
            'vers': re_bios_vers
        },
        'FPGA': {
            'desc': 'Used for managing the system LEDs',
            'vers': re_cpld_fpga_vers
        },
        'BMC': {
            'desc': 'Platform management controller for on-board temperature '
                    'monitoring, in-chassis power, Fan and LED control',
            'vers': re_bmc_vers
        },
        'System CPLD': {
            'desc': 'Used for managing the CPU power sequence and CPU states',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 1': {
            'desc': 'Used for managing SFP28/QSFP28 port transceivers (SFP28 1-24, QSFP28 1-4)',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 2': {
            'desc': 'Used for managing SFP28/QSFP28 port transceivers (SFP28 25-48, QSFP28 5-8)',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 3': {
            'desc': 'Used for managing SFP28/QSFP28 port transceivers (SFP28 49-72)',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 4': {
            'desc': 'Used for managing SFP28/QSFP28 port transceivers (SFP28 73-96)',
            'vers': re_cpld_fpga_vers
        }
    },

    's6000': {
        'BIOS': {
            'desc': 'Performs initialization of hardware components during booting',
            'vers': re_bios_vers
        },
        'System-CPLD': {
            'desc': 'Used for managing CPU board devices and power',
            'vers': re_cpld_fpga_vers
        },
        'Master-CPLD': {
            'desc': 'Used for managing Fan, PSU, system LEDs, QSFP modules (1-16)',
            'vers': re_cpld_fpga_vers
        },
        'Slave-CPLD': {
            'desc': 'Used for managing QSFP modules (17-32)',
            'vers': re_cpld_fpga_vers
        }
    },

    's6100': {
        'BIOS': {
            'desc': 'Performs initialization of hardware components during booting',
            'vers': re_bios_vers
        },
        'CPLD': {
            'desc': 'Used for managing IO modules, SFP+ modules and system LEDs',
            'vers': re_cpld_fpga_vers
        },
        'FPGA': {
            'desc': 'Platform management controller for on-board temperature '
                    'monitoring, in-chassis power, Fan and LED control',
            'vers': re_cpld_fpga_vers
        }            
    },

    'z9100': {
        'BIOS': {
            'desc': 'Performs initialization of hardware components during booting',
            'vers': re_bios_vers
        },
        'CPLD1': {
            'desc': 'Used for managing the system LEDs',
            'vers': re_cpld_fpga_vers
        },
        'CPLD2': {
            'desc': 'Used for managing QSFP28 modules (1-12)',
            'vers': re_cpld_fpga_vers
        },            
        'CPLD3': {
            'desc': 'Used for managing QSFP28 modules (13-22)',
            'vers': re_cpld_fpga_vers
        },
        'CPLD4': {
            'desc': 'Used for managing QSFP28 modules (23-32) and SFP+ modules',
            'vers': re_cpld_fpga_vers
        },
        'FPGA': {
            'desc': 'Platform management controller for on-board temperature '
                    'monitoring, in-chassis power, Fan and LED control',
            'vers': re_cpld_fpga_vers
        }
    },

    'z9264f': {
        'BIOS': {
            'desc': 'Performs initialization of hardware components during booting',
            'vers': re_bios_vers
        },
        'FPGA': {
            'desc': 'Used for managing the system LEDs',
            'vers': re_cpld_fpga_vers
        },
        'BMC': {
            'desc': 'Platform management controller for on-board temperature '
                    'monitoring, in-chassis power, Fan and LED control',
            'vers': re_bmc_vers
        },
        'System CPLD': {
            'desc': 'Used for managing the CPU power sequence and CPU states',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 1': {
            'desc': 'Used for managing SFP28/QSFP28 port transceivers (SFP28 1-24, QSFP28 1-4)',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 2': {
            'desc': 'Used for managing SFP28/QSFP28 port transceivers (SFP28 25-48, QSFP28 5-8)',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 3': {
            'desc': 'CHECK THIS -- Used for managing SFP28/QSFP28 port transceivers (SFP28 49-72)',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 4': {
            'desc': 'CHECK THIS -- Used for managing SFP28/QSFP28 port transceivers (SFP28 73-96)',
            'vers': re_cpld_fpga_vers
        }
    },

    'z9332f': {
        'BIOS': {
            'desc': 'Performs initialization of hardware components during booting',
            'vers': re_bios_vers
        },
        'FPGA': {
            'desc': 'Used for managing the system LEDs',
            'vers': re_cpld_fpga_vers
        },
        'BMC': {
            'desc': 'Platform management controller for on-board temperature '
                    'monitoring, in-chassis power, Fan and LED control',
            'vers': re_bmc_vers
        },
        'Baseboard CPLD': {
            'desc': 'Used for managing the CPU power sequence and CPU states',
            'vers': re_cpld_fpga_vers
        },
        'Switch CPLD 1': {
            'desc': 'Used for managing QSFP28/SFP port transceivers ',
            'vers': re_cpld_fpga_vers
        },
        'Switch CPLD 2': {
            'desc': 'Used for managing QSFP28/SFP port transceivers',
            'vers': re_cpld_fpga_vers
        }
    },

    'z9432f': {
        'BIOS': {
            'desc': 'Performs initialization of hardware components during booting',
            'vers': re_bios_vers
        },
        'FPGA': {
            'desc': 'Used for managing the system LEDs',
            'vers': re_cpld_fpga_vers
        },
        'BMC': {
            'desc': 'Platform management controller for on-board temperature '
                    'monitoring, in-chassis power, Fan and LED control',
            'vers': re_bmc_vers
        },
        'System CPLD': {
            'desc': 'Used for managing the CPU power sequence and CPU states',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 1': {
            'desc': 'Used for managing SFP28/QSFP28 port transceivers (SFP28 1-24, QSFP28 1-4)',
            'vers': re_cpld_fpga_vers
        },
        'Slave CPLD 2': {
            'desc': 'CHECK THIS -- Used for managing SFP28/QSFP28 port transceivers (SFP28 25-48, QSFP28 5-8)',
            'vers': re_cpld_fpga_vers
        }
    }
}

def test(platform):
    test_name_set('component_test')
    test_item_set('component')
    if platform not in platforms_dict:
        print_mesg(mesg_lvl_err, 'unknown platform {}'.format(platform))
        return False
    platform_dict = dict(platforms_dict[platform])
    chassis = chassis_get()
    if chassis is None:
        return False
    api_status, components_list = api_wrapper(None, chassis, 'get_all_components', check_type=list)
    if not api_status:
        return False
    result, num_components = api_wrapper(None, chassis, 'get_num_components', check_type=int)
    if result and num_components != len(components_list):
        print_mesg(mesg_lvl_err, 'get_num_components() not consistent')
        print_mesg(mesg_lvl_info, 'len(get_all_components()) = {}'.format(len(components_list)))
        result = False
    idx = -1
    for component in components_list:
        idx += 1
        errid = component
        api_status, component_by_idx = api_wrapper(None, chassis, 'get_component', idx)
        if api_status:
            if component_by_idx is not component:
                print_mesg(mesg_lvl_err, 'get_component({}) not consistent'.format(idx))
                result = False
        else:
            result = False    
        api_status, name = api_wrapper(errid, component, 'get_name')
        if api_status:
            errid = name
        else:
            result = False
        api_status, desc = api_wrapper(errid, component, 'get_description')
        result &= api_status
        api_status, vers = api_wrapper(errid, component, 'get_firmware_version')
        result &= api_status

        component_dict = None
        if name is not None:
            if name in platform_dict:
                component_dict = platform_dict[name]
            else:
                print_mesg(mesg_lvl_err, 'unexpected component {!r}'.format(errid))
                result = False
        if component_dict is not None:
            if desc is not None and desc != component_dict['desc']:
                print_item_mesg(mesg_lvl_err, errid, 'description incorrect')
                print_mesg(mesg_lvl_info, 'expected description {!r}'.format(component_dict['desc']))
                result = False
            if vers is not None and re.match(component_dict['vers'], vers) is None:
                print_item_mesg(mesg_lvl_err, errid, 'badly-formed version')
                result = False
            del platform_dict[name]
    if platform_dict:
        print_mesg(mesg_lvl_err, 'platform missing components {}'.format(platform_dict.keys()))
        result = False
    return result

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run Platform API 2.0 test for components')
    parser.add_argument('-q', action='store_true', help='Quiet mode, no messages printed')
    parser.add_argument('-v', action='store_true', help='Verbose mode, extra messages printed')
    parser.add_argument('platform', choices=sorted(platforms_dict.keys()), help='Platform to test')
    args = parser.parse_args()
    if args.q:
        mesg_lvl_set(mesg_lvl_none)
    if args.v:
        mesg_lvl_set(mesg_lvl_all)
    sys.exit(0 if test(args.platform) else 1)
