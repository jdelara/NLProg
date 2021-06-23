class Item:
    def __init__(self, name):
        self.name = name
        self.actions = {}
        self.open = False
    
    def add_action(self, name, action):
        self.actions[name] = action
    
    def get_action(self, name):
        return self.actions[name]
    
    def describe_item_in(self):        
        sen = ""
        size = len(self.actions["open"].item_in)
        sen += "Inside the " + self.name + " you can find "
        for idx, i_in in enumerate(self.actions["open"].item_in):
            sen += "a " + i_in.name + "." if size == 1 else ""
            sen += "a " + i_in.name + ", " if idx < size-1 and idx != size-2 else ""
            sen += "a " + i_in.name + " " if idx == size-2 else ""                    
            sen += "and a " + i_in.name + "." if size > 1 and idx == size-1 else "" 
        return sen

    def describe_item_need(self, missing):
        sen = "You can't open the " + self.name + ". You are missing "
        size = len(missing)
        for idx,item in enumerate(missing):
            sen += "a " + item + "." if size == 1 else ""
            sen += "a " + item + ", " if idx < size-1 and idx != size-2 else ""
            sen += "a " + item + " " if idx == size-2 else ""                    
            sen += "and a " + item + "." if size > 1 and idx == size-1 else ""
        return sen
         

    