import time
import pandas as pd

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
    # (1) source: code for underline text taken from source "stackoverflow"
    print('\033[4m' + '\nHello! Let\'s explore some US bikeshare data!' + '\033[0m')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # (2) source: method for while loop taken from "stackoverflow"
    while True:
        city = input('Please enter city name you want to analyze data for (chicago,new york city,washington): ')
        if city.lower() not in ['chicago','new york city','washington']:
            print('Fault: please enter the city as shown above...')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please select a month you want to analyze data for (all, january, february, ... , june): ')
        if month.lower() not in ['all','january','february','march','april','may','june']:
            print('Fault: please enter the month as shown above...')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please select a weekday you want to analyze data for (all, monday, tuesday, ... sunday): ')
        if day.lower() not in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
            print('Fault: please enter the weekday as shown above...')
        else:
            break

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating the ' + '\033[4m' + 'Most Frequent Times of Travel' + '\033[0m' + '...\n')
    start_time = time.time()

    # display the most common month
    mc_month = df['month'].mode()[0]
    print('Most common travel month is: {}'.format(mc_month))

    # display the most common day of week
    mc_dayofweek = df['day_of_week'].mode()[0]
    print('Most common travel day of week is: {}'.format(mc_dayofweek))

    # display the most common start hour
    df['Start hour'] = pd.DatetimeIndex(df['Start Time']).hour
    mc_starthour = df['Start hour'].mode()[0]
    print('Most common travel start hour is: {}'.format(mc_starthour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the ' + '\033[4m' + 'Most Popular Stations and Trip' + '\033[0m' + '...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station is: {}'.format(start_station))

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most commonly used end station is: {}'.format(end_station))

    # display most frequent combination of start station and end station trip
    df['comb_station'] = df['Start Station'] +'/'+ df['End Station']
    combstation = df['comb_station'].mode()[0]
    print('The most frequent combination of start/end station is: {}'.format(combstation) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating ' + '\033[4m' + 'Trip Duration' + '\033[0m' + '...\n')
    start_time = time.time()

    # function that calculates a different day format (source (3))
    def time_calculation(time):
        day = time // (24 * 3600)
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time

        return ('{} days {} hours {} mins {} sec'.format(day,hour,minutes,seconds))

    # calculate, transform and display total travel time
    total_tt = int(df['Trip Duration'].sum())
    print('The total travel time is:', time_calculation(total_tt))

    # calculate, transform and display mean travel time
    avg_tt = int(df['Trip Duration'].mean())
    print('The average travel time is:', time_calculation(avg_tt))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating ' + '\033[4m' + 'User Stats' + '\033[0m' + '...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The user types are: \n{}\n'.format(user_types))


    # Display counts of gender
    try:
        df['Gender'].fillna('Unknown', inplace = True)
        gender = df['Gender'].value_counts()
        print('The gender types are: \n{}\n'.format(gender))

    # Display earliest, most recent, and most common year of birth
        earliest_BY = int(df['Birth Year'].min())
        mostrecent_BY = int(df['Birth Year'].max())
        mostcommon_BY = int(df['Birth Year'].mode()[0])
        print('Earliest Birth Year: {}'.format(earliest_BY))
        print('Most recent Birth Year: {}'.format(mostrecent_BY))
        print('Most common Birth Year: {}'.format(mostcommon_BY))
        pass
    # Avoid "Keyerror" due to missing birth year and gender data for Washington
    except KeyError:
        print('Unfortunately, there is no Gender/Birth Year data for Washington...')
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_data(df):
    """Displays concrete trip data as examples."""

    print('\nPulling ' + '\033[4m' + 'individual trip data for you' + '\033[0m' + '...\n')
    x = 5
    while True:
        print(df.head(x))
        x += 5
        moredata = input('\nWould you like to see more individual trip data? Enter \'yes\' or \'no\'.')
        if moredata.lower() != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        trip_data(df)

        restart = input('\nWould you like to restart? Enter \'yes\' or \'no\'.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
