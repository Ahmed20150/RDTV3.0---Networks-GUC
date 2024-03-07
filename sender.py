import threading
import time

#Dr.Saad accepted 

class SenderProcess:
    """ Represent the sender process in the application layer  """

    __buffer = list()

    @staticmethod
    def set_outgoing_data(buffer):
        """ To set the message the process would send out over the network
        :param buffer:  a python list of characters represent the outgoing message
        :return: no return value
        """
        SenderProcess.__buffer = buffer
        return

    @staticmethod
    def get_outgoing_data():
        """ To get the message the process would send out over the network
        :return:  a python list of characters represent the outgoing message
        """
        return SenderProcess.__buffer


class RDTSender:
    """ Implement the Reliable Data Transfer Protocol V2.2 Sender Side """

    sequence = '0'
    
    wait_done = False
    
    def __init__(self, net_srv):
        """ This is a class constructor
            It initialize the RDT sender sequence number  to '0' and the network layer services
            The network layer service provide the method udt_send(send_pkt)
        """
        self.sequence = '0'
        self.net_srv = net_srv
        self.reply=None
        self.wait_done = False

    @staticmethod
    def get_checksum(data):
        """ Calculate the checksum for outgoing data
        :param data: one and only one character, for example data = 'A'
        :return: the ASCII code of the character, for example ASCII('A') = 65
        """
        # TODO provide your own implementation

        checksum = ord(data)  # you need to change that
        return checksum

    @staticmethod
    def clone_packet(packet):
        """ Make a copy of the outgoing packet
        :param packet: a python dictionary represent a packet
        :return: return a packet as python dictionary
        """
        pkt_clone = {
            'sequence_number': packet['sequence_number'],
            'data': packet['data'],
            'checksum': packet['checksum']
        }
        return pkt_clone

    @staticmethod
    def is_corrupted(reply):
        """ Check if the received reply from receiver is corrupted or not
        :param reply: a python dictionary represent a reply sent by the receiver
        :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted
        """
        # TODO provide your own implementation
 
        return reply['checksum'] != ord(reply['ack'])
        

    @staticmethod
    def is_expected_seq(reply, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
        :param reply: a python dictionary represent a reply sent by the receiver
        :param exp_seq: the sender expected sequence number '0' or '1' represented as a character
        :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        # TODO provide your own implementation
        checker1 = reply['ack']
        if (checker1 == exp_seq):
            return True
        
        return False
    
    @staticmethod
    def is_lost(reply):
        """ Check if the received reply from receiver is lost or not
        :param reply: a python dictionary represent a reply sent by the receiver
        :return: True -> if the reply is lost | False ->  if the reply is NOT lost
        """
        
        return reply == None
        
        

    @staticmethod
    def make_pkt(seq, data, checksum):
        """ Create an outgoing packet as a python dictionary
        :param seq: a character represent the sequence number of the packet, the one expected by the receiver '0' or '1'
        :param data: a single character the sender want to send to the receiver
        :param checksum: the checksum of the data the sender will send to the receiver
        :return: a python dictionary represent the packet to be sent
        """
        
        packet = {
            'sequence_number': seq,
            'data': data,
            'checksum': checksum
        }
        return packet
    
    
    def __wait(self):
        self.wait_done = False
        time.sleep(self.net_srv.pkt_wait)
        self.wait_done=True

        return

    def __send(self,pkt):
        print(pkt)
        self.reply= None
        self.reply=self.net_srv.udt_send(pkt)
        return 




    def rdt_send(self, process_buffer):
        """ Implement the RDT v2.2 for the sender
        :param process_buffer:  a list storing the message the sender process wish to send to the receiver process
        :return: terminate without returning any value
        """
        # TODO provide your own implementation
        # for every character in the buffer
        for data in process_buffer:
            
            print("sender expected sequence: " + self.sequence)
            

            checksum = RDTSender.get_checksum(data)
            pkt = RDTSender.make_pkt(self.sequence, data, checksum)
            
            print("sender sending packet: " + str(pkt))
            
            cloned_pkt = RDTSender.clone_packet(pkt)
            reply = self.net_srv.udt_send(pkt)
            
            while True:

                # while not self.net_srv.loseAck:

                # reply = self.net_srv.udt_send(pkt)


                waiting_thread = threading.Thread(target=self.__wait)
                    
                waiting_thread.start()

                sending_thread= threading.Thread(target=self.__send,args=(pkt,))

                sending_thread.start()

                # while(self.net_srv.loseAck or not self.wait_done):
                #     print(f"loseAck: {self.net_srv.loseAck}, wait-done: {self.wait_done}")
                #         # pass

                while self.reply == None and self.wait_done == False:
                    pass

                if self.reply != None:
                # and not self.is_corrupted(reply) and RDTSender.is_expected_seq(reply, self.sequence):



                    while( self.is_corrupted(reply) or not RDTSender.is_expected_seq(reply, self.sequence) ):  
                        
                        
                        pkt = RDTSender.clone_packet(cloned_pkt)
                        
                        reply = self.net_srv.udt_send(pkt)

                
                
                    self.sequence = '1' if self.sequence == '0' else '0'

                    break

                else:
                    pkt = RDTSender.clone_packet(cloned_pkt)
                    
                    continue


        print(f'Sender Done!')
        return
