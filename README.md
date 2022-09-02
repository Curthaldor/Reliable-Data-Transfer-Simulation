# Reliable-Data-Transfer-Simulation
A simulation of data transmission to demonstrate how data transmission can be flawed, and the methods clients/servers use to maintain authenticity.

## Description
This script uses 'RDTLayer()' and 'UnreliableChannel()' to simulate a faulty data transfer. The script will instantiate two layers, each with a channel connecting them to each other, and a number of segments containing data as it is sent through the channels. Note that for this problem, the code I was tasked with implementing is only in the functions that I specify (all of which are in rdt_layer.py). All other functions are pre-written to define the premise of the problem that I was tasked with solving.

Example animations of operation are included in the images directory.

### rdt_main.py
The main script of this program. Here the objects are instantiated, and the data to be sent is defined.

"dataToSend" can be altered to change the message to whatever the user wishes.

The boolean values "outOfOrder", "dropPackets", "delayPackets", and "dataErrors" represent the types of flaws that are enabled in the UnreliableChannels, and can be toggled on or off.

main will then instantiate the operational objects and begin looping to represent packets being sent back and fourth.

main will end when it has detected that all the data has been sent and received.

### segment.py
A segment represents a single packet of data, and many are defined and utilized as the script runs.

### unreliable.py
A channel is a connection between two layer objects.

Channels in this script are designed to be faulty, based on the boolean flags set in main. With these flags, channel can be made unreliable, thus testing the validity of the data transfer algorithm.

### rdt_layer.py
A layer is a data-handling object that defines segments based on the "dataToSend" in rdt_main.py, and sends and receives them through a segment.

In this script, two layers are instantiated, representing a sender and a recipient, and the two will transfer and validate data until the recipient has a complete set of data.

The primary functions in this problem that were blank and I was tasked with defining were:

  getDataReceived() - Called when a segment has new segment that needs to be identified.

  processSend() - Called When a segment sends a segment.

  processReceiveAndSendRespond() - Called when a segment receives a segment.

The details of how I define these functions can be seen in the comments for each of them.
