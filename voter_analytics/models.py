# File: models.py
# Author: Pavana Manoj (pavana@bu.edu), 04/04/2025
# Description: the code in this file defines the voter model, and specifies what data is needed for each voter
# includes a load_data function to import voter data from a csv file into the db

from django.db import models
import csv
from datetime import datetime
# Create your models here.

class Voter(models.Model):
    '''model representing a registered voter in newton, ma'''

    # name
    first_name = models.TextField()
    last_name = models.TextField()

    # address
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True)
    zip_code = models.CharField(max_length=10)

    # dates
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()

    # other info
    party = models.CharField(max_length=2)
    precinct = models.CharField(max_length=10)

    # voting participation
    v20state = models.CharField(max_length=1)
    v21town = models.CharField(max_length=1)
    v21primary = models.CharField(max_length=1)
    v22general = models.CharField(max_length=1)
    v23town = models.CharField(max_length=1)

    # score
    voter_score = models.IntegerField()

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.first_name} {self.last_name}, {self.street_number} {self.street_name}, precinct {self.precinct}'

def load_data():
    '''Load voters from CSV into the database'''

    from .models import Voter

    Voter.objects.all().delete()

    path = 'C:/Users/Pavana/OneDrive/Desktop/django/voter_analytics/data/newton_voters.csv'
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                v = Voter(
                    first_name = row['First Name'],
                    last_name = row['Last Name'],
                    street_number = row['Residential Address - Street Number'],
                    street_name = row['Residential Address - Street Name'],
                    apartment_number = row['Residential Address - Apartment Number'],
                    zip_code = row['Residential Address - Zip Code'],
                    date_of_birth = datetime.strptime(row['Date of Birth'], '%Y-%m-%d'),
                    date_of_registration = datetime.strptime(row['Date of Registration'], '%Y-%m-%d'),
                    party = row['Party Affiliation'],
                    precinct = row['Precinct Number'],
                    v20state = row['v20state'],
                    v21town = row['v21town'],
                    v21primary = row['v21primary'],
                    v22general = row['v22general'],
                    v23town = row['v23town'],
                    voter_score = int(row['voter_score'])
                )
                v.save()
            except Exception as e:
                print(f"Error with row: {row}")
                print(e)

    print(f'Done. Created {Voter.objects.count()} voters.')