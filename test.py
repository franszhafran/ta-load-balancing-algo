# check given array of tasks `t` for unassigned tasks
def checkAllAssigned(t):
    for d in t:
        if d["assigned"] == False:
            return False
    return True

# init tasks
tasks = [
    {
        "length": 635,
        "deadline": 3256,
        "assigned": False,
        "assigned_vm_idx": -1,
        "phase": -1,
        'start': -1,
        'finished_at': -1,
        'expected_time': -1,
    },
    {
        "length": 635,
        "deadline": 3256,
        "assigned": False,
        "assigned_vm_idx": -1,
        "phase": -1,
        'start': -1,
        'finished_at': -1,
        'expected_time': -1,
    },
    {
        "length": 635,
        "deadline": 3256,
        "assigned": False,
        "assigned_vm_idx": -1,
        "phase": -1,
        'start': -1,
        'finished_at': -1,
        'expected_time': -1,
    },
    {
        "length": 635,
        "deadline": 3256,
        "assigned": False,
        "assigned_vm_idx": -1,
        "phase": -1,
        'start': -1,
        'finished_at': -1,
        'expected_time': -1,
    },
    {
        "length": 635,
        "deadline": 3256,
        "assigned": False,
        "assigned_vm_idx": -1,
        "phase": -1,
        'start': -1,
        'finished_at': -1,
        'expected_time': -1,
    },
    {
        "length": 635,
        "deadline": 3256,
        "assigned": False,
        "assigned_vm_idx": -1,
        "phase": -1,
        'start': -1,
        'finished_at': -1,
        'expected_time': -1,
    },
    {
        "length": 1,
        "deadline": 3256,
        "assigned": False,
        "assigned_vm_idx": -1,
        "phase": -1,
        'start': -1,
        'finished_at': -1,
        'expected_time': -1,
    },
    {
        "length": 1,
        "deadline": 3256,
        "assigned": False,
        "assigned_vm_idx": -1,
        "phase": -1,
        'start': -1,
        'finished_at': -1,
        'expected_time': -1,
    },
]

# init workers data, with assumption equal portion of vm != same mips
workers = [
    {
        'name': "vm2",
        'mips': 0.166361,
        'mips_capacity': 0.166361,
        'finished_at': 0,
        'start': 0,
    },
    {
        'name': "vm1",
        'mips': 0.210613,
        'mips_capacity': 0.210613,
        'finished_at': 0,
        'start': 0,
    }, 
]
worker_num = len(workers)
vij = []
cij = []
result = []

# initialization
for i, t in enumerate(tasks):
    vij.append([])
    cij.append([])
    for j, w in enumerate(workers):
        vij[i].append(0)
        cij[i].append(0)
# initialization

# compute violation cost for each task on each vm
def computeVIJ(tasks, workers):
    for i, t in enumerate(tasks):
        for j, w in enumerate(workers):
            cij_now = 0
            vij_now = 0

            # no need to compute if task already assigned
            if t["assigned"]:
                continue

            # if worker mips is zero (high utilization), then assign high value so algorithm won't pickup the vm
            if w["mips"] == 0:
                # not available
                cij_now = t["deadline"]*100
                vij_now = cij_now-t["deadline"]
            else:
                cij_now = t["length"]/w["mips"]
                vij_now = cij_now-t["deadline"]

            cij[i][j] = cij_now
            vij[i][j] = abs(vij_now)

# compute Vij matrix for the first time
computeVIJ(tasks, workers)

closestCT = 10000
closestCTIndex = -1

anyTaskAssigned = -1
time = 0
last_time = time
phase = 0

# core of algorithm, run until all tasks assigned
while checkAllAssigned(tasks) == False:
    anyTaskAssigned = 0
    print("Phase", phase)
    for j, w in enumerate(workers):
        next_index = j+1
        if j == len(workers)-1:
            next_index = 0
        
        for i, t in enumerate(tasks):
            if t["assigned"]:
                continue
            
            print("Trying task", i, "on VM", j)
            
            next_w = workers[next_index]
            # check task priority
            if w["mips"] >= next_w["mips"]:
                expected_time = cij[i][j]
                minimum_mips = t["length"]/expected_time
                
                # if vm is possible to be assigned, then assign task to it
                # with true condition of, task deadline is more than completion time
                # and required mips is less than worker mips
                if t["deadline"] >= cij[i][j] and w["mips"]-minimum_mips >= 0:
                    # assigning...
                    print("assign task", i, "to", j)
                    t["assigned"] = True
                    t["assigned_vm_idx"] = j
                    t["phase"] = phase
                    t["expected_time"] = expected_time
                    t["start"] = w["finished_at"]
                    t["finished_at"] = t["start"] + expected_time
                    anyTaskAssigned += 1
                    
                    w["mips"] -= minimum_mips
                    w["finished_at"] = t["finished_at"]
                    if w["mips"] != 0:
                        raise Exception("worker with left mips")
                    print("Decreasing worker", j, "mips to", w["mips"], ",required mips for task", minimum_mips)

                    # recompute VIJ matrix
                    computeVIJ(tasks, workers)
                    
                    expected_finish = t["length"]/minimum_mips
                    
                    if closestCT > expected_finish:
                        closestCT = expected_finish
                        closestCTIndex = j
                else:
                    continue
                    
            else:
                print("skip worker", j, "prioritize next worker")
                break
            
    if anyTaskAssigned == 0:
        print(workers)
        print("Couldn't allocate task with current resource, next phase after", closestCT , "seconds at VM")
        # workers[cti]['mips'] = workers[cti]['mips_capacity']
        ctin = -1
        ctn = 10000000
        
        # find minimum completed VM
        for j, w in enumerate(workers):
            if ctn > w["finished_at"] and w["finished_at"] > 0 and w["finished_at"] > time:
                ctn = w["finished_at"]
                ctin = j

        # check for ready workers
        for j, w in enumerate(workers):
            if w["finished_at"] > 0 and w["finished_at"] >= time:
                w['mips'] = w['mips_capacity']

        print("Minimum completed VM", ctin, "at", ctn, "time now", ctn)
        workers[ctin]['mips'] = workers[ctin]['mips_capacity']
        computeVIJ(tasks, workers)
        phase += 1
        time = ctn
        # input()
print("")
print("Scheduling done, result:")
for i, t in enumerate(tasks):
    print("Task", i+1, "assigned to VM", t["assigned_vm_idx"], "phase", t["phase"], "start time", t["start"], "finished at", t["finished_at"], "expected time required", t["expected_time"])
        