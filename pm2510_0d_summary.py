#!/usr/bin/env python3
from pymodbus.client import ModbusTcpClient

HOST, PORT, UNIT = "10.1.2.1", 502, 4
TIMEOUT = 3

REG_PM25 = 0x0004
REG_PM10 = 0x0009
REG_ADDR = 0x0100
REG_BAUD = 0x0101
BAUD_MAP = {0: 2400, 1: 4800, 2: 9600}

def rd03(cli, addr, n=1):
    r = cli.read_holding_registers(address=addr, count=n, slave=UNIT)
    return None if r.isError() else r.registers

def main():
    cli = ModbusTcpClient(HOST, port=PORT, timeout=TIMEOUT)
    if not cli.connect():
        print("❌ Connect failed"); return
    try:
        # วิธี A: อ่านทีละค่า (เสถียรสุด)
        r25 = rd03(cli, REG_PM25, 1)
        r10 = rd03(cli, REG_PM10, 1)

        pm25 = None if not r25 else int(r25[0])
        pm10 = None if not r10 else int(r10[0])

        # วิธี B (fallback): บางรุ่นอ่านยาว 6 คำจาก 0x0004 เพื่อได้ PM2.5+PM10
        if pm25 is None or pm10 is None:
            blk = rd03(cli, REG_PM25, 6)
            # รูปแบบโดยทั่วไป: [PM2.5, 0x0005?, 8, PM10, 0x0005?, ...]
            if blk and len(blk) >= 4:
                pm25 = pm25 if pm25 is not None else int(blk[0])
                pm10 = pm10 if pm10 is not None else int(blk[3])

        # พารามิเตอร์ Address/baud
        par = rd03(cli, REG_ADDR, 2)
        dev_addr = par[0] if par and len(par) >= 2 else None
        baud = BAUD_MAP.get(par[1], par[1]) if par and len(par) >= 2 else None

        # สรุปหน้าเดียว
        print("--- PM2510-0D (ID 4) ---")
        print(f"PM2.5          : {pm25} µg/m³" if pm25 is not None else "PM2.5          : —")
        print(f"PM10           : {pm10} µg/m³" if pm10 is not None else "PM10           : —")
        if dev_addr is not None: print(f"Device Address : {dev_addr}")
        if baud is not None:     print(f"Baud Rate      : {baud} bps")

    finally:
        cli.close()

if __name__ == "__main__":
    main()
