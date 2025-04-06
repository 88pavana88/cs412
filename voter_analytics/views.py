# File: views.py
# Author: Pavana Manoj (pavana@bu.edu), 04/06/2025
# Description: Defines views for listing and viewing individual voters

from django.views.generic import ListView, DetailView
from .models import Voter


class VoterListView(ListView):
    '''List view for all voters with search and filtering.'''
    template_name = 'voter_analytics/all_voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        '''Adds years and parties to context for the search form.'''
        context = super().get_context_data(**kwargs)
        context['years'] = list(range(1900, 2005))
        context['parties'] = [
            'U', 'D', 'R', 'A', 'AA', 'CC', 'E', 'EE', 'FF', 'G', 'GG', 'H',
            'HH', 'J', 'K', 'L', 'O', 'P', 'Q', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'
        ]
        return context

    def get_queryset(self):
        '''Filters voters based on query params.'''
        filtered_voters = super().get_queryset().order_by('last_name')

        selected_score = self.request.GET.get('voter_score')
        if selected_score:
            filtered_voters = filtered_voters.filter(voter_score=selected_score)

        maximum_birth_year = self.request.GET.get('max_birth_year')
        if maximum_birth_year:
            filtered_voters = filtered_voters.filter(date_of_birth__year__lte=maximum_birth_year)

        minimum_birth_year = self.request.GET.get('min_birth_year')
        if minimum_birth_year:
            filtered_voters = filtered_voters.filter(date_of_birth__year__gte=minimum_birth_year)

        selected_party = self.request.GET.get('party')
        if selected_party:
            filtered_voters = filtered_voters.filter(party_affiliation=selected_party.ljust(2))

        for election_field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if self.request.GET.get(election_field) == 'on':
                filtered_voters = filtered_voters.filter(**{election_field: True})

        return filtered_voters


class VoterDetailView(DetailView):
    '''Detail view for a single voter.'''
    template_name = 'voter_analytics/individual_voter.html'
    model = Voter
    context_object_name = 'voter'
