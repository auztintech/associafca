from django.core.management.base import BaseCommand
from registrations.models import State, LGA
import json

class Command(BaseCommand):
    help = 'Load Nigerian states and LGAs from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.stdout.write('Loading states and LGAs...')
        
        for state_data in data['states']:
            state, created = State.objects.get_or_create(
                name=state_data['name'],
                defaults={'capital': state_data['capital']}
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created state: {state.name}')
                )
            
            for lga_name in state_data['lgas']:
                lga, lga_created = LGA.objects.get_or_create(
                    name=lga_name,
                    state=state
                )
                if lga_created:
                    self.stdout.write(f'  - Created LGA: {lga_name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded {State.objects.count()} states '
                f'and {LGA.objects.count()} LGAs'
            )
        )