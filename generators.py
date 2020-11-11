# from time import time
#
#
# def gen_filename():
#     while True:
#         pattern = 'file-{}.jpeg'
#         t = int(time() * 1000)
#         yield pattern.format(str(t))
#
#         sum = 234 + 123
#         print(sum)
#
# g = gen_filename()


def gen_str(s):
    for i in s:
        yield i


def gen_num(n):
    for i in range(n):
        yield i


gens = gen_str('anton')
genn = gen_num(3)

tasks = [gens, genn]

while tasks:
    task = tasks.pop(0)

    try:
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration:
        pass
