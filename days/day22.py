import collections
import math

def parse(inp):
    actions = []
    for line in inp.splitlines():
        action, *words = line.split()
        if action == 'cut':
            actions.append((action, int(words[0])))
        elif words[0] == 'with':
            actions.append((action, int(words[2])))
        else:
            actions.append(('new', 0))
    return actions

def part1(inp):
    actions = parse(inp)
    n_cards = 10007
    card_idx = 2019

    for action, n in actions:
        if action == 'new':
            card_idx = (n_cards - 1) - card_idx
        elif action == 'cut':
            card_idx = (card_idx - n) % n_cards
        else:
            card_idx = (card_idx * n) % n_cards
    return card_idx

def inv_mod(n, n_cards):
    return pow(n, n_cards-2, n_cards)

def get_idx(offset, increment, n, n_cards):
    return (offset + n*increment) % n_cards

def part2(inp):
    actions = parse(inp)
    n_cards = 119315717514047
    n_shuffles = 101741582076661
    card_idx = 2020

    increment_mul = 1
    offset_diff = 0

    for action, n in actions:
        if action == 'new':
            increment_mul *= -1
            increment_mul %= n_cards
            offset_diff += increment_mul
            offset_diff %= n_cards
        elif action == 'cut':
            offset_diff += n * increment_mul
            offset_diff %= n_cards
        else:
            increment_mul *= inv_mod(n, n_cards)
            increment_mul %= n_cards

    increment = pow(increment_mul, n_shuffles, n_cards)

    offset_mul = inv_mod((1-increment_mul) % n_cards, n_cards)
    offset = offset_diff * (1-increment)  * offset_mul
    offset %= n_cards

    return get_idx(offset, increment, card_idx, n_cards)

