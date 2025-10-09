input = '5445555435543545555455545453545435345445553354'
# as_list = input.split('')
as_int = [x for x in map(int, input)]
print(f'{(sum(as_int) / len(as_int)):.2f}')