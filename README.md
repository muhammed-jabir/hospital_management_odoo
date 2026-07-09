# Hospital Management System (Odoo 16 Custom Module)

A full-featured hospital appointment booking and management system built as a custom Odoo 16 module — covering a public-facing website, backend administration, role-based access control, automated reporting, and online payments.

## Overview

This module was built end-to-end as a hands-on learning project covering the complete Odoo development lifecycle: data modeling, backend views, website controllers, security, reporting, and third-party payment integration.

Patients can browse doctors, book appointments online, and pay through Razorpay — while hospital staff manage doctors, departments, appointments, and available time slots through a role-restricted backend.

## Features

### Public Website
- Doctor listing page (`/doctors`) with photos and department info
- Appointment booking page (`/booking`) with dynamic doctor filtering by department
- Real-time available time slot selection per doctor, per date
- Medical report upload during booking
- Razorpay payment gateway integration for appointment confirmation
- Patient portal — "My Appointments" page for logged-in users

### Backend Management
- **Doctors** — profile, department, experience level (auto-computed from age), linked user login, photo
- **Departments** — with assigned manager and doctor list
- **Doctor Time Slots** — multiple bookable slots per doctor per day, editable inline; also manageable directly from a doctor's own form via a dedicated tab
- **Appointments** — full lifecycle (Pending → Confirmed → Cancelled), linked to a specific time slot, patient contact, and optional medical report
- **Dashboard** — quick-access views for Today's Appointments, Pending Appointments, Confirmed Appointments, and a Revenue Report (graph + pivot)

### Role-Based Access Control (RBAC)
Four distinct roles, enforced via Odoo groups and record rules:
| Role | Access |
|---|---|
| Admin | Full access to all records |
| Doctor | Own appointments and department only |
| Department Manager | Doctors and appointments within their managed department |
| Patient (Portal) | Their own appointments only, via the website |

### Reporting & Automation
- QWeb PDF report for appointment details
- Automated email confirmation on booking (Odoo mail templates)
- Slot state automatically flips between Available / Booked as appointments are created, edited, or cancelled

## Tech Stack
- **Framework:** Odoo 16
- **Backend:** Python, Odoo ORM
- **Frontend:** QWeb templates, Bootstrap 5, JavaScript
- **Database:** PostgreSQL 15
- **Payments:** Razorpay (via Odoo's `payment.provider` / `payment.transaction` framework)

## Module Structure
```
hospital_management/
├── controllers/       # Website routes (doctors, booking, payment flow)
├── models/             # Doctor, Department, Appointment, Doctor Slots
├── views/              # Backend forms/trees/graphs + website templates
├── security/           # Groups, record rules, access rights
├── data/               # Mail templates, demo/report data
├── static/src/css/      # Website styling
├── __manifest__.py
└── __init__.py
```

## Key Design Decisions
- Time slots are modeled as a separate `hospital.doctor.slots` model (not a field on the doctor), allowing multiple bookable slots per doctor per day
- Appointment creation is deferred until payment succeeds — a `payment.transaction` is created first, and the actual `hospital.appoinment` record is only written once payment is confirmed, preventing unpaid "ghost" bookings
- Department → Doctor → Slot selection uses dynamic view-level domains, so each dropdown is filtered live based on the form's current values

## What I Learned Building This
- Designing relational data models (One2many / Many2one) for a real booking system
- Implementing multi-role security with Odoo's group and record rule system
- Debugging Odoo's Website Builder COW (Copy-On-Write) view corruption
- Integrating a third-party payment gateway using Odoo's native payment framework
- Writing QWeb PDF reports and dynamic email templates
- Git version control fundamentals

## Roadmap
- [ ] Bulk time-slot generator wizard (TransientModel)
- [ ] Automatic slot release for abandoned/failed payments (via scheduled `ir.cron` job)
- [ ] Deployment to a live server

## Author
**Muhammed Jabir M T**
[LinkedIn](https://www.linkedin.com/in/muhammed-jabir-m-t-550a50350) · [GitHub](https://github.com/muhammed-jabir)
