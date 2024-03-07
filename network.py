import random
import time
from receiver import RDTReceiver
import threading

"""
NOTE: YOU SHOULD NOT MODIFY THIS CLASS
"""


class NetworkLayer:
    """ The network layer that deliver packets and acknowledgments between sender and receiver """

    def __init__(self, reliability=1.0, delay=1.0, pkt_corrupt=True, ack_corrupt=True, pkt_loss=True, ack_loss=True,pkt_wait=0):
        """ initialize the network layer
        :param reliability: the probability that the network layer will deliver the message correctly
        :param delay: the round trip time for sending a packet and receive a reply
        :param pkt_corrupt: sender packets will be corrupted
        :param ack_corrupt: receiver acknowledgments will be corrupted
        """
        self.reliability = reliability
        self.packet = None
        self.reply = None
        self.delay = delay
        self.pkt_corrupt = pkt_corrupt
        self.ack_corrupt = ack_corrupt
        self.pkt_loss = pkt_loss
        self.ack_loss = ack_loss
        self.pkt_wait = pkt_wait
        # self.loseAck = False
        
        self.recv = RDTReceiver()  # connect the network layer to the receiver

    def get_network_reliability(self):
        """ show network layer reliability
        :return: a float number represent the current network reliability
        """
        return self.reliability

    def __packet_loss_probability(self):
        """ calculate the probability that a pocket will be lost
        :return: True if the probability greater than the network reliability
        """
        ran = random.uniform(0, 1)
        if ran > self.reliability:
            return True
        return False
    
    def __packet_corruption_probability(self):
        """ calculate the probability that a pocket will be corrupted
        :return: True if the probability greater than the network reliability
        """
        ran = random.uniform(0, 1)
        if ran > self.reliability:
            return True
        return False

    def __corrupt_packet(self):
        """ Corrupt the sender packet, it could corrupt the seq_num, the data or the checksum
        :return: no return value
        """
        ran = random.randint(1, 90)
        if ran < 30:
            self.packet['sequence_number'] = chr(random.randint(ord('2'), ord('9')))
            return
        if ran < 60:
            self.packet['data'] = chr(random.randint(ord('!'), ord('}')))
            return
        if ran < 90:
            self.packet['checksum'] = random.randint(ord('!'), ord('}'))

    def __corrupt_reply(self):
        """ Corrupt the receiver reply (acknowledgments) packet
        :return: no return value
        """
        ran = random.randint(1, 100)
        if ran < 50:
            self.reply['ack'] = chr(random.randint(2, 9))
        else:
            self.reply['checksum'] = chr(random.randint(ord('2'), ord('9')))
            
    def __lose_packet(self):
        """ Lose the sender packet
        :return: no return value
        """
        self.packet = None
        
    def __lose_reply(self):
        """ Lose the receiver reply (acknowledgments) packet
        :return: no return value
        """
        self.reply = None


    def udt_send(self, frame):
        """ implement the delivery service of the unreliable network layer
        :param frame: a python dictionary represent the a sender's packet or a receiver's reply
        :return: the receiver's reply as a python dictionary returned to the sender
        """

        # TODO: You may add ONLY print statements to this function for debugging purpose
        self.packet = frame
        print("Packet Sent")
        s_test = self.__packet_corruption_probability()
        s_test_loss = self.__packet_loss_probability()
        wait_time = self.delay / 2

        if s_test and self.pkt_corrupt and self.packet is not None:
            self.__corrupt_packet()
            print("network layer: Packet Corrupted " + str(self.packet))

        if s_test_loss and self.pkt_loss and self.pkt_wait < wait_time:
            # self.__lose_packet()
            print("network layer: Lost Packet  " + str(self.packet))

        time.sleep(self.delay)
    

        # bridge|connect the RDT sender and receiver
        self.reply = self.recv.rdt_rcv(self.packet)

        r_test = self.__packet_corruption_probability()
        r_test_loss = self.__packet_loss_probability()
        if r_test and self.ack_corrupt and self.reply is not None:
            self.__corrupt_reply()
            print("network layer: receiver acknowledgment corrupted " + str(self.reply))

        if r_test_loss and self.ack_loss and self.pkt_wait < wait_time:
            # self.__lose_reply()
            print("network layer: Lost Acknowledgment  " + str(self.reply))
            
        return self.reply
