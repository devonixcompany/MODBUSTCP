#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian as _Endian

# --- Endian compatibility: รองรับทั้ง pymodbus 2.x และ 3.x ---
try:
    ENDIAN_BIG = _Endian.BIG
    ENDIAN_LITTLE = _Endian.LITTLE
except AttributeError:
    ENDIAN_BIG = _Endian.Big
    ENDIAN_LITTLE = _Endian.Little

HOST = "10.1.2.1"
PORT = 502
UNIT = 1
TIMEOUT = 3

# ===== SDM120 Input Registers (FC=04), offsets (0-based) =====
REG = {
    # Core
    "voltage_V":            0x0000,  # 30001
    "current_A":            0x0006,  # 30007
    "active_W":             0x000C,  # 30013
    "apparent_VA":          0x0012,  # 30019
    "reactive_var":         0x0018,  # 30025
    "power_factor":         0x001E,  # 30031
    "freq_Hz":              0x0046,  # 30071
    "total_kWh":            0x0156,  # 30343

    # Energy & Demand (เสริม)
    "imp_kWh":              0x0048,  # 30073
    "exp_kWh":              0x004A,  # 30075
    "imp_kvarh":            0x004C,  # 30077
    "exp_kvarh":            0x004E,  # 30079
    "tot_demand_W":         0x0054,  # 30085
    "max_tot_demand_W":     0x0056,  # 30087
    "imp_demand_W":         0x0058,  # 30089
    "max_imp_demand_W":     0x005A,  # 30091
    "exp_demand_W":         0x005C,  # 30093
    "max_exp_demand_W":     0x005E,  # 30095
    "curr_demand_A":        0x0102,  # 30259
    "max_curr_demand_A":    0x0108,  # 30265
    "total_kvarh":          0x0158,  # 30345
}

LABELS = {
    "voltage_V":         ("Voltage", "V", 2),
    "current_A":         ("Current", "A", 3),
    "active_W":          ("Active Power", "W", 1),
    "apparent_VA":       ("Apparent Power", "VA", 1),
    "reactive_var":      ("Reactive Power", "var", 1),
    "power_factor":      ("Power Factor", "", 3),
    "freq_Hz":           ("Frequency", "Hz", 2),
    "total_kWh":         ("Energy (Total)", "kWh", 3),

    "imp_kWh":           ("Import Energy", "kWh", 3),
    "exp_kWh":           ("Export Energy", "kWh", 3),
    "imp_kvarh":         ("Import Reactive", "kvarh", 3),
    "exp_kvarh":         ("Export Reactive", "kvarh", 3),
    "tot_demand_W":      ("Total Demand", "W", 1),
    "max_tot_demand_W":  ("Max Total Demand", "W", 1),
    "imp_demand_W":      ("Import Demand", "W", 1),
    "max_imp_demand_W":  ("Max Import Demand", "W", 1),
    "exp_demand_W":      ("Export Demand", "W", 1),
    "max_exp_demand_W":  ("Max Export Demand", "W", 1),
    "curr_demand_A":     ("Current Demand", "A", 3),
    "max_curr_demand_A": ("Max Current Demand", "A", 3),
    "total_kvarh":       ("Reactive (Total)", "kvarh", 3),
}

CORE_KEYS   = ["voltage_V","current_A","active_W","apparent_VA","reactive_var","power_factor","freq_Hz","total_kWh"]
EXTRA_KEYS  = ["imp_kWh","exp_kWh","imp_kvarh","exp_kvarh","tot_demand_W","max_tot_demand_W","imp_demand_W","max_imp_demand_W","exp_demand_W","max_exp_demand_W","curr_demand_A","max_curr_demand_A","total_kvarh"]

def read_f32_input(cli: ModbusTcpClient, offset: int, unit: int):
    rr = cli.read_input_registers(address=offset, count=2, slave=unit)
    if rr.isError():
        return None
    dec = BinaryPayloadDecoder.fromRegisters(rr.registers, byteorder=ENDIAN_BIG, wordorder=ENDIAN_BIG)
    return dec.decode_32bit_float()

def fmt_value(name: str, val):
    label, unit, prec = LABELS[name]
    if val is None:
        return f"{label:16} : —"
    if unit:
        return f"{label:16} : {val:.{prec}f} {unit}"
    return f"{label:16} : {val:.{prec}f}"

def main():
    cli = ModbusTcpClient(HOST, port=PORT, timeout=TIMEOUT)
    if not cli.connect():
        print(f"❌ Connect failed: {HOST}:{PORT}")
        return

    try:
        # อ่านทุกค่า
        data = {}
        for key in CORE_KEYS + EXTRA_KEYS:
            data[key] = read_f32_input(cli, REG[key], UNIT)

        # สรุปหน้าเดียว
        print("--- SDM120 readings ---")
        for key in CORE_KEYS:
            print(fmt_value(key, data[key]))

        # แสดงกลุ่มเสริมต่อท้าย (มีค่าแสดงได้ก็พิมพ์)
        extras_to_show = [k for k in EXTRA_KEYS if data[k] is not None]
        if extras_to_show:
            print("\n--- Energy & Demand ---")
            for key in extras_to_show:
                print(fmt_value(key, data[key]))

    finally:
        cli.close()

if __name__ == "__main__":
    main()
