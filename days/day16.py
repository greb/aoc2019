def gen_pattern(n):
    while True:
        for p in [0, 1, 0, -1]:
            for _ in range(n):
                yield p

def part1(inp):
    nums = list(map(int, inp.strip()))
    for _ in range(100):
        new_nums = []
        for i in range(len(nums)):
            gen = gen_pattern(i+1)
            next(gen)

            total = 0
            for n, g in zip(nums, gen):
                total += n*g
            new_nums.append(abs(total) % 10)
        nums = new_nums
    return ''.join((map(str, nums[:8])))


def part2(inp):
    nums = list(map(int, inp.strip()))

    start = int(''.join(inp[:7]))
    end = len(nums) * 10_000

    digits = [nums[i % len(nums)] for i in range(start, end)]
    # phase pattern looks like this for all relevant digits
    # ...0,1,1,1,1 d_end-3
    # ...0,0,1,1,1 d_end-2
    # ...0,0,0,1,1 d_end-1
    # ...0,0,0,0,1 d_end
    for _ in range(100):
        digit = 0 
        for i in reversed(range(len(digits))):
            digit = (digit + digits[i]) % 10
            digits[i] = digit

    return ''.join((map(str, digits[:8])))
