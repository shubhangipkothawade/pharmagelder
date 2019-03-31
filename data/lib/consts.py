fix_columns = ['name', 'location', 'country', 'address', 'plz', 'uci', 'donations_grants', 'sponsorship', 'registration_fees', 'travel_accommodation', 'fees', 'related_expenses', 'total', 'type', 'source']
number_fields = ["donations_grants", "sponsorship", "registration_fees", "travel_accommodation", "fees", "related_expenses", "total"]
column_export_information = '_export_information'
fix_columns_accumulations = ['type', 'donations_grants', 'sponsorship', 'registration_fees','travel_accommodation', 'fees', 'related_expenses', 'total', 'source']

regex_title = r'\b(Doctor|Dr|Dott|med|méd|ssa|Professor|prof|phil|pharm|prakt|pd|dipl|Arzt|Mr|Ms|Mrs|Docteur|Herr|Hr|Frau|Fr|Madame|Signora|Monsieur|lic.  I|pract.|Professeur|lic.)[\s[.]]*'

dataframe_types = {
    'name': 'str',
    'location': 'str',
    'country': 'str',
    'address': 'str',
    'plz': 'str',
    'uci': 'str',
    'donations_grants': 'float',
    'sponsorship': 'float',
    'registration_fees': 'float',
    'travel_accommodation': 'float',
    'fees': 'float',
    'related_expenses': 'float',
    'total': 'float',
    'type': 'str',
    'source': 'str'
}

dataframe_types_numbers_as_string = {
    'name': 'str',
    'location': 'str',
    'country': 'str',
    'address': 'str',
    'plz': 'str',
    'uci': 'str',
    'donations_grants': 'str',
    'sponsorship': 'str',
    'registration_fees': 'str',
    'travel_accommodation': 'str',
    'fees': 'str',
    'related_expenses': 'str',
    'total': 'str',
    'type': 'str',
    'source': 'str'
}