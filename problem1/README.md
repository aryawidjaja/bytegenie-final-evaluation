# Problem 1: Data Filtering Functionality

## Problem Description
We have several interconnected dataframes related to events, companies, and people. The goal is to write a filtering function or class that allows filtering across all dataframes based on conditions applied to any column. The interconnectedness of the dataframes must be considered, meaning that filtering on one dataframe should appropriately filter related records in the other dataframes.

## Approach 1: Propagated Filtering Across Dataframes

### *Description*:
The approach involves applying filters dynamically across all interconnected dataframes. Instead of merging all dataframes into one, the filters are propagated across related entities. For instance, filtering by employee attributes will first filter the relevant employees, then propagate to companies, and finally to events, ensuring that the final filtered data across all dataframes is interconnected and relevant.

### *Pros*🟩:
- Straightforward to implement using Pandas.
- Easy to extend with additional dataframes if required.
- Works well for most filtering operations.

### *Cons*🟥:
- Memory-intensive, as merging large dataframes can significantly increase memory usage.
- Potentially slow for very large datasets due to repeated merging and filtering.

## Approach 2: Indexed Filtering with Pre-Built Indexes

### *Description*:
This approach involves creating indexes on key columns like `event_url`, `company_url`, and `person_id` across all dataframes. Filters are applied using these pre-built indexes, allowing for fast and efficient retrieval of relevant rows. Instead of merging entire dataframes, the filtering process uses indexes to directly access and filter the necessary data.

### *Pros*🟩:
- Efficient filtering with faster lookups.
- Reduced memory usage by retrieving only relevant rows.
- Scales well with large datasets.

### *Cons*🟥:
- Requires additional complexity in managing and maintaining indexes.
- Initial setup of indexes can be time-consuming.
- Limited benefit for filters on non-indexed columns.

## Chosen Approach: Propagated Filtering Across Dataframes
Given the requirements and for simplicity, we'll implement the first approach. This approach is easier to implement and understand, making it a suitable choice for this task.

## How to Run the Code

1. **Set Up the Environment**:
   - Navigate to this `problem1` directory:
     ```sh
     cd problem1
     ```

2. **Run the Filtering Function**:
   - Run the `data_filter.py` script to test the filtering functionality with the provided dummy data:
     ```sh
     python data_filter.py
     ```

# Example Usage

Here’s an example of how to use the `DataFilter` class to filter the dataframes:

1. **Dummy Data**:
   - The `data_filter.py` script already includes dummy data for testing, so you can simply run the script to see the output.

2. **Accessing Filtered Data**:
   - The `DataFilter` class merges the relevant dataframes and applies the specified filters to return the filtered results. The filtered data is then printed to the console.
