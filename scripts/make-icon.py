#!/usr/bin/env python3
"""Regenerate the Español Akademie home-screen icon as crisp pixel-art.

Pure standard library (no Pillow). Authors a 36x36 logical grid and scales
it x5 with nearest-neighbour to 180x180 so every pixel stays a hard block
(no anti-aliasing / blur). Run from the repo root:

    python3 scripts/make-icon.py

Writes both apple-touch-icon.png and assets/icon-180.png.
"""
import zlib, struct

G, SCALE = 36, 5
INK   = (65,38,95,255)
WHITE = (255,255,255,255)
PURPLE = (181,140,240)              # --purple / lavender #b58cf0

# solid lavender background (no gradient — looks cleaner at small sizes)
px=[[(*PURPLE,255) for _ in range(G)] for _ in range(G)]

def setp(x,y,c):
    if 0<=x<G and 0<=y<G: px[y][x]=c

# (no border frame — plain lavender background)

xoff, yoff = 12, 7
# tilde: bold 2-row descending wave (left high -> right low) = ñ mark
tilde = {0:[1,2,3,4,5], 1:[1,2,3,4,5,6,7], 2:[6,7,8,9,10,11], 3:[8,9,10,11]}
for r,cols in tilde.items():
    for c in cols: setp(xoff+c, yoff+r, WHITE)

# N body rows 5..20
for i in range(16):
    y=yoff+5+i
    for c in (0,1,2,10,11,12): setp(xoff+c,y,WHITE)
    center=round(1+(i/15)*10)
    for c in (center-1,center,center+1):
        if 0<=c<=12: setp(xoff+c,y,WHITE)

for (cx,cy) in [(28,9),(8,28),(27,27)]:
    for dx,dy in [(0,0),(-1,0),(1,0),(0,-1),(0,1)]: setp(cx+dx,cy+dy,WHITE)

W=H=G*SCALE
raw=bytearray()
for y in range(H):
    raw.append(0); row=px[y//SCALE]
    for x in range(W): raw.extend(row[x//SCALE])

def chunk(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
png=b"\x89PNG\r\n\x1a\n"
png+=chunk(b"IHDR",struct.pack(">IIBBBBB",W,H,8,6,0,0,0))
png+=chunk(b"IDAT",zlib.compress(bytes(raw),9))
png+=chunk(b"IEND",b"")
open("apple-touch-icon.png","wb").write(png)
open("assets/icon-180.png","wb").write(png)
print("ok", len(png))
