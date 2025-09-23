# xy_md02_summary.py
from pymodbus.client import ModbusTcpClient

HOST, PORT = "10.1.2.1", 502
UNIT = 2            # XY-MD02 ของพี่อยู่ที่ ID=2
TIMEOUT = 3

# Input Registers (FC=04)
REG_TEMP = 0x0001   # temperature (signed, /10)
REG_RH   = 0x0002   # humidity   (unsigned, /10)

def int16_signed(x):
    return x - 0x10000 if x >= 0x8000 else x

def read_u16_input(cli, addr):
    rr = cli.read_input_registers(address=addr, count=1, slave=UNIT)
    return None if rr.isError() else rr.registers[0]

def main():
    cli = ModbusTcpClient(HOST, port=PORT, timeout=TIMEOUT)
    if not cli.connect():
        print(f"❌ Connect failed: {HOST}:{PORT}")
        return
    try:
        # อ่านรวดเดียว 2 คำ (Temp+RH) ก็ได้ตามคู่มือ
        rr = cli.read_input_registers(address=REG_TEMP, count=2, slave=UNIT)
        if not rr.isError():
            raw_t, raw_h = rr.registers[0], rr.registers[1]
        else:
            # เผื่ออุปกรณ์/เฟิร์มแวร์บางเวอร์ชัน ตอบแยกทีละค่า
            raw_t = read_u16_input(cli, REG_TEMP)
            raw_h = read_u16_input(cli, REG_RH)

        temp = rh = None
        if raw_t is not None:
            temp = int16_signed(raw_t) / 10.0
        if raw_h is not None:
            rh = raw_h / 10.0

        # แสดงสรุปหน้าเดียว
        print("--- XY-MD02 readings ---")
        print(f"Temperature    : {temp:.1f} °C" if temp is not None else "Temperature    : —")
        print(f"Humidity       : {rh:.1f} %RH" if rh is not None else "Humidity       : —")

    finally:
        cli.close()

if __name__ == "__main__":
    main()
