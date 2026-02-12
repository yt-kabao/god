import time
import hashlib
import sys

def collect_timing_bytes(samples=256, busy=50):
    buf = bytearray()
    for _ in range(samples):
        t0 = time.perf_counter_ns()
        for i in range(busy):
            _ = i * i
        t1 = time.perf_counter_ns()
        delta = (t1 - t0) & 0xFFFFFFFFFFFFFFFF
        buf += delta.to_bytes(8, 'little')
    return bytes(buf)

def hash_to_u32(data):
    h = hashlib.sha256(data).digest()
    return int.from_bytes(h[:4], 'little')

def to_1_10(u32):
    MOD = 10
    MAX32 = 1 << 32
    limit = (MAX32 // MOD) * MOD
    if u32 >= limit:
        return None
    return (u32 % MOD) + 1

def generate_one():
    while True:
        raw = collect_timing_bytes()
        u = hash_to_u32(raw)
        v = to_1_10(u)
        if v is not None:
            return v

def main():
    count = 1
    if len(sys.argv) > 1:
        try:
            count = max(1, int(sys.argv[1]))
        except ValueError:
            pass
    for _ in range(count):
        print(generate_one())

if __name__ == "__main__":
    main()
