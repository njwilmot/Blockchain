#!/usr/bin/python3

import os
import sys
import re
from collections import Counter
from datetime import datetime, timezone
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
    tail = None

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

    def forward_log(self):
        log = self.head
        blocks = []
        items = []
        while log is not None:
            block = []
            if log.item_id is None:
                print("\nCase: " + str(log.case_id))
                print("\tAdded item: " + str(log.item_id) + "\n\tAction: " + str(log.state) +
                      "\n\tTime: " + str(log.time_stamp) + "\n")

            if log.item_id is not None:
                block.append(str(log.case_id))
                block.append(str(log.state))
                block.append(str(log.time_stamp))

                for item in log.item_id:
                    block.append(str(item))
                    items.append(str(item))
            if len(block) > 0:
                blocks.append(block)
            log = log.next

        case_IDs = []
        for i in blocks:
            case_IDs.append(i[0])
        non_duplicates = list(dict.fromkeys(case_IDs))

        for unique in non_duplicates:
            print("\nCase: " + str(unique))
            for nodes in blocks:
                if unique == nodes[0]:
                    for it in nodes[3:]:
                        print("\tAdded item: " + str(it) + "\n\tAction: " + str(nodes[1]) + "\n\tTime: " + str(nodes[2]) + "\n")


    def reverse_log(self, log):
        if log:
            self.reverse_log(log.next)
            print("\nCase: " + str(log.case_id) + "\nItem: " + str(log.item_id) + "\nAction: " + str(log.state) +
                  "\nTime: " + str(log.time_stamp))
        else:
            return

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
    global case_list
    blockchain = Blockchain()
    cheese = True
    while cheese:
        try:
            inp = input("\n")
            user_input = inp.split()
            time = datetime.now(timezone.utc).isoformat()  # timestamp in UTC
            if len(user_input) > 1:
                if user_input[0] == 'bchoc':
                    match user_input[1]:  # fix will cause arr out of bounds error
                        case 'add':

                            indices = []
                            for idx, value in enumerate(user_input):
                                if value == '-i':
                                    indices.append(idx)

                            item_ids = []
                            for i in indices:
                                item_ids.append(user_input[i + 1])

                            cid = user_input.index('-c')
                            case_id = user_input[cid + 1]

                            # item_id = user_input[i_id_list]
                            if size > 0:
                                new_block = Block(None, time, case_id, item_ids, "CHECKEDIN", None, None)
                                blockchain.add(new_block)
                            else:
                                print("bchoc init first")

                        case 'checkout':
                            print("add")
                        case 'checkin':
                            print("add")
                        case 'log':
                            blockchain.forward_log()
                            # reverse print if user inputs "-r" blockchain.reverse_log(blockchain.head)
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
                            print("default error")
                else:
                    print("enter bchoc first")
            else:
                print("No user input")
        except EOFError:
            cheese = False
        except KeyboardInterrupt:
            cheese = False


if __name__ == "__main__":
    main()
