from segment import Segment
import math


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4  # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15  # in characters          # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0  # Use this for segment 'timeouts'
    # Add items as needed
    countSegmentTimeouts = 0

    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.currentIteration = 0
        # Add items as needed
        self.seqnum = 0 # The next data segment to be sent.
        self.recieved = {} # The list of data segments recieved.
        self.prevAck = 0 # The last ACK recieved.
        self.timoutCount = 0 # Timeout counter.

    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self, data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # ############################################################################################################ #
        # Identify the data that has been received...

        recieved = ""
        i = 0

        # Until a data segment is missing in the sequence...
        while i in self.recieved:
            # Put the data segment in-order
            recieved += self.recieved[i]
            # Incriment the iterator through the data list.
            i += self.DATA_LENGTH

        # ############################################################################################################ #
        return recieved

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()

    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processSend(self):

        # ############################################################################################################ #

        # You should pipeline segments to fit the flow-control window
        # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
        # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
        # These constants are given in # characters

        # Somewhere in here you will be creating data segments to send.
        # The data is just part of the entire string that you are trying to send.
        # The seqnum is the sequence number for the segment (in character number, not bytes)

        # Determine number of packets to be sent at once in pipeline
        # End function if no data to send (this will happen on server calls).

        # If there is no data to send, do nothing.
        if self.dataToSend == '':
            return

        # If there's been a timeout, send the segment corresponding with the ACK.
        # Or if all data has already been sent, bypass the timout and default to sending missing ACKs.
        if self.timoutCount >= 5 or self.seqnum > len(self.dataToSend):
            # Send the latest requested sequence.
            segmentSend = Segment()
            segmentSend.setData(self.prevAck, self.dataToSend[self.prevAck: (self.prevAck + self.DATA_LENGTH)])
            print("Sending segment: ", segmentSend.to_string())
            self.sendChannel.send(segmentSend)

            # Reset the timeout counter.
            self.timoutCount = 0
            
        # If the resend flags have not been set...
        else:
            # For as many data segments that can fit in the window size...
            for i in range(0, math.floor(self.FLOW_CONTROL_WIN_SIZE / self.DATA_LENGTH)):
                # Send those new segments.
                segmentSend = Segment()
                segmentSend.setData(self.seqnum, self.dataToSend[self.seqnum: (self.seqnum + self.DATA_LENGTH)])
                print("Sending segment: ", segmentSend.to_string())
                self.sendChannel.send(segmentSend)

                # Increment the data sent counter.
                self.seqnum += self.DATA_LENGTH

    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):
    
        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()
        # If the list is empty(aka there were no segments recieved), do nothing.
        if listIncomingSegments == []:
            return

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented
        
        # If the segments have data...
        if listIncomingSegments[0].acknum == -1:
            # For each segment...
            for segment in listIncomingSegments:
                # If the segment data is valid...
                if segment.checkChecksum() == True:
                    # Add it to the list of stored data.
                    self.recieved[segment.seqnum] = segment.payload

            # Send an ACK with the value of the highest in-order segment catalogued.
            segmentAck = Segment()
            segmentAck.setAck(len(self.getDataReceived()))
            print("Sending ack: ", segmentAck.to_string())
            self.sendChannel.send(segmentAck)
        
        # If the segment is an ACK...
        else:
            # If it's the same ACK as last time...
            if self.prevAck == listIncomingSegments[0].acknum:
                # Increment the timeout counter.
                self.timoutCount += 1
            # Note the new ACK value.
            self.prevAck = listIncomingSegments[0].acknum
            # If the same ACK has been seen too many times...
            if self.timoutCount >= 5:
                # Increment the total timeouts counter.
                self.countSegmentTimeouts += 1

        # ############################################################################################################ #
        # How do you respond to what you have received?
        # How can you tell data segments apart from ack segemnts?

        # Data segments return with a -1 in the acknum.

        # Somewhere in here you will be setting the contents of the ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...

