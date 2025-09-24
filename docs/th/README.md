# เซอร์วิส MODBUS TCP - เอกสารภาษาไทย

ยินดีต้อนรับสู่เอกสารฉบับครอบคลุมสำหรับเซอร์วิส MODBUS TCP ซึ่งเป็นโซลูชันที่พร้อมใช้ในการผลิตสำหรับการรวบรวมข้อมูลจากอุปกรณ์ MODBUS ด้วยหลักการ Clean Architecture

## 📋 สารบัญ

### 🚀 [เริ่มต้นใช้งาน](getting-started/)
ใหม่กับเซอร์วิส MODBUS TCP? เริ่มที่นี่!
- [คู่มือเริ่มต้นอย่างรวดเร็ว](getting-started/quick-start.md)
- [คู่มือการติดตั้ง](getting-started/installation.md)
- [ขั้นตอนแรก](getting-started/first-steps.md)
- [การตั้งค่าเบื้องต้น](getting-started/configuration.md)

### 👥 [คู่มือผู้ใช้](user-guide/)
คู่มือสมบูรณ์สำหรับผู้ใช้งาน
- [การจัดการอุปกรณ์](user-guide/device-management.md)
- [การรวบรวมข้อมูล](user-guide/data-collection.md)
- [การตรวจสอบและสุขภาพระบบ](user-guide/monitoring.md)
- [การจัดการการตั้งค่า](user-guide/configuration.md)
- [การใช้งาน CLI](user-guide/cli-usage.md)
- [การแก้ไขปัญหา](user-guide/troubleshooting.md)

### 🛠️ [คู่มือนักพัฒนา](developer-guide/)
เอกสารทางเทคนิคสำหรับนักพัฒนา
- [ภาพรวมสถาปัตยกรรม](developer-guide/architecture.md)
- [หลักการ Clean Architecture](developer-guide/clean-architecture.md)
- [ชั้น Domain](developer-guide/domain-layer.md)
- [ชั้น Application](developer-guide/application-layer.md)
- [ชั้น Infrastructure](developer-guide/infrastructure-layer.md)
- [ชั้น Presentation](developer-guide/presentation-layer.md)
- [การเพิ่มอุปกรณ์ใหม่](developer-guide/adding-devices.md)
- [โครงสร้างฐานข้อมูล](developer-guide/database-schema.md)
- [คู่มือการทดสอบ](developer-guide/testing.md)
- [การมีส่วนร่วม](developer-guide/contributing.md)

### 🌐 [เอกสารอ้างอิง API](api-reference/)
เอกสาร REST API ฉบับสมบูรณ์
- [ภาพรวม API](api-reference/overview.md)
- [การยืนยันตัวตน](api-reference/authentication.md)
- [Endpoints สำหรับอุปกรณ์](api-reference/devices.md)
- [Endpoints สำหรับการอ่านค่า](api-reference/readings.md)
- [Endpoints สำหรับการตรวจสอบ](api-reference/monitoring.md)
- [การจัดการข้อผิดพลาด](api-reference/errors.md)
- [ข้อมูลจำเพาะ OpenAPI](api-reference/openapi.md)

### 🚀 [การติดตั้งระบบ](deployment/)
คู่มือการติดตั้งระบบการผลิต
- [การติดตั้งด้วย Docker](deployment/docker.md)
- [การติดตั้งด้วย Kubernetes](deployment/kubernetes.md)
- [การตั้งค่าสภาพแวดล้อม](deployment/environment.md)
- [การตั้งค่าฐานข้อมูล](deployment/database.md)
- [การตรวจสอบและ Logging](deployment/monitoring.md)
- [การพิจารณาด้านความปลอดภัย](deployment/security.md)
- [การปรับแต่งประสิทธิภาพ](deployment/performance.md)

### 💡 [ตัวอย่าง](examples/)
ตัวอย่างการใช้งานจริงและบทเรียน
- [ตัวอย่างการใช้งานพื้นฐาน](examples/basic-usage.md)
- [ตัวอย่างการตั้งค่าอุปกรณ์](examples/device-configs.md)
- [ตัวอย่างการใช้งาน API](examples/api-examples.md)
- [ตัวอย่างการเชื่อมต่อ](examples/integrations.md)
- [การสร้างอุปกรณ์แบบกำหนดเอง](examples/custom-devices.md)

## 🎯 การนำทางด่วน

| ฉันต้องการ... | ไปที่ |
|---------------|-------|
| เริ่มใช้เซอร์วิสอย่างรวดเร็ว | [เริ่มต้นใช้งาน](getting-started/) |
| เรียนรู้เกี่ยวกับการตั้งค่าอุปกรณ์ | [คู่มือผู้ใช้ - การจัดการอุปกรณ์](user-guide/device-management.md) |
| ใช้งาน REST API | [เอกสารอ้างอิง API](api-reference/) |
| ติดตั้งระบบการผลิต | [คู่มือการติดตั้ง](deployment/) |
| ขยายโค้ดเบส | [คู่มือนักพัฒนา](developer-guide/) |
| ดูตัวอย่างการทำงาน | [ตัวอย่าง](examples/) |

## 📖 เกี่ยวกับเซอร์วิสนี้

เซอร์วิส MODBUS TCP เป็นโซลูชันที่พร้อมใช้ในการผลิต ซึ่งเปลี่ยนสคริปต์แยกแต่ละตัวให้เป็นระบบที่รวมเป็นหนึ่งเดียวและบำรุงรักษาได้ โดยมีคุณสมบัติ:

- **Clean Architecture** - โค้ดเบสที่บำรุงรักษาและทดสอบได้
- **หลายอินเทอร์เฟซ** - ทั้ง CLI และ REST API
- **การจัดเก็บฐานข้อมูล** - รองรับ PostgreSQL และ InfluxDB
- **รองรับ Docker** - การบรรจุแพ็กเกจที่พร้อมใช้ในการผลิต
- **การตรวจสอบที่ครอบคลุม** - การตรวจสอบสุขภาพและสถานะระบบ
- **รองรับอุปกรณ์หลายชนิด** - SDM120, PM2510-0D, XY-MD02 และอุปกรณ์ทั่วไป

## 🔧 คุณสมบัติหลัก

### อุปกรณ์ที่รองรับ
- **SDM120** - มิเตอร์พลังงานพร้อมการวัดแรงดัน กระแส พลังงาน
- **PM2510-0D** - เซ็นเซอร์ฝุ่นพร้อมการตรวจสอบ PM2.5 และ PM10
- **XY-MD02** - เซ็นเซอร์สิ่งแวดล้อมพร้อมอุณหภูมิและความชื้น
- **MODBUS ทั่วไป** - รองรับอุปกรณ์ MODBUS ใดๆ ที่กำหนดค่าได้

### อินเทอร์เฟซ
- **Command Line Interface (CLI)** - อินเทอร์เฟซเทอร์มินัลที่มีคุณสมบัติครบ
- **REST API** - API ที่เป็นมิตรกับเว็บพร้อมเอกสาร Swagger
- **ไฟล์การตั้งค่า** - การตั้งค่าอุปกรณ์ในรูปแบบ YAML

### การจัดเก็บข้อมูล
- **PostgreSQL** - ข้อมูลเชิงสัมพันธ์สำหรับอุปกรณ์และการตั้งค่า
- **InfluxDB** - ข้อมูลอนุกรมเวลาสำหรับการอ่านค่าเซ็นเซอร์
- **In-Memory** - รองรับการพัฒนาและทดสอบ

## 🤝 รับความช่วยเหลือ

- **ปัญหา**: รายงานข้อบกพร่องหรือขอคุณสมบัติใน [GitHub Issues](https://github.com/devonixcompany/MODBUSTCP/issues)
- **การสนทนา**: เข้าร่วมการสนทนาชุมชน
- **เอกสาร**: คู่มือที่ครอบคลุมนี้ครอบคลุมทุกด้านของเซอร์วิส

## 📄 ใบอนุญาต

โครงการนี้ได้รับอนุญาตภายใต้ใบอนุญาต MIT ดูไฟล์ LICENSE สำหรับรายละเอียด