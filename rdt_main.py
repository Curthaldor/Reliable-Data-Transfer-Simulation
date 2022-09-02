from rdt_layer import *
from unreliable import UnreliableChannel
import time

# #################################################################################################################### #
# Main                                                                                                                 #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #

# #################################################################################################################### #
# The following are two sets of data input to the communication test. The first is small and the second is longer.     #
# Start by uncomming the shorter until you feel you have a good algorithm. Then confirm it still works on a larger     #
# scale by switching to the larger.                                                                                    #
#                                                                                                                      #
# #################################################################################################################### #

dataToSend = "The quick brown fox jumped over the lazy dog"

# #################################################################################################################### #

# Create client and server
client = RDTLayer()
server = RDTLayer()

# Start with a reliable channel (all flags false)
# As you create your rdt algorithm for send and receive, turn these on.
outOfOrder = True
dropPackets = True
delayPackets = True
dataErrors = True

# Create unreliable communication channels
clientToServerChannel = UnreliableChannel(outOfOrder,dropPackets,delayPackets,dataErrors)
serverToClientChannel = UnreliableChannel(outOfOrder,dropPackets,delayPackets,dataErrors)

# Creat client and server that connect to unreliable channels
client.setSendChannel(clientToServerChannel)
client.setReceiveChannel(serverToClientChannel)
server.setSendChannel(serverToClientChannel)
server.setReceiveChannel(clientToServerChannel)

# Set initial data that will be sent from client to server
client.setDataToSend(dataToSend)

input("Press enter to begin...")
loopIter = 0            # Used to track communication timing in iterations
while True:
    print("-----------------------------------------------------------------------------------------------------------")
    loopIter += 1
    print("Time (iterations) = {0}".format(loopIter))

    # Sequence to pass segments back and forth between client and server
    print("Client------------------------------------------")
    client.processData()
    clientToServerChannel.processData()
    print("Server------------------------------------------")
    server.processData()
    serverToClientChannel.processData()


    # show the data received so far
    print("Main--------------------------------------------")
    dataReceivedFromClient = server.getDataReceived()
    print("DataReceivedFromClient: {0}".format(dataReceivedFromClient))

    if dataReceivedFromClient == dataToSend:
        print('$$$$$$$$ ALL DATA RECEIVED $$$$$$$$')
        break

    time.sleep(0.001)
    #input("Press enter to continue...")

print("countTotalDataPackets: {0}".format(clientToServerChannel.countTotalDataPackets))
print("countSentPackets: {0}".format(clientToServerChannel.countSentPackets + serverToClientChannel.countSentPackets))
print("countChecksumErrorPackets: {0}".format(clientToServerChannel.countChecksumErrorPackets))
print("countOutOfOrderPackets: {0}".format(clientToServerChannel.countOutOfOrderPackets))
print("countDelayedPackets: {0}".format(clientToServerChannel.countDelayedPackets + serverToClientChannel.countDelayedPackets))
print("countDroppedDataPackets: {0}".format(clientToServerChannel.countDroppedPackets))
print("countAckPackets: {0}".format(serverToClientChannel.countAckPackets))
print("countDroppedAckPackets: {0}".format(serverToClientChannel.countDroppedPackets))
print("# segment timeouts: {0}".format(client.countSegmentTimeouts))
print("TOTAL ITERATIONS: {0}".format(loopIter))

print()
input("Press enter to continue...")