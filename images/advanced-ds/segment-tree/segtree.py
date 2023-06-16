def draw(l, r, L, R, dpt, ty, num, pr):
    if l <= L and R <= r and ty == 'pass node':
        ty = 'end node'
    elif ty == 'end node':
        ty = 'more node'
    elif max(l, L) > min(r, R):
        ty = 'normal node'
    print('\\node[', ty,'] (v', num, ') at (', (L + R) / 2, ',', -dpt, ') {};', sep='')
    if pr != -1:
        print('\\draw (v', pr, ') -- (v', num, ');', sep='')
    if L == R: 
            return
    M = (L + R) // 2
    draw(l, r, L, M, dpt + 1, ty, 2 * num, num)
    draw(l, r, M + 1, R, dpt + 1, ty, 2 * num + 1, num)

draw(10, 26, 1, 32, 0, 'pass node', 1, -1)
