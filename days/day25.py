import re
import itertools

import pdb

from . import intcode

reverse_door = {
    'north': 'south',
    'east': 'west',
    'south': 'north',
    'west': 'east'
}

def parse_screen(adventure):
    room = None
    doors = []
    items = []
    success = False
    pw = None

    is_doors = False
    is_items = False
    sec_room = False

    for idx, line in enumerate(adventure.read_lines()):
        if idx > 100:
            # Assume infinite loop
            success = False
            break
        if is_doors:
            if not line:
                is_doors = False
                continue
            doors.append(line[2:])
            continue
        if is_items:
            if not line:
                is_items = False
                continue
            items.append(line[2:])
            continue
        if line.startswith('=='):
            room = line[3:-3]
        elif line.startswith('Doors'):
            is_doors = True
        elif line.startswith('Items'):
            is_items = True
        elif line.startswith('Command?'):
            success = True
        else:
            nums = re.findall(r'\d+', line)
            if nums:
                pw = nums[0]

    return room, doors, items, success, pw


def map_spaceship(adventure):
    sec_room = None
    paths = dict()
    stack = []
    item_locs = dict()

    room, doors, _, _, _ = parse_screen(adventure)
    paths[room] = []
    stack.append((room, None, doors))

    while stack:
        prev_room, prev_door, doors = stack[-1]
        if doors:
            door = doors.pop()
            if door == prev_door:
                continue
            adventure.write(f'{door}\n')
            room, doors, items, _, _ = parse_screen(adventure)
            if room == prev_room:
                sec_room = room, door
                continue

            if room in paths:
                continue
            for item in items:
                item_locs[item] = room

            paths[room] = paths[prev_room] + [door]
            stack.append((room, reverse_door[door], doors))
        else:
            adventure.write(f'{prev_door}\n')
            parse_screen(adventure)
            stack.pop()
    return paths, item_locs, sec_room


def take_item(adventure, item, path):
    for door in path:
        adventure.write(f'{door}\n')
        parse_screen(adventure)

    adventure.write(f'take {item}\n')
    _, _, _, success, _ = parse_screen(adventure)
    if not success:
        return False

    for door in reversed(path):
        prev_door = reverse_door[door]
        adventure.write(f'{prev_door}\n')
        room, _, _, _, _ = parse_screen(adventure)
        if room is None:
            return False
    return True

def check_items(adventure, paths, item_locs):
    valid_items = []
    for item, room in item_locs.items():
        adventure.reset()
        if take_item(adventure, item, paths[room]):
            valid_items.append(item)
    return valid_items

def part1(inp):
    adventure = intcode.Machine(inp, iomode=intcode.IOMode.TXT)
    paths, item_locs, sec_room = map_spaceship(adventure)

    valid_items = check_items(adventure, paths, item_locs)
    for item in valid_items:
        take_item(adventure, item, paths[item_locs[item]])

    sec_room, sec_door = sec_room
    for door in paths[sec_room]:
        adventure.write(f'{door}\n')
        parse_screen(adventure)

    combinations = (itertools.combinations(valid_items, n)
            for n in range(1, len(valid_items)+1))
    combinations = list(map(set, itertools.chain.from_iterable(combinations)))

    for items in combinations:
        for item in valid_items:
            if item in items:
                adventure.write(f'take {item}\n')
            else:
                adventure.write(f'drop {item}\n')
        parse_screen(adventure)

        adventure.write(f'{sec_door}\n')
        room, _, _, _, pw = parse_screen(adventure)
        if room != sec_room:
            break
    return pw

