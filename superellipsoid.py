#Kiah Johnson
#CS 536

import math
import sys

def sgn(x):
    if x >= 0:
        return 1
    else:
        return -1

def compute_point(u, v, s1, s2, A, B, C):
    x = A * sgn(math.cos(u)) * (abs(math.cos(u)) ** s1) * sgn(math.cos(v)) * (abs(math.cos(v)) ** s2)
    y = B * sgn(math.cos(u)) * (abs(math.cos(u)) ** s1) * sgn(math.sin(v)) * (abs(math.sin(v)) ** s2)
    z = C * sgn(math.sin(u)) * (abs(math.sin(u)) ** s1)
    
    return x, y, z

def compute_normals(u, v, s1, s2, A, B, C):
    norm_x = sgn(math.cos(u)) * (abs(math.cos(u)) ** (2 - s1)) * sgn(math.cos(v)) * (abs(math.cos(v)) ** (2 - s2)) / A
    norm_y = sgn(math.cos(u)) * (abs(math.cos(u)) ** (2 - s1)) * sgn(math.sin(v)) * (abs(math.sin(v)) ** (2 - s2)) / B
    norm_z = sgn(math.sin(u)) * (abs(math.sin(u)) ** (2 - s1)) / C
    
    norm = math.sqrt(norm_x ** 2 + norm_y ** 2 + norm_z ** 2)
    return norm_x / norm, norm_y / norm, norm_z / norm

def compute_mesh(s1, s2, A, B, C, u_num, v_num, flat_shaded):
    vertices = []
    normals = []
    indices = []

    vertices.append((0, 0, C))
    if not flat_shaded:
        normals.append((0, 0, 1))
    
    for k in range(1, u_num):
        u = math.pi * (0.5 - k / u_num)
        for j in range(v_num + 1):
            v = 2 * math.pi * j / v_num
            x, y, z = compute_point(u, v, s1, s2, A, B, C)
            vertices.append((x, y, z))
            if not flat_shaded:
                norm_x, norm_y, norm_z = compute_normals(u, v, s1, s2, A, B, C)
                normals.append((norm_x, norm_y, norm_z))

    vertices.append((0, 0, -C))
    if not flat_shaded:
        normals.append((0, 0, -1))

    for kj in range(v_num):
        indices.append((0, kj + 1, kj + 2))
    
    for k in range(1, u_num - 1):
        for j in range(v_num):
            idx1 = (k - 1) * (v_num + 1) + j + 1
            idx2 = idx1 + v_num + 1
            idx3 = idx1 + 1
            idx4 = idx2 + 1
            
            if flat_shaded:
                indices.append((idx1, idx2, idx4))
                indices.append((idx1, idx4, idx3))
            else:
                indices.append((idx1, idx3, idx2))
                indices.append((idx3, idx4, idx2))

    bottom_pole = len(vertices) - 1
    base = (u_num - 2) * (v_num + 1) + 1
    for kjj in range(v_num):
        indices.append((bottom_pole, base + kjj + 1, base + kjj))

    return vertices, normals, indices

def make_iv(vertices, normals, indices, flat_shaded):
    print("#Inventor V2.0 ascii")
    print("Separator {")
    print("Coordinate3 {")
    print("point [")
    for v in vertices:
        print(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f},")
    print("]")
    print("}")
    if not flat_shaded:
        print("NormalBinding {")
        print("value PER_VERTEX_INDEXED }")
        print("Normal {")
        print("vector [")
        for norm in normals:
            print(f"{norm[0]:.6f} {norm[1]:.6f} {norm[2]:.6f},")
        print("]")
        print("}")
    print("IndexedFaceSet {")
    print("coordIndex [")
    for idx in indices:
        print(f"{idx[0]}, {idx[1]}, {idx[2]}, -1,")
    print("]")
    print("}")
    print("}")

def main():
    u_num = 18 #u
    v_num = 9 #v
    s1_val = 1 #r
    s2_val = 1 #t
    A = 1 #A
    B = 1 #B
    C = 1 #C
    flat_shaded = True

    for k in range(len(sys.argv)):
        arg = sys.argv[k]
        if arg == "-r":
            s1_val = float(sys.argv[k + 1])
        elif arg == "-t":
            s2_val = float(sys.argv[k + 1])
        elif arg == "-A":
            A = float(sys.argv[k + 1])
        elif arg == "-B":
            B = float(sys.argv[k + 1])
        elif arg == "-C":
            C = float(sys.argv[k + 1])
        elif arg == "-u":
            u_num = int(sys.argv[k + 1])
        elif arg == "-v":
            v_num = int(sys.argv[k + 1])
        elif arg == "-F":
            flat_shaded = True
        elif arg == "-S":
            flat_shaded = False

    vertices, normals, indices = compute_mesh(s1_val, s2_val, A, B, C, u_num, v_num, flat_shaded)
    make_iv(vertices, normals, indices, flat_shaded)

if __name__ == "__main__":
    main()
