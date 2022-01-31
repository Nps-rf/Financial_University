n = int(input())  # 1 <= n <= 100 000 | Total amount of tanks
Volumes = list(map(int, input().split()))  # Volume of each tank
answer = 0
maximal = Volumes[0]
for i in range(len(set(Volumes))):
    maximal = max(Volumes[i], maximal)
    if Volumes[i] < maximal:
        answer = -1
print(max(Volumes) - min(Volumes) if answer == 0 else answer)
