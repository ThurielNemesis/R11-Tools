import mmap, struct, sys, os

def compress_file(input_file, output_file):
    with open(input_file, "rb") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
            in_size = len(m)
            out_size = (in_size * 9 + 7) // 8 + 4
            out = bytearray(out_size)
            
            struct.pack_into("<i", out, 0, in_size) 
            
            i, o = 0, 4
            while i < in_size:
                if not (i & 7):
                    out[o] = 0xff                  
                    o += 1
                out[o] = m[i]
                i += 1
                o += 1

            with open(output_file, "wb") as o:
                o.write(out)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    compress_file(input_file, output_file)
