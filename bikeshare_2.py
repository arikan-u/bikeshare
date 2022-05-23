# import packages
import time
import pandas as pd
import numpy as np

# Put Datafiles in a Dict
CITY_DATA = {'ch': 'chicago.csv',
             'ny': 'new_york_city.csv',
             'w': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or ALL to apply no month filter
        (str) day - name of the day of week to filter by, or ALL to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # checks and confirms input validation for city
    # ask the user to input city (chicago (ch), new york city (ny), washington(w)
    while True:
        city = input(
            "please, pick a city to analyze:(ch) for chicago or (ny) for new_york_city or (w) for washington:\n").lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("Invalid Input, please try again.")

    # checks and confirms for input validation for month
    # asks the user to input month (jan, feb, ... , jun, all)
    months = ["all", "jan", "feb", "mar", "apr", "may", "jun"]
    while True:
        month = input(
            "please, pick month (jan, feb, mar, apr, may, jun) to filter or type all:\n").lower()
        if month in months:
            break
        else:
            print("Invalid Input, please try again.")

    # asks the user to input day of week (all, mon ... sun)
    # check for input validation
    days = ["all", "mon", "tue", "wed", "thur", "fri", "sat", "sun"]
    while True:
        day = input(
            "please, pick day of week(mon, tue, wed, thur, fri, sat, sun)to filter or all:\n").lower()
        if day in days:
            break
        else:
            print("Invalid Input, please try again.")

    return city, month, day

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by a month(or all months) and day(or all days)
    """
    # dict of csv to dataframe using pandas
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month
    if month != 'all':
        # filter by month to create new dataframe
        df = df[df['month'].str.startswith(month.title())]

    # filter by day of week
    if day != 'all':
        # filter by day of week to create new dataframe
        df = df[df['day_of_week'].str.startswith(day.title())]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # returns the most common month
    df['month'] = df['Start Time'].dt.month_name()
    most_common_month = df['month'].mode()[0]
    print("Most Common Month: ", most_common_month)

    # returns the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day: ', most_common_day)

    # returns the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Hour: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # returns most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('Most Common Start Station: ', most_common_start)

    # returns most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print('Most Common End Station: ', most_common_end)

    # returns most frequent combination of start station and end station trip
    common_trip = 'From ' + df['Start Station'] + " to " + df['End Station'].mode()[0]
    print('Most Popular Start and End stations:', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # returns total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('Total Travel Time: ', total_trip_duration)

    # returns mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # returns counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print('User Types:\n', user_types)
    # returns counts of gender

    # while loop used as washington has no data for gender
    try:
        print("Gender: \n", df['Gender'].value_counts())
        # TO DO: Display earliest, most recent, and most common year of birth
        print('Earliest Birth Year:', df['Birth Year'].min())
        print('Most Recent Birth Year: ', df['Birth Year'].max())
        print('Most Common Birth Year: ', df['Birth Year'].mode()[0])

    except:
        print('Sorry, we don\'t have data for Birth Year in Washington!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# Asking if the user want show more data
def ask_more_data(df):
    more_data = input("Would you like to view 10 rows of data? yes or no? ").lower()
    start_loc = 0
    while more_data == 'yes':
        print(df.iloc[0:10])
        start_loc += 10
        more_data = input("Would you like to view 10 rows of data? Enter yes or no? ").lower()

    return df


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        ask_more_data(df)

        restart = input('\nRestart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        else:
            print("Thank you for exploring!")


if __name__ == "__main__":
    main()