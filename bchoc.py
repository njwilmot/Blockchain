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
            tail = new_block
        else:
            self.head = new_block

    def checkout(self, passed_item_id):  # checks out a block item and marks its state as "CHECKED OUT"
        current = self.head
        while current.next and (current.item_id != passed_item_id):
            current = current.next
        if current.item_id == passed_item_id and current.state == "CHECKEDIN":
            current.state = "CHECKEDOUT"
            checkout_time = datetime.now(timezone.utc).isoformat()
            print("Case: " + current.case_id + "\nChecked out item: " + current.item_id + "\n\tStatus: " + current.state
                  + "\n\tTime of action: " + checkout_time)
        elif current.state == "CHECKEDOUT":
            print("Error: Cannot check out a checked out item. Must check it in first.")

    def checkin(self, passed_item_id):  # checks in a block item and marks its state as "CHECKED IN"
        current = self.head
        while current.next and (current.item_id != passed_item_id):
            current = current.next
        if current.item_id == passed_item_id and current.state == "CHECKEDOUT":
            current.state = "CHECKEDIN"
            checkin_time = datetime.now(timezone.utc).isoformat()
            print("Case: " + current.case_id + "\nChecked in item: " + current.item_id + "\n\tStatus: " + current.state
                  + "\n\tTime of action: " + checkin_time)

    def forward_log(self):  # prints Blockchain
        log = self.head
        while log is not None:
            print("Case: " + str(log.case_id) + "\nItem: " + str(log.item_id) + "\nAction: " + str(log.state) +
                  "\nTime: " + str(log.time_stamp) + "\n")
            log = log.next

    def reverse_log(self, log):  # prints Blockchain in reverse
        if log:
            self.reverse_log(log.next)
            print("Case: " + str(log.case_id) + "\nItem: " + str(log.item_id) + "\nAction: " + str(log.state) +
                  "\nTime: " + str(log.time_stamp) + "\n")
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
    blockchain = Blockchain()
    cheese = True
    while cheese:
        try:
            inp = input()
            user_input = inp.split()
            time = datetime.now(timezone.utc).isoformat()  # timestamp in UTC
            if len(user_input) > 0:
                if user_input[0] == 'bchoc':
                    match user_input[1]:  # fix will cause arr out of bounds error
                        case 'add':
                            case_id = user_input[3]
                            item_id = user_input[5]
                            if size > 0:
                                new_block = Block(None, time, case_id, item_id, "CHECKEDIN", None, None)
                                blockchain.add(new_block)
                                # blockchain.add = Block(None, time, case_id, item_id, "CHECKEDIN", None, None)
                                # blockchain.head.next = blockchain.add
                            else:
                                print("error")

                        case 'checkout':
                            if user_input[2] == "-i":
                                item = user_input[3]
                                blockchain.checkout(item)
                            else:
                                print("error")
                        case 'checkin':
                            if user_input[2] == "-i":
                                item = user_input[3]
                                blockchain.checkin(item)
                            else:
                                print("error")

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
                            print("error")
                else:
                    print("error")
            else:
                print("No user input")
        except EOFError:
            cheese = False
        except KeyboardInterrupt:
            cheese = False


if __name__ == "__main__":
    main()
