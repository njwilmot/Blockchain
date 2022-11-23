#!/usr/bin/env python3
import maya
import datetime as DT
import sys, os, hashlib, struct, uuid

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
        self.prev = None
        self.next = None


class Blockchain:

    def check_size(self, file):
        struct_format = '32s d 16s I 12s I'
        struct_size = struct.calcsize(struct_format)
        while file is not None:
            try:
                data = file.read(struct_size)
                if not data:
                    return 1
                else:
                    return 0
            except StopIteration:
                return 0

    def write_blockchain(self, file):
        current = self.head
        while current is not None:
            struct_parameters = '32s d 16s I 12s I ' + str(current.data_length) + "s"
            packed_struct = struct.pack(struct_parameters, bytes(current.prev_hash, encoding='utf-8'),
                                        maya.parse(str(current.time_stamp)).datetime().timestamp(),
                                        bytes(reversed(uuid.UUID(current.case_id).bytes)), int(current.item_id),
                                        bytes(current.state, encoding='utf-8'), int(current.data_length),
                                        bytes(current.data, encoding='utf-8'))
            file.write(packed_struct)
            current = current.next

    def read_blockchain(self, file):
        """
        struct_format = '32s d 16s I 12s I'
        struct_size = struct.calcsize(struct_format)
        while file is not None:
            try:
                data = file.read(struct_size)
                if not data:
                    break
                s = struct.unpack('32s d 16s I 12s I', data)
                prev_hash = s[0].decode("utf-8").replace("\x00", "")
                if s[1] == 0:
                    time_stamp = s[1]
                else:
                    time_stamp = DT.datetime.utcfromtimestamp(s[1]).isoformat()
                case_id = str(uuid.UUID(s[2].hex()))
                item_id = s[3]
                state = s[4].decode("utf-8").replace("\x00", "")
                data_length = s[5]
                if data_length != 0:
                    block_data = file.read(data_length - 1).decode("utf-8").replace("\x00", "")
                else:
                    block_data = file.read(data_length).decode("utf-8").replace("\x00", "")
                new_block = Block(prev_hash, time_stamp, case_id, item_id, state, data_length, block_data)
                self.add(new_block)
            except StopIteration:
                break
      """
        data = file.read()
        index = 0
        length = 0
        while index <= (len(data) - 1):
            prev_hash = (str(struct.unpack("32s", data[index: index + 32])).split("\\x")[0].split("'")[1])
            temp = struct.unpack("d", data[index + 32: index + 40])[0]
            if temp == 0:
                time_stamp = temp
            else:
                time_stamp = DT.datetime.utcfromtimestamp(temp).isoformat()
            case_id = (str(uuid.UUID(bytes=bytes(reversed(struct.unpack("16s", data[index + 40: index + 56])[0])))))
            item_id = struct.unpack("I", data[index + 56: index + 60])[0]
            state = (str(struct.unpack("12s", data[index + 60: index + 72])[0]).split("\\x")[0].split("'")[1])
            data_length = struct.unpack("I", data[index + 72: index + 76])[0]
            data_length_string = str(data_length) + "s"
            block_data = (str(struct.unpack(data_length_string, data[index + 76: index + 76 + data_length])).split("\\x")[0].split("'")[1])
            new_block = Block(prev_hash, time_stamp, case_id, item_id, state, data_length, block_data)
            self.add(new_block)
            index = index + data_length + 76

    def __init__(self, head=None):
        self.prev = head
        self.head = head
        self.tail = head

    def is_empty(self):
        return self.__sizeof__()

    def find_bchoc_item(self, item_id):
        current = self.tail
        if self.head != self.tail:
            while current.prev is not None and current.item_id != int(item_id):
                current = current.prev
            if current.item_id == int(item_id):
                return current
            else:
                temp_block = Block(None, None, None, None, "DNE", None, None)
                return temp_block
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
            new_block.prev = current
            self.tail = new_block
        else:
            self.head = new_block
            self.tail = self.head
            self.prev = None

    def checkout(self, passed_item_id):  # checks out a block item and marks its state as "CHECKED OUT"
        current = self.find_bchoc_item(passed_item_id)
        if current.state != 'RELEASED' and current.state != "DESTROYED" and current.state != "DISPOSED":
            if current.state != "DNE" and current.state != "CHECKEDOUT":
                parent = self.tail
                struct_parameters = '32s d 16s I 12s I ' + str(parent.data_length) + 's'
                packed_struct = struct.pack(struct_parameters,
                                            bytes(parent.prev_hash, encoding='utf-8'),
                                            maya.parse(str(parent.time_stamp)).datetime().timestamp(),
                                            bytes(parent.case_id, encoding='utf-8'),
                                            int(parent.item_id),
                                            bytes(parent.state, encoding='utf-8'),
                                            int(parent.data_length), bytes(parent.data, encoding='utf-8'))
                sha256 = hashlib.sha256(packed_struct).hexdigest()
                checkout_time = maya.now().iso8601()
                new_block = Block(sha256, checkout_time, current.case_id, current.item_id, "CHECKEDOUT", 0, "")
                self.add(new_block)
                print("Case: " + new_block.case_id + "\nChecked out item: " + str(new_block.item_id) + "\n\tStatus: "
                      + new_block.state + "\n\tTime of action: " + checkout_time)
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
                parent = self.tail
                struct_parameters = '32s d 16s I 12s I ' + str(parent.data_length) + 's'
                packed_struct = struct.pack(struct_parameters,
                                            bytes(parent.prev_hash,
                                                  encoding='utf-8'),
                                            maya.parse(str(parent.time_stamp)).datetime().timestamp(),
                                            bytes(parent.case_id, encoding='utf-8'),
                                            int(parent.item_id),
                                            bytes(parent.state, encoding='utf-8'),
                                            int(parent.data_length), bytes(parent.data, encoding='utf-8'))
                sha256 = hashlib.sha256(packed_struct).hexdigest()
                checkin_time = maya.now().iso8601()
                new_block = Block(sha256, checkin_time, current.case_id, current.item_id, "CHECKEDIN", 0, "")
                self.add(new_block)
                print("Case: " + new_block.case_id + "\nChecked in item: " + str(new_block.item_id) + "\n\tStatus: "
                      + new_block.state + "\n\tTime of action: " + checkin_time)
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
                    for data in rev2:
                        print("\nCase: " + str(data[0]))
                        print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(data[3]))
                else:
                    for data in rev2:
                        for i in data:
                            if i == item_id:
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(data[3]))
            else:
                if item_id == '':
                    for data in rev2:
                        for d in data:
                            if d == case_id:
                                print("\nCase: " + str(data[0]) + "\nItem: " + str(data[1]) + "\nAction: " + str(
                                    data[2]) + "\nTime: " + str(data[3]))
                                if d == case_id and data[1] == d:
                                    break
                else:
                    for data in rev2:
                        for i in data:
                            if i == item_id and data[0] == case_id:
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(data[3]))

        else:
            if case_id == '':
                if item_id == '':
                    for data in (rev2[:num_entries]):
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
                    for data in (rev2[:num_entries]):
                        for d in data:
                            if d == case_id:
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(
                                    data[3]))
                            if d == case_id and data[1] == d:
                                break

                else:
                    for data in (rev2[:num_entries]):
                        for d in data:
                            if d == case_id and data[1] == item_id:
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(
                                    data[3]))

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
                    for data in (reversed(rev2)):
                        print("\nCase: " + str(data[0]))
                        print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(data[3]))
                else:
                    for data in (reversed(rev2)):
                        for i in data:
                            if i == item_id:
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(data[3]))
            else:
                if item_id == '':
                    for data in (reversed(rev2)):
                        for d in data:
                            if d == case_id:
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(data[3]))
                            if d == case_id and data[1] == d:
                                break
                else:
                    for data in (reversed(rev2)):
                        for d in data:
                            if d == case_id:
                                if data[1] == item_id:
                                    print("\nCase: " + str(data[0]))
                                    print("Item: " + str(data[1]) + "\nAction: " + str(data[2]) + "\nTime: " + str(
                                        data[3]))
                            if d == case_id and data[1] == d:
                                break
        else:
            if case_id == '':
                if item_id == '':
                    if num_entries == 1:
                        for data in (reversed(rev2[num_entries:])):
                            print("\nCase: " + str(data[0]))
                            print("Item: " + str(data[1]) + "\nAction: " + str(
                                data[2]) + "\nTime: " + str(data[3]))
                    else:
                        for data in (reversed(rev2)):
                            print("\nCase: " + str(data[0]))
                            print("Item: " + str(data[1]) + "\nAction: " + str(
                                data[2]) + "\nTime: " + str(data[3]))
                else:
                    for data in (reversed(rev2)):
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
                    for data in (reversed(rev2[:num_entries])):
                        for d in data:
                            if d == case_id:
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(
                                    data[2]) + "\nTime: " + str(
                                    data[3]))
                            if d == case_id and data[1] == d:
                                break

                else:
                    for data in (reversed(rev2[num_entries:])):
                        for d in data:
                            if d == case_id and data[1] == item_id:
                                print("\nCase: " + str(data[0]))
                                print("Item: " + str(data[1]) + "\nAction: " + str(
                                    data[2]) + "\nTime: " + str(
                                    data[3]))
                            if d == case_id and data[1] == d:
                                break

    def remove(self, passed_item_id, reason, owner_info):
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
        check = False
        for i in rev2:
            if i[1] == passed_item_id:
                check = True
        if not check:
            exit(1)
        # removes a block
        current = self.find_bchoc_item(passed_item_id)
        if current.state == 'CHECKEDOUT':
            print('error item CHECKEDOUT')
            exit(1)
        if reason != 'RELEASED' and reason != 'DISPOSED' and reason != 'DESTROYED':
            exit(1)
        if reason == 'RELEASED':
            if owner_info is not None:
                remove_time = maya.now().iso8601()
                parent = self.tail
                struct_parameters = '32s d 16s I 12s I ' + str(parent.data_length) + 's'
                packed_struct = struct.pack(struct_parameters,
                                            bytes(parent.prev_hash,
                                                  encoding='utf-8'),
                                            maya.parse(str(parent.time_stamp)).datetime().timestamp(),
                                            bytes(parent.case_id, encoding='utf-8'),
                                            int(parent.item_id),
                                            bytes(parent.state, encoding='utf-8'),
                                            int(parent.data_length), bytes(parent.data, encoding='utf-8'))
                sha256 = hashlib.sha256(packed_struct).hexdigest()
                new_block = Block(sha256, remove_time, current.case_id, current.item_id, reason, len(owner_info), owner_info)
                self.add(new_block)
                print("Case: " + parent.case_id + "\nRemoved Item: " + str(
                    parent.item_id) + "\n\tStatus: " + parent.state +
                      "\n\tOwner info: " + owner_info + "\n\tTime of action: " + remove_time)
            else:
                print("Error! Must input owner info")
                exit(1)
        else:
            remove_time = maya.now().iso8601()
            parent = self.tail
            struct_parameters = '32s d 16s I 12s I ' + str(parent.data_length) + 's'
            packed_struct = struct.pack(struct_parameters,
                                        bytes(parent.prev_hash,
                                              encoding='utf-8'),
                                        maya.parse(str(parent.time_stamp)).datetime().timestamp(),
                                        bytes(parent.case_id, encoding='utf-8'),
                                        int(parent.item_id),
                                        bytes(parent.state, encoding='utf-8'),
                                        int(parent.data_length), bytes(parent.data, encoding='utf-8'))
            sha256 = hashlib.sha256(packed_struct).hexdigest()
            new_block = Block(sha256, remove_time, current.case_id, current.item_id, reason, 0, "")
            self.add(new_block)
            print("Case: " + parent.case_id + "\nRemoved Item: " + str(parent.item_id) + "\n\tStatus: " + parent.state +
                  "\n\tTime of action: " + remove_time)

        """
        current = self.head
        while current.next and (current.item_id != passed_item_id):
            prev = current
            current = current.next
        if current.item_id == passed_item_id:
            if current.state == "CHECKEDIN":
                prev = current.next
        """

"""
    def verify(self):
        parent = self.head
        child = parent.next
        transactions = size
        while child:
            if child.prev_hash == 0:
                print("Transactions in blockchain: " + transactions + "\nState of blockchain: ERROR\n" + Bad block)
            struct_parameters = '32s d 16s I 12s I ' + str(parent.data_length) + 's'
            packed_struct = struct.pack(struct_parameters,
                                        bytes(parent.prev_hash,
                                              encoding='utf-8'),
                                        maya.parse(str(parent.time_stamp)).datetime().timestamp(),
                                        bytes(parent.case_id, encoding='utf-8'),
                                        int(parent.item_id),
                                        bytes(parent.state, encoding='utf-8'),
                                        int(parent.data_length), bytes(parent.data, encoding='utf-8'))
            checksum_verification = hashlib.sha256(packed_struct).hexdigest()
            if child.prev_hash != checksum_verification:
                bchoc_state = "ERROR"
                reason = "Block contents do not match block checksum."
            else:
                bchoc_state = "CLEAN"
                reason = ""
"""

def main():
    blockchain = Blockchain()

    if not ("BCHOC_FILE_PATH" in os.environ):
        os.environ["BCHOC_FILE_PATH"] = "file.bin"

    path = os.environ["BCHOC_FILE_PATH"]
    if not os.path.exists(path):
        open(path, 'wb')

    global size, rever
    # cheese = True  # Noah likes cheese
    # while cheese:

    #inp = input()
    #user_input = inp.split()
    user_input = sys.argv[1:]
    if len(user_input) > 0:
        match user_input[0]:  # fix will cause arr out of bounds error
            case 'add':
                blockchain.read_blockchain(open(path, 'rb'))
                if blockchain.head is not None:
                    try:
                        case_id = user_input[2]
                        item_id = user_input[4]
                        search = blockchain.find_bchoc_item(item_id)
                        time = maya.now().iso8601()
                        if search.state == "DNE":
                            if size > 0:
                                sha256 = "0"
                                new_block = Block(sha256, time, case_id, item_id, "CHECKEDIN", 0, "")
                                print("Case: " + new_block.case_id + "\nAdded item: " + new_block.item_id +
                                      "\n\tStatus: " + new_block.state + "\n\tTime of action: " + new_block.time_stamp)
                                blockchain.add(new_block)
                                more_items = True
                                offset = 0
                                while more_items:
                                    try:
                                        if user_input[5 + offset] == "-i":
                                            item_id = user_input[6 + offset]
                                            sha256 = "0"
                                            time = maya.now().iso8601()
                                            new_block = Block(sha256, time, case_id, item_id, "CHECKEDIN", 0, "")
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
                    blockchain_file = open(path, 'wb')
                    blockchain.write_blockchain(blockchain_file)
                    blockchain_file.close()
                else:
                    time = maya.now().iso8601()
                    blockchain.head = Block("0", time, "00000000-0000-0000-0000-000000000000", 0, "INITIAL", 14, "Initial block")
                    blockchain.tail = blockchain.head
                    size += 1
                    blockchain_file = open(path, 'wb')
                    blockchain.write_blockchain(blockchain_file)
                    blockchain_file.close()
                    print("Blockchain file not found. Created INITIAL block.\n")

            case 'checkout':
                blockchain.read_blockchain(open(path, 'rb'))
                if user_input[1] == "-i":
                    item = user_input[2]
                    blockchain.checkout(item)
                    blockchain_file = open(path, 'wb')
                    blockchain.write_blockchain(blockchain_file)
                    blockchain_file.close()
                else:
                    print("Checkout Error")
                    exit(1)
            case 'checkin':
                blockchain.read_blockchain(open(path, 'rb'))
                if user_input[1] == "-i":
                    item = user_input[2]
                    blockchain.checkin(item)
                    blockchain_file = open(path, 'wb')
                    blockchain.write_blockchain(blockchain_file)
                    blockchain_file.close()
                else:
                    print("Checkin Error")
                    exit(1)
            case 'log':
                blockchain.read_blockchain(open(path, 'rb'))
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
                blockchain.read_blockchain(open(path, 'rb'))
                if user_input[1] == '-i':
                    item_id = user_input[2]
                    if user_input[3] == "-y" or user_input[3] == "--why":
                        reason = user_input[4]
                        try:
                            if user_input[5] == "-o":
                                info = " ".join(user_input[6:])
                                blockchain.remove(item_id, reason, info)
                                blockchain_file = open(path, 'wb')
                                blockchain.write_blockchain(blockchain_file)
                                blockchain_file.close()
                        except IndexError:
                            blockchain.remove(item_id, reason, None)
                            blockchain_file = open(path, 'wb')
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

                if len(user_input) > 1:
                    exit(1)
                else:
                    if blockchain.check_size(open(path, 'rb')) == 0:
                        print("Blockchain file found with INITIAL block.")
                    else:
                        time = maya.now().iso8601()
                        blockchain.head = Block("0", time, "00000000-0000-0000-0000-000000000000", 0, "INITIAL", 14, "Initial block")
                        blockchain.tail = blockchain.head
                        size += 1
                        blockchain_file = open(path, 'wb')
                        blockchain.write_blockchain(blockchain_file)
                        blockchain_file.close()
                        print("Blockchain file not found. Created INITIAL block.\n")
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
