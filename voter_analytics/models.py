# File: models.py
# Author: Pavana Manoj (pavana@bu.edu), 04/06/2025
# Description: Defines the Voter model representing Newton, MA voters and a function to load voter data from a CSV file into the database.

from django.db import models

class Voter(models.Model):
    '''Represents a registered voter and their voting history.'''
    first_name = models.TextField()
    last_name = models.TextField()
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''string representation of voter model'''
        return f'{self.first_name} {self.last_name} ({self.party_affiliation.strip()})'

def load_data():
    '''Reads voter data from a CSV and stores it in the db'''
    filename = 'C:/Users/Pavana/OneDrive/Desktop/django/newton_voters.csv'
    f = open(filename)
    f.readline()
    for line in f:
        fields = line.split(',')
        try:
            voter = Voter(
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3],
                street_name=fields[4],
                apartment_number=fields[5],
                zip_code=fields[6],
                date_of_birth=fields[7],
                date_of_registration=fields[8],
                party_affiliation=fields[9],
                precinct_number=fields[10],
                v20state=fields[11] == "TRUE",
                v21town=fields[12] == "TRUE",
                v21primary=fields[13] == "TRUE",
                v22general=fields[14] == "TRUE",
                v23town=fields[15] == "TRUE",
                voter_score=int(fields[16]),
            )
            voter.save()
            print(f'Created voter: {voter}')
        except:
            print(f'Skipped over: {fields}')
    print(f'Successfully created {len(Voter.objects.all())} voters.')
