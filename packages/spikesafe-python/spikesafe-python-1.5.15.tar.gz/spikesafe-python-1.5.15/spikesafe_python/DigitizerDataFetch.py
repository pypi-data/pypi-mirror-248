# Goal: Read all new voltage readings from SpikeSafe PSMU Digitizer
# SCPI Command: VOLT:FETC?
# Array of voltage readings are parsed into DigitizerData class
# Example data return: b'9.9712145e-01,1.0005457e+00,3.2105038e+01\n'

import sys
import logging
from .DigitizerData import DigitizerData
from .Threading import wait
from .ReadAllEvents import read_all_events

log = logging.getLogger(__name__)

def fetch_voltage_data(spike_safe_socket, enable_logging = None):
    """Returns an array of voltage readings from the digitizer obtained through a fetch query 

    Parameters
    ----------
    spike_safe_socket : TcpSocket
        Socket object used to communicate with SpikeSafe
    enable_logging : bool, Optional
        Overrides spike_safe_socket.enable_logging attribute (default to None will use spike_safe_socket.enable_logging value)
    
    Returns
    -------
    digitizer_data_collection: DigitizerData[]
        Contains an array of DigitizerData objects which each have a Sample Number and Voltage Reading

    Raises
    ------
    Exception
        On any error
    """
    try:
        # fetch the Digitizer voltage readings
        spike_safe_socket.send_scpi_command('VOLT:FETC?', enable_logging)
        digitizer_data_string = spike_safe_socket.read_data(enable_logging)

        # set up the DigitizerData array to be returned
        digitizer_data_collection = []

        # put the fetched data in a plottable data format
        voltage_reading_strings = digitizer_data_string.split(",")
        sample = 1
        for v in voltage_reading_strings:
            data_point = DigitizerData()
            data_point.voltage_reading = float(v)
            data_point.sample_number = sample

            digitizer_data_collection.append(data_point)
            sample += 1

        return digitizer_data_collection

    except Exception as err:
        # print any error to the log file and raise error to function caller
        log.error("Error fetching digitizer voltage data: {}".format(err))                                     
        raise

def wait_for_new_voltage_data(spike_safe_socket, wait_time = 0.0, enable_logging = None):
    """Queries the SpikeSafe PSMU digitizer until it responds that it has acquired new data

    This is a useful function to call prior to sending a fetch query, because it determines whether fetched data will be freshly acquired

    Parameters
    ----------
    spike_safe_socket : TcpSocket
        Socket object used to communicate with SpikeSafe
    wait_time: float
        Wait time in between each set of VOLT:NDAT? queries in seconds. Use get_new_voltage_data_estimated_complete_time() for the recommended value
    enable_logging : bool, Optional
        Overrides spike_safe_socket.enable_logging attribute (default to None will use spike_safe_socket.enable_logging value)
    
    Raises
    ------
    Exception
        On any error
    """
    try:
        digitizer_has_new_data = ''
        while True:                  
            # check for new digitizer data
            spike_safe_socket.send_scpi_command('VOLT:NDAT?', enable_logging)
            digitizer_has_new_data = spike_safe_socket.read_data(enable_logging)
            if (digitizer_has_new_data == 'TRUE'):
                break
            elif digitizer_has_new_data == 'ERROR':
                raise ValueError('SpikeSafe digitizer data error')

            wait(wait_time)  

    except Exception as err:
        # print any error to the log file and raise error to function caller
        log.error("Error waiting for new digitizer voltage data: %s", err)
        raise

def get_new_voltage_data_estimated_complete_time(aperture_microseconds, reading_count, hardware_trigger_count=None, hardware_trigger_delay_microseconds=None):
    """
    Returns the estimated minimum possible time it will take for the SpikeSafe PSMU digitizer to acquire new voltage readings. If hardware triggering is used, this does not take into account the pulse period, so the actual time may be longer.

    Parameters
    ----------
    aperture_microseconds : int
        Aperture in microseconds
    
    reading_count : int
        Number of readings to be taken

    hardware_trigger_count : int, optional
        Number of hardware triggers to be sent
    
    hardware_trigger_delay_microseconds : int, optional
        Delay in microseconds between each hardware trigger

    Returns
    -------
    float
        Estimated fetch time in seconds

    Raises
    ------
    None

    """
    if hardware_trigger_count is None:
        hardware_trigger_count = 1  # There is always 1 software "trigger" to start the Digitizer processing new voltage data

    if hardware_trigger_delay_microseconds is None:
        hardware_trigger_delay_microseconds = 0  # Default value if not provided

    if hardware_trigger_count == 1:
        # 𝑀𝑖𝑛𝑖𝑚𝑢𝑚 𝑇𝑜𝑡𝑎𝑙 𝐴𝑐𝑞𝑢𝑖𝑠𝑖𝑡𝑖𝑜𝑛 𝑇𝑖𝑚𝑒 = 𝑇𝑟𝑖𝑔𝑔𝑒𝑟 𝐶𝑜𝑢𝑛𝑡 (𝑇𝑟𝑖𝑔𝑔𝑒𝑟 𝐷𝑒𝑙𝑎𝑦+𝐴𝑝𝑒𝑟𝑡𝑢𝑟𝑒 𝑇𝑖𝑚𝑒×𝑅𝑒𝑎𝑑𝑖𝑛𝑔 𝐶𝑜𝑢𝑛𝑡)
        estimated_complete_time_seconds = (hardware_trigger_count * (hardware_trigger_delay_microseconds + aperture_microseconds * reading_count)) / 100000
    else:
        retrigger_time_microseconds = 600
        # 𝑀𝑖𝑛𝑖𝑚𝑢𝑚 𝑇𝑜𝑡𝑎𝑙 𝐴𝑐𝑞𝑢𝑖𝑠𝑖𝑡𝑖𝑜𝑛 𝑇𝑖𝑚𝑒 = 𝑇𝑟𝑖𝑔𝑔𝑒𝑟 𝐶𝑜𝑢𝑛𝑡 (𝑇𝑟𝑖𝑔𝑔𝑒𝑟 𝐷𝑒𝑙𝑎𝑦 + Retrigger Time + 𝐴𝑝𝑒𝑟𝑡𝑢𝑟𝑒 𝑇𝑖𝑚𝑒 × 𝑅𝑒𝑎𝑑𝑖𝑛𝑔 𝐶𝑜𝑢𝑛𝑡) - Retrigger Time (ignore time last trigger)
        estimated_complete_time_seconds = (hardware_trigger_count * (hardware_trigger_delay_microseconds + retrigger_time_microseconds + aperture_microseconds * reading_count) - retrigger_time_microseconds) / 100000

    # wait time cannot be less than 0s
    estimated_complete_time_seconds = max(estimated_complete_time_seconds, 0)

    return estimated_complete_time_seconds
