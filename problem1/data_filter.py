import pandas as pd

class DataFilter:
    def __init__(self, events_df, attendees_df, companies_df, contacts_df, employees_df):
        """
        Initialize the DataFilter with all the necessary dataframes.
        """
        self.events_df = events_df
        self.attendees_df = attendees_df
        self.companies_df = companies_df
        self.contacts_df = contacts_df
        self.employees_df = employees_df

        # Normalize the case of the dataframes for case-insensitive filtering
        self.events_df = self.events_df.apply(lambda s: s.str.lower() if s.dtype == 'object' else s)
        self.attendees_df = self.attendees_df.apply(lambda s: s.str.lower() if s.dtype == 'object' else s)
        self.companies_df = self.companies_df.apply(lambda s: s.str.lower() if s.dtype == 'object' else s)
        self.contacts_df = self.contacts_df.apply(lambda s: s.str.lower() if s.dtype == 'object' else s)
        self.employees_df = self.employees_df.apply(lambda s: s.str.lower() if s.dtype == 'object' else s)

    def filter_data(self, filters):
        """
        Apply filters to the dataframes and return the filtered result dynamically.
        This function is case-insensitive.

        :param filters: A dictionary where keys are column names and values are the conditions.
                        Example: {'event_name': 'Tech Summit', 'person_seniority': 'Director'}
        :return: Filtered dataframes as a dictionary.
        """
        # Start by filtering the employees, as people filters should propagate through companies and events
        filtered_employees = self.employees_df.copy()
        if any(col in filters for col in ['person_id', 'person_seniority', 'person_department', 'person_city', 'person_country']):
            for col in ['person_id', 'person_seniority', 'person_department', 'person_city', 'person_country']:
                if col in filters:
                    filtered_employees = filtered_employees[filtered_employees[col] == filters[col].lower()]

        # Filter companies based on employee filter
        filtered_company_urls = filtered_employees['company_url'].unique()
        filtered_companies = self.companies_df[self.companies_df['company_url'].isin(filtered_company_urls)]
        
        # Apply additional company-related filters
        if any(col in filters for col in ['company_url', 'company_name', 'company_industry', 'company_country']):
            for col in ['company_url', 'company_name', 'company_industry', 'company_country']:
                if col in filters:
                    filtered_companies = filtered_companies[filtered_companies[col] == filters[col].lower()]
            filtered_company_urls = filtered_companies['company_url'].unique()

        # Filter attendees based on filtered companies
        filtered_attendees = self.attendees_df[self.attendees_df['company_url'].isin(filtered_company_urls)]
        
        # Apply additional event-related filters
        filtered_event_urls = filtered_attendees['event_url'].unique()
        filtered_events = self.events_df[self.events_df['event_url'].isin(filtered_event_urls)]
        if any(col in filters for col in ['event_name', 'event_city', 'event_country', 'event_industry']):
            for col in ['event_name', 'event_city', 'event_country', 'event_industry']:
                if col in filters:
                    filtered_events = filtered_events[filtered_events[col] == filters[col].lower()]
            filtered_event_urls = filtered_events['event_url'].unique()

        # Re-filter attendees based on events
        filtered_attendees = filtered_attendees[filtered_attendees['event_url'].isin(filtered_event_urls)]
        filtered_company_urls = filtered_attendees['company_url'].unique()
        
        # Re-filter companies and employees based on attendees
        filtered_companies = filtered_companies[filtered_companies['company_url'].isin(filtered_company_urls)]
        filtered_employees = filtered_employees[filtered_employees['company_url'].isin(filtered_company_urls)]

        # Filter contacts based on filtered companies
        filtered_contacts = self.contacts_df[self.contacts_df['company_url'].isin(filtered_company_urls)]

        # Selectively return the dataframes that have been affected by the filters
        result = {
            'events': filtered_events.drop_duplicates(),
            'attendees': filtered_attendees.drop_duplicates(),
            'companies': filtered_companies.drop_duplicates(),
            'contacts': filtered_contacts.drop_duplicates(),
            'employees': filtered_employees.drop_duplicates()
        }

        return result

def run_test():
    # Example dummy data to test the filtering functionality
    events_df = pd.DataFrame({
        'event_url': ['test1.com', 'test2.com', 'test3.com', 'test4.com', 'test5.com'],
        'event_name': ['Tech Summit', 'Oil & Gas Expo', 'Health Conference', 'AI Conference', 'Green Energy Summit'],
        'event_start_date': ['2024-01-01', '2024-06-15', '2024-08-27', '2024-05-10', '2024-09-01'],
        'event_city': ['Singapore', 'Dubai', 'New York', 'San Francisco', 'Berlin'],
        'event_country': ['SG', 'UAE', 'USA', 'USA', 'DE'],
        'event_industry': ['Tech', 'Oil & Gas', 'Healthcare', 'Tech', 'Energy']
    })

    attendees_df = pd.DataFrame({
        'event_url': ['test1.com', 'test1.com', 'test2.com', 'test3.com', 'test4.com', 'test4.com', 'test5.com'],
        'company_url': ['company1.com', 'company4.com', 'company2.com', 'company3.com', 'company1.com', 'company5.com', 'company6.com'],
        'company_relation_to_event': ['Sponsor', 'Exhibitor', 'Exhibitor', 'Attendee', 'Sponsor', 'Attendee', 'Exhibitor']
    })

    companies_df = pd.DataFrame({
        'company_url': ['company1.com', 'company2.com', 'company3.com', 'company4.com', 'company5.com', 'company6.com'],
        'company_name': ['company1', 'company2', 'company3', 'company4', 'company5', 'company6'],
        'company_industry': ['Tech', 'Oil & Gas', 'Healthcare', 'Tech', 'Energy', 'Energy'],
        'company_revenue': ['100M', '200M', '150M', '300M', '250M', '180M'],
        'company_country': ['SG', 'UAE', 'USA', 'USA', 'DE', 'USA']
    })

    contacts_df = pd.DataFrame({
        'company_url': ['company1.com', 'company2.com', 'company3.com', 'company4.com', 'company5.com', 'company6.com'],
        'office_city': ['Singapore', 'Dubai', 'New York', 'San Francisco', 'Berlin', 'New York'],
        'office_country': ['SG', 'UAE', 'USA', 'USA', 'DE', 'USA'],
        'office_address': ['123 Test St', '456 Test Rd', '789 Test Blvd', '321 AI Ave', '654 Green St', '987 Energy Blvd'],
        'office_email': ['info@company1.com', 'info@company2.com', 'info@company3.com', 'info@company4.com', 'info@company5.com', 'info@company6.com']
    })

    employees_df = pd.DataFrame({
        'company_url': ['company1.com', 'company2.com', 'company3.com', 'company4.com', 'company5.com', 'company6.com', 'company1.com', 'company5.com'],
        'person_id': ['person1', 'person2', 'person3', 'person4', 'person5', 'person6', 'person7', 'person8'],
        'person_first_name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Helen'],
        'person_last_name': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Davis', 'Miller'],
        'person_email': ['alice@company1.com', 'bob@company2.com', 'charlie@company3.com', 'david@company4.com', 'eva@company5.com', 'frank@company6.com', 'grace@company1.com', 'helen@company5.com'],
        'person_city': ['Singapore', 'Dubai', 'New York', 'San Francisco', 'Berlin', 'New York', 'Singapore', 'Berlin'],
        'person_country': ['SG', 'UAE', 'USA', 'USA', 'DE', 'USA', 'SG', 'DE'],
        'person_seniority': ['Director', 'Manager', 'Director', 'Senior Engineer', 'Engineer', 'Director', 'Manager', 'Engineer'],
        'person_department': ['Engineering', 'Operations', 'R&D', 'AI Research', 'Sustainability', 'Energy', 'HR', 'Sustainability']
    })

    # Create an instance of the DataFilter class
    data_filter = DataFilter(events_df, attendees_df, companies_df, contacts_df, employees_df)

    print("Enter your filter criteria (e.g., event_city=Singapore, person_seniority=Director):")
    user_input = input().split(',')
    filters = {}

    for criteria in user_input:
        key, value = criteria.split('=')
        filters[key.strip()] = value.strip()

    filtered_data = data_filter.filter_data(filters)

    for key, df in filtered_data.items():
        print(f"\nFiltered {key.capitalize()}:")
        print(df)

if __name__ == "__main__":
    run_test()
