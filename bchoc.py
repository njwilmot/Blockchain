import calendar
import time

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
    def add(self, new_block): # adds a new block to the blockchain
        current = self.head
        if current:
            while current.next:
                current = current.next
            current.next = new_block
        else:
            self.head = new_block
    def checkout(self, passed_item_id): # marks a block state as "CHECKED OUT"
        current = self.head
        while (current.next) and (current.item_id != passed_item_id):
            current = current.next
        if current.item_id == passed_item_id:
            current.state = "CHECKEDOUT"
    def checkin(self, item_id): # marks a block state as "CHECKED IN"
        current = self.head
        while (current.next) and (current.item_id != passed_item_id):
            current = current.next
        if current.item_id == passed_item_id:
            current.state = "CHECKEDIN"

    def log():

    def remove(self, item_id): # removes a block
        current = self.head
        while (current.next) and (current.item_id != passed_item_id):
            prev = current
            current = current.next
        if current.item_id == passed_item_id:
            if current.state == "CHECKEDIN":
                prev = current.next

    def init():

    def verify():
