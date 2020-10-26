
'''
Author David Snoble
This function is just simple for now to create a triangular board 
I need to figure out how to create hexagons instead of hashs

'''
def triangle():
    size = 8
    m = (2 * size) - 2
    for i in range(0, size):
        for j in range(0, m):
            print(end = " ")
        m = m - 1
        for j in range(0, i + 1):
            print("# ", end= ' ')
        print(" ")