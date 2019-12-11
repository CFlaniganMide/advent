import numpy as np

def checkAscending(iStr):
    return np.all(np.diff(iStr) >= 0)

def checkDouble(iStr):
    return np.any(np.diff(iStr) == 0)

def checkExactDoubles(iStr):
    iDiff = np.diff(iStr)
    if iDiff[0] == 0 and iDiff[1] != 0:
        return True
    if iDiff[-1] == 0 and iDiff[-2] != 0:
        return True
    for i in range(1,5):
        if iDiff[i] == 0:
            if iDiff[i-1] != 0 and iDiff[i+1] != 0:
                return True
    return False


count = 0
count2 = 0
for i in range(108457, 562041 + 1):
    iStr = np.array([int(x) for x in str(i)])
    if not checkAscending(iStr):
        continue

    if not checkDouble(iStr):
        continue

    count += 1

    if not checkExactDoubles(iStr):
        continue
    count2 += 1

print(count, count2)
