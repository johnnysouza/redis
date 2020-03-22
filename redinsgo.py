import redis

r = redis.Redis(host='localhost', port=6379, db=0)

for n in range(1, 100):
    r.sadd('cartela', n)

for i in range(1, 50):
    user = 'user:{}'.format(i)
    user_name = 'user{}'.format(i)
    cartela = 'cartela:{}'.format(i)
    score =  'score:{}'.format(i)
    r.hset(user, 'name', user_name)
    r.hset(user, 'bcartela', cartela)
    r.hset(user, 'bscore', score)

    for n in range(15):
        number = int(r.srandmember('cartela'))
        r.sadd(cartela, number)

    r.set(score, 0)

print('Começando o bingo')

is_end_game = False
while not is_end_game:
   number_drawn = int(r.srandmember('cartela'))

   for i in range(1, 50):
        user = 'user:{}'.format(i)
        user_name  = r.hget(user, 'name')
        cartela = r.hget(user, 'bcartela')
        score = r.hget(user, 'bscore')

        if (r.sismember(cartela, number_drawn)):
           r.incr(score)

        if (int(r.get(score)) >= 15):
            print('O vencendor do bingo é: {}'.format(user))
            is_end_game = True

# limpar scorea base
r.flushdb()