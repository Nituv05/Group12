# Input
N, Q = map(int, input().split())
pred = []
for _ in range(Q):
    pred.append(tuple(map(int, input().split())))
d = [0] + list(map(int, input().split()))
M = int(input())
s = [0] + list(map(int, input().split()))
K = int(input())
c = [[0 for i in range(M+1)] for j in range(N+1)]
deg = [0 for i in range(N+1)]
for _ in range(K):
    task, team, cost = map(int, input().split())
    c[task][team] = cost
    deg[task] += 1


before = [set() for i in range(N+1)]
after = [set() for i in range(N+1)]
time = [0 for i in range(N+1)]
completed = [0 for i in range(N+1)]

for i, j in pred:
    after[i].add(j)
    before[j].add(i) 

def TopologicalSort():
    edge = [set() for i in range(N+1)]
    in_degree = [0 for i in range(N+1)]
    for u, v in pred:
        edge[u].add(v)
        in_degree[v] += 1
    zero_in_degree = []
    for i in range(1, N+1):
        if in_degree[i] == 0:
            zero_in_degree = [i] + zero_in_degree
    topo = []
    while len(zero_in_degree) > 0:
        node = zero_in_degree[-1]
        zero_in_degree.pop()
        topo.append(node)
        for u in edge[node]:
            in_degree[u] -= 1
            if in_degree[u] == 0:
                zero_in_degree = [u] + zero_in_degree
    return topo

def chooseFirstTask():
    for task in range(1, N+1):
        if completed[task] == 0:
            if len(before[task]) == 0:
                return task
    return -1

def chooseMostImportantTask(): # choose a task which is the predecence of the most tasks
    l = [(-len(after[task]), task) for task in range(1, N+1) if completed[task] == 0 and len(before[task]) == 0]
    if len(l) == 0: return -1
    index = 0
    for i in range(len(l)):
        if l[i] < l[index]:
            index = i
    return l[index][1]


def SelectTeamForTask(task):
    teams = [(max(s[i], time[task]), c[task][i], i) for i in range(1, M+1) if c[task][i] > 0]
    if len(teams) == 0:
        completed[task] = -1
        return -1
    index = 0
    for i in range(len(teams)):
        if teams[i] < teams[index]:
            index = i
    team = teams[index][2]
    return team



l = TopologicalSort()
for task in l:
    if completed[task] == -1:
        for i in after[task]:
            completed[i] = -1
        continue
    team = SelectTeamForTask(task)
    if team == -1:
        completed[task] = -1
        for i in after[task]:
            completed[i] = -1
    time[task] = max(s[team], time[task])
    s[team] = time[task] + d[task]
    completed[task] = team
    for i in after[task]:
        time[i] = max(time[i], time[task] + d[task])
    
ans = ""
schedule = [i for i in range(1, N+1) if completed[i] not in {0, -1}]
print(len(schedule))
for i in schedule:
    print(i, completed[i], time[i])
