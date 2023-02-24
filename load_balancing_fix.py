from typing import List
from random import randint
import hashlib

class Task:
    def __init__(self, length: int, deadline: int):
        self.length = length
        self.deadline = deadline
        self.scheduled = False
        self.executed_at = -1
        self.finished_at = -1

    def minimum_mips(self) -> float:
        return float(self.length)/self.deadline

    def string_repr(self) -> str:
        return "{}{}{}{}".format(self.length, self.deadline, self.executed_at, self.finished_at)

class VM:
    def __init__(self, id:int, mips: float):
        self.id = id
        self.mips = mips
        self.mips_capacity = mips
        self.available_at = 0
        self.mips_used = 0
        self.host_id = -1
    
    def allocateTask(self, task: Task):
        global time_now
        mips_required = task.minimum_mips()
        if mips_required > self.mips:
            return False
        
        this_task_time = t.deadline / mips_required
        time_after_task = this_task_time + time_now
        if self.available_at < time_after_task:
            self.available_at = time_after_task
        
        self.mips_used += mips_required
        self.mips -= mips_required

        task.executed_at = time_now
        task.finished_at = time_after_task
        
class Host:
    vm = None
    id = 0
    def __init__(self, id:int, mips: float):
        self.mips = mips
        self.id = id
        self.mips_capacity = mips
        self.mips_used = 0

    def allocateVM(self, vm: VM):
        if self.vm is None:
            self.vm = []
            return self.allocateVM(vm)
        self.vm.append(vm)
        self.mips -= vm.mips
        self.mips_used += vm.mips
        vm.host_id = self.id

    def releaseVM(self, vm):
        if self.vm is None:
            raise Exception("VM not allocated in host", self.id)
        index = -1
        for i, v in enumerate(self.vm):
            if vm.id == v.id:
                index = i
                break
    
        if index == -1:
            raise Exception("VM not allocated")

        self.vm.pop(index)
        vm.host_id = -1
        self.mips += vm.mips
        self.mips_used -= vm.mips
        vm.mips += vm.mips_used
        vm.mips_used = 0


class DataCenter:
    hosts = None

    def getHost(self, id: int) -> Host:
        for host in self.hosts:
            if host.id == id:
                return host
        return None

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
    host = Host(i+1, 100)
    dc.addHost(host)

vms = []
# create VM
for i in range(6): 
    vm = VM(i+1, 30)
    host = dc.hostForVM(vm)
    vms.append(vm)

tasks = []

# create Tasks
task_str = """995,20,49.75
882,13,67.84615384615384
500,14,35.714285714285715
722,15,48.13333333333333
594,16,37.125
653,15,43.53333333333333
820,13,63.07692307692308
114,2,57.0
891,16,55.6875
749,16,46.8125""".split("\n")

task_small_str = """697,170
652,175
622,176
613,182
286,109
106,23
732,233
362,99
912,223
961,225""".split("\n")

for t in task_str:
    v = t.split(",")
    task = Task(int(v[0]), int(v[1]))
    tasks.append(task)


# mips_treshold = 5
# for i in range(10):
#     while True:
#         length = randint(mips_treshold, 1000)
#         deadline_min = length/mips_treshold
#         deadline = randint(int(deadline_min), 2*int(deadline_min))
#         task = Task(length, deadline)
#         if task.minimum_mips() <= mips_treshold:
#             tasks.append(task)
#             print(task.length, task.deadline, task.minimum_mips())
#             break

# initialization
vij = []
cij = []
for i, t in enumerate(tasks):
    vij.append([])
    cij.append([])
    for j, w in enumerate(dc.hosts):
        vij[i].append(0)
        cij[i].append(0)

def checkAllScheduled(tasks):
    for t in tasks:
        if t.scheduled == False:
            return False
    return True

# compute violation cost for each task on each vm
def computeVIJ(tasks, workers):
    for i, t in enumerate(tasks):
        for j, w in enumerate(workers):
            cij_now = 0
            vij_now = 0

            # no need to compute if task already assigned
            if t.scheduled:
                continue

            # if worker mips is zero (high utilization), then assign high value so algorithm won't pickup the vm
            if w.mips == 0:
                # not available
                cij_now = t.deadline*100
                vij_now = cij_now-t.deadline
            else:
                cij_now = t.length/w.mips
                vij_now = cij_now-t.deadline

            cij[i][j] = cij_now
            vij[i][j] = abs(vij_now)

# compute Vij matrix for the first time
computeVIJ(tasks, dc.hosts)

time_now = 0

def schedule():
    while checkAllScheduled(tasks) == False:
        scheduled_task_count = 0
        for y, t in enumerate(tasks):
            if t.scheduled:
                continue
            # print("Trying to schedule task", y, t.length, t.deadline)
            for j, vm in enumerate(vms):
                next_index = j+1

                if j == len(vms)-1:
                    next_index = 0

                next_vm = vms[next_index]

                if vm.mips >= next_vm.mips:
                    if vm.host_id != -1:
                        # vm is busy
                        continue

                    vm.mips = t.minimum_mips()
                    host = dc.hostForVM(vm)
                    if host is None:
                        print("Cannot execute task", y)
                    else:
                        vm.allocateTask(t)
                        host.allocateVM(vm)
                        t.scheduled = True
                        print("==> Task", y, "scheduled", "on vm", vm.id, "with mips", vm.mips_used, vm.mips, vm.mips_capacity, vm.available_at)
                        scheduled_task_count += 1
                        break
                else:
                    continue
                    print("Skipping non priority vm", j)
        break
        if scheduled_task_count == 0:
            break

while True:
    schedule()
    if checkAllScheduled(tasks):
        break
    next_time = 100000
    vm_released = None

    for vm in vms:
        if next_time >= vm.available_at and vm.host_id != -1:
            next_time = vm.available_at
            vm_released = vm
    
    if vm_released is None:
        for host in dc.hosts:
            print("Host status", host.id, host.mips_used, host.mips)

        for vm in vms:
            print("VM status", vm.available_at, vm.id, vm.host_id)
        raise Exception("No vm released")

    host = dc.getHost(vm_released.host_id)
    if host is None:
        for vm in vms:
            print("VM id {} on host {}".format(vm.id, vm.host_id))
        raise Exception("Host not found: {} for vm id {}".format(vm_released.host_id, vm_released.id))
    else:
        host.releaseVM(vm_released)
    
    print("===FORWARD AT {}===".format(next_time))
    time_now = next_time

    # x = input()
    # for host in dc.hosts:
    #     print("Host status", host.id, host.mips_used, host.mips)

    # for vm in vms:
    #     print("VM status", vm.available_at, vm.id, vm.host_id)

hash_payload = ""
for t in tasks:
    hash_payload += t.string_repr()

print(hashlib.md5(hash_payload.encode()).hexdigest())

# for x, v in enumerate(vms):
#     print("VM", x, v.mips, v.available_at)