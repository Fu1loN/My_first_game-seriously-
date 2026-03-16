PRINT_IO = False

def read_file_by_chunks(filename):
    with open(filename, 'rb') as f:
        chunk = f.read(8)
        while chunk:
            yield chunk
            chunk = f.read(8)
    return

def show_res(func):
    def wrapper(*args):
        print('start', *args)
        res = func(*args)
        print('end', res)
        return res
    if PRINT_IO:
        return wrapper
    else:
        return func


def M(bits_16):
    # print(bits_16)
    left = bits_16[0]
    right = bits_16[1]
    yl =  P(h(left) ^ right)
    yr = P(cycle_move(left, 8) ^ right)
    return bytes([yl, yr])

def perestanovka(bytes_8):
    return bytes([bytes_8[i] for i in perestanovka_vector])

def xor(bytes_8, c):
    res = bytes([i ^ j for i, j in zip(bytes_8, c)])
    return res


def P(x:int) -> int:
    pr = x & 15
    pl = x >> 4
    t = (pl ^ f(pr))
    qr = pr ^ g(t) << 4 >> 4
    ql = (t ^ f(qr)) << 4 
    return ql | qr

def F(k, c):
    # print(list(map(hex, k)), list(map(hex, c)), sep='\n')
    res = bytes([P(x) for x in xor(k, c)])
    # print(res)
    # print([hex(P(x)) for x in xor(k, c)])
    res = T(res)
    return res

def T(bytes_64:bytes)->bytes:
    mask = 2**8
    res = []
    for i in range(8):
        byte = 0
        mask = mask >> 1
        for j in range(8):
            if i <= j:
                byte += (bytes_64[j] & mask) >> (j-i)
            else:
                byte += (bytes_64[j] & mask) << (i-j)
        res.append(byte)
    return bytes(res)

def get_bytes_array_from_string(bytes_value):
    return [int(bytes_value[i:i+2], 16) for i in range(0, len(bytes_value), 2)]


@show_res
def time(bytes_8):
    prev = bytes_8
    for c in c1, c2:
        res = b''
        for group in every_2_bytes(prev):
            res += M(group)
        # print('t=', *map(hex, perestanovka(res)), sep=' ')
        res = xor(perestanovka(res), c)
        # print(res)
        prev = res
    res = b''
    for group in every_2_bytes(prev):
            res += M(group)
    res = perestanovka(res)
    return res


def encode(chunk):
    print(f'encoding chunk {chunk.hex()}')
    for i in range(8):
        print(f'раунд {i}')
        chunk = time(xor(chunk, keys[i]))
    return xor(chunk, keys[8]) 

def encode_file(filename):
    with open(f'{filename}.encoded.bin', 'wb') as f:
        for chunk in read_file_by_chunks(filename):
            f.write(encode(chunk))

def every_2_bytes(bytes_8):
    for i in range(0, 8, 2):
        yield bytes_8[i:i+2]
    return 

ftable = [int(i, 16) for i in 'fdbb7577edabedef']
def f(x):
    return ftable[x]

def complemente(x, size=4):
    return 2 ** size - 1 - x

gtable = [10, 6, 0, 2, 11, 14, 1, 8, 13, 4, 5, 3, 15, 12, 7, 9]
def g(x):
    return gtable[x]

perestanovka_vector = [0, 2, 4, 6, 1, 3, 5, 7]


def h(x):
    return cycle_move(x, 8) & int('55', 16) ^ x 
def cycle_move(x, size):
    y = x << 1
    first = (x & 2 ** (size-1)) >> (size -1)
    # print(f'cycle_move input {bin(x)} output {bin((y | first) & (2 ** size - 1))}')
    # print(bin(first), size)
    return (y | first) & (2 ** size - 1)


c1_string = 'b7e151628aed2a6a'       
c1 = [int(c1_string[i:i+2], 16) for i in range(0, 16, 2)]
c2_string = 'bf7158809cf4f3c7'       
c2 = [int(c2_string[i:i+2], 16) for i in range(0, 16, 2)]




def get_keys(k:str):
    k = get_bytes_array_from_string(k)
    kl = k[:8]
    kr = k[8:]
    # print(kl, kr, sep='\n')
    keys = [kr, kl]
    c = [[int(ci[i:i+2], 16) for i in range(0, 16, 2)] for ci in [
            '290d61409ceb9e8f',
            '1f855f585b013986',
            '972ed7d635ae1716',
            '21b6694ea5728708',
            '3c18e6e7faadb889',
            'b700f76f73841163',
            '3f967f6ebf149dac',
            'a40e7ef6204a6230',
            '03c54b5a46a34465',
        ]]

    # print(*c, sep='\n')
    for i in range(9):
        ki = xor(F(keys[i-1+2], c[i]), keys[i-2+2])
        keys.append(ki)
    return  keys[2:]
keys = get_keys('0123456789abcdeffedcba9876543210')
# print('keys=')
# print(*keys, sep='\n')
# print(encode(bytes(get_bytes_array_from_string('0123456789abcdef'))))


def M_1(bytes_2:bytes) -> bytes:
    yl = bytes_2[0]
    yr = bytes_2[1]
    xl = h_1(P(yl) ^ P(yr)) 
    xr = (cycle_move(xl, 8) ^ P(yr))
    return bytes([xl, xr])

def h_1(x:int)->int:
    return (cycle_move(x, 8) & int('aa', 16)) ^ x

perestanovka_vector2 = [0, 4, 1, 5, 2, 6, 3, 7]
def peresranocka2(bytes_8):
    return bytes([bytes_8[i] for i in perestanovka_vector2])

@show_res
def time_r(bytes_8:bytes):
    prev = res = bytes_8
    for c in c2, c1:
        prev = res = peresranocka2(res)
        res = b''
        for group in every_2_bytes(prev):
            res += M_1(group)
        # print('t=', *map(hex, perestanovka(res)), sep=' ')
        res = xor(res, c)
        # print(res)
        prev = res
    prev = peresranocka2(res)
    res = b''
    for group in every_2_bytes(prev):
        res += M_1(group)
    return res
def decode(chunk:bytes):
    print(f'decoding chunk {chunk.hex()}')
    chunk = xor(chunk, keys[-1])
    for i in range(7, -1, -1):
        print(f'раунд {i}')
        chunk = xor(keys[i], time_r(chunk))
        # print(chunk.hex())
    return chunk
print(encode(bytes(get_bytes_array_from_string('0123456789abcdef'))).hex())
print(decode(bytes(get_bytes_array_from_string('88fddfbe954479d7'))).hex())



encode_file('text.txt')