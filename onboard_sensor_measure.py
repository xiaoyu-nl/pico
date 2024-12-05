import machine
import utime

# Initialize the onboard temperature sensor
sensor = machine.ADC(4)

# Constants for converting ADC reading to temperature
VOLTAGE_CONVERSION = 3.3 / (65535)  # Conversion factor for 16-bit ADC
TEMP_OFFSET = 27.0  # Temperature at 0.706V
TEMP_SLOPE = -0.001721  # Voltage-to-temp slope (approx.)

def read_temperature():
    """Reads the temperature from the onboard sensor and returns it in Celsius."""
    adc_value = sensor.read_u16()  # Read raw ADC value
    voltage = adc_value * VOLTAGE_CONVERSION  # Convert to voltage
    temperature = TEMP_OFFSET + (voltage - 0.706) / TEMP_SLOPE  # Convert to Celsius
    return temperature

def get_log_file_path():
    """Generates the file name for the current month's log."""
    timestamp = utime.localtime()  # Get the current time (assumes RTC is set)
    year = timestamp[0]
    month = timestamp[1]
    file_name = f"temperature_{year:04}_{month:02}.txt"
    return file_name

def log_temperature():
    """Logs the temperature with a timestamp to the current month's file."""
    try:
        temperature = read_temperature()
        timestamp = utime.localtime()  # Get the current time
        formatted_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
            timestamp[0], timestamp[1], timestamp[2], 
            timestamp[3], timestamp[4], timestamp[5]
        )
        
        # Create log entry
        log_entry = f"{formatted_time} - Temperature: {temperature:.2f}°C\n"
        print(log_entry, end="")  # Print to console for debugging
        
        # Write to the appropriate file for the current month
        log_file = get_log_file_path()
        with open(log_file, "a") as file:
            file.write(log_entry)
    
    except Exception as e:
        print(f"Error reading temperature or writing to file: {e}")
    print("Starting monthly temperature logging...")

while True:
    log_temperature()
    utime.sleep(15 * 60)  # Wait for 15 minutes


