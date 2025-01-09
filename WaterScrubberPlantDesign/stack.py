class PlantStack:
    def __init__(self):
        self.stack = []
    
    def push(self, setup):
        self.stack.append(setup)
    
    def pop(self):
        return self.stack.pop() if self.stack else None
    
    def peek(self):
        return self.stack[-1] if self.stack else None
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def get_full_setup(self):
        return self.stack
