def first():
    a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    print( [elem for elem in a if elem > 5])


def second():
    a = [1, 1, 2, 3, 5, 34, 21, 21, 34, 55, 89]
    b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    print([elem for elem in b if elem in a])
    print(a.sort())
def third():
    d = {'a' : '4',  'b' : '2', 'c': 3}
    sorted(d.items(), )
    print(d)
third()

array = [('Argentina', 83), ('Bolgaria', 33), ('Filipins', 65)]
to_degree = lambda a: (a[0], a[1]* 2)
print(list(map(to_degree, array)))

def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))
