import time
import pandas as pd
import numpy as np

# Refactoring: added comments to improve readability
# Refactoring: cleaned up variable names
# Refactoring: added spacing for better structure

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" for no month filter
        (str) day   - name of the day of week to filter by, or "all" for no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? ").lower()
        if city in CITY_DATA:
            break
        print("Invalid input. Please enter Chicago, New York City, or Washington.")

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month? January, February, March, April, May, June, or all? ").lower()
        if month in months:
            break
        print("Invalid input. Please enter a valid month.")

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all? ").lower()
        if day in days:
            break
        print("Invalid input. Please enter a valid day.")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day   - name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df - Pandas DataFrame containing filtered city data
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month) + 1
        df = df[df['month'] == month_num]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('Most common month:', df['month'].mode()[0])
    print('Most common day of week:', df['day_of_week'].mode()[0])

    df['hour'] = df['Start Time'].dt.hour
    print('Most common start hour:', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most commonly used start station:', df['Start Station'].mode()[0])
    print('Most commonly used end station:', df['End Station'].mode()[0])

    df['Start-End Combination'] = df['Start Station'] + " to " + df['End Station']
    print('Most frequent trip:', df['Start-End Combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total travel time:', df['Trip Duration'].sum(), 'seconds')
    print('Mean travel time:', df['Trip Duration'].mean(), 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('Counts of user types:\n', df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print('Counts of gender:\n', df['Gender'].value_counts())
    else:
        print('Gender data not available for this city.')

    if 'Birth Year' in df.columns:
        print('Earliest year of birth:', int(df['Birth Year'].min()))
        print('Most recent year of birth:', int(df['Birth Year'].max()))
        print('Most common year of birth:', int(df['Birth Year'].mode()[0]))
    else:
        print('Birth year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """
    Displays 5 lines of raw data at a time upon user request.
    Stops when the user says 'no' or when there is no more data to display.
    """
    start_row = 0

    while True:
        show_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no: ').lower()

        if show_data != 'yes':
            break

        print(df.iloc[start_row:start_row + 5])
        start_row += 5

        if start_row >= len(df):
            print("\nNo more raw data to display.")
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()