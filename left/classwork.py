def n000():
    print(sum([int(el) for el in input().split()]))


def n001_v1():
    def rec(i, j, steps):
        nonlocal answer

        if j >= m or j < 0 or i >= n or i < 0:
            return
        if steps > m + n - 1:
            return

        if prison_map[i][j] == '0':
            return
        if i == 0 and j == m - 1:
            answer += 1
            return

        rec(i, j + 1, steps + 1)
        rec(i, j - 1, steps + 1)
        rec(i + 1, j, steps + 1)
        rec(i - 1, j, steps + 1)

    answer = 0
    n, m = [int(el) for el in input().split()]
    prison_map = [list(input()) for _ in range(n)]
    rec(n - 1, 0, 1)

    print(answer if answer else 'impossible')


def n001_v2():
    n, m = [int(el) for el in input().split()]  # 3 5
    # prison_map = [[int(el) - 1 for el in input()] for _ in range(n)]

    prison_map = []
    for i in range(n):
        line = []
        for el in input():
            line.append(int(el) - 1)
        prison_map.append(line)

    prison_map[n - 1][0] = 1
    for i in range(n - 2, -1, -1):
        if prison_map[i][0] != -1 and prison_map[i + 1][0] not in [-1, 0]:
            prison_map[i][0] = 1

    for j in range(1, m):
        if prison_map[n - 1][j] != -1 and prison_map[n - 1][j - 1] not in [-1, 0]:
            prison_map[n - 1][j] = 1

    for i in range(n - 2, -1, -1):
        for j in range(1, m):
            if prison_map[i][j] != -1:
                if prison_map[i + 1][j] != -1:
                    prison_map[i][j] += prison_map[i + 1][j]
                if prison_map[i][j - 1] != -1:
                    prison_map[i][j] += prison_map[i][j - 1]

    for line in prison_map:
        print(line)


def n002():
    cards = sorted([int(el) for el in input().split()])

    if cards[0] == cards[4]:
        print('poker')
    elif cards[0] == cards[3] or cards[1] == cards[4]:
        print('four of a king')
    elif cards[0] == cards[2] or cards[1] == cards:
        pass


if __name__ == '__main__':
    n001_v2()
    pass
