#!/usr/bin/python3

from datetime import datetime, timezone
import sys, os

size = 0


class Block:
    def __init__(self, prev_hash, time_stamp, case_id, item_id, state, data_length, data):
        self.prev_hash = prev_hash
        self.time_stamp = time_stamp
        self.case_id = case_id
        self.item_id = item_id
        self.state = state
        self.data_length = data_length
        self.data = data
        self.next = None


class Blockchain:

    def __init__(self, head=None):
        self.head = head

    def is_empty(self):
        return self.__sizeof__()

    def add(self, new_block):  # adds a new block to the blockchain
        global size
        size += 1
        current = self.head
        if current:
            while current.next:
                current = current.next
            current.next = new_block
        else:
            self.head = new_block

    def checkout(self, passed_item_id):  # marks a block state as "CHECKED OUT"
        current = self.head
        while current.next and (current.item_id != passed_item_id):
            current = current.next
        if current.item_id == passed_item_id:
            current.state = "CHECKEDOUT"

    def checkin(self, passed_item_id):  # marks a block state as "CHECKED IN"
        current = self.head
        while current.next and (current.item_id != passed_item_id):
            current = current.next
        if current.item_id == passed_item_id:
            current.state = "CHECKEDIN"

    def log(self):
        log = self.head
        while log is not None:
            print(log.prev_hash, log.time_stamp, log.case_id, log.item_id, log.state, log.data_length, log.data)
            log = log.next

    def remove(self, passed_item_id):  # removes a block
        current = self.head
        while current.next and (current.item_id != passed_item_id):
            prev = current
            current = current.next
        if current.item_id == passed_item_id:
            if current.state == "CHECKEDIN":
                prev = current.next

    # def init(self):

    # def verify(self):


def main():
    global size
    blockchain = Blockchain()
    cheese = True
    while cheese:
        try:
            inp = input()
            user_input = inp.split()
            time = datetime.now().isoformat()
            if len(user_input) > 0:
                if user_input[0] == 'bchoc':
                    match user_input[1]:
                        case 'add':
                            case_id = user_input[3]
                            item_id = user_input[5]
                            # print(time)
                            # blockchain.head = Block(None, time, case_id, item_id, "CHECKEDIN", None, None)
                            '''
                            if blockchain.block_chain_size > 0:
                                block = Block(None, time, case_id, item_id, "CHECKEDIN", None, None)
                            else:
                                block = Block(None, time, None, None, "INITIAL", 14, "Initial block")
                            '''
                            #blockchain.add(block)
                            if size > 0:
                                list = []
                                blockchain.add = Block(None, time, case_id, item_id, "CHECKEDIN", None, None)
                                blockchain.head.next = blockchain.add
                            else:
                                print("error")

                        case 'checkout':
                            print("add")
                        case 'checkin':
                            print("add")
                        case 'log':
                            blockchain.log()
                        case 'Remove':
                            print("remove")
                        case 'init':
                            if size > 0:
                                print("Blockchain file found with INITIAL block.")
                            else:
                                blockchain.head = Block(None, time, None, None, "INITIAL", 14, "Initial block")
                                print("Blockchain file not found. Created INITIAL block.")
                                size += 1
                        case 'verify':
                            print("verify")
                        case _:
                            print("error")
                else:
                    print("error")
        except EOFError:
            cheese = False
        except KeyboardInterrupt:
            cheese = False


if __name__ == "__main__":
    main()
