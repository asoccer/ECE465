import socket
import sys
import os
import code
import readline
import rlcompleter


'''Connect to Drone'''
sys.path.append('../src')


print 'Connecting to drone...'
from Bybop_Discovery import *
import Bybop_Device


discovery = Discovery(DeviceID.ALL)
discovery.wait_for_change()
devices = discovery.get_devices()
discovery.stop()

#Check if connected
if not devices:
    print 'Shit didnt connect wtf'
    sys.exit(1)

device = devices.itervalues().next()
print 'Connecting to drone!'

d2c_port = 54322
controller_type = "PC_Server"
controller_name = "Group_Adam_Kevin_Kevin"

#Drone Variable
drone = Bybop_Device.create_and_connect(device, d2c_port, controller_type, controller_name)
drone.dump_state()

print 'Drone battery level is at ' + str(drone.get_battery())


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('', 4001)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)
options = {1: 'EOff',2:'Toff',3:'Land',4:'Lroll',6:'RRoll'}
while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >> sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            choice = int(data) #Don't send stupid letters
            if choice not in options.keys():
                print >> sys.stderr, 'not recognized command'
                connection.sendall('wrong command')
            else:
                print >> sys.stderr, 'Command Received->' + options.get(choice)
                connection.sendall(options.get(choice))
            #Evaluate the choice that was sent
            if choice in options.keys():
                if choice ==1:
                    drone.emergency()
                    
                elif choice== 2:
                    drone.take_off()
                elif choice ==3: 
                    drone.land()
                elif choice ==4: 
                    drone.send_data('ardrone3.Piloting.PCMD',(0,-50,0,0,0,0))
                elif choice ==6:
                    drone.send_data('ardrone3.Piloting.PCMD',(0,50,0,0,0,0))
                elif choice == 9:
                    drone.land()
                    drone.stop()
            
    except Exception as e:
        print e
        sys.exit(1)
    finally:
        # Clean up the connection
        connection.close()
