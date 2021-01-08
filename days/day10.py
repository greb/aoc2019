import math
import collections

def parse(inp):
    asteroids = set()
    for y, row in enumerate(inp.splitlines()):
        for x, tile in enumerate(row):
            if tile == '#':
                asteroids.add((x,y))
    return asteroids

def slope_dist(src, dst):
    sx,sy = (d-s for s,d in zip(src, dst))
    d = math.gcd(sx,sy)
    return (sx//d, sy//d), d

def angle(slope):
    sx, sy = slope
    # due to laser atan(x,y) instead of atan(y,x) and diff from pi to get
    # clockwise heading.
    return math.pi - math.atan2(sx, sy)

def find_station(asteroids):
    cnts = []
    for src in asteroids:
        slopes = set()
        for dst in asteroids:
            if src == dst:
                continue
            slope, _ = slope_dist(src,dst)
            slopes.add(slope)
        cnts.append((len(slopes), src))
    return max(cnts)

def part1(inp):
    asteroids = parse(inp)
    n_seen, _ = find_station(asteroids)
    return n_seen

def part2(inp):
    asteroids = parse(inp)
    _, station = find_station(asteroids)
    asteroids.discard(station)

    by_slope = collections.defaultdict(list)
    for asteroid in asteroids:
        slope, dist = slope_dist(station, asteroid)
        by_slope[slope].append((dist, asteroid))

    targets = []
    while len(targets) < len(asteroids):
        for slope in sorted(by_slope, key=angle):
            for _, asteroid in sorted(by_slope[slope]):
                if asteroid not in targets:
                    targets.append(asteroid)
                    # found a onvaporzied one
                    break

    bet = targets[199]
    return bet[0]*100 + bet[1]

