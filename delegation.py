def corutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


class ExmpleExeption(Exception):
    pass

# @corutine
def subgen():
    while True:
        try:
            message = yield
        except StopIteration:
            print('Exeption')
            break
        else:
            print('_________', message)
    return 'Returned from subgen()'
@corutine
def delegator(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     # deleg.throw(ExmpleExeption)
    #     except ExmpleExeption as e:
    #         g.throw(e)
    result = yield from g
    print(result)

subgen = subgen()

deleg = delegator(subgen)
