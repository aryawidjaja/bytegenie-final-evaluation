import psycopg2
import pandas as pd
from typing import List

def query_data(filter_arguments: List[List], output_columns: List[str]) -> pd.DataFrame:
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname="bytegenie_db",
        user="aryawijaya",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Step 1: Filter the event_attributes table
    event_urls = set()
    for column, condition, values in filter_arguments:
        if column.startswith('event_'):
            query = f"SELECT DISTINCT event_url FROM event_attributes WHERE attribute = '{column}'"
            if condition == 'includes':
                query += f" AND value IN ({', '.join([f"'{v}'" for v in values])})"
            elif condition in ['greater-than-equal-to', 'less-than-equal-to']:
                operator = '>=' if condition == 'greater-than-equal-to' else '<='
                query += f" AND CAST(value AS DATE) {operator} '{values}'"
            
            cur.execute(query)
            result = {row[0] for row in cur.fetchall()}
            if not event_urls:
                event_urls = result
            else:
                event_urls.intersection_update(result)

    if not event_urls:
        return pd.DataFrame(columns=output_columns)

    # Step 2: Filter the attendees table to find matching company_urls
    company_urls = set()
    query = f"""
    SELECT DISTINCT company_url 
    FROM attendees 
    WHERE event_url IN ({', '.join([f"'{url}'" for url in event_urls])})
    """
    cur.execute(query)
    company_urls = {row[0] for row in cur.fetchall()}

    # Step 3: Filter the company_attributes table based on company conditions
    for column, condition, values in filter_arguments:
        if column.startswith('company_'):
            query = f"SELECT DISTINCT company_url FROM company_attributes WHERE attribute = '{column}'"
            if condition == 'includes':
                query += f" AND value IN ({', '.join([f"'{v}'" for v in values])})"
            
            cur.execute(query)
            result = {row[0] for row in cur.fetchall()}
            company_urls.intersection_update(result)

    if not company_urls:
        return pd.DataFrame(columns=output_columns)

    # Step 4: Filter the people_attributes table to find matching person_ids
    person_ids = set()
    for column, condition, values in filter_arguments:
        if column.startswith('person_'):
            query = f"SELECT DISTINCT person_id FROM people_attributes WHERE attribute = '{column}'"
            if condition == 'includes':
                query += f" AND LOWER(value) IN ({', '.join([f"'{v.lower()}'" for v in values])})"
            
            cur.execute(query)
            result = {row[0] for row in cur.fetchall()}
            if not person_ids:
                person_ids = result
            else:
                person_ids.intersection_update(result)

    # Step 5: Map person_ids to company_urls using email domain
    person_company_map = {}
    if person_ids:
        person_query = f"""
        SELECT pa.person_id, pa.value AS person_email
        FROM people_attributes pa
        WHERE pa.attribute = 'person_email' AND pa.person_id IN ({', '.join([f"'{pid}'" for pid in person_ids])})
        """
        cur.execute(person_query)
        for row in cur.fetchall():
            person_id, email = row
            company_domain = email.split('@')[-1]
            for company_url in company_urls:
                if company_domain.startswith(company_url.split('.')[0]):
                    person_company_map[company_url] = person_id

    # Step 6: For each combination of event_url and company_url, fetch the required output columns
    final_rows = []
    for event_url in event_urls:
        for company_url in company_urls:
            # Fetch event-related data
            event_data = {col: None for col in output_columns if col.startswith('event_')}
            cur.execute(f"SELECT attribute, value FROM event_attributes WHERE event_url = '{event_url}'")
            for attribute, value in cur.fetchall():
                event_data[attribute] = value

            # Fetch company-related data
            company_data = {col: None for col in output_columns if col.startswith('company_')}
            cur.execute(f"SELECT attribute, value FROM company_attributes WHERE company_url = '{company_url}'")
            for attribute, value in cur.fetchall():
                company_data[attribute] = value

            # Fetch person-related data, if applicable
            person_data = {col: None for col in output_columns if col.startswith('person_')}
            person_id = person_company_map.get(company_url)
            if person_id:
                cur.execute(f"SELECT attribute, value FROM people_attributes WHERE person_id = '{person_id}'")
                for attribute, value in cur.fetchall():
                    person_data[attribute] = value

            final_row = {**event_data, **company_data, **person_data, 'event_url': event_url, 'company_url': company_url}
            final_rows.append(final_row)

    # Convert the final rows to a DataFrame
    final_df = pd.DataFrame(final_rows, columns=output_columns)

    # Drop rows with None or NaN values
    final_df.dropna(inplace=True)

    # Close the database connection
    cur.close()
    conn.close()

    return final_df

# Example usage:
if __name__ == "__main__":
    # SCENARIO 1
    filter_arguments_1 = [
        ['event_city', 'includes', ['Singapore']],
        ['company_industry', 'includes', ['Tech']],
    ]
    output_columns_1 = ['event_url', 'company_url', 'event_city', 'event_name', 'event_country', 'company_industry', 'company_name']

    result1 = query_data(filter_arguments_1, output_columns_1)
    print("\nScenario 1 Result:")
    print(result1)

    # SCENARIO 2
    filter_arguments_2 = [
        ['event_city', 'includes', ['San Francisco']],
        ['event_start_date', 'less-than-equal-to', '2024-05-31'],
        ['event_start_date', 'greater-than-equal-to', '2024-05-01'],
        ['company_industry', 'includes', ['Tech', 'Energy']],
        ['person_seniority', 'includes', ['Director']],
    ]
    output_columns_2 = ['event_url', 'company_url', 'event_city', 'event_name', 'event_country', 'company_industry', 'company_name', 'person_first_name', 'person_last_name', 'person_seniority', 'person_email']
    
    result2 = query_data(filter_arguments_2, output_columns_2)
    print("\nScenario 2 Result:")
    print(result2)

    # SCENARIO 3
    filter_arguments_3 = [
        ['event_city', 'includes', ['San Francisco']],
        ['company_industry', 'includes', ['Tech']],
        ['person_city', 'includes', ['Singapore']],
    ]
    output_columns_3 = ['event_url', 'company_url', 'event_city', 'event_name', 'event_country', 'company_industry', 'company_name', 'person_first_name', 'person_last_name', 'person_seniority', 'person_email']

    result3 = query_data(filter_arguments_3, output_columns_3)
    print("\nScenario 3 Result:")
    print(result3)
