# User Manual: Real Estate Management Platform

Welcome to the Real Estate Management Platform! This system connects Property Owners directly with prospective Seekers, while leaving robust administrative controls to verify security. 

Due to our Role-Based Access structure, the features you see will be strictly tailored to whether you are a **Seeker**, an **Owner**, or an **Admin**.

---

## 1. Quick Start (How to Run Locally)

If you are setting this up for a demonstration or testing, run the following commands in your terminal to start the local web server:

```bash
# Navigate to the project directory
cd c:\Users\kavya\se_lab\se_lab\real_estate_project

# Make sure all database migrations are applied
python manage.py migrate

# Start the server!
python manage.py runserver
```
Once it says "Starting development server," open your web browser and navigate to `http://127.0.0.1:8000/`.

---

## 2. Seeker's Guide (Looking for a Property)

As a Seeker, your goal is to locate, inspect, and safely reserve real estate properties.

**Step 1: Registration**
1. Click **Register** on the top navigation bar.
2. Fill out your details. Look at the checkboxes under "Account Type" and purposely select **Is Seeker**. 
3. Click register. You will be automatically logged in and dropped onto your Dashboard.

**Step 2: Browsing the Catalog**
1. Click **Catalog** on the navigation bar. This shows you every property currently *Approved* and available for rent.
2. Use the search bars at the top to filter by precise location or Maximum budget.
3. If a property looks appealing, click the prominent **View Details** button.

**Step 3: Inspecting a Property**
1. **The Gallery:** On the left side of the screen, you can click through large photograph carousels representing the property. 
2. **The Map:** Scroll down slightly to interact with the Live Neighborhood map. You can drag and zoom to check the exact geographical area.
3. **The Owner:** On the right, you will see a profile card with the Owner's Name and Phone number if you wish to contact them before proceeding.

**Step 4: Checking Out**
1. Underneath the Owner card, you will find the **Book This Property** panel.
2. Select your `Start Date`.
3. Input your desired lease duration (in months). The **Price Breakdown** module will instantly calculate your Security Deposit and total amount payable.
4. Click **Confirm Booking**.
5. You will be redirected to the secure **Razorpay Mock Checkout** screen. Review the mock details, hit *Pay*, and you're done! The property is yours.

---

## 3. Owner's Guide (Listing a Property)

As an Owner, your goal is to upload beautiful listings quickly, and verify who is renting them.

**Step 1: Registration**
1. Click **Register** on the top bar. Fill out your info, and check the box that says **Is Owner**. 

**Step 2: Adding a New Property**
1. Click **Add Property** on the top navigation bar.
2. Input the monthly Rent.
3. **Map Tool:** Do not manually type your address unless you want to! Simply look at the map, drag the blue marker exactly to your building, and watch the Address field intelligently populate itself using GPS. (Alternatively, start typing an address and the map pin will jump there).
4. **Photo Uploads:** Click the "Property Photos" button. You can highlight and select as many photos from your computer as you want at the exact same time. The first photo will mechanically become your thumbnail.
5. Hit Submit.
*Note: Your property will be flagged as **Pending**. It will not appear in the Seeker Catalog until an Admin approves it.*

**Step 3: Managing your Properties**
1. Go to your **Dashboard**.
2. Click **View Details** on any listing.
3. If your property's status says **Booked**, you will unlock a brand new section on the right side of the screen revealing exactly what Seeker booked it, along with their confidential contact details so you can prepare the physical lease!

---

## 4. Administrator Guide (System Overwatch)

As an Admin, your goal is to eliminate spam/fake listings and oversee transactions. 

**Step 1: Accessing the System**
Admins are "Superusers" created in the backend. 
1. Log in. You will immediately be brought to the Master Admin Dashboard. 

**Step 2: Moderating Listings**
Your dashboard is a clean table showcasing every single property submitted by Owners, regardless of status.
1. Find a property labeled **Pending** and click **View Details**.
2. You will be given the exact same immersive experience as Seekers (large maps, robust photo galleries).
3. If it looks legitimate, click the green **Approve** button at the bottom of the Owner Profile Panel. The property will instantly become Live and hit the public catalog.
4. If it looks like spam, click the red **Reject** button. 
*(Note: If a property gets Booked, you can use this same dashboard to review exactly which Seeker rented it).*
