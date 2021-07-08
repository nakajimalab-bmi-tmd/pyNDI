class A:
    def get_name(self):
        return 'A'
    
    def call_name(self):
        print(self.get_name())

class B(A):
    def get_name(self):
        return 'B'

b = B()
b.call_name()

