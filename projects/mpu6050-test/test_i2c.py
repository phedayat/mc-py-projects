from machine import Pin, I2C

def bytes_to_int(msb, lsb):
    if not msb & 0x80:
        return msb << 8 | lsb
    return -(((msb^255)<<8) | (lsb^255)+1)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

def read(addr, maddr, buffer):
    i2c.readfrom_mem_into(addr, maddr, buffer)
    return True

def write(addr, maddr, data):
    n = len(data)
    buffer = bytearray(n)
    buffer[:n] = data
    i2c.writeto_mem(addr, maddr, buffer)
    return True

def temp():
    b = bytearray(2)
    fahrenheit = lambda x: (x*(9/5))+32
    read(104, 0x41, b)
    #temp_c = bytes_to_int(b[0], b[1])/340+35
    temp_c = int.from_bytes(b, "big")/340+35
    temp_f = fahrenheit(temp_c)
    return (temp_c, temp_f)

def accel():
    bx = bytearray(8)
    by = bytearray(8)
    bz = bytearray(8)
    read(104, 0x3B, bx)
    read(104, 0x3D, by)
    read(104, 0x3F, bz)
    print(bytes_to_int(bx[0], bx[len(bx)-1]))
    print(bytes_to_int(by[0], by[len(by)-1]))
    print(bytes_to_int(bz[0], bz[len(bz)-1]))
    print(bytes_to_int(bx[0], bx[1]))
    print(bytes_to_int(by[0], by[1]))
    print(bytes_to_int(bz[0], bz[1]))
    return (bx, by, bz)

while True:
    print(temp())
