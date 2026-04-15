from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, PropertyForm, BookingForm
from .models import Property, Booking

class MockPaymentService:
    @staticmethod
    def processTransaction(amount):
        # Mock payment processing
        return True

def home(request):
    # Public landing page / web
    # site
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'real_estate_app/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_admin or request.user.is_superuser:
        properties = Property.objects.all().order_by('-property_id')
        return render(request, 'real_estate_app/admin_dashboard.html', {'properties': properties})
    elif request.user.is_owner:
        properties = Property.objects.filter(owner=request.user).order_by('-property_id')
        return render(request, 'real_estate_app/owner_dashboard.html', {'properties': properties})
    elif request.user.is_seeker:
        bookings = Booking.objects.filter(seeker=request.user)
        return render(request, 'real_estate_app/seeker_dashboard.html', {'bookings': bookings})
    else:
        return render(request, 'real_estate_app/dashboard.html')

@login_required
def add_property(request):
    if not request.user.is_owner:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.status = 'Pending'
            
            files = request.FILES.getlist('property_photos')
            if files:
                property.photo = files[0]
                
            property.save()
            # Save gallery images
            from .models import PropertyImage
            if len(files) > 1:
                for f in files[1:]:
                    PropertyImage.objects.create(property=property, image=f)

            messages.success(request, 'Property listed successfully and is pending approval.')
            return redirect('dashboard')
    else:
        form = PropertyForm()
    return render(request, 'real_estate_app/add_property.html', {'form': form})

@login_required
def property_catalog(request):
    if not request.user.is_seeker:
        return redirect('dashboard')
        
    properties = Property.objects.filter(status='Live')
    
    # Filtering
    address_query = request.GET.get('address')
    max_price = request.GET.get('max_price')
    
    if address_query:
        properties = properties.filter(address__icontains=address_query)
    if max_price:
        properties = properties.filter(price__lte=max_price)
        
    return render(request, 'real_estate_app/property_catalog.html', {'properties': properties})

@login_required
def book_property(request, property_id):
    if not request.user.is_seeker:
        return redirect('dashboard')
        
    property_obj = get_object_or_404(Property, property_id=property_id, status='Live')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            duration = booking.duration_months
            # Total amount = (First month rent + deposit) * duration? No.
            # "System calculates the total amount (first month rent + deposit)." Usually deposit = 1 month rent. Let's assume deposit is 1 month rent.
            # So total_amount = (property_obj.price * duration) + property_obj.price (deposit). Let's assume deposit = 1 month rent.
            deposit = property_obj.price
            total_amount = (property_obj.price * duration) + deposit
            
            # Initiate payment
            payment_success = MockPaymentService.processTransaction(total_amount)
            
            if payment_success:
                property_obj.status = 'Booked'
                property_obj.save()
                
                booking.property = property_obj
                booking.seeker = request.user
                booking.total_amount = total_amount
                booking.payment_status = 'Paid'
                booking.save()
                
                messages.success(request, f'Booking successful! Amount paid: {total_amount}')
                return redirect('dashboard')
            else:
                messages.error(request, 'Payment failed. Please try again.')
    else:
        form = BookingForm()
        
    return render(request, 'real_estate_app/book_property.html', {
        'form': form, 
        'property': property_obj
    })

@login_required
def admin_property_detail(request, property_id):
    if not (request.user.is_admin or request.user.is_superuser):
        return redirect('dashboard')
        
    property_obj = get_object_or_404(Property, property_id=property_id)
    return render(request, 'real_estate_app/admin_property_detail.html', {'property': property_obj})

@login_required
def owner_property_detail(request, property_id):
    if not request.user.is_owner:
        return redirect('dashboard')
        
    property_obj = get_object_or_404(Property, property_id=property_id, owner=request.user)
    return render(request, 'real_estate_app/owner_property_detail.html', {'property': property_obj})

@login_required
def seeker_property_detail(request, property_id):
    if not request.user.is_seeker:
        return redirect('dashboard')
        
    property_obj = get_object_or_404(Property, property_id=property_id)
    form = BookingForm()
    
    if request.method == 'POST' and property_obj.status == 'Live':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            duration = booking.duration_months
            deposit = property_obj.price
            total_amount = (property_obj.price * duration) + deposit
            
            # Register pending checkout
            booking.property = property_obj
            booking.seeker = request.user
            booking.total_amount = total_amount
            booking.payment_status = 'Pending'
            booking.save()
            
            return redirect('mock_payment', booking_id=booking.booking_id)
                
    return render(request, 'real_estate_app/seeker_property_detail.html', {'property': property_obj, 'form': form})

@login_required
def approve_property(request, property_id):
    if not (request.user.is_admin or request.user.is_superuser):
        return redirect('dashboard')
        
    property_obj = get_object_or_404(Property, property_id=property_id)
    property_obj.status = 'Live'
    property_obj.save()
    messages.success(request, 'Property approved and is now Live.')
    return redirect('dashboard')

@login_required
def reject_property(request, property_id):
    if not (request.user.is_admin or request.user.is_superuser):
        return redirect('dashboard')
        
    property_obj = get_object_or_404(Property, property_id=property_id)
    property_obj.status = 'Rejected'
    property_obj.save()
    messages.success(request, 'Property rejected.')
    return redirect('dashboard')

@login_required
def mock_payment(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, seeker=request.user)
    
    if booking.payment_status == 'Paid':
        return redirect('dashboard')
        
    property_obj = booking.property
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'pay':
            payment_success = MockPaymentService.processTransaction(booking.total_amount)
            if payment_success:
                property_obj.status = 'Booked'
                property_obj.save()
                
                booking.payment_status = 'Paid'
                booking.save()
                
                messages.success(request, f'Payment via Razorpay Mockup successful! Amount paid: ₹{booking.total_amount}')
                return redirect('dashboard')
            else:
                messages.error(request, 'Payment failed during processing.')
        elif action == 'cancel':
            messages.info(request, 'Payment transaction cancelled.')
            return redirect('seeker_property_detail', property_id=property_obj.property_id)
            
    return render(request, 'real_estate_app/payment_mockup.html', {'booking': booking})
