# rectangles is a list of tuples (xL, xR, h)
def hidden_lines(rectangles):
    n = len(rectangles)
    if n == 0:
        return []
    elif n == 1:
        # return [(xL, h), (xR, 0)]
        return [(rectangles[0][0], rectangles[0][2]), (rectangles[0][1], 0)]
    else:
        # recursive steps!
        L = hidden_lines(rectangles[:n//2])
        R = hidden_lines(rectangles[n//2:])

        # current height of Left and Right silhouettes respectively
        yL = -1*float('inf')
        yR = -1*float('inf')
        index_L = 0
        index_R = 0
        points = []
        while index_L < len(L) and index_R < len(R):

            # sort by x coordinate!
            if L[index_L][0] < R[index_R][0]:
                next_point = L[index_L]
                index_L += 1
                next_y = next_point[1]

                if next_y > yR:
                    points.append(next_point)
                elif yL > yR:
                    points.append((next_point[0], yR))

                yL = next_point[1]
            else:
                next_point = R[index_R]
                index_R += 1
                next_y = next_point[1]

                if next_y > yL:
                    points.append(next_point)
                elif yR > yL:
                    points.append((next_point[0], yL))

                yR = next_point[1]


        while index_R < len(R):
            points.append(R[index_R])
            index_R += 1

        while index_L < len(L):
            points.append(L[index_L])
            index_L += 1
        
        return points

# ================================================ Testing Code

test = [(1,6,1), (10,13,2), (2,4,2), (11,12,1), (5,8,3), (3,6,4)]
print(hidden_lines(test))
