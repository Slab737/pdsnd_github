import time
import pandas as pd
import numpy as np

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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ['chicago', 'new york city', 'washington']
    city=''
    while True:
        try:
            city = input ("Would you like to see data for Chicago, New York City, or Washington? ")
            if city.lower() not in city_list:
                print('Please enter the correct spelling for the city you\'ve selected.')
            else:
                city = city.lower()
                break
        except:
            print('Oops, something went wrong')


    #Get user input for filter type.
    filter_list = ['month', 'day', 'both', 'none']
    filter_input=''
    while True:
        try:
            filter_input = input ("Would you like to filter the data by month, day, both or none? ")
            if filter_input.lower() not in filter_list:
                print('Please enter the correct spelling for either month, day, both or none.')
            else:
                filter_input = filter_input.lower()
                break
        except:
            print('Oops, something went wrong')

    # TO DO: get user input for month (all, january, february, ... , june)
    if filter_input == 'month' or filter_input == 'both':
        month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        month=''
        while True:
            try:
                month = input ("Which month - January, February, March, April, May, June or All for no filter? ")
                if month.lower() not in month_list:
                    print('Please enter the full correct spelling for the month.')
                else:
                    month = month.lower()
                    break
            except:
                print('Oops, something went wrong')
    else:
        month = 'all'

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_input == 'day' or filter_input == 'both':
        day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day=''
        while True:
            try:
                day = input ("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All for no filter? ")
                if day.lower() not in day_list:
                    print('Please enter the full correct spelling for the day.')
                else:
                    day = day.lower()
                    break
            except:
                print('Oops, something went wrong')
    else:
        day = 'all'
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
    df = pd.read_csv(CITY_DATA[city])

    df['city_input'] = city
    df['month_input'] = month
    df['day_input'] = day

    #Create missing variables for Washington, fill with nan
    if city == 'washington':
        df['Gender'] = np.nan
        df['Birth Year'] = np.nan

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # TO DO: display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    comm_month = df['month'].mode()[0]
    if 'all' in df['month_input'].unique():
        print("\nThis was the most common month to travel: ", months[comm_month-1])
    else:
        print("\nThe month is filtered down to {}".format(months[comm_month-1]))

    # TO DO: display the most common day of week
    comm_dow = df['day_of_week'].mode()[0]
    if 'all' in df['day_input'].unique():
        print("\nThis was the most common day of week: ", comm_dow)
    else:
        print("\nWith the day filtered down to {}".format(comm_dow))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    comm_start_hour = df['hour'].mode()[0]
    print("\nThis was the most common start hour: ", comm_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    nextstat = input("***Hit ENTER to continue and show statistics on the most popular stations and trip***")

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    comm_start_station = df['Start Station'].mode()[0]
    print("\nThis was the most common start station: ", comm_start_station)
    print("Trips started here: ",df['Start Station'].value_counts()[comm_start_station]," times.")

    # TO DO: display most commonly used end station
    comm_end_station = df['End Station'].mode()[0]
    print("\nThis was the most common end station: ", comm_end_station)
    print("Trips ended here: ",df['End Station'].value_counts()[comm_end_station]," times.")

    # TO DO: display most frequent combination of start station and end station trip
    df['Combination Station'] = df['Start Station'] + df['End Station']
    comb_station = df['Combination Station'].mode()[0]
    print("\nThis was the most common start and end station combination.")
    print("Start station: ", comm_start_station)
    print("End station: ", comm_end_station)
    print("Trips between the two stations: ",df['Combination Station'].value_counts()[comb_station]," times.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    nextstat = input("***Hit ENTER to continue and show statistics on the total and average trip duration***")

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = np.sum(df['Trip Duration'])
    print("\nTotal Travel time in seconds:",total_travel_time)
    print("\nTotal Travel time in minutes:",total_travel_time / 60)
    print("\nTotal Travel time in hours",total_travel_time / 60 / 60)


    # TO DO: display mean travel time
    mean_travel_time = np.mean(df['Trip Duration'])
    print("\n\nMean Travel time in seconds:",mean_travel_time)
    print("\nMean Travel time in minutes:",mean_travel_time / 60)

    print("\n\nWith",df['Trip Duration'].count(), 'total trips taken.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    nextstat = input("***Hit ENTER to continue and show statistics on bikeshare users***")

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('\nUser Type Count: ')
    print(user_types_count)


    # TO DO: Display counts of gender
    while True:
        try:
            if 'washington' not in df['city_input'].unique():
                gender_count = df['Gender'].value_counts()
                print('\nGender count: ')
                print(gender_count)
                break
            else:
                print('\nWashington does not keep records about gender.')
                break
        except:
            print('\nOops, something went wrong.')
            break

    # TO DO: Display earliest, most recent, and most common year of birth
    while True:
        try:
            if 'washington' not in df['city_input'].unique():
                birth_count = df['Birth Year'].mode()[0]
                print('\nMost common birth year: ',int(birth_count))
                print("Number of people born in {}:".format(int(birth_count)),df['Birth Year'].value_counts()[birth_count])
                print("Earliest year of birth: ",int(df['Birth Year'].min()))
                print("Most recent year of birth: ",int(df['Birth Year'].max()))
                break
            else:
                print('\nWashington does not keep records about birth year.')
                break
        except:
            print('\nOops, something went wrong.')
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #nextstat = input("***Hit ENTER to continue and show raw data info of users***")


def raw_info(df):
    """
        Asks user if they would like to receive raw bikeshare user info.
        Displays raw information on bikeshare users, 5 users information at a time.
    """
    print('\nDisplaying Raw User Information...\n')
    start_time = time.time()

    df=df.fillna('Not Recorded')

    i = 0
    length_of_dataframe = len(df)

    while i <= (length_of_dataframe - 5):
        raw_data=df[i:i+5]
        for j in raw_data.index:
            print('User Number: ',raw_data['Unnamed: 0'][j])
            print('Start Station:',raw_data['Start Station'][j])
            print('End Station:',raw_data['End Station'][j])
            print('Start Time:',raw_data['Start Time'][j])
            print('End Time:',raw_data['End Time'][j])
            print('Trip Duration:',raw_data['Trip Duration'][j],'seconds')
            print('User Type:',raw_data['User Type'][j])
            if 'washington' not in raw_data['city_input'][j]:
                print('Gender:',raw_data['Gender'][j])
                print('Birth Year:',raw_data['Birth Year'][j])
            print('\n')

        i=i+5

        restart = input('\nWould you like more info? Enter y or yes for yes or anything else for no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
             break



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_start = input('\nWould you like to see raw user info? Enter y or yes for yes or anything else for no.\n')
        if raw_start.lower() == 'yes' or raw_start.lower() == 'y':
            raw_info(df)

        restart = input('\nWould you like to restart? Enter y or yes for yes or anything else for no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
