d = 0 # current depth / number of parts
S = sort(Intervals) # sorted intervals by start time
parts = dict() # our interval partitions!

for i in S:
    for part in parts.keys():
        values = parts[part]
        if values.peak().finish_time < i.start_time:
            values.push(i)
            break
    else:
        s = Stack()
        s.push(i)
        parts[d] = s
        d += 1
