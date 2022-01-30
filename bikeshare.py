import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    """User inputs the city they would like to see data for, the case is lowered. Should the city they enter not be recognised they
    will be asked to enter it again. After failing to enter a recognised city four times the user is told that they have exceeded
    the maximum amount of attempts and the programme
    is closed using the exit() function from the system module. """
    count_city=0
    city = input('Please enter the city that you would like to view data for, you can choose from Chicago, New York City and Washington:')
    city = city.lower()
    while count_city < 4:
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            break
        elif count_city < 3:
            city = input('I am sorry, you did not select a valid city, please check your spelling and try again:').lower()
            count_city+=1
        else:
            print('I am sorry, you have exceded the maximum number of attempts, the programme will now close.')
            sys.exit()
    """Users are asked to specify either the month they would like to see data for or they can select all to see the data for all months.
    The same convention for correcting capitilisations and user input error from city input is utilised here."""
    count_month=0
    month = input('Please enter the month that you would like to view data for; you can choose from January to June (inclusive) or alternatively type \'all\' to see the data for all months:')
    month = month.lower()
    while count_month < 4:
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        elif count_month < 3:
            month = input('I am sorry, you did not select a valid month, please check your spelling and try again:').lower()
            count_month+=1
        else:
            print('I am sorry, you have exceded the maximum number of attempts, the programme will now close.')
            sys.exit()
    """Users are asked to enter the day they would like to see data for following the same conventions as for month above."""
    count_day = 0
    day = input('Please enter the day of the week that you would like to view data for or alternatively type \'all\' to see the data for all days:')
    day = day.lower()
    while count_day < 4:
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        elif count_day < 3:
            day = input('I am sorry, you did not select a valid day, please check your spelling and try again:').lower()
            count_day+=1
        else:
            print('I am sorry, you have exceded the maximum number of attempts, the programme will now close.')
            sys.exit()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    """The csv file associated with the selected city is opened and read to produce the dataframe, df."""
    df = pd.read_csv(CITY_DATA[city])
    """Here the start time is converted to a date time variable and the month and day of week are generated as new columns."""
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    """The data is now filtered by the selected month. If all months are selected then no filtering takes place."""
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    """The data is now filtered by day, unless all days have been requested."""
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    """The most popular month only prints a value when 'all' months is chosen"""
    if month == 'all':
        df['month'] = df['Start Time'].dt.month
        month_names = ['January', 'February', 'March', 'April', 'May', 'June']
        popular_month = month_names[df['month'].mode()[0] - 1]
        print('The most popular month for rides was {}.'.format(popular_month))
    """The most popular day of the week only prints a value when 'all' days is chosen"""
    if day == 'all':
        df['day'] = df['Start Time'].dt.weekday_name
        popular_day = df['day'].mode()[0]
        print('The most popular day of the week for rides was {}.'.format(popular_day))
    """The most popular start hour is found and converted to the corresponding time frame this translates to."""
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular time of the day for rides to start was {}:00 - {}:59.'.format(popular_hour, popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    """Below the most popular starting and ending station are found and printed."""
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular station to start a ride was:', popular_start_station)

    popular_end_station = df['End Station'].mode()[0]
    print('The most popular station to end a ride was:', popular_end_station)
    """In order to find the most popular trip the starting and end station were combined into a string
    and then the mode function was used to find the most common out of all of these. The result is
    then printed."""
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('The most popular trip was from', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    """The total trip duration for the filtered data was found by summing the Trip Duration column. It was then broken
    down into hours, minutes and seconds to make it more accessible to the user."""
    total_travel_time = df['Trip Duration'].sum()
    total_seconds = int(total_travel_time % 60)
    total_minutes = int(((total_travel_time - total_seconds)/60) % 60)
    total_hours = int((total_travel_time - total_seconds - (total_minutes * 60)) / 3600)
    print('The total trip duration for the selected time period was {} hours, {} minutes and {} seconds.'.format(total_hours, total_minutes, total_seconds))
    """The average trip duration is found by finding the mean of the Trip Duration column and then converting to minutes
    and seconds."""
    mean_time = df['Trip Duration'].mean()
    mean_seconds = int(mean_time % 60)
    mean_minutes = int(mean_time / 60)
    print('The average trip duration was {} minutes and {} seconds.'.format(mean_minutes, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """A value_counts function was used to generate the numbers of each type of user and also gender and birth year below."""
    print('The number of each type of user was:')
    print(df['User Type'].value_counts())

    """As Washington does not include data for gender or birth year the following statements are only printed when
    the city selected IS NOT Washington. The year data is converted to an integer. Some of the years returned
    seemed a little suspect (e.g 1899, 2016) but without further detail of the required minimum age of the riders and also
    the programmer not wanting to potentially discriminate against older users they birth year data was not altered."""
    if city != 'washington':
        print('The number of each gender recorded was:')
        print(df['Gender'].value_counts())

    if city != 'washington':
        print('The youngest rider was born in: ', int(df['Birth Year'].max()))
        print('The oldest rider was born in: ', int(df['Birth Year'].min()))
        print('The most common year for riders to be born in was: ', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """This function allows the user to see the raw data should they so wish. It allows the user to keep adding
    more rows five at a time until all of the data has been viewed."""
    raw_data_select = input('Would you like to see a sample of the raw data? Enter yes or no.').lower()
    count_raw = 5
    while raw_data_select == 'yes':
        if count_raw < len(df.index):
            print(df[count_raw - 5:count_raw])
            raw_data_select=input('Enter yes if you would like to see the next five rows of data, otherwise enter no.').lower()
            count_raw += 5
        else:
            print(df[count_raw - 5:])
            print('This is the end of the raw data. Thank you for using bikeshare.')
            break

def total_rides(df, city):
    """This function begins the data feedback by telling the user how many rides are included in the sample they selected."""
    num_rides_total = len(df.index)
    print('\nThe total number of rides during your selected time parameters in {} was {}.\n'.format(city,num_rides_total))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        total_rides(df, city)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
