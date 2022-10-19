from datetime import timezone
import datetime
import sys


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
    block_chain_size = 0

    def __init__(self, head=None):
        self.head = head

    def is_empty(self):
        return self.__sizeof__()

    def add(self, new_block):  # adds a new block to the blockchain
        current = self.head
        if current:
            while current.next:
                current = current.next
            current.next = new_block
        else:
            self.head = new_block

    block_chain_size += 1

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

    # def log():

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
    user_input = sys.argv
    user_action = user_input[2]

    blockchain = Blockchain()

    match user_action:
        case 'add':
            # print("add")
            case_id = user_input[4]
            item_id = user_input[6]
            time = maya.MayaDT.from_datetime(datetime.utcnow())
            if blockchain.block_chain_size > 0:
                block = Block(None, time, case_id, item_id, "CHECKEDIN", )
            else:
                block = Block(None, time, None, None, "INITIAL", 14, "Initial block")

            blockchain.add(block)

        case 'checkout':
            print("add")
        case 'checkin':
            print("add")
        case 'log':
            print("log")
        case 'remove':
            print("remove")
        case 'init':
            print("init")
        case 'verify':
            print("verify")


if __name__ == "__main__":
    main()
