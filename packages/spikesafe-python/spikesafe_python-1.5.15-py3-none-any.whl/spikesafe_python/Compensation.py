from .SpikeSafeEnums import LoadImpedance, RiseTime

# Dictionary string constants
low_current_range_maximum = 'low_current_range_maximum'
load_impedance_high_range_1 = 'load_impedance_high_range_1'
rise_time_high_range_1 = 'rise_time_high_range_1'
load_impedance_high_range_2 = 'load_impedance_high_range_2'
rise_time_high_range_2 = 'rise_time_high_range_2'
load_impedance_high_range_3 = 'load_impedance_high_range_3'
rise_time_high_range_3 = 'rise_time_high_range_3'
load_impedance_low_range_1 = 'load_impedance_low_range_1'
rise_time_low_range_1 = 'rise_time_low_range_1'
load_impedance_low_range_2 = 'load_impedance_low_range_2'
rise_time_low_range_2 = 'rise_time_low_range_2'

def get_optimum_compensation(spikesafe_model_max_current_amps, set_current_amps, pulse_on_time_seconds = None):
    """
    Returns the optimum compensation for a given set current, and optionally a given pulse on time

    Parameters
    ----------
    spikesafe_model_max_current_amps : float
        Maximum current of the SpikeSafe model
    set_current_amps : float
        Current to be set on SpikeSafe
    pulse_on_time_seconds : float, optional
        Pulse On Time to be set on SpikeSafe
    
    Returns
    -------
    int
        Load impedance command argument with optimum compensation
    int
        Rise time command argument with optimum compensation

    Remarks
    -------
    This function assumes the set current is operating on the optimized current range. If operating on the high range with a set current normally programmed on the low range, the compensation values will not be optimal. See online specification for range limits.

    If Load Impedance is returned as Medium or High, it is best practice to increase the Compliance Voltage setting by 5V to 30V. This helps the current amplifier to overcome inductance. If Compliance Voltage is not increased, then a Low Side Over Current or an Unstable Waveform error may occur.

    If an Operating Mode is used to sweep through steps of currents where the compensation settings are the same across the sweep, such as Pulse Sweep or Multiple Pulse Burst, it is recommended use the optimum compensation settings targeting the Stop Current.

    Raises
    ------
    ValueError
        If set_current_amps is greater than spikesafe_model_max_current_amps
    """

    if set_current_amps > spikesafe_model_max_current_amps:
        raise ValueError(f'Measurement current exceeds SpikeSafe model maximum current capability of {spikesafe_model_max_current_amps}A.')

    # Non-pulsing, or DC based modes, do not require compensation
    if pulse_on_time_seconds is None:
        return LoadImpedance.VERY_LOW, RiseTime.VERY_SLOW

    # Optimum compensation is intended for Pulse On Time of 500us or less
    if pulse_on_time_seconds is not None and pulse_on_time_seconds > 0.0005:
        return LoadImpedance.VERY_LOW, RiseTime.VERY_SLOW

    # Dictionary to store values for different model max currents
    model_params = {
        0.05: {
            low_current_range_maximum: 0.004,
            load_impedance_high_range_1: LoadImpedance.MEDIUM, rise_time_high_range_1: RiseTime.MEDIUM,
            load_impedance_high_range_2: LoadImpedance.LOW, rise_time_high_range_2: RiseTime.FAST,
            load_impedance_high_range_3: LoadImpedance.VERY_LOW, rise_time_high_range_3: RiseTime.SLOW,
            load_impedance_low_range_1: LoadImpedance.HIGH, rise_time_low_range_1: RiseTime.FAST,
            load_impedance_low_range_2: LoadImpedance.MEDIUM, rise_time_low_range_2: RiseTime.FAST
        },
        0.5: {
            low_current_range_maximum: 0.04,
            load_impedance_high_range_1: LoadImpedance.MEDIUM, rise_time_high_range_1: RiseTime.FAST,
            load_impedance_high_range_2: LoadImpedance.LOW, rise_time_high_range_2: RiseTime.FAST,
            load_impedance_high_range_3: LoadImpedance.LOW, rise_time_high_range_3: RiseTime.MEDIUM,
            load_impedance_low_range_1: LoadImpedance.HIGH, rise_time_low_range_1: RiseTime.FAST,
            load_impedance_low_range_2: LoadImpedance.MEDIUM, rise_time_low_range_2: RiseTime.FAST
        },
        2: {
            low_current_range_maximum: 0.2,
            load_impedance_high_range_1: LoadImpedance.MEDIUM, rise_time_high_range_1: RiseTime.FAST,
            load_impedance_high_range_2: LoadImpedance.LOW, rise_time_high_range_2: RiseTime.FAST,
            load_impedance_high_range_3: LoadImpedance.LOW, rise_time_high_range_3: RiseTime.MEDIUM,
            load_impedance_low_range_1: LoadImpedance.HIGH, rise_time_low_range_1: RiseTime.FAST,
            load_impedance_low_range_2: LoadImpedance.MEDIUM, rise_time_low_range_2: RiseTime.FAST
        },
        3: {
            low_current_range_maximum: 0.2,
            load_impedance_high_range_1: LoadImpedance.MEDIUM, rise_time_high_range_1: RiseTime.FAST,
            load_impedance_high_range_2: LoadImpedance.LOW, rise_time_high_range_2: RiseTime.FAST,
            load_impedance_high_range_3: LoadImpedance.LOW, rise_time_high_range_3: RiseTime.MEDIUM,
            load_impedance_low_range_1: LoadImpedance.HIGH, rise_time_low_range_1: RiseTime.FAST,
            load_impedance_low_range_2: LoadImpedance.MEDIUM, rise_time_low_range_2: RiseTime.FAST
        },
        4: {
            low_current_range_maximum: 0.2,
            load_impedance_high_range_1: LoadImpedance.MEDIUM, rise_time_high_range_1: RiseTime.FAST,
            load_impedance_high_range_2: LoadImpedance.LOW, rise_time_high_range_2: RiseTime.FAST,
            load_impedance_high_range_3: LoadImpedance.LOW, rise_time_high_range_3: RiseTime.MEDIUM,
            load_impedance_low_range_1: LoadImpedance.HIGH, rise_time_low_range_1: RiseTime.FAST,
            load_impedance_low_range_2: LoadImpedance.MEDIUM, rise_time_low_range_2: RiseTime.FAST
        },
        5: {
            low_current_range_maximum: 0.2,
            load_impedance_high_range_1: LoadImpedance.MEDIUM, rise_time_high_range_1: RiseTime.FAST,
            load_impedance_high_range_2: LoadImpedance.MEDIUM, rise_time_high_range_2: RiseTime.FAST,
            load_impedance_high_range_3: LoadImpedance.LOW, rise_time_high_range_3: RiseTime.MEDIUM,
            load_impedance_low_range_1: LoadImpedance.HIGH, rise_time_low_range_1: RiseTime.FAST,
            load_impedance_low_range_2: LoadImpedance.MEDIUM, rise_time_low_range_2: RiseTime.FAST
        },
        8: {
            low_current_range_maximum: 0.4,
            load_impedance_high_range_1: LoadImpedance.MEDIUM, rise_time_high_range_1: RiseTime.FAST,
            load_impedance_high_range_2: LoadImpedance.MEDIUM, rise_time_high_range_2: RiseTime.FAST,
            load_impedance_high_range_3: LoadImpedance.MEDIUM, rise_time_high_range_3: RiseTime.MEDIUM,
            load_impedance_low_range_1: LoadImpedance.HIGH, rise_time_low_range_1: RiseTime.FAST,
            load_impedance_low_range_2: LoadImpedance.MEDIUM, rise_time_low_range_2: RiseTime.FAST
        },
        # Tested for Mini 10A, but will also be used for PSMU HC 10A
        10: {
            low_current_range_maximum: 0.4,
            load_impedance_high_range_1: LoadImpedance.MEDIUM, rise_time_high_range_1: RiseTime.FAST,
            load_impedance_high_range_2: LoadImpedance.MEDIUM, rise_time_high_range_2: RiseTime.FAST,
            load_impedance_high_range_3: LoadImpedance.MEDIUM, rise_time_high_range_3: RiseTime.MEDIUM,
            load_impedance_low_range_1: LoadImpedance.HIGH, rise_time_low_range_1: RiseTime.FAST,
            load_impedance_low_range_2: LoadImpedance.MEDIUM, rise_time_low_range_2: RiseTime.FAST
        },
        16: {
            low_current_range_maximum: 0.8,
            load_impedance_high_range_1: LoadImpedance.MEDIUM, rise_time_high_range_1: RiseTime.FAST,
            load_impedance_high_range_2: LoadImpedance.LOW, rise_time_high_range_2: RiseTime.FAST,
            load_impedance_high_range_3: LoadImpedance.LOW, rise_time_high_range_3: RiseTime.MEDIUM,
            load_impedance_low_range_1: LoadImpedance.HIGH, rise_time_low_range_1: RiseTime.FAST,
            load_impedance_low_range_2: LoadImpedance.MEDIUM, rise_time_low_range_2: RiseTime.FAST
        },
        20: {
            low_current_range_maximum: 0.8,
            load_impedance_high_range_1: LoadImpedance.MEDIUM, rise_time_high_range_1: RiseTime.FAST,
            load_impedance_high_range_2: LoadImpedance.LOW, rise_time_high_range_2: RiseTime.FAST,
            load_impedance_high_range_3: LoadImpedance.LOW, rise_time_high_range_3: RiseTime.MEDIUM,
            load_impedance_low_range_1: LoadImpedance.HIGH, rise_time_low_range_1: RiseTime.FAST,
            load_impedance_low_range_2: LoadImpedance.MEDIUM, rise_time_low_range_2: RiseTime.FAST
        },
        32: {
            low_current_range_maximum: 1.6,
            load_impedance_high_range_1: LoadImpedance.MEDIUM, rise_time_high_range_1: RiseTime.FAST,
            load_impedance_high_range_2: LoadImpedance.LOW, rise_time_high_range_2: RiseTime.FAST,
            load_impedance_high_range_3: LoadImpedance.LOW, rise_time_high_range_3: RiseTime.MEDIUM,
            load_impedance_low_range_1: LoadImpedance.HIGH, rise_time_low_range_1: RiseTime.FAST,
            load_impedance_low_range_2: LoadImpedance.MEDIUM, rise_time_low_range_2: RiseTime.FAST
        },
        40: {
            low_current_range_maximum: 1.6,
            load_impedance_high_range_1: LoadImpedance.MEDIUM, rise_time_high_range_1: RiseTime.FAST,
            load_impedance_high_range_2: LoadImpedance.LOW, rise_time_high_range_2: RiseTime.FAST,
            load_impedance_high_range_3: LoadImpedance.LOW, rise_time_high_range_3: RiseTime.MEDIUM,
            load_impedance_low_range_1: LoadImpedance.HIGH, rise_time_low_range_1: RiseTime.FAST,
            load_impedance_low_range_2: LoadImpedance.MEDIUM, rise_time_low_range_2: RiseTime.FAST
        },
        60: {
            low_current_range_maximum: 3.2,
            load_impedance_high_range_1: LoadImpedance.MEDIUM, rise_time_high_range_1: RiseTime.FAST,
            load_impedance_high_range_2: LoadImpedance.LOW, rise_time_high_range_2: RiseTime.FAST,
            load_impedance_high_range_3: LoadImpedance.LOW, rise_time_high_range_3: RiseTime.MEDIUM,
            load_impedance_low_range_1: LoadImpedance.HIGH, rise_time_low_range_1: RiseTime.FAST,
            load_impedance_low_range_2: LoadImpedance.MEDIUM, rise_time_low_range_2: RiseTime.FAST
        }
    }

    model_params_current = model_params[spikesafe_model_max_current_amps]

    if __is_high_range__(set_current_amps, model_params_current):
        load_impedance, rise_time = __use_high_range_compensation__(spikesafe_model_max_current_amps, set_current_amps, model_params_current)
    else:
        load_impedance, rise_time = __use_low_range_compensation__(set_current_amps, model_params_current)

    return load_impedance, rise_time

# Helper function to determine if high current range should be used
def __is_high_range__(set_current_amps, model_params_current):
    if set_current_amps > model_params_current[low_current_range_maximum]:
        return True
    else:
        return False

# Helper function to use high current range compensation settings
def __use_high_range_compensation__(spikesafe_model_max_current_amps, set_current_amps, model_params_current):
    range_ratio = set_current_amps / spikesafe_model_max_current_amps
    if range_ratio < 0.5:
        return model_params_current[load_impedance_high_range_1], model_params_current[rise_time_high_range_1]
    elif range_ratio < 0.7:
        return model_params_current[load_impedance_high_range_2], model_params_current[rise_time_high_range_2]
    else:
        return model_params_current[load_impedance_high_range_3], model_params_current[rise_time_high_range_3]

# Helper function to use low current range compensation settings
def __use_low_range_compensation__(set_current_amps, model_params_current):
    range_ratio = set_current_amps / model_params_current[low_current_range_maximum]
    if range_ratio < 0.7:
        return model_params_current[load_impedance_low_range_1], model_params_current[rise_time_low_range_1]
    else:
        return model_params_current[load_impedance_low_range_2], model_params_current[rise_time_low_range_2]
