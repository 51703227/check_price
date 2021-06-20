txt = 'Laptop Đồ họa ConceptD 7 Ezel Pro CC715-91P-X8CX (NX.C5FSV.001) (Xeon W 10885M/ 32Gb/ 1Tb SSD/ 15.6" UHD 4K Touch/ Pen/ Màn hình xoay gặp 180 độ/Quadro RTX5000 16G/ Win10 Pro/ Trắng)'

a = list(txt)

while "(" and ")" in a:
    x = a.index("(")
    y = a.index(")")

    for i in range(x,y+1):
        a[i] = ''
    
print(''.join(a))