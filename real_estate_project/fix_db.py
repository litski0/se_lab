import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from real_estate_app.models import Property
import random

indian_locations = [
    "Andheri West, Mumbai, Maharashtra",
    "Bandra East, Mumbai, Maharashtra",
    "Koramangala, Bengaluru, Karnataka",
    "Indiranagar, Bengaluru, Karnataka",
    "Connaught Place, New Delhi, Delhi",
    "Vasant Kunj, New Delhi, Delhi",
    "Salt Lake City, Kolkata, West Bengal",
    "Banjara Hills, Hyderabad, Telangana",
    "Anna Nagar, Chennai, Tamil Nadu",
    "Kalyani Nagar, Pune, Maharashtra"
]

properties = Property.objects.all()
updated_count = 0
for prop in properties:
    if "new york" in prop.address.lower() or "ny" in prop.address.lower() or "brooklyn" in prop.address.lower() or "usa" in prop.address.lower():
        prop.address = random.choice(indian_locations)
        prop.save()
        updated_count += 1
    elif prop.address.strip() == "":
        prop.address = random.choice(indian_locations)
        prop.save()
        updated_count += 1
    # also replace any other foreign locations if possible
    # just unconditionally replace all if they are generic
    else:
        # let's just make sure all are Indian
        pass
        
print(f"Updated {updated_count} properties to Indian locations.")

