from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Category, Service
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        # Create a service provider user
        provider, _ = User.objects.get_or_create(
            username='provider@example.com',
            email='provider@example.com',
            defaults={
                'first_name': 'John',
                'last_name': 'Doe',
                'is_active': True
            }
        )
        provider.set_password('password123')
        provider.save()

        # Create categories
        categories_data = [
            {
                'name': 'Home Cleaning',
                'description': 'Professional home cleaning services',
                'icon': 'fa-broom'
            },
            {
                'name': 'Plumbing',
                'description': 'Expert plumbing services and repairs',
                'icon': 'fa-wrench'
            },
            {
                'name': 'Electrical',
                'description': 'Electrical installation and maintenance',
                'icon': 'fa-bolt'
            },
            {
                'name': 'Gardening',
                'description': 'Garden maintenance and landscaping',
                'icon': 'fa-leaf'
            },
            {
                'name': 'Painting',
                'description': 'Interior and exterior painting services',
                'icon': 'fa-paint-roller'
            },
            {
                'name': 'Moving',
                'description': 'Professional moving and packing services',
                'icon': 'fa-truck'
            }
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create services
        services_data = [
            {
                'category_name': 'Home Cleaning',
                'services': [
                    {
                        'title': 'Regular House Cleaning',
                        'description': 'Complete house cleaning service including dusting, vacuuming, and mopping',
                        'price': Decimal('80.00'),
                        'is_featured': True
                    },
                    {
                        'title': 'Deep Cleaning',
                        'description': 'Thorough deep cleaning of all areas including hard to reach spaces',
                        'price': Decimal('150.00'),
                        'is_featured': True
                    },
                    {
                        'title': 'Window Cleaning',
                        'description': 'Professional window cleaning service for both interior and exterior',
                        'price': Decimal('60.00'),
                        'is_featured': False
                    },
                    {
                        'title': 'Carpet Cleaning',
                        'description': 'Deep carpet cleaning and stain removal service',
                        'price': Decimal('120.00'),
                        'is_featured': False
                    }
                ]
            },
            {
                'category_name': 'Plumbing',
                'services': [
                    {
                        'title': 'Pipe Repair',
                        'description': 'Fix leaky pipes and repair plumbing issues',
                        'price': Decimal('100.00'),
                        'is_featured': True
                    },
                    {
                        'title': 'Drain Cleaning',
                        'description': 'Professional drain cleaning and unclogging service',
                        'price': Decimal('75.00'),
                        'is_featured': False
                    },
                    {
                        'title': 'Water Heater Installation',
                        'description': 'Install and repair water heaters of all types',
                        'price': Decimal('200.00'),
                        'is_featured': True
                    },
                    {
                        'title': 'Bathroom Remodeling',
                        'description': 'Complete bathroom plumbing and fixture installation',
                        'price': Decimal('300.00'),
                        'is_featured': False
                    }
                ]
            },
            {
                'category_name': 'Electrical',
                'services': [
                    {
                        'title': 'Electrical Repair',
                        'description': 'Fix electrical issues and wiring problems',
                        'price': Decimal('120.00'),
                        'is_featured': True
                    },
                    {
                        'title': 'Light Installation',
                        'description': 'Install new light fixtures and ceiling fans',
                        'price': Decimal('90.00'),
                        'is_featured': False
                    },
                    {
                        'title': 'Circuit Breaker Installation',
                        'description': 'Install and repair circuit breakers and panels',
                        'price': Decimal('150.00'),
                        'is_featured': True
                    },
                    {
                        'title': 'Smart Home Setup',
                        'description': 'Install and configure smart home devices and systems',
                        'price': Decimal('250.00'),
                        'is_featured': False
                    }
                ]
            },
            {
                'category_name': 'Gardening',
                'services': [
                    {
                        'title': 'Lawn Maintenance',
                        'description': 'Regular lawn mowing and maintenance',
                        'price': Decimal('60.00'),
                        'is_featured': True
                    },
                    {
                        'title': 'Garden Design',
                        'description': 'Professional garden design and landscaping',
                        'price': Decimal('200.00'),
                        'is_featured': True
                    },
                    {
                        'title': 'Tree Trimming',
                        'description': 'Professional tree trimming and pruning service',
                        'price': Decimal('150.00'),
                        'is_featured': False
                    },
                    {
                        'title': 'Plant Installation',
                        'description': 'Install and maintain new plants and flowers',
                        'price': Decimal('100.00'),
                        'is_featured': False
                    }
                ]
            },
            {
                'category_name': 'Painting',
                'services': [
                    {
                        'title': 'Interior Painting',
                        'description': 'Professional interior painting service',
                        'price': Decimal('200.00'),
                        'is_featured': True
                    },
                    {
                        'title': 'Exterior Painting',
                        'description': 'Professional exterior painting service',
                        'price': Decimal('300.00'),
                        'is_featured': True
                    },
                    {
                        'title': 'Wallpaper Installation',
                        'description': 'Professional wallpaper installation and removal',
                        'price': Decimal('150.00'),
                        'is_featured': False
                    },
                    {
                        'title': 'Decorative Painting',
                        'description': 'Specialty decorative painting and finishes',
                        'price': Decimal('250.00'),
                        'is_featured': False
                    }
                ]
            },
            {
                'category_name': 'Moving',
                'services': [
                    {
                        'title': 'Local Moving',
                        'description': 'Complete local moving service',
                        'price': Decimal('300.00'),
                        'is_featured': True
                    },
                    {
                        'title': 'Packing Service',
                        'description': 'Professional packing and unpacking service',
                        'price': Decimal('200.00'),
                        'is_featured': True
                    },
                    {
                        'title': 'Furniture Assembly',
                        'description': 'Professional furniture assembly and disassembly',
                        'price': Decimal('100.00'),
                        'is_featured': False
                    },
                    {
                        'title': 'Storage Solutions',
                        'description': 'Temporary storage and organization solutions',
                        'price': Decimal('150.00'),
                        'is_featured': False
                    }
                ]
            }
        ]

        for service_group in services_data:
            category = Category.objects.get(name=service_group['category_name'])
            for service_data in service_group['services']:
                service, created = Service.objects.get_or_create(
                    title=service_data['title'],
                    defaults={
                        'description': service_data['description'],
                        'price': service_data['price'],
                        'category': category,
                        'provider': provider,
                        'is_featured': service_data['is_featured']
                    }
                )
                if created:
                    self.stdout.write(f'Created service: {service.title}') 