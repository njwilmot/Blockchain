class Node:    
	def __init__(self,value):        
		self.value = value        
		self.next = None
		
class LinkedList:
	def __init__(self,head=None):
		self.head = head    
		def append(self, new_node):
            current = self.head
            if current:
                while current.next:
                    current = current.next
                current.next = new_node
            else:
                self.head = new_node
