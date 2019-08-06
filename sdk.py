n = 3      
n2, n3, n4 = n**2, n**3, n**4

def show(flatline):
    
    fmt = '|'.join(['%s' * n] * n)
    sep = '+'.join(['-'  * n] * n)
    for i in range(n):
        for j in range(n):
            offset = (i*n+j)*n2
            print fmt % tuple(flatline[offset:offset+n2])
        if i != n-1:
            print sep

def _find_friends(cell):
    
    friends = set()
    row, col = cell // n2, cell % n2
    friends.update(row * n2 + i for i in range(n2))
    friends.update(i * n2 + col for i in range(n2))   
    nw_corner = row // n * n3 + col // n * n
    friends.update(nw_corner + i + j for i in range(n) for j in range(0,n3,n2))
    friends.remove(cell)
    return tuple(friends)
friend_cells = map(_find_friends, range(n4))

def select_an_unsolved_cell(possibles, heuristic=min):
    
    return heuristic((len(p), cell) for cell, p in enumerate(possibles) if len(p)>1)[1]

def solve(possibles, pending_marks):
    
    for cell, v in pending_marks:
        possibles[cell] = v
        for f in friend_cells[cell]:
            p = possibles[f]
            if v in p:
                p = possibles[f] = p.replace(v, '')     
                if not p:
                    return None               
                if len(p) == 1:
                    pending_marks.append((f, p[0]))

    
    if max(map(len, possibles)) == 1:
        return ''.join(possibles)
    
    
    cell = select_an_unsolved_cell(possibles)
    for v in possibles[cell]:           
        ans = solve(possibles[:], [(cell, v)])
        if ans is not None:
            return ans


for given in [
    input("enter string(81 max ,9  min)")
    ]:
    show(given)
    pending_marks = [(i,v) for i, v in enumerate(given) if v != ' ']
    possibles = ['123456789'] * len(given)
    result = solve(possibles, pending_marks)
    print
    show(result)
    print '=-' * 20
