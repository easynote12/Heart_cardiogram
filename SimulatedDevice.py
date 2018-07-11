import time
import sys
import serial
# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=HeartDev.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=mP5anzqU0JObxbeJEYDKiVCKg+H+oHCp8dXNIa+8jF8="
ser=serial.Serial(port='COM3', baudrate = 9600, bytesize = serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=2)



# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = "{\"heart_point\": %.2f}"

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        k=0
        res=''
        while True:
            inp=ser.read()
            if(inp.isdigit()):
                res=res+inp
                k=k+1
                if(k==3):
                    #print(res)
                    
                    heart_point =float(res)
                    #print(heart_point)
                    msg_txt_formatted = MSG_TXT % (heart_point)
                    message = IoTHubMessage(msg_txt_formatted)
                    print( "Sending message: %s" % message.get_string() )
                    client.send_event_async(message, send_confirmation_callback, None)
                    time.sleep(1)
                    
                    res=''
                    k=0                                                   
            else:
                if(res.isdigit()):
                    heart_point=float(res)
                    #print(heart_point)
                    msg_txt_formatted = MSG_TXT % (heart_point)
                    message = IoTHubMessage(msg_txt_formatted)
                    print( "Sending message: %s" % message.get_string() )
                    client.send_event_async(message, send_confirmation_callback, None)
                    time.sleep(1)
                #print(res)
                res=''
                k=0
                                
           

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub device" )
    print ( "Press Ctrl-C to exit" )
    if(ser.isOpen()):
        print("Port opened")
        iothub_client_telemetry_sample_run()
    else:
        print("Can not open")
        
       
        
    
