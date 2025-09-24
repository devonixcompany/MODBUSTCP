# คู่มือเริ่มต้นอย่างรวดเร็ว

ให้เซอร์วิส MODBUS TCP ทำงานได้ภายในเวลาไม่ถึง 5 นาทีด้วย Docker

## 🚀 ขั้นตอนที่ 1: โคลน Repository

```bash
git clone https://github.com/devonixcompany/MODBUSTCP.git
cd MODBUSTCP
```

## 🐳 ขั้นตอนที่ 2: เริ่มต้นด้วย Docker Compose

วิธีที่เร็วที่สุดในการเริ่มต้นทุกอย่าง:

```bash
# เริ่มต้นเซอร์วิสทั้งหมด (API, PostgreSQL, InfluxDB)
docker-compose up -d

# ตรวจสอบว่าเซอร์วิสทำงานอยู่
docker-compose ps
```

นี่จะเริ่มต้น:
- **MODBUS TCP API** บน `http://localhost:8000`
- **ฐานข้อมูล PostgreSQL** บนพอร์ต `5432`
- **InfluxDB** บนพอร์ต `8086`

## 🌐 ขั้นตอนที่ 3: เข้าถึง API

เปิดเบราว์เซอร์และไปที่:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **การตรวจสอบสุขภาพ**: http://localhost:8000/api/v1/health

## 🔧 ขั้นตอนที่ 4: เพิ่มอุปกรณ์แรกของคุณ

### การใช้อินเทอร์เฟซเว็บ (Swagger UI)

1. ไปที่ http://localhost:8000/docs
2. คลิกที่ **"POST /api/v1/devices"**
3. คลิก **"Try it out"**
4. ใช้การตั้งค่าตัวอย่างนี้:

```json
{
  "name": "มิเตอร์พลังงานของฉัน",
  "device_type": "SDM120",
  "host": "10.1.2.1",
  "port": 502,
  "unit_id": 1,
  "timeout": 3
}
```

5. คลิก **"Execute"**

### การใช้ Command Line

```bash
# เข้าสู่คอนเทนเนอร์ API
docker-compose exec modbustcp-api bash

# เพิ่มอุปกรณ์
python modbustcp.py device add \
  --name "มิเตอร์พลังงานของฉัน" \
  --type SDM120 \
  --host 10.1.2.1 \
  --unit 1

# แสดงรายการอุปกรณ์
python modbustcp.py device list
```

## 📊 ขั้นตอนที่ 5: ทดสอบการเชื่อมต่อ

ก่อนรวบรวมข้อมูล ให้ทดสอบการเชื่อมต่อ:

### การใช้ API

1. ใน Swagger UI ค้นหา **"POST /api/v1/devices/test-connection"**
2. ทดสอบด้วยการตั้งค่าอุปกรณ์ของคุณ:

```json
{
  "host": "10.1.2.1",
  "port": 502,
  "unit_id": 1,
  "timeout": 3
}
```

### การใช้ CLI

```bash
# ทดสอบการเชื่อมต่อ
python modbustcp.py test-connection --host 10.1.2.1 --unit 1
```

## 📈 ขั้นตอนที่ 6: รวบรวมข้อมูล

เมื่ออุปกรณ์ของคุณเชื่อมต่อแล้ว:

### การใช้ API

1. ค้นหา **"POST /api/v1/readings/collect"**
2. ใช้ ID อุปกรณ์ของคุณเพื่อรวบรวมข้อมูล:

```json
{
  "device_id": "your-device-id"
}
```

### การใช้ CLI

```bash
# รวบรวมข้อมูลจากอุปกรณ์เฉพาะ
python modbustcp.py data collect <device-id>

# รวบรวมจากอุปกรณ์ทั้งหมด
python modbustcp.py data collect-all
```

## 🏥 ขั้นตอนที่ 7: ตรวจสอบสุขภาพ

ตรวจสอบสุขภาพของอุปกรณ์ของคุณ:

### การใช้ API

- **อุปกรณ์เดียว**: GET `/api/v1/monitoring/health/{device_id}`
- **อุปกรณ์ทั้งหมด**: GET `/api/v1/monitoring/health`
- **ภาพรวมระบบ**: GET `/api/v1/monitoring/system-health`

### การใช้ CLI

```bash
# ตรวจสอบอุปกรณ์ทั้งหมด
python modbustcp.py monitor health-all

# ตรวจสอบอุปกรณ์เฉพาะ
python modbustcp.py monitor health <device-id>
```

## 🎯 ขั้นตอนต่อไป

ยินดีด้วย! ตอนนี้คุณมีเซอร์วิส MODBUS TCP ที่ทำงานอยู่แล้ว นี่คือสิ่งที่ควรทำต่อไป:

### สำรวจคุณสมบัติ
- **[การจัดการอุปกรณ์](../user-guide/device-management.md)** - เรียนรู้การตั้งค่าอุปกรณ์
- **[การรวบรวมข้อมูล](../user-guide/data-collection.md)** - ทำความเข้าใจตัวเลือกการรวบรวมข้อมูล
- **[เอกสารอ้างอิง API](../api-reference/)** - สำรวจ endpoints ทั้งหมด

### ตั้งค่าสำหรับสภาพแวดล้อมของคุณ
- **[คู่มือการตั้งค่า](configuration.md)** - ปรับแต่งการตั้งค่า
- **[เทมเพลตอุปกรณ์](../examples/device-configs.md)** - การตั้งค่าอุปกรณ์ที่สร้างไว้แล้ว

### การติดตั้งระบบการผลิต
- **[การตั้งค่าสภาพแวดล้อม](../deployment/environment.md)** - การตั้งค่าการผลิต
- **[ความปลอดภัย](../deployment/security.md)** - การพิจารณาด้านความปลอดภัย
- **[การตรวจสอบ](../deployment/monitoring.md)** - การตรวจสอบการผลิต

## 🛑 การแก้ไขปัญหา

### ปัญหาทั่วไป

**เซอร์วิสไม่เริ่มต้น?**
```bash
# ตรวจสอบ logs
docker-compose logs

# รีสตาร์ทเซอร์วิส
docker-compose down
docker-compose up -d
```

**ไม่สามารถเชื่อมต่อกับอุปกรณ์?**
```bash
# ตรวจสอบการเชื่อมต่อเครือข่าย
ping 10.1.2.1

# ตรวจสอบการตั้งค่า MODBUS
python modbustcp.py test-connection --host 10.1.2.1 --unit 1
```

**ปัญหาการเชื่อมต่อฐานข้อมูล?**
```bash
# ตรวจสอบ logs ฐานข้อมูล
docker-compose logs postgres
docker-compose logs influxdb

# รีเซ็ตฐานข้อมูล
docker-compose down -v
docker-compose up -d
```

สำหรับความช่วยเหลือเพิ่มเติม ดู **[คู่มือการแก้ไขปัญหา](../user-guide/troubleshooting.md)**

## 🎉 สำเร็จ!

ตอนนี้คุณมีเซอร์วิส MODBUS TCP ที่ทำงานเต็มรูปแบบด้วย:
- ✅ REST API พร้อมเอกสาร Swagger
- ✅ การจัดเก็บฐานข้อมูล (PostgreSQL + InfluxDB)
- ✅ ความสามารถในการจัดการอุปกรณ์
- ✅ การรวบรวมและตรวจสอบข้อมูล
- ✅ การตรวจสอบสุขภาพและสถานะระบบ

พร้อมที่จะสำรวจคุณสมบัติเพิ่มเติม? ดู **[คู่มือผู้ใช้](../user-guide/)** หรือ **[เอกสารอ้างอิง API](../api-reference/)**!