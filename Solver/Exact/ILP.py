from ortools.linear_solver import pywraplp

# Input
N, Q = map(int, input().split())
pred = []
for _ in range(Q):
    pred.append(map(int, input().split()))
d = [0] + list(map(int, input().split()))
M = int(input())
s = [0] + list(map(int, input().split()))
K = int(input())
c = [[0 for i in range(M+1)] for j in range(N+1)]
for _ in range(K):
    task, team, cost = map(int, input().split())
    c[task][team] = cost



max_completion_time = sum(d) + sum(s)
max_cost = sum([sum(c[i]) for i in range(N+1)])

# Declare the solver
solver = pywraplp.Solver.CreateSolver('SAT')

# Declare variables
a = [[0 for i in range(M+1)] for j in range(N+1)]
for i in range(1, N+1):
    for j in range(1, M+1):
        a[i][j] = solver.IntVar(0, 1, 'a' + str(i) + str(j))

t = [0 for _ in range(N+1)]
for i in range(1, N+1):
    t[i] = solver.IntVar(0, max_completion_time, 'time' + str(i))

u = [0 for _ in range(N+1)]
for i in range(1, N+1):
    u[i] = solver.IntVar(0, 1, 'u' + str(i))

m = [[0 for j in range(N+1)] for i in range(N+1)]
b = [[0 for j in range(N+1)] for i in range(N+1)]

for i in range(1, N+1):
    for j in range(1, N+1):
        m[i][j] = solver.IntVar(-max_completion_time, max_completion_time, 'm' + str(i) + str(j))
        b[i][j] = solver.IntVar(0, 1, 'b' + str(i) + str(j))

num_tasks = solver.IntVar(0, N, 'num_tasks')
completion_time = solver.IntVar(0, max_completion_time, 'completion_time')
total_cost = solver.IntVar(0, max_cost, 'total_cost')

# Declare the constraints
for i in range(1, N+1):
    solver.Add(sum([a[i][j] for j in range(1, M+1)]) == u[i])

for i, j in pred:
    solver.Add(t[j] >= t[i] + d[i])
    solver.Add(u[i] >= u[j]) 

for i in range(1, N+1):
    solver.Add(t[i] >= sum([s[j]*a[i][j] for j in range(1, M+1)]))
    solver.Add(t[i] - (1 - u[i])*2*max_completion_time + d[i] <= completion_time)

for i in range(1, N+1):
    for j in range(1, M+1):
        solver.Add(a[i][j] <= min(c[i][j], 1))

for i1 in range(1, N+1):
    for i2 in range(i1+1, N+1):
        solver.Add(t[i1] - t[i2] - d[i2] <= m[i1][i2])
        solver.Add(t[i2] - t[i1] - d[i1] <= m[i1][i2])
        solver.Add(t[i1] - t[i2] - d[i2] + 2*max_completion_time*b[i1][i2] >= m[i1][i2])
        solver.Add(t[i2] - t[i1] - d[i1] + 2*max_completion_time*(1-b[i1][i2]) >= m[i1][i2])
        
        for j in range(1, M+1):
            solver.Add(m[i1][i2] + max_completion_time*(2 - a[i1][j] - a[i2][j]) >= 0)

solver.Add(num_tasks == sum([u[i] for i in range(1, N+1)]))
solver.Add(total_cost == sum(sum([c[i][j]*a[i][j] for j in range(1, M+1)]) for i in range(1, N+1)))

# Declare the objective function
c1 = (max_cost + 1)*(max_completion_time + 1)
c2 = max_cost + 1
c3 = 1
solver.Maximize(c1*num_tasks - c2*completion_time -c3*total_cost)

# solver.SetTimeLimit(300*1000)

# Solve the problem and print the answer
ans = ""

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    team = [0 for _ in range(N+1)]
    for i in range(1, N+1):
        for j in range(1, M+1):
            if a[i][j].solution_value() != 0:
                team[i] = j
                break
    schedule = []
    for i in range(1, N+1):
        if team[i] != 0:
            schedule.append(i)
    ans = ans + str(len(schedule)) + "\n"
    print(len(schedule))
    for i in schedule:
        print(i, team[i], int(t[i].solution_value()))
        ans = ans + str(i) + " " + str(team[i]) + " " + str(int(t[i].solution_value())) + "\n"



print("Total tasks completed:", num_tasks.solution_value())
print("Total completion time:", completion_time.solution_value())
print("Total cost:", total_cost.solution_value())
# print(solver.ExportModelAsLpFormat(False).replace('\\', '').replace(',_', ','), sep='\n')
print(f"Total time elapsed: {solver.wall_time()} ms")

