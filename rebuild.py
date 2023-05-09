tasks = [
    {
        "length": 8,
        "deadline": 4,
        "scheduled": False,
        "scheduled_at_vm": -1,
        "scheduled_step_at": -1,
        "execution_time": -1,
        
    },
    {
        "length": 13,
        "deadline": 3,
        "scheduled": False,
        "scheduled_at_vm": -1,
        "scheduled_step_at": -1,
        "execution_time": -1,
    },
    {
        "length": 3,
        "deadline": 2,
        "scheduled": False,
        "scheduled_at_vm": -1,
        "scheduled_step_at": -1,
        "execution_time": -1,
    },
    {
        "length": 5,
        "deadline": 4,
        "scheduled": False,
        "scheduled_at_vm": -1,
        "scheduled_step_at": -1,
        "execution_time": -1,
    },
    {
        "length": 10,
        "deadline": 3,
        "scheduled": False,
        "scheduled_at_vm": -1,
        "scheduled_step_at": -1,
        "execution_time": -1,
    },
]

vms = [
    2, 3, 4
]

vms_work_time = [0, 0, 0]

computed_map = []

for i, t in enumerate(tasks):
    for j, v in enumerate(vms):
        time_needed = t['length']/v
        computed_map.append({
            "time_needed": time_needed,
            "task_index": i,
            "vm_index": j,
        })


computed_map_sorted = sorted(computed_map, key=lambda x: x['time_needed'])

def findMinimumIndex(r):
    min_value = 10000000000
    min_index = -1
    for i, j in enumerate(r):
        if min_value > j:
            min_value = j
            min_index = i

    return min_index
any_task_scheduled = False
scheduled_step_at = 1

def allTaskScheduled(t):
    for v in t:
        if v['scheduled'] == False:
            return False
    return True

while allTaskScheduled(tasks) == False:
    for i, c in enumerate(computed_map_sorted):
        task_index = c['task_index']
        vm_index = c['vm_index']
        time_needed = c['time_needed']

        # continue if task already assigned
        if tasks[c['task_index']]['scheduled']:
            continue

        # p = input()

        if any_task_scheduled == False:
            vms_work_time[vm_index] += c['time_needed']
            tasks[task_index]['scheduled'] = True
            tasks[task_index]['scheduled_at_vm'] = vm_index+1
            tasks[task_index]['execution_time'] = time_needed
            tasks[task_index]['scheduled_step_at'] = scheduled_step_at
            scheduled_step_at += 1

            any_task_scheduled = True
        else:
            priority_vm_index = findMinimumIndex(vms_work_time)
            if priority_vm_index == vm_index or vms_work_time[priority_vm_index] == vms_work_time[vm_index]:
                vms_work_time[vm_index] += c['time_needed']
                tasks[task_index]['scheduled'] = True
                tasks[task_index]['scheduled_at_vm'] = vm_index+1
                tasks[task_index]['execution_time'] = time_needed
                tasks[task_index]['scheduled_step_at'] = scheduled_step_at
                print("Task", task_index+1, "scheduled")
                scheduled_step_at += 1

for t in tasks:
    print(t)

print(vms_work_time)