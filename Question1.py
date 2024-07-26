from collections import defaultdict, deque

class TaskScheduler:
    def __init__(self, tasks, dependencies):
        self.tasks = tasks
        self.dependencies = dependencies
        self.graph = defaultdict(list)
        self.in_degree = {task: 0 for task in tasks}
        self.durations = {task: tasks[task] for task in tasks}
        self.EST = {task: 0 for task in tasks}
        self.EFT = {task: 0 for task in tasks}
        self.LFT = {task: float('inf') for task in tasks}
        self.LST = {task: float('inf') for task in tasks}

    def build_graph(self):
        for u, v in self.dependencies:
            self.graph[u].append(v)
            self.in_degree[v] += 1

    def topological_sort(self):
        zero_in_degree_queue = deque([task for task in self.tasks if self.in_degree[task] == 0])
        topological_order = []

        while zero_in_degree_queue:
            current_task = zero_in_degree_queue.popleft()
            topological_order.append(current_task)

            for neighbor in self.graph[current_task]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    zero_in_degree_queue.append(neighbor)

        return topological_order

    def forward_pass(self, topological_order):
        for task in topological_order:
            for neighbor in self.graph[task]:
                self.EST[neighbor] = max(self.EST[neighbor], self.EFT[task])
                self.EFT[neighbor] = self.EST[neighbor] + self.durations[neighbor]

    def backward_pass(self, topological_order):
        project_duration = max(self.EFT.values())
        for task in topological_order:
            self.LFT[task] = project_duration

        for task in reversed(topological_order):
            for neighbor in self.graph[task]:
                self.LFT[task] = min(self.LFT[task], self.LST[neighbor])
                self.LST[task] = self.LFT[task] - self.durations[task]

    def calculate_critical_path(self):
        self.build_graph()
        topological_order = self.topological_sort()
        self.forward_pass(topological_order)
        self.backward_pass(topological_order)

        earliest_completion_time = max(self.EFT.values())
        latest_completion_time = max(self.LFT.values())
        
        return earliest_completion_time, latest_completion_time

def get_user_input():
    tasks = {}
    dependencies = []

    num_tasks = int(input("Enter the number of tasks: "))
    for _ in range(num_tasks):
        task = input("Enter task name: ")
        duration = int(input(f"Enter duration for task {task}: "))
        tasks[task] = duration

    num_dependencies = int(input("Enter the number of dependencies: "))
    for _ in range(num_dependencies):
        dependency = input("Enter dependency (Task1 must be completed before Task2): ")
        u, v = dependency.split()
        dependencies.append((u, v))

    return tasks, dependencies

if __name__ == "__main__":
    tasks, dependencies = get_user_input()
    
    if 'T_START' not in tasks:
        tasks['T_START'] = 0
    
    scheduler = TaskScheduler(tasks, dependencies)
    earliest, latest = scheduler.calculate_critical_path()
    print(f"Earliest completion time: {earliest}")
    print(f"Latest completion time: {latest}")
#Overall Space Complexity: 𝑂(𝑉+𝐸)
#Overall Time Complexity: O(V+E)