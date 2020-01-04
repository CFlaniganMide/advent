import numpy as np
from tqdm import tqdm

def _fft(signal, n, offset=0):
    # for each iteration, run the fft process to replace the signal
    sigLen = len(signal)

    if offset > sigLen/2:
        partSignal = signal[offset:]
        for _ in tqdm(range(n)):
            partSignal = partSignal[::-1].cumsum()[::-1] % 10
        signal[offset:] = partSignal
        return signal

    for _ in tqdm(range(n)):  # iterate across all runs
        i = offset
        if offset != 0:
            lastSig = signal[i-1]

        # if we are in the first quarter, do a thing
        # for i to 1*i+1, stepping 4*(i+1), sum all of them and add to next value
        # then, for 3*i+2 to 4*i+3 sum all then subtract from next value
        while (3*i + 2) < sigLen:
            # if i % 1000 == 999:
            #     print(i/sigLen)
            nextVal = 0
            step = 4*(i + 1)
            # for j in range(i, 2*i + 1):
            #     nextVal += signal[j::step].sum()
            for j in range(i, sigLen, step):
                for k in range(j, min(j + i + 1, sigLen)):
                    nextVal += signal[k]

            # for j in range(3*i + 2, 4*i + 3):
            #     nextVal -= signal[j::step].sum()
            for j in range(3*i + 2, sigLen, step):
                for k in range(j, min(j + i + 1, sigLen)):
                    nextVal -= signal[k]
            lastSig = signal[i]
            signal[i] = np.abs(nextVal) % 10
            i += 1

        # if we are in the second quarter, do a different thing
        # in this thing, we take the running total from i to 2*i+1, so we start with signal[i:2*i+1].sum() and
        # subtract signal[i-1] and add signal[2*n-1:2*n+1].sum()
        rollingSum = lastSig + signal[i:2*i-1].sum()
        while (2*i + 1) < sigLen:
            # if i % 10000 == 9999:
            #     print(i/sigLen)
            rollingSum -= lastSig
            rollingSum += signal[2*i-1:2*i+1].sum()

            lastSig = signal[i]
            signal[i] = rollingSum % 10
            i += 1

        # if we are in the second half, do a third thing
        # In this thing, we take the sum from i to the end, so we start with the sum from i to the end, then we
        # subtract signal[i-1] from that running total
        rollingSum = lastSig + signal[i:].sum()
        while i < sigLen:
            # if i % 10000 == 9999:
            #     print(i/sigLen)
            rollingSum -= lastSig

            lastSig = signal[i]
            signal[i] = rollingSum % 10
            i += 1

    return signal

def fft(signal, n, offset):
    signal = np.array([int(x) for x in list(signal)], dtype=np.uint64)
    signal = _fft(signal, np.int64(n), offset)
    signal = "".join(str(int(x)) for x in signal)
    return signal

if __name__ == "__main__":
    with open("./input.txt") as f:
        inputString = f.read()
    print(fft(inputString, 100, 0)[:8])

    # exit(0)

    newMessage = inputString*10000
    offset = int(newMessage[:7])
    message = fft(inputString*10000, 100, offset)
    print(offset)

    print(message[offset:offset+8])

