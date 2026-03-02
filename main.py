import task
import sys

TASK_MANAGER_MAIN = task.TaskManager()

def Add_Section():
    name = input("Enter Section name > ")
    TASK_MANAGER_MAIN.Add_Section(name)

def Add_Task():
    section = input("Enter Section name > ")
    task = input("Enter Task name > ")
    time = input("Enter Task Length in min > ")
    TASK_MANAGER_MAIN.Add_Task(section, task, time)
    
def Del_Section():
    section = input("Enter Section name > ")
    TASK_MANAGER_MAIN.Del_Section(section)
    
def Del_Task():
    section = input("Enter Section name > ")
    task = input("Enter Task name > ")
    TASK_MANAGER_MAIN.Del_Task(section, task)
    
def Calc_Time(full):
    if not full:
        section = input("Enter Section name > ")
        print(f"{section} will take {TASK_MANAGER_MAIN.Calc_Time(section)} min to complete.")
    else:
        print(f"All tasks will take {TASK_MANAGER_MAIN.Calc_Full_Time()} min to complete.")

def Show_Manager():
    for section in TASK_MANAGER_MAIN.data:
        print(f"{section}:")
        for task in TASK_MANAGER_MAIN.data[section]:
            print(f"name: {task['name']} time: {task['time']}")

while True:
    choice1 = input("\nAdd a Section or Task?(1)\nDelete a Section or Task?(2)\nCalculate Section time to complete?(3)\nCalculate All tasks time to complete?(4)\nSee manager?(5)\nExit(6) > ")
    if choice1 == "1":
        choice2 = input("\nSection or Task? S/T > ")
        if choice2.lower() == "s":
            Add_Section()
        elif choice2.lower() == "t":
            Add_Task()
    elif choice1 == "2":
        choice2 = input("\nSection or Task? S/T > ")
        if choice2.lower() == "s":
            Del_Section()
        elif choice2.lower() == "t":
            Del_Task()
    elif choice1 == "3":
        Calc_Time(False)
    elif choice1 == "4":
        Calc_Time(True)
    elif choice1 == "5":
        Show_Manager()
    elif choice1 == "6":
        sys.exit()