# Online Real Estate Management System MVP - Complete Codebase Breakdown

This document provides a complete, authoritative, from-first-principles explanation of every single file, feature, and logic block written in this project. You can use this directly to explain the architecture to your professor.

---

## 1. Project Configuration & App Registration
### `core/settings.py`
This is the master configuration file for the Django project. 
*   **`INSTALLED_APPS`:** We registered our custom app `real_estate_app` here so Django knows its models and views exist. We also added `sass_processor` to allow us to compile `.scss` styling files into CSS dynamically.
*   **`DATABASES`:** Configured to use SQLite3 (`db.sqlite3`) for local development, allowing us to store all users, properties, and bookings without needing a separate database server.
*   **`AUTH_USER_MODEL = 'real_estate_app.User'`:** This is a crucial override. We told Django *not* to use its built-in User model, and instead use the Custom User model we built in our app.

### `core/urls.py`
This is the master router for the whole site. It links web addresses (like `127.0.0.1:8000/admin/`) to specific Python functions. 
*   It includes built-in Django paths for the Admin panel.
*   It delegates all other routing down to our app's specific URL file: `path('', include('real_estate_app.urls'))`.

---

## 2. The Database Schema (Models)
**File: `real_estate_app/models.py`**
This file defines the literal tables in our SQLite database using object-oriented Python.

### Feature: Role-Based Access Control (RBAC) User System
*   **`class User(AbstractUser)`:** We inherited Django's authentication system but expanded it. 
*   **Role Flags:** We added boolean (True/False) fields for `is_admin`, `is_owner`, and `is_seeker`. This allows us to strictly control who can see what dashboard.
*   **Additional Data:** Implemented Regex-validated fields for `phone_number` and `pincode` to ensure data integrity.

### Feature: Property Listing Engine
*   **`class Property(models.Model)`:** This stores all real estate listings.
*   **Relational Database Mapping:** We use a `ForeignKey` to link every Property entry to a specific `User` (the Owner). If the Owner is deleted, `on_delete=models.CASCADE` ensures their properties are also deleted to prevent abandoned data.
*   **State Machine:** The `status` field is restricted by `STATUS_CHOICES` (Pending, Live, Booked). New properties default to 'Pending'.

### Feature: Booking Architecture
*   **`class Booking(models.Model)`:** The junction table connecting a Seeker and a Property.
*   It stores timeline data (`start_date`, `duration_months`), financial data (`total_amount`), and tracks whether the transaction completed via `payment_status`.

---

## 3. Data Validation Interface (Forms)
**File: `real_estate_app/forms.py`**
Forms act as the security layer between the user's HTML inputs and our database.

*   **`CustomUserCreationForm`:** Overrides Django's default signup form. We explicitly tell it to use our custom `User` model, and we require the user to input their `email` and select their Role (Owner vs Seeker) upon registration.
*   **`PropertyForm`:** Generates the secure HTML inputs for Owners to add properties. We purposely exclude the `owner` and `status` fields from this form so users can't hack the form to assign the property to someone else or bypass the 'Pending' status.
*   **`BookingForm`:** Collects the `start_date` and `duration_months` from Seekers when they try to reserve a 'Live' property.

---

## 4. The Business Logic & Controllers (Views)
**File: `real_estate_app/views.py`**
This is the "brain" of the application. It receives an HTTP Request, processes business logic, and returns an HTTP Response (usually an HTML template). Every view except the register page uses the `@login_required` decorator to protect the routes.

### Feature: Dynamic Role Routing
*   **`def dashboard(request):`** Instead of having 3 separate URLs for 3 different dashboards, this single function checks `request.user.is_owner`, `request.user.is_seeker`, or `is_admin`. Depending on who is logged in, it queries the DB for different data (e.g., retrieving only *their* properties) and renders entirely different HTML templates.

### Feature: User Registration
*   **`def register(request):`** Validates the `CustomUserCreationForm` via a POST request. If the data is clean, it saves the new user to the database and automatically logs them in using Django's `login()` function.

### Feature: Creating Properties
*   **`def add_property(request):`** First, it verifies the user is actually an Owner. If a POST request is received, it validates the `PropertyForm`. Before saving to the database, it intercepts the save process (`commit=False`), attaches the currently logged-in user as the `property.owner`, forces the status to 'Pending', and then saves it.

### Feature: Searchable Property Catalog
*   **`def property_catalog(request):`** Restricted to Seekers. It executes a database query: `Property.objects.filter(status='Live')`.
*   **Search Filters:** It looks into the URL parameters (`request.GET.get`). If the user searched for an address or maximum price, it dynamically appends those filters (`icontains` for partial address matching, `lte` for Less-Than-or-Equal price matching) to the SQL query.

### Feature: The Booking & Mock Payment Flow
*   **`def book_property(request, property_id):`** First ensures the property stringently exists and is 'Live' via `get_object_or_404`. It calculates the financial obligation (`total_amount = (rent * duration) + deposit`).
*   **`MockPaymentService`:** A dummy structural class meant to simulate calling Stripe/Razorpay. If it returns True, the view changes the Property status to 'Booked', saves the new Booking receipt to the database, and redirects the user.

### Feature: Admin Verification
*   **`def approve_property(request, property_id):`** A simple administrative endpoint that locates a 'Pending' property by its ID and flips its status to 'Live'.

---

## 5. The User Interface (Templates)
**Folder: `templates/` and `templates/real_estate_app/`**
We utilize the Django Templating Language (DTL) to seamlessly inject Python variables straight into the HTML structure.

### The Master Layout
*   **`base.html`:** The foundational skeleton of the app. It imports the Bootstrap CSS framework. It contains the overarching Navigation bar, which uses DTL `{% if %}` statements to dynamically show or hide links (like 'Add Property' vs 'Catalog') based on the logged-in user's role. It defines a `{% block content %}` where child templates inject their specific HTML.

### The Child Views
*   **`owner_dashboard.html` / `admin_dashboard.html` / `seeker_dashboard.html`:** These templates `{% extends 'base.html' %}`. They use DTL `{% for %}` loops to iterate over datasets passed by `views.py` (like the QuerySet of properties) to generate HTML tables or cards dynamically.
*   **`add_property.html` / `book_property.html`:** These templates render the Django Forms (`{{ form.as_p }}`) and wrap them in a secure `method="post"` HTML form utilizing a `{% csrf_token %}` to prevent Cross-Site Request Forgery hacking attempts.
