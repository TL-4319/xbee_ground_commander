from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
import time

# Pre generated commands
sbus_frame_zero_all_ch = bytearray([15,172,96,5,43,88,193,10,86,176,130,21,172,96,5,43,88,193,10,86,176,130,21,0,0])
sbus_frame_set_mode_2 = bytearray([15,172,96,5,43,88,49,113,86,176,130,21,172,96,5,43,88,193,10,86,176,130,21,0,0])
sbus_frame_set_mode_1 = bytearray([15,172,96,5,43,88,241,61,86,176,130,21,172,96,5,43,88,193,10,86,176,130,21,0,0])
sbus_frame_set_take_off = bytearray([15,172,96,5,43,88,49,113,86,76,156,21,172,96,5,43,88,193,10,86,176,130,21,0,0])
sbus_frame_set_land = sbus_frame_set_mode_2

# Radio module MAC address
radio1_addr = "0013A20042179B54"
radio2_addr = "0013A2004214BAAF"

###################################################################
#           Main script
###################################################################
# Instantiate devices
local = XBeeDevice("/dev/ttyUSB0",115200)

# Begin communication with local radio
local.open()
# Instantiate remote radio --- ADD radio modules here
remote2 = RemoteXBeeDevice(local, XBee64BitAddress.from_hex_string(radio2_addr))

try:
    # Flight sequence begins here
    print ("Reseting all RC channel")
    local.send_data_broadcast(sbus_frame_zero_all_ch)
    time.sleep(2)

    print ("Set flight mode to auto for all UAV")
    local.send_data_broadcast(sbus_frame_set_mode_2)
    time.sleep(2)

    # Malt 2 take of
    print ("Malt 2 takes off")
    local.send_data(remote2,sbus_frame_set_take_off)

    while True:
        print("Mission Inprogress")
        time.sleep(5)

except KeyboardInterrupt:
    print ("Ending mission. All UAV to LAND mode")
    local.send_data_broadcast(sbus_frame_set_land)
    time.sleep(10)
    local.close()

except:
    print ("Unexpected error. All UAV to LAND mode")
    local.send_data_broadcast(sbus_frame_set_land)
    time.sleep(10)
    local.close()



