import itertools

W, H = 25, 6

def chunks(it, n):
    it = iter(it)
    chunk = list(itertools.islice(it, n))
    while chunk:
        yield chunk
        chunk = list(itertools.islice(it, n))

def count_layer(layer):
    cnt = [0,0,0]
    for digit in layer:
        cnt[digit] += 1
    return cnt

def part1(inp):
    digits = [int(c) for  c in inp.strip()]

    cnts = []
    for layer in chunks(digits, W*H):
        cnts.append(count_layer(layer))
    _, ones, twos = min(cnts)
    return ones * twos


def part2(inp):
    digits = [int(c) for  c in inp.strip()]

    pic = [[2 for _ in range(W)] for _ in range(H)]
    for layer in chunks(digits, W*H):
        for y, row in enumerate(chunks(layer, W)):
            for x, d in enumerate(row):
                if d == 2:
                    continue
                if pic[y][x] < 2:
                    continue
                pic[y][x] = d

    for row in pic:
        print(''.join('.#X'[d] for d in row))

    # Put here your own solution
    return "GZKJY"
