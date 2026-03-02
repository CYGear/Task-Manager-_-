import json

class TaskManager:
    def __init__(self):
        try:
            with open("data.json", "r") as file:
                try:
                    self.data = json.load(file)
                except:
                    self.data = {}
        except:
            print("data.json not found. please add a data.json file.")
                
    def Add_Section(self, name):
        if name not in self.data:
            self.data[name] = []
            self.save()
            
    def Del_Section(self, name):
        try:
            del self.data[name]
            self.save()
        except:
            print(f"{name} not a valid section!")
    
    def Add_Task(self, section, name, time):
        try:
            task = {"name": name, "time": time}
            self.data[section].append(task)
            self.save()
        except:
            print("Invalid Section!")

    def Del_Task(self, section, name):
        if section in self.data:
            for i,task in enumerate(self.data[section]):
                if task["name"] == name:
                    del self.data[section][i]
                    self.save()
                    break
    
    def  Show_Tasks(self):
        print(self.data)
    
    def Calc_Time(self, section):
        time = 0
        try:
            for task in self.data[section]:
                time += int(task["time"])
            return time
        except:
            return time
    
    def Calc_Full_Time(self):
        time = 0
        for section in self.data:
           for task in self.data[section]:
                time += int(task["time"])
        return time
                  
    def save(self):
        with open("data.json", "w") as file:
            json.dump(self.data, file, indent=4)