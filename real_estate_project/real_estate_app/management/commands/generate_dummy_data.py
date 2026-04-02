import random
from django.core.management.base import BaseCommand
from real_estate_app.models import User, Property

class Command(BaseCommand):
    help = 'Populates the database with fake owners, seekers, and properties'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating fake data...')

        # Create Owners
        owners = []
        for i in range(1, 6):
            username = f'owner{i}'
            if not User.objects.filter(username=username).exists():
                owner = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123',
                    is_owner=True,
                    phone_number=f'987654321{i}',
                    pincode=f'11000{i}'
                )
                owners.append(owner)
                self.stdout.write(f'Created owner: {username}')
            else:
                owners.append(User.objects.get(username=username))

        # Create Seekers
        seekers = []
        for i in range(1, 6):
            username = f'seeker{i}'
            if not User.objects.filter(username=username).exists():
                seeker = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123',
                    is_seeker=True,
                    phone_number=f'987654322{i}',
                    pincode=f'22000{i}'
                )
                seekers.append(seeker)
                self.stdout.write(f'Created seeker: {username}')

        # Create Properties
        property_types = ['Apartment', 'House', 'Commercial']
        locations = ['Downtown', 'Suburbs', 'Uptown', 'Westside', 'Eastside']
        
        if Property.objects.count() < 15:
            for i in range(1, 16):
                owner = random.choice(owners)
                prop_type = random.choice(property_types)
                location = random.choice(locations)
                
                status_choices = ['Pending', 'Live', 'Booked']
                status = random.choice(status_choices)
                
                Property.objects.create(
                    owner=owner,
                    address=f'{random.randint(100, 999)} {location} Street, NY {random.randint(10000, 99999)} - {prop_type}',
                    price=random.randint(1000, 5000) if prop_type == 'Apartment' else random.randint(3000, 10000),
                    status=status
                )
            self.stdout.write(f'Created 15 properties')

        self.stdout.write(self.style.SUCCESS('Fake data generation complete!'))
