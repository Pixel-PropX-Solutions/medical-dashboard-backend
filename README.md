# Clinova - Functionality Overview

## Project Purpose

**Clinova** is a cloud-based clinic management system designed to streamline operations for healthcare clinics. It enables clinics to manage patients, record medical visits, generate digital receipts and invoices, track financials, and access business analytics—all from a single platform.

The system is built as a **multi-tenant SaaS** (Software-as-a-Service), allowing multiple independent clinics to operate securely within the same application with complete data isolation.

---

## Core User Roles

1. **Super Admin** - Platform administrator who sets up new clinics and manages clinic onboarding
2. **Clinic Admin** - Clinic owner/manager with full access to clinic operations and settings
3. **Clinic Staff** (Doctors, Receptionists) - Staff members who perform daily clinic operations (patient registration, visit recording, etc.)

---

## Key Features & Modules

### 1. **Authentication & Security**

- Secure login system with JWT tokens (JSON Web Tokens)
- Role-based access control (admin vs. clinic users)
- Password reset and account management
- Multi-tenant data isolation using clinic identifiers

### 2. **Clinic Management**

- Clinic onboarding and registration
- Clinic profile management (name, contact info, email)
- Automatic welcome email notification for new clinics
- Logo upload and management through cloud storage
- Self-service clinic settings panel for staff

### 3. **Patient Management**

- **Patient Registration** - Add new patients to the system with basic information (name, phone, gender, age, address, notes)
- **Patient Search** - Quick search by phone number to find existing patients
- **Patient Profiles** - View complete patient information including:
  - Demographics (age, gender, address)
  - Medical notes and allergies
  - Complete visit history
  - First and last visit dates
  - Total number of visits

### 4. **Visit/Appointment Management**

- Record doctor-patient visits with detailed information:
  - Doctor name and notes
  - Diagnosis and disease identification
  - Medical specialization
  - Medicines prescribed
  - Services provided (with pricing)
  - Payment method and fees
- Automatic visit numbering (token numbers)
- Track visit timestamps
- Embedded visit summaries on patient records for quick reference

### 5. **Financial Management**

- **Visit-based Billing** - Each visit generates a bill with itemized services and fees
- **Multiple Payment Methods** - Support for cash, card, and other payment types
- **Receipt Generation** - Automatic receipt numbering for tracking
- **Financial Reporting** - Dashboard analytics showing:
  - Total revenue and income trends
  - Payment method breakdown
  - Average fees per visit

### 6. **Templates & Document Generation**

- **HTML Template Management** - Create and manage custom templates for different document types:
  - Invoices
  - Medical prescriptions/receipts (called "parchi")
  - Visit receipts
- **Global Templates** - Default templates available to all clinics
- **Clinic-Specific Templates** - Custom templates for individual clinic branding
- **Dynamic Content Generation** - Templates can include clinic information, patient details, visit data, and services
- **HTML-to-PDF Rendering** - Convert template-based content to PDF for printing and digital sharing

### 7. **Exports & Reporting**

- **CSV/Excel Exports** - Export patient lists and billing records in standard formats for:
  - External analysis
  - Backup and archival
  - Accountant and regulatory reporting
- **Supports:**
  - Patient data export
  - Visit/billing records export

### 8. **Business Analytics Dashboard**

- **Key Performance Indicators (KPIs):**
  - Total revenue generated
  - Payment method mix (cash vs. card breakdown)
  - Patient demographics overview
  - Visit trends and patterns
- **Data Insights** - Visual analytics to help clinic owners understand their business performance

### 9. **Email Communications**

- Automated welcome emails when new clinics are onboarded
- Password reset email notifications
- Clinic invitation emails for new staff members

---

## Typical Workflow

### Day-to-Day Operations:

1. **Patient Arrival** → Receptionist searches for patient by phone number
2. **New or Existing?**
   - If new: Register patient in the system
   - If existing: Retrieve patient profile
3. **Doctor Visit** → Doctor records visit details:
   - Diagnosis and notes
   - Services provided and fees
   - Medicines prescribed
4. **Bill Generation** → System generates receipt with automatic numbering
5. **Patient History** → Visit is automatically added to patient's record

### Administrative Tasks:

1. **Setup** → Clinic admin creates:
   - Custom PDF templates for clinic branding
   - Default settings (template preferences, clinic logo)
2. **Reporting** → View dashboard analytics or export data for monthly reviews
3. **Account Management** → Update clinic profile, change password, upload logo

---

## Data Entities

### Patient

- Contains personal information (name, age, gender, phone, address)
- Stores medical notes and allergies
- Tracks visit history and dates
- Maintains total visit count

### Visit

- Records details of each clinic visit
- Links patient to visit for medical record keeping
- Captures services provided with pricing
- Stores payment information
- Generates receipt for billing

### Clinic

- Represents a tenant/organization in the system
- Stores clinic information (name, contact, plan type)
- Manages clinic-specific settings and branding

### Template

- HTML-based document templates
- Can be global (available to all clinics) or clinic-specific
- Types: invoices, prescriptions, receipts

### User

- Represents clinic staff or admin
- Attached to a specific clinic
- Has role-based permissions

---

## Key Capabilities

✅ **Multi-clinic Support** - One platform serves multiple clinics with complete data separation  
✅ **Patient History Tracking** - Full medical record retention for continuity of care  
✅ **Financial Transparency** - Detailed revenue tracking and payment method reporting  
✅ **Customizable Branding** - Clinics can create branded invoices and receipts  
✅ **Data Portability** - Export data in standard formats (CSV, Excel)  
✅ **Mobile-Friendly** - Accessible from any device via web interface  
✅ **Secure Access** - Token-based authentication and role-based permissions  
✅ **Scalable** - Cloud-based architecture supports growth

---

## Benefits for Clinic Owners

- **Time Savings** - Reduce manual paperwork and administration
- **Better Organization** - Centralized patient records and visit history
- **Financial Insights** - Real-time dashboard showing revenue and trends
- **Professional Appearance** - Custom branded invoices and receipts
- **Data Backup** - Cloud storage ensures data safety
- **Easy Reporting** - Export data for tax and accounting purposes
- **Compliance Ready** - Organized records for regulatory requirements

---

## Summary

Clinova is a comprehensive clinic management solution that digitizes and streamlines the entire clinic workflow—from patient registration through visit recording, billing, and financial reporting. It combines ease of use with powerful analytics, enabling clinic staff to focus on patient care while the system handles administrative tasks automatically.

---

## Tech Stack

- FastAPI (async API framework)
- Motor (async MongoDB driver)
- Pydantic v2 + pydantic-settings
- JWT auth (python-jose)
- Pandas + OpenPyXL (CSV/XLSX exports)
- Cloudinary (clinic logo uploads)

---

## Features

- Multi-tenant data isolation using `clinic_id`
- Admin and clinic-user authentication/authorization
- Clinic onboarding with optional auto user creation + welcome email
- Patient registration, search, profile, and visit history
- Visit management with embedded visit summaries on patient records
- HTML template management (clinic + global templates)
- HTML content generation endpoint for printing/PDF flows
- Dashboard analytics (revenue, payment mix, demographics)
- CSV/XLSX exports for patients and bills (visits)
- Clinic self-service settings (profile, password, default template, logo)

---

## Project Structure

```text
app/
   auth/         # JWT, dependencies, login/admin/password reset routes
   clinics/      # Clinic CRUD + admin stats + logo upload
   patients/     # Patient create/list/search/profile
   visits/       # Visit create/list/delete
   templates/    # Clinic/admin template management
   pdf/          # Render-ready HTML content from visit/template data
   exports/      # CSV/XLSX exports
   dashboard/    # KPI and analytics APIs
   settings/     # Clinic self-service profile/settings APIs
   utils/        # Logger, email sender, pagination, common query params
```

---

## Requirements

- Python 3.12+
- MongoDB (local or hosted)
- `uv` (recommended) or `pip`

---

## Quick Start

### 1. Install dependencies

Using `uv`:

```bash
uv sync
```

Using `pip`:

```bash
pip install -r requirement.txt
```

### 2. Configure environment

Create a `.env` file in the project root:

```env
PROJECT_NAME=Clinova
API_V1_STR=/api/v1

MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=clinic_saas_db

SECRET_KEY=replace-with-a-strong-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Optional: Cloudinary (logo uploads)
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# Optional: SMTP (forgot-password + onboarding email)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
```

If SMTP credentials are not set, email sending falls back to console output.

### 3. Run the app

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Alternative:

```bash
python start.py
```

API docs:

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health: `http://localhost:8000/health`

---

## Authentication and Roles

- Roles:
  - `admin`: manage clinics and admin template operations
  - `clinic_user`: clinic operations (patients, visits, templates, dashboard, exports, settings)
- Tokens are returned from login endpoints and also set as HTTP-only cookies.
- Authorization header format: `Authorization: Bearer <access_token>`

Bootstrap admin user:

1. Call `POST /api/v1/auth/create-admin` with email/password.
2. Login with `POST /api/v1/auth/login` or `POST /api/v1/auth/token`.

---

## API Summary

All routes are prefixed by `/api/v1`.

### Auth (`/auth`)

- `POST /token` - OAuth2-style login
- `POST /login` - JSON login
- `POST /refresh` - refresh access token
- `POST /logout` - clear cookies
- `POST /create-admin` - create initial admin user
- `POST /forgot-password` - reset password + send temporary credentials

### Clinics (`/clinics`) - admin

- `POST /` - create clinic (optionally creates clinic user from clinic email)
- `GET /` - list clinics
- `PATCH /{clinic_id}` - update clinic
- `GET /{clinic_id}/stats` - clinic-level usage/revenue metrics
- `POST /{clinic_id}/upload-logo` - upload clinic logo

### Patients (`/patients`) - clinic/admin

- `POST /` - create patient
- `GET /` - paginated list
- `GET /search?phone=...` - phone search
- `GET /{id}` - get patient by id
- `GET /{id}/profile` - patient + visit timeline + total fees

### Visits (`/visits`) - clinic/admin

- `POST /` - create visit
- `GET /{patient_id}` - list visits for patient
- `DELETE /{visit_id}` - delete visit and sync patient summary fields

### Templates (`/templates`) - clinic/admin

- Clinic routes:
  - `POST /`
  - `GET /` (clinic templates + global templates)
  - `PATCH /{id}`
  - `DELETE /{id}`
- Admin routes:
  - `POST /admin`
  - `GET /admin`
  - `PATCH /admin/{id}`
  - `DELETE /admin/{id}`

### PDF Content (`/pdf`) - clinic/admin

- `GET /content/{visit_id}/{template_id}`

Returns template HTML with placeholders replaced from patient/visit/clinic data.
`template_id` can be `default` to use clinic default template.

### Dashboard (`/dashboard`) - clinic/admin

- `GET /stats` - summary metrics, payment breakdown, monthly and daily revenue, demographics

Supports optional query params: `start_date`, `end_date`.

### Exports (`/export`) - clinic/admin

- `GET /patients?format=csv|xlsx`
- `GET /bills?format=csv|xlsx`

Supports optional query params: `start_date`, `end_date`.

### Settings (`/settings`) - clinic/admin

- `GET /profile`
- `PATCH /profile`
- `POST /upload-logo`
- `POST /change-password`
- `POST /default-template`

---

## Template Placeholders

The PDF content endpoint supports placeholders in `${var}` and `{{var}}` styles.

| Placeholder                          | Meaning                   |
| ------------------------------------ | ------------------------- |
| `${name}`                            | Patient name              |
| `${phone}`, `${mobile}`              | Phone number              |
| `${age}`                             | Age                       |
| `${gender}`, `${sex}`                | Gender                    |
| `${address}`                         | Address                   |
| `${fees}`                            | Visit fees                |
| `${dr_name}`                         | Doctor name               |
| `${disease}`                         | Disease                   |
| `${diagnosis}`                       | Diagnosis                 |
| `${specialization}`, `${speciality}` | Specialization            |
| `${payment_method}`                  | Payment method            |
| `${date}`                            | Visit date                |
| `${time}`                            | Visit time                |
| `${datetime}`                        | Full datetime             |
| `${medicines}`                       | Comma-separated medicines |
| `${clinic_name}`                     | Clinic name               |
| `${clinic_phone}`                    | Clinic phone              |
| `${clinic_email}`                    | Clinic email              |
| `${clinic_logo}`                     | Clinic logo URL           |
| `${clinic_address}`                  | Clinic address            |

---

## Notes for Production

- Replace `SECRET_KEY` with a strong secret.
- Consider moving from SHA-256 password hashing to bcrypt/argon2.
- Review CORS origins in `app/main.py` to match your frontend domains.
- Ensure MongoDB backups and index monitoring are configured.

---

## Deployment

The repository includes `vercel.json` for Vercel Python runtime.

Important:

- Keep Python version at 3.12+ (see `pyproject.toml`).
- Ensure `pyproject.toml` remains valid for `uv` parsing in CI/CD.
