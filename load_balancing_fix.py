from typing import List
from random import randint

class Task:
    def __init__(self, length: int, deadline: int):
        self.length = length
        self.deadline = deadline
        self.scheduled = False
        self.executed_at = -1
        self.finished_at = -1

    def minimum_mips(self) -> float:
        return float(self.length)/self.deadline

class VM:
    def __init__(self, mips: float):
        self.mips = mips
        self.mips_capacity = mips
        self.available_at = 0
    
    def allocateTask(self, task: Task):
        mips_required = task.minimum_mips()
        if mips_required > self.mips:
            return False
        
        self.mips -= mips_required
        
class Host:
    def __init__(self, mips: float):
        self.mips = mips
        self.mips_capacity = mips

    def allocateVM(self, vm: VM):
        if self.vm is None:
            self.vm = []
            return self.allocateVM(vm)
        self.vm.append(vm)
        self.mips -= vm.mips

class DataCenter:
    hosts = None

    def addHost(self, host: Host):
        if self.hosts is None:
            self.hosts = []
            return self.addHost(host)
        self.hosts.append(host)

    def hostForVM(self, vm: VM) -> Host:
        result = []
        resulting_host = None
        lowest_mips_left = 1000000
        for host in self.hosts:
            if host.mips >= vm.mips:
                result.append(host)
                
        for host in result:
            next_mips = host.mips - vm.mips
            if lowest_mips_left > next_mips:
                resulting_host = host
        return resulting_host
        
    def retrieveVMs(self):
        vms = []
        for host in self.hosts:
            for vm in host.vm:
                vms.append(vm)
        return vms



dc = DataCenter()

# create host
for i in range(3):
    host = Host(100)
    dc.addHost(host)

# create VM
for i in range(6): 
    vm = VM(30)
    host = dc.hostForVM(vm)

tasks = []

# create Tasks
mips_treshold = 70
for i in range(10):
    while True:
        length = randint(mips_treshold, 1000)
        deadline_min = length/mips_treshold
        deadline = randint(int(deadline_min), 2*int(deadline_min))
        task = Task(length, deadline)
        if task.minimum_mips() <= mips_treshold:
            tasks.append(task)
            print(task.length, task.deadline, task.minimum_mips())
            break