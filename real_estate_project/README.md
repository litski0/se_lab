# Online Real Estate Management System MVP - Complete Codebase Breakdown

This document provides a complete, authoritative explanation of every single file, feature, and logic block written in this project. You can use this directly to explain the architecture to your professor.

---

## 1. Project Configuration & App Registration
### `core/settings.py`
This is the master configuration file for the Django project. 
*   **`INSTALLED_APPS`:** We registered our custom app `real_estate_app` here so Django knows its models and views exist.
*   **`DATABASES`:** Configured to use SQLite3 (`db.sqlite3`) for local development, allowing us to store all users, properties, and bookings statically.
*   **`AUTH_USER_MODEL = 'real_estate_app.User'`:** We overrode the Django default to strictly utilize the Custom User model we built. 

### `core/urls.py`
This is the master router for the whole site. It routes `/admin/` inherently and delegates all standard paths down to our app's specific URL configuration: `path('', include('real_estate_app.urls'))`.

---

## 2. The Database Schema (Models)
**File: `real_estate_app/models.py`**
This file defines the literal tables in our SQLite database using object-oriented Python.

### Feature: Role-Based Access Control (RBAC) User System
*   **`class User(AbstractUser)`:** We inherited Django's authentication system but expanded it. 
*   **Role Flags:** We added boolean (True/False) fields for `is_admin`, `is_owner`, and `is_seeker`. This allows us to strictly control who can see what dashboard.

### Feature: Multi-Image Property System
*   **`class Property(models.Model)`:** This stores all core real estate specs (Address, Price, Status). It is linked directly to an Owner via `ForeignKey`. It uses geographical coordinates (`latitude` and `longitude`) to map its location.
*   **`class PropertyImage(models.Model)`:** Connected to the parent Property with a Foreign Key. This enables an unlimited 1-to-many relationship allowing property carousels to hold infinite supplemental photos.

### Feature: Booking Architecture
*   **`class Booking(models.Model)`:** The junction table connecting a Seeker and a Property.
*   It stores timeline data, precise financial aggregates (`total_amount`), and tracks whether the transaction completed via `payment_status`.

---

## 3. Data Validation Interface (Forms)
**File: `real_estate_app/forms.py`**

*   **`CustomUserCreationForm`:** Overrides Django's default signup form. We require the user to input their `email` and strictly select their Role upon registration.
*   **`PropertyForm`:** Generates the secure HTML inputs for Owners to add properties. Features backend validation via `clean_price` blocking illicit entries. It utilizes a custom Python file widget `MultipleFileField` to intercept standard HTML5 multi-file inputs seamlessly.
*   **`BookingForm`:** Collects the `duration_months` from Seekers. Protected by strict backend logic prohibiting inputs underneath 1 Month via `clean_duration_months`.

---

## 4. The Business Logic & Controllers (Views)
**File: `real_estate_app/views.py`**
This is the "brain" of the application. Every standard user route is protected by `@login_required`.

### Feature: UI Detailing & Parity
*   Instead of cluttered dashboards, the app routes users (Admin, Owner, Seeker) to dedicated `_property_detail` views containing massive, full-screen map integrations and image carousels while hiding conditionally sensitive data based on session roles.

### Feature: Adding Properties & Map Synchronization
*   **`def add_property(request)`:** Verifies Owner permissions. Before committing to the database, it natively cycles through the array of `MultipleFileField` request images, assigns the first as the Primary Thumbnail, and creates trailing gallery loops out of the rest.

### Feature: Seeker Catalog & Dynamic Payment Breakdown
*   **`seeker_property_detail`:** Allows precise checkout operations directly from the view. Natively syncs javascript EventListeners to calculate the Deposit and multiplying Rent outputs into an aggregate Checkout Total before finalizing the form data.

### Feature: Razorpay Sandbox Integration
*   The checkout process halts immediately after standard booking. Django initiates a `Pending` state and dynamically reroutes the transaction payload directly to `views.mock_payment()`. 
*   Here, an immersive standalone URL acts as a mockup for a Razorpay integration, demanding specific UI resolution to simulate a standard E-commerce pipeline rather than executing simple instant bookings.

---

## 5. The User Interface (Templates)
**Folder: `templates/` and `templates/real_estate_app/`**
We utilize standard HTML5 mapped deeply with the latest Bootstrap library.

### OpenStreetMap & Leaflet Integration
*   Templates requiring Address validation utilize custom CDN calls to Leaflet JS, mounting interactive dynamic world maps inside HTML containers. 
*   **Reverse Geocoding**: Owners dragging the map pin trigger `nominatim` API callbacks to automatically populate the exact typed Address into the backend form blocks.
*   **Forward Geocoding**: Typing physical locales automatically moves the marker. 

### The Razorpay Environment
*   **`payment_mockup.html`:** The app steps entirely away from the generic navigation styling to deploy a targeted, pure-CSS simulated Razorpay Checkout frame highlighting security badges, fake test cards, and confirmation variables rendered seamlessly over the DTL (Django Template Language) engine.

---

## 6. End-to-End Testing Environment
**File: `real_estate_app/tests.py`**
*   Built using `django.test.TestCase` arrays.
*   Configured to aggressively assert 10 distinct failure tests simulating bad model data (`negative rents`), unauthenticated routing attempts, standard checkout resolutions, and mocking out the `admin` approval pipelines to continuously authenticate code durability.
