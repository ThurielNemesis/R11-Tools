import sys
import struct

def mmap_file(name):
    with open(name, "rb") as f:
        content = f.read()
        return bytearray(content)

def write_file(name, buf):
    with open(name, "wb") as f:
        f.write(buf)

def assert2(cond, msg):
    if not cond:
        print(msg)
        sys.exit(1)

def main():
    assert2(len(sys.argv) == 3, "usage: " + sys.argv[0] + " in.bip out")

    in_file = mmap_file(sys.argv[1])
    in_size = len(in_file)
    out_size = struct.unpack("<i", in_file[0:4])[0]
    out = bytearray(out_size + 18)
    out[0:18] = bytearray([0] * 18)
    i = 4
    o = 0
    mask = 0
    j = 0
    while i < in_size:
        mask >>= 1
        if mask < 0x100:
            mask = in_file[i] | 0x8000
            i += 1
        if mask & 1:
            assert2(o < out_size, "overrun\n")
            out[o] = in_file[i]
            i += 1
            o += 1
        else: # run
            off = ((in_file[i+1]>>4)<<8)+in_file[i]+18
            len_ = (in_file[i+1]&0xf)+3
            m = (o&~0xfff)|(off&0xfff)
            if m >= o:
                m -= 0x1000
            if m < -18:
                print("invalid match %d len %d at %x/%x\n" % (m, len_, i, o))
            assert2(o+len_ <= out_size, "overrun\n")
            i += 2
            for j in range(len_):
                out[o] = out[m]
                o += 1
                m += 1
    assert2(o == out_size, "underrun\n")
    
    while len(out) > 0 and out[-1] == 0:
        out.pop()
        
    if out[-1] != 0:
        out.append(0)
    
    write_file(sys.argv[2], out)

if __name__ == "__main__":
    main()
