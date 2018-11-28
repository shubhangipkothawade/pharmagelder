fix_columns = ['name', 'location', 'country', 'address', 'plz', 'uci', 'donations_grants', 'sponsorship', 'registration_fees', 'travel_accommodation', 'fees', 'related_expenses', 'total', 'type', 'source']
number_fields = ["donations_grants", "sponsorship", "registration_fees", "travel_accommodation", "fees", "related_expenses", "total"]

fix_columns_accumulations = ['type', 'donations_grants', 'sponsorship', 'registration_fees','travel_accommodation', 'fees', 'related_expenses', 'total', 'source']

regex_title = r'\b(Dr|med|prof|prakt|pd)[\s[.]]*'