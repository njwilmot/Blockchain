#!/usr/bin/env python3

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
    tail = None

    def write_blockchain(self, file):
        current = self.head
        while current is not None:
            '''
            lines = (str(current.prev_hash) + "\n"), (str(current.time_stamp) + "\n"), (str(current.case_id) + "\n"),
                     (str(current.item_id) + "\n"), (str(current.state) + "\n"), (str(current.data_length) + "\n"),
                     (str(current.data) + "\n")
            file.write(lines)
            current = current.next
            '''
            file.write(str(current.prev_hash) + "\n")
            file.write(str(current.time_stamp) + "\n")
            file.write(str(current.case_id) + "\n")
            file.write(str(current.item_id) + "\n")
            file.write(str(current.state) + "\n")
            file.write(str(current.data_length) + "\n")
            file.write(str(current.data) + "\n")
            current = current.next

    def read_blockchain(self, file):
        while True:
            try:
                prev_hash = next(file).strip("\n")
                time_stamp = next(file).strip("\n")
                case_id = next(file).strip("\n")
                item_id = next(file).strip("\n")
                state = next(file).strip("\n")
                data_length = next(file).strip("\n")
                data = next(file).strip("\n")
                new_block = Block(prev_hash, time_stamp, case_id, item_id, state, data_length, data)
                self.add(new_block)
            except StopIteration:
                break

    def __init__(self, head=None):
        self.head = head

    def is_empty(self):
        return self.__sizeof__()

    def find_bchoc_item(self, item_id):
        current = self.head
        while current.next and (current.item_id != item_id):
            current = current.next
        if current.item_id == item_id:
            return current
        else:
            temp_block = Block(None, None, None, None, "DNE", None, None)
            return temp_block

    def add(self, new_block):  # adds a new block to the blockchain
        global size
        size += 1
        current = self.head
        if current:
            while current.next:
                current = current.next
            current.next = new_block
            tail = new_block
        else:
            self.head = new_block

    def checkout(self, passed_item_id):  # checks out a block item and marks its state as "CHECKED OUT"
        current = self.find_bchoc_item(passed_item_id)
        if current.state != 'RELEASED' and current.state != "DESTROYED" and current.state != "DISPOSED":
            if current.state != "DNE" and current.state != "CHECKEDOUT":
                current.state = "CHECKEDOUT"
                checkout_time = datetime.now(timezone.utc).isoformat()
                print("Case: " + current.case_id + "\nChecked out item: " + current.item_id + "\n\tStatus: "
                      + current.state + "\n\tTime of action: " + checkout_time)
            elif current.state == "CHECKEDOUT":
                print("Error: Cannot check out a checked out item. Must check it in first.")
            else:
                print("item not found")
        else:
            print("Cannot check out, item is " + current.state)

    def checkin(self, passed_item_id):  # checks in a block item and marks its state as "CHECKED IN"
        current = self.find_bchoc_item(passed_item_id)
        if current.state != "RELEASED" and current.state != "DESTROYED" and current.state != "DISPOSED":
            if current.state != "DNE":
                current.state = "CHECKEDIN"
                checkin_time = datetime.now(timezone.utc).isoformat()
                print("Case: " + current.case_id + "\nChecked in item: " + current.item_id + "\n\tStatus: "
                      + current.state + "\n\tTime of action: " + checkin_time)
            else:
                print("Cannot checkin an item that does not exist")
        else:
            print("Cannot check in, item is " + current.state)

    def forward_log(self, num_entries):  # prints Blockchain
        log = self.head
        if num_entries == -1:
            while log is not None:
                print("Case: " + str(log.case_id) + "\nItem: " + str(log.item_id) + "\nAction: " + str(log.state) +
                      "\nTime: " + str(log.time_stamp) + "\n")
                log = log.next
        else:
            for x in range(num_entries):
                print("Case: " + str(log.case_id) + "\nItem: " + str(log.item_id) + "\nAction: " + str(log.state) +
                      "\nTime: " + str(log.time_stamp) + "\n")
                log = log.next

    def reverse_log(self, log, num_entries):  # prints Blockchain in reverse
        if log:
            self.reverse_log(log.next)
            print("Case: " + str(log.case_id) + "\nItem: " + str(log.item_id) + "\nAction: " + str(log.state) +
                  "\nTime: " + str(log.time_stamp) + "\n")
        else:
            return

    def remove(self, passed_item_id, reason, owner_info):  # removes a block
        if reason == 'RELEASED':
            if owner_info != 'NONE':
                curr_time = datetime.now(timezone.utc).isoformat()
                item = self.find_bchoc_item(passed_item_id)
                item.state = "RELEASED"
                print("Case: " + item.case_id + "\nRemoved Item: " + item.item_id + "\n\tStatus: " + item.state +
                      "\n\tOwner info: " + owner_info + "\n\tTime of action: " + curr_time)
            else:
                print("Error! Must input owner info")
        else:
            curr_time = datetime.now(timezone.utc).isoformat()
            item = self.find_bchoc_item(passed_item_id)
            item.state = "RELEASED"
            print("Case: " + item.case_id + "\nRemoved Item: " + item.item_id + "\n\tStatus: " + item.state +
                  "\n\tTime of action: " + curr_time)

        """
        current = self.head
        while current.next and (current.item_id != passed_item_id):
            prev = current
            current = current.next
        if current.item_id == passed_item_id:
            if current.state == "CHECKEDIN":
                prev = current.next
        """

    # def init(self):

    # def verify(self):


def main():
    blockchain = Blockchain()
    blockchain_file = open('blockchain.txt', 'r')
    blockchain.read_blockchain(blockchain_file)
    global size

    # cheese = True  # Noah likes cheese
    # while cheese:

    inp = input()
    user_input = inp.split()
    time = datetime.now(timezone.utc).isoformat()  # timestamp in UTC
    if len(user_input) > 0:
        if user_input[0] == 'bchoc':
            match user_input[1]:  # fix will cause arr out of bounds error
                case 'add':
                    try:
                        case_id = user_input[3]
                        item_id = user_input[5]
                        search = blockchain.find_bchoc_item(item_id)
                        if search.state == "DNE":
                            if size > 0:
                                new_block = Block(None, time, case_id, item_id, "CHECKEDIN", None, None)
                                blockchain.add(new_block)
                                more_items = True
                                offset = 0
                                while more_items:
                                    try:
                                        if user_input[6 + offset] == "-i":
                                            item_id = user_input[7 + offset]
                                            new_block = Block(None, time, case_id, item_id, "CHECKEDIN", None, None)
                                            blockchain.add(new_block)
                                            offset += 2
                                    except IndexError:
                                        more_items = False
                                        pass
                                    continue
                            else:
                                print("error")
                        elif search.state == "RELEASED" or search.state == "DISPOSED" or \
                                search.state == "DESTROYED":
                            exit(1)
                    except IndexError:
                        exit(1)
                        pass
                    blockchain_file = open('blockchain.txt', 'w')
                    blockchain.write_blockchain(blockchain_file)
                    blockchain_file.close()

                case 'checkout':
                    if user_input[2] == "-i":
                        item = user_input[3]
                        blockchain.checkout(item)
                        blockchain_file = open('blockchain.txt', 'w')
                        blockchain.write_blockchain(blockchain_file)
                        blockchain_file.close()
                    else:
                        print("Checkout Error")
                        exit(1)
                case 'checkin':
                    if user_input[2] == "-i":
                        item = user_input[3]
                        blockchain.checkin(item)
                        blockchain_file = open('blockchain.txt', 'w')
                        blockchain.write_blockchain(blockchain_file)
                        blockchain_file.close()
                    else:
                        print("Checkin Error")
                        exit(1)

                case 'log':
                    blockchain.forward_log(-1)
                    # reverse print if user inputs "-r" blockchain.reverse_log(blockchain.head)
                case 'remove':
                    if user_input[2] == '-i':
                        item_id = user_input[3]
                        if user_input[4] == "-y":
                            reason = user_input[5]
                            try:
                                if user_input[6] == "-o":
                                    info = " ".join(user_input[7:])
                                    blockchain.remove(item_id, reason, info)
                                    blockchain_file = open('blockchain.txt', 'w')
                                    blockchain.write_blockchain(blockchain_file)
                                    blockchain_file.close()
                                else:
                                    blockchain.remove(item_id, reason, "NONE")
                                    blockchain_file = open('blockchain.txt', 'w')
                                    blockchain.write_blockchain(blockchain_file)
                                    blockchain_file.close()
                            except IndexError:
                                pass
                        else:
                            print("Error, reason not given for removal")
                            exit(1)
                    else:
                        print("Error, no item given for removal")
                        exit(1)

                case 'init':
                    if size > 0:
                        print("Blockchain file found with INITIAL block.")
                    else:
                        blockchain.head = Block("None", time, None, None, "INITIAL", 14, "Initial block")
                        size += 1
                        blockchain_file = open('blockchain.txt', 'w')
                        blockchain.write_blockchain(blockchain_file)
                        blockchain_file.close()
                        print("Blockchain file not found. Created INITIAL block.")
                        size += 1
                case 'verify':
                    print("verify")
                case _:
                    print("error")
                    exit(1)
        else:
            print("error")
            exit(1)
    else:
        print("No user input")
        exit(1)


if __name__ == "__main__":
    main()
