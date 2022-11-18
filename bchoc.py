#!/usr/bin/env python3
import maya
import sys, os, hashlib, struct

size = 0
os.environ.get("BCHOC_FILE_PATH")


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
        s = "\n"
        while True:
            try:
                prev_hash = next(file).strip(s)
                time_stamp = next(file).strip(s)
                case_id = next(file).strip(s)
                item_id = next(file).strip(s)
                state = next(file).strip(s)
                data_length = next(file).strip(s)
                data = next(file).strip(s)
                new_block = Block(prev_hash, time_stamp, case_id, item_id, state, data_length, data)
                self.add(new_block)
            except StopIteration:
                break

    def __init__(self, head=None):
        self.bchoc_tail = head
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
            self.bchoc_tail = new_block
        else:
            self.head = new_block
            self.bchoc_tail = self.head

    def checkout(self, passed_item_id):  # checks out a block item and marks its state as "CHECKED OUT"
        current = self.find_bchoc_item(passed_item_id)
        if current.state != 'RELEASED' and current.state != "DESTROYED" and current.state != "DISPOSED":
            if current.state != "DNE" and current.state != "CHECKEDOUT":
                current.state = "CHECKEDOUT"
                checkout_time = maya.now().iso8601()
                print("Case: " + current.case_id + "\nChecked out item: " + current.item_id + "\n\tStatus: "
                      + current.state + "\n\tTime of action: " + checkout_time)
            elif current.state == "CHECKEDOUT":
                print("Error: Cannot check out a checked out item. Must check it in first.")
                exit(1)
            else:
                print("item not found")
                exit(1)
        else:
            print("Cannot check out, item is " + current.state)
            exit(1)

    def checkin(self, passed_item_id):  # checks in a block item and marks its state as "CHECKED IN"
        current = self.find_bchoc_item(passed_item_id)
        if current.state != "RELEASED" and current.state != "DESTROYED" and current.state != "DISPOSED":
            if current.state != "DNE" and current.state != "CHECKEDIN":
                current.state = "CHECKEDIN"
                checkin_time = maya.now().iso8601()
                print("Case: " + current.case_id + "\nChecked in item: " + current.item_id + "\n\tStatus: "
                      + current.state + "\n\tTime of action: " + checkin_time)
            elif current.state == "CHECKEDIN":
                print("Cannot checkin an item that is already checkedin")
                exit(1)
            else:
                print("Cannot checkin an item that does not exist")
                exit(1)
        else:
            print("Cannot check in, item is " + current.state)
            exit(1)

    def forward_log(self, num_entries, case_id, item_id):  # prints Blockchain
        log = self.head
        rev2 = []
        while log is not None:
            rev = []
            if log.item_id is not None:
                rev.append(str(log.case_id))
                rev.append(str(log.item_id))
                rev.append(str(log.state))
                rev.append(str(log.time_stamp))
            if len(rev) > 0:
                rev2.append(rev)
            log = log.next

        length = len(rev2)
        if num_entries == -1:
            if case_id == '':
                if item_id == '':
                    for data in (rev2[1:]):
                        print("\nCase: " + str(data[0]))
                        print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(data[3]))
                else:
                    for data in (rev2[1:]):
                        for i in data:
                            if i == item_id:
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(data[3]))
            else:
                if item_id == '':
                    for data in (rev2[1:]):
                        for d in data:
                            if d == case_id:
                                print("\nCase: " + str(data[0]) + "\nItem: " + str(data[1]) + "\nAction: " + str(
                                    data[2]) + "\nTime: " + str(data[3]))
                                if d == case_id and data[1] == d:
                                    break
                else:
                    for data in (rev2[1:]):
                        for i in data:
                            if i == item_id and data[0] == case_id:
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(data[3]))

        else:
            if num_entries + 1 <= length:
                if case_id == '':
                    if item_id == '':
                        for data in (rev2[1:num_entries + 1]):
                            print("\nCase: " + str(data[0]))
                            print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(
                                data[3]))
                    else:
                        for data in (rev2[1:]):
                            for i in data:
                                if i == data[1] and i != data[0]:
                                    print("\nCase: " + str(data[0]))
                                    print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(
                                        data[3]))
                else:
                    if item_id == '':
                        for data in (rev2[1:num_entries + 1]):
                            for d in data:
                                if d == case_id:
                                    print("\nCase: " + str(data[0]))
                                    print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(
                                        data[3]))
                                if d == case_id and data[1] == d:
                                    break

                    else:
                        for data in (rev2[1:num_entries + 1]):
                            for d in data:
                                if d == case_id and data[1] == item_id:
                                    print("\nCase: " + str(data[0]))
                                    print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(
                                        data[3]))
            else:
                print("too many entries")

    def reverse_log(self, num_entries, case_id, item_id):
        log = self.head
        rev2 = []
        while log is not None:
            rev = []
            if log.item_id is not None:
                rev.append(str(log.case_id))
                rev.append(str(log.item_id))
                rev.append(str(log.state))
                rev.append(str(log.time_stamp))
            if len(rev) > 0:
                rev2.append(rev)
            log = log.next

        length = len(rev2)
        if num_entries == -1:
            if case_id == '':
                if item_id == '':
                    for data in (reversed(rev2[1:])):
                        print("\nCase: " + str(data[0]))
                        print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(data[3]))
                else:
                    for data in (reversed(rev2[1:])):
                        for i in data:
                            if i == item_id:
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(data[3]))
            else:
                if item_id == '':
                    for data in (reversed(rev2[1:])):
                        for d in data:
                            if d == case_id:
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(data[3]))
                            if d == case_id and data[1] == d:
                                break
                else:
                    for data in (reversed(rev2[1:])):
                        for d in data:
                            if d == case_id:
                                if data[1] == item_id:
                                    print("\nCase: " + str(data[0]))
                                    print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(
                                        data[3]))
                            if d == case_id and data[1] == d:
                                break
        else:
            if num_entries + 1 <= length:
                if case_id == '':
                    if item_id == '':
                        if num_entries == 1:
                            for data in (reversed(rev2[num_entries + 1:])):
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(
                                    data[2]) + "\nTime: " + str(data[3]))
                        else:
                            for data in (reversed(rev2[1:])):
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(
                                    data[2]) + "\nTime: " + str(data[3]))
                    else:
                        for data in (reversed(rev2[1:])):
                            for i in data:
                                if i == data[1] and i != data[0]:
                                    print("\nCase: " + str(data[0]))
                                    print("Item: " + str(data[1]) + "\nAction: " + str(
                                        data[2]) + "\nTime: " + str(
                                        data[3]))
                                if i == case_id and data[1] == i:
                                    break
                else:
                    if item_id == '':
                        for data in (reversed(rev2[1:num_entries + 1])):
                            for d in data:
                                if d == case_id:
                                    print("\nCase: " + str(data[0]))
                                    print("Item: " + str(data[1]) + "\nAction: " + str(
                                        data[2]) + "\nTime: " + str(
                                        data[3]))
                                if d == case_id and data[1] == d:
                                    break

                    else:
                        for data in (reversed(rev2[num_entries + 1:])):
                            for d in data:
                                if d == case_id and data[1] == item_id:
                                    print("\nCase: " + str(data[0]))
                                    print("Item: " + str(data[1]) + "\nAction: " + str(
                                        data[2]) + "\nTime: " + str(
                                        data[3]))
                                if d == case_id and data[1] == d:
                                    break
            else:
                print("too many entries")

    def remove(self, passed_item_id, reason, owner_info):  # removes a block
        if reason == 'RELEASED':
            if owner_info != 'NONE':
                curr_time = maya.now().iso8601()
                item = self.find_bchoc_item(passed_item_id)
                item.state = reason
                print("Case: " + item.case_id + "\nRemoved Item: " + item.item_id + "\n\tStatus: " + item.state +
                      "\n\tOwner info: " + owner_info + "\n\tTime of action: " + curr_time)
            else:
                print("Error! Must input owner info")
                exit(1)
        else:
            curr_time = maya.now().iso8601()
            item = self.find_bchoc_item(passed_item_id)
            item.state = reason
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

    if not ("BCHOC_FILE_PATH" in os.environ):
        os.environ["BCHOC_FILE_PATH"] = "file.bin"

    path = os.environ["BCHOC_FILE_PATH"]
    if not os.path.exists(path):
        open(path, 'w')

    global size, rever
    # cheese = True  # Noah likes cheese
    # while cheese:

    #inp = input()
    #user_input = inp.split()
    user_input = sys.argv[1:]
    if len(user_input) > 0:
        match user_input[0]:  # fix will cause arr out of bounds error
            case 'add':
                blockchain.read_blockchain(open(path, 'r'))
                if blockchain.head:
                    try:
                        case_id = user_input[2]
                        item_id = user_input[4]
                        search = blockchain.find_bchoc_item(item_id)
                        time = maya.now().iso8601()
                        if search.state == "DNE":
                            if size > 0:
                                if blockchain.bchoc_tail.state != "INITIAL":
                                    tail = blockchain.bchoc_tail
                                    packed_struct = struct.pack('32s d 16s I 12s I',
                                                                bytes(tail.prev_hash,
                                                                      encoding='utf-8'), maya.parse(str(tail.time_stamp)).datetime().timestamp(),
                                                                bytes(tail.case_id, encoding='utf-8'),
                                                                int(tail.item_id),
                                                                bytes(tail.state, encoding='utf-8'),
                                                                int(tail.data_length))
                                    sha256 = hashlib.sha256(packed_struct).hexdigest()
                                else:
                                    sha256 = str(hex(0))
                                new_block = Block(sha256, time, case_id, item_id, "CHECKEDIN", 0, None)
                                print("Case: " + new_block.case_id + "\nAdded item: " + new_block.item_id +
                                      "\n\tStatus: " + new_block.state + "\n\tTime of action: " + new_block.time_stamp)
                                blockchain.add(new_block)
                                more_items = True
                                offset = 0
                                while more_items:
                                    try:
                                        if user_input[5 + offset] == "-i":
                                            item_id = user_input[6 + offset]
                                            tail = blockchain.bchoc_tail
                                            packed_struct = struct.pack('32s d 16s I 12s I',
                                                                        bytes(tail.prev_hash, encoding='utf-8'),
                                                                        maya.parse(str(tail.time_stamp)).datetime().timestamp(),
                                                                        bytes(tail.case_id, encoding='utf-8'),
                                                                        int(tail.item_id),
                                                                        bytes(tail.state, encoding='utf-8'),
                                                                        int(tail.data_length))
                                            sha256 = hashlib.sha256(packed_struct).hexdigest()
                                            time = maya.now().iso8601()
                                            new_block = Block(sha256, time, case_id, item_id, "CHECKEDIN", 0, None)
                                            print("Case: " + new_block.case_id + "\nAdded item: " + new_block.item_id +
                                                  "\n\tStatus: " + new_block.state + "\n\tTime of action: " + new_block.time_stamp)
                                            blockchain.add(new_block)
                                            offset += 2
                                    except IndexError:
                                        more_items = False
                                        pass
                                    continue
                            else:
                                print("error")
                        elif search.state == "RELEASED" or search.state == "DISPOSED" or search.state == "DESTROYED" or "CHECKEDIN" or "CHECKEDOUT":
                            exit(1)
                    except IndexError:
                        exit(1)
                        pass
                    blockchain_file = open(path, 'w')
                    blockchain.write_blockchain(blockchain_file)
                    blockchain_file.close()
                else:
                    time = maya.now().iso8601()
                    blockchain.head = Block(None, time, None, None, "INITIAL", 14, "Initial block")
                    size += 1
                    blockchain_file = open(path, 'w')
                    blockchain.write_blockchain(blockchain_file)
                    blockchain_file.close()
                    print("Blockchain file not found. Created INITIAL block.")

            case 'checkout':
                blockchain.read_blockchain(open(path, 'r'))
                if user_input[1] == "-i":
                    item = user_input[2]
                    blockchain.checkout(item)
                    blockchain_file = open(path, 'w')
                    blockchain.write_blockchain(blockchain_file)
                    blockchain_file.close()
                else:
                    print("Checkout Error")
                    exit(1)
            case 'checkin':
                blockchain.read_blockchain(open(path, 'r'))
                if user_input[1] == "-i":
                    item = user_input[2]
                    blockchain.checkin(item)
                    blockchain_file = open(path, 'w')
                    blockchain.write_blockchain(blockchain_file)
                    blockchain_file.close()
                else:
                    print("Checkin Error")
                    exit(1)
            case 'log':
                blockchain.read_blockchain(open(path, 'r'))
                rever = False
                num = -1
                case = ''
                id = ''
                if len(user_input) > 1:
                    for it in user_input[1:]:
                        if it == '-n':
                            n = user_input.index('-n')
                            num = user_input[n + 1]
                        if it == '-i':
                            i = user_input.index('-i')
                            id = user_input[i + 1]
                        if it == '-c':
                            c = user_input.index('-c')
                            case = user_input[c + 1]
                        if it == '-r' or it == '--reverse':
                            rever = True
                    for it in user_input[1:]:
                        if it == '-r' or it == '--reverse':
                            blockchain.reverse_log(int(num), case, id)
                        if rever is False:
                            blockchain.forward_log(int(num), case, id)
                            break

                else:
                    blockchain.forward_log(int(num), case, id)
            case 'remove':
                blockchain.read_blockchain(open(path, 'r'))
                if user_input[1] == '-i':
                    item_id = user_input[2]
                    if user_input[3] == "-y" or user_input[3] == "--why":
                        reason = user_input[4]
                        try:
                            if user_input[5] == "-o":
                                info = " ".join(user_input[6:])
                                blockchain.remove(item_id, reason, info)
                                blockchain_file = open(path, 'w')
                                blockchain.write_blockchain(blockchain_file)
                                blockchain_file.close()
                        except IndexError:
                            blockchain.remove(item_id, reason, None)
                            blockchain_file = open(path, 'w')
                            blockchain.write_blockchain(blockchain_file)
                            blockchain_file.close()
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
                    time = maya.now().iso8601()
                    blockchain.head = Block("None", time, None, None, "INITIAL", 14, "Initial block")
                    size += 1
                    blockchain_file = open(path, 'w')
                    blockchain.write_blockchain(blockchain_file)
                    blockchain_file.close()
                    print("Blockchain file not found. Created INITIAL block.")
            case 'verify':
                print("verify")
            case _:
                print("error")
                exit(1)
    else:
        print("No user input")
        exit(1)


if __name__ == "__main__":
    main()
