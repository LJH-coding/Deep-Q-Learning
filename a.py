def f(List):
    for i, j in enumerate(List):
        List[i] += 1
    return List

List = [1, 2, 3, 4, 5]
for i in range(0, 5):
    print(List)
    List = f(List)
    print(List)

print(List)