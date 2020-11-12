
def corutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


def subgen():
    x = 'Girst hello'
    message = yield x
    print(message)


class ExmpleExeption(Exception):
    pass
# необходимо передавать g.send(None) в самом начале, что бы дойти до первого yield
# g.throw(StopIteration)
@corutine
def average():
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print('Done')
        # можем вызвать исключение с помощью g.throw(ExampleExeption)
        except ExmpleExeption:
            print('This is ExampleExeption')
        else:
            count += 1
            summ += x
            average = round(summ / count, 2)
