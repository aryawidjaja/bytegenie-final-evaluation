# Problem 2: Query Data from PostgreSQL with Filters

This script provides a Python function, `query_data`, that queries data from a PostgreSQL database based on specified filter conditions. The database consists of three main tables: `event_attributes`, `company_attributes`, and `people_attributes`.

## Database Schema

1. **event_attributes**
   - Columns: `event_url`, `attribute`, `value`
   - Example attributes: `event_start_date`, `event_city`, `event_country`, `event_industry`

2. **company_attributes**
   - Columns: `company_url`, `attribute`, `value`
   - Example attributes: `company_name`, `company_country`, `company_industry`, `company_revenue`

3. **people_attributes**
   - Columns: `person_id`, `attribute`, `value`
   - Example attributes: `person_first_name`, `person_last_name`, `person_email`, `person_seniority`, `person_department`

## Function Overview

The `query_data` function allows filtering based on multiple conditions and returns a DataFrame with the specified output columns. The inputs are:

- `filter_arguments`: A list of lists, where each inner list contains a column name, a condition, and a value (or list of values). Supported conditions are `includes`, `greater-than-equal-to`, and `less-than-equal-to`.
- `output_columns`: A list of column names that specify the attributes to be included in the output.

### Example Usage

1. **Retrieve Tech Companies Attending Events in Singapore:**

    ```python
    filter_arguments = [
        ['event_city', 'includes', ['Singapore']],
        ['company_industry', 'includes', ['Tech']],
    ]
    output_columns = ['event_city', 'event_name', 'event_country', 'company_industry', 'company_name']
    ```

2. **Retrieve Email Addresses of Directors of Tech Companies Attending Events in Singapore in January 2025:**

    ```python
    filter_arguments = [
        ['event_city', 'includes', ['Singapore']],
        ['event_start_date', 'less-than-equal-to', '2025-01-31'],
        ['event_start_date', 'greater-than-equal-to', '2025-01-01'],
        ['company_industry', 'includes', ['Tech']],
        ['person_seniority', 'includes', ['Director']],
    ]
    output_columns = ['event_city', 'event_name', 'event_country', 'company_industry', 'company_name', 'person_first_name', 'person_last_name', 'person_seniority', 'person_email']
    ```

### How It Works

1. **Filter `event_attributes` Table:**
   - The function starts by filtering the `event_attributes` table based on the conditions related to events (e.g., `event_city`, `event_start_date`).

2. **Match `company_url` from `attendees` Table:**
   - The filtered `event_url` results are used to query the `attendees` table to find the matching `company_url`.

3. **Filter `company_attributes` Table:**
   - The function then filters the `company_attributes` table based on the conditions related to companies (e.g., `company_industry`).

4. **Filter `people_attributes` Table:**
   - If people-related filters are provided (e.g., `person_seniority`), the function filters the `people_attributes` table.

5. **Combine Results:**
   - Finally, the relevant data is combined based on the relationships between `event_url`, `company_url`, and `person_id`, and the specified output columns are returned.

### Conclusion

This solution is flexible and can handle a wide range of queries involving events, companies, and people attributes, ensuring that only relevant data is returned based on the specified filters.
