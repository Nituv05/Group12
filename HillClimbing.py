import random
from time import time as tm


# Input
def InputFromFile(filepath):
    f = open(filepath, 'r')
    N, Q = map(int, f.readline().strip("\n").split())
    pred = []
    for _ in range(Q):
        pred.append(tuple(map(int, f.readline().strip("\n").split())))
    d = [0] + list(map(int, f.readline().strip("\n").split()))
    M = int(f.readline().strip("\n"))
    s = [0] + list(map(int, f.readline().strip("\n").split()))
    K = int(f.readline().strip("\n"))
    c = [[0 for i in range(M + 1)] for j in range(N + 1)]
    for _ in range(K):
        task, team, cost = map(int, f.readline().strip("\n").split())
        c[task][team] = cost
    f.close()
    return N, Q, pred, d, M, s, K, c


# Topological Sort implementation
def TopologicalSort(N, pred):
    edge = [set() for i in range(N + 1)]
    in_degree = [0 for i in range(N + 1)]
    for u, v in pred:
        edge[u].add(v)
        in_degree[v] += 1
    zero_in_degree = []
    for i in range(1, N + 1):
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


# Read the input
N, Q, pred, d, M, s, K, c = InputFromFile('input.txt')

max_cost = sum([sum(c[i]) for i in range(N + 1)])

# Initialize the available list, where available[i] is list of teams that can do task i
available = [[] for i in range(N + 1)]
for i in range(1, N + 1):
    for j in range(1, M + 1):
        if c[i][j] > 0:
            available[i].append(j)

before = [set() for i in range(N + 1)]
after = [set() for i in range(N + 1)]

for u, v in pred:
    after[u].add(v)
    before[v].add(u)


class State:
    def __init__(self, l, cal_evaluation=True):
        self.l = l[:]
        self.index = self.GetIndex()
        self.evaluation = (0, 0)

    def GetEvaluation(self, Print=False):
        scheduled = 0
        tmp_s = s[:]
        tmp_time = [0 for i in range(N + 1)]
        tmp_completed = [0 for i in range(N + 1)]
        for task in self.l:
            if tmp_completed[task] == -1:
                for i in after[task]:
                    tmp_completed[i] = -1
                continue
            teams = [(max(tmp_s[i], tmp_time[task]), c[task][i], i) for i in available[task]]
            if len(teams) == 0:
                tmp_completed[task] = -1
                for i in after[task]:
                    tmp_completed[i] = -1
                continue
            index = 0
            for i in range(len(teams)):
                if teams[i] < teams[index]:
                    index = i
            team = teams[index][2]
            tmp_completed[task] = team
            scheduled += 1
            tmp_time[task] = max(tmp_s[team], tmp_time[task])
            tmp_s[team] = tmp_time[task] + d[task]
            for i in after[task]:
                tmp_time[i] = max(tmp_time[i], tmp_time[task] + d[task])
        total_time = 0
        total_cost = 0
        for i in range(1, N + 1):
            if tmp_completed[i] not in {-1, 0}:
                total_time = max(total_time, tmp_time[i] + d[i])
                total_cost += c[i][tmp_completed[i]]

        if Print:
            ans = ""
            f = open('output.txt', 'w')
            ans = ans + str(scheduled) + "\n"
            for i in range(1, N + 1):
                if tmp_completed[i] not in {-1, 0}:
                    ans = ans + str(i) + " " + str(tmp_completed[i]) + " " + str(tmp_time[i]) + "\n"
            f.write(ans)
            f.close()
        return (total_time, total_cost)

    def GetIndex(self):
        index = [0 for i in range(N + 1)]
        for i in range(len(self.l)):
            index[self.l[i]] = i
        return index

    def Evaluation(self):
        if self.evaluation != (0, 0):
            return self.evaluation
        return self.GetEvaluation()

    def GetNeighbor(self, task):
        left = 0
        right = N - 1
        for t in before[task]:
            left = max(left, self.index[t])
        for t in after[task]:
            right = min(right, self.index[t])
        BeforeIndex = self.index[task]
        if left + 1 >= right - 1:
            return self
        AfterIndex = random.randint(left + 1, right - 1)
        new_l = self.l[:]
        if BeforeIndex < AfterIndex:
            tmp = new_l[BeforeIndex]
            i = BeforeIndex
            while i < AfterIndex:
                new_l[i] = new_l[i + 1]
                i += 1
            new_l[AfterIndex] = tmp
        elif BeforeIndex > AfterIndex:
            tmp = new_l[BeforeIndex]
            i = BeforeIndex
            while i > AfterIndex:
                new_l[i] = new_l[i - 1]
                i -= 1
            new_l[AfterIndex] = tmp
        return State(new_l)

    def Mutation(self):
        state = State(self.l)
        for task in set(range(1, N + 1)):
            state = state.GetNeighbor(task)
        return state


class HillClimb:
    def __init__(self):
        pass

    def Solve(self, time_limit=10, step_limit=120):
        t = tm()
        ans = State(TopologicalSort(N, pred))
        step = 0
        print(f'Step: {step},', 'Evaluation:', ans.Evaluation())
        while tm() - t <= time_limit and step <= step_limit:
            preans = ans
            step += 1
            MinEvaluation = ans.Evaluation()
            candidate = set()
            for task in range(1, N + 1):
                neighbor = ans.GetNeighbor(task)
                if neighbor.Evaluation() < MinEvaluation:
                    MinEvaluation = neighbor.Evaluation()
                    candidate = set()
                    candidate.add(neighbor)
                elif neighbor.Evaluation() == MinEvaluation:
                    candidate.add(neighbor)
            if MinEvaluation < ans.Evaluation():
                for v in candidate:
                    ans = v
                    break
                print(f'Step: {step},', 'Evaluation:', ans.Evaluation(), 'runtime', (tm() - t) * 1000)
        return ans


l = TopologicalSort(N, pred)
solver = HillClimb()
state = solver.Solve(time_limit=30)
state.GetEvaluation(True)

print("Solution written to output.txt")
