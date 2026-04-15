from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta
from .models import User, Property, Booking, PropertyImage
from .forms import PropertyForm, BookingForm

class CustomUserModelTest(TestCase):
    def test_create_owner(self):
        owner = User.objects.create_user(username='owner1', password='password@123', is_owner=True)
        self.assertTrue(owner.is_owner)
        self.assertFalse(owner.is_seeker)

    def test_create_seeker(self):
        seeker = User.objects.create_user(username='seeker1', password='password@123', is_seeker=True)
        self.assertTrue(seeker.is_seeker)
        self.assertFalse(seeker.is_owner)

class FormValidationTests(TestCase):
    def test_property_form_negative_price_invalid(self):
        form_data = {
            'address': '123 Valid St',
            'latitude': 20.0,
            'longitude': 78.0,
            'price': -500
        }
        form = PropertyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_property_form_zero_price_invalid(self):
        form_data = {
            'address': '123 Valid St',
            'latitude': 20.0,
            'longitude': 78.0,
            'price': 0
        }
        form = PropertyForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_booking_form_negative_duration_invalid(self):
        form_data = {
            'start_date': date.today() + timedelta(days=1),
            'duration_months': -2
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('duration_months', form.errors)

class ViewRoutingAndLogicTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='adminboss', password='password@123')
        self.owner_user = User.objects.create_user(username='ownerjoe', password='password@123', is_owner=True)
        self.seeker_user = User.objects.create_user(username='seekerjane', password='password@123', is_seeker=True)

        self.property = Property.objects.create(
            owner=self.owner_user,
            address='456 Main St',
            latitude=28.7,
            longitude=77.2,
            price=15000,
            status='Live'
        )

    def test_unauthenticated_dashboard_access_redirects(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_add_property_view_enforces_owner_role(self):
        self.client.login(username='seekerjane', password='password@123')
        response = self.client.get(reverse('add_property'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_admin_approve_flow(self):
        self.property.status = 'Pending'
        self.property.save()
        
        self.client.login(username='adminboss', password='password@123')
        response = self.client.post(reverse('approve_property', args=[self.property.property_id]))
        
        self.property.refresh_from_db()
        self.assertEqual(self.property.status, 'Live')

    def test_seeker_booking_creates_pending_payment(self):
        self.client.login(username='seekerjane', password='password@123')
        form_data = {
            'start_date': date.today() + timedelta(days=5),
            'duration_months': 3
        }
        response = self.client.post(reverse('seeker_property_detail', args=[self.property.property_id]), data=form_data)
        
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.total_amount, 60000)
        self.assertEqual(booking.payment_status, 'Pending')
        self.assertEqual(self.property.status, 'Live')
        self.assertRedirects(response, reverse('mock_payment', args=[booking.booking_id]))

    def test_razorpay_mockup_completes_booking(self):
        booking = Booking.objects.create(
            property=self.property,
            seeker=self.seeker_user,
            start_date=date.today(),
            duration_months=3,
            total_amount=60000,
            payment_status='Pending'
        )
        self.client.login(username='seekerjane', password='password@123')
        
        response = self.client.post(reverse('mock_payment', args=[booking.booking_id]), data={'action': 'pay'})
        
        booking.refresh_from_db()
        self.property.refresh_from_db()
        
        self.assertEqual(booking.payment_status, 'Paid')
        self.assertEqual(self.property.status, 'Booked')
        self.assertRedirects(response, reverse('dashboard'))
