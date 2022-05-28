# Interactive BikeShare data Project

import time
import pandas as pd
import numpy as np
import calendar
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    # gets user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    """
    Asks user to specify a city, month, and day to analyze.
    

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    # defaults in case of early exit
    city = ''
    month = ''
    day = ''

    # creating lists for all the data required depending on user choice fpr project parameters
    
    city_name = ['chicago', 'new york city', 'washington']
    month_name = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 
                  'october', 'november', 'december', 'all']
    day_name = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','all']

    
    def yes_or_no():
        """
        Asks users to specify entry into the program and loops out if they do not.
        Returns:
        (str) "yes" gathers initial information on city name, month name, day name
        (str) "no"  exits program
        
        """
        YesNo = input("Welcome to my Bikeshare Project! Would you like to continue? ")
    # Creating a loop for input- using .lower method so that regardless of case, the code doesn't break
        YesNo = YesNo.lower()
        if(YesNo == "yes"):
            return 1
        elif(YesNo == "no"):
            return 0
        else:
            return -1

    while(True):
        inp = yes_or_no()
        if(inp == -1):
            continue

        elif(inp == 1):
            print("Please enter the city you would like information on! ")
            # Creating while loop with a condition to catch invalid entries asking user for a city name from a selection      
            while True:
                city = str(input('Kindly select a city name in full from this selection: Chicago, New York City or Washington. \n')).lower()
                #print(city)
                if city not in city_name:
                    print('Whoops! You did not enter a valid selection! Please enter a valid city name.\n')
                else:
                    break
            # creating second while loop with a condition to filter data by the month 
            while True:
                month = str(input('Which month would you like information on? \nFor all months, please type "all".\n')).lower()
                #print(month)
                if month not in month_name:
                    print('Whoops! You did not enter a valid selection! Please enter a valid month name.\n')
                else:
                      break
            #  Here is a third nested loop retreiving user input for days, with a condition if an inccorect response is indicated, thus restarting this loop     
            while True:
                day = str(input('Would you want to filter the data further by day?\nIf this is so, then type out the day, or for all days, type "all".\n')).lower()
                if day not in day_name:
                    print('Whoops! You did not enter a valid selection! Please enter a valid day name.')
                else:
                    break   

        elif(inp == 0):
                print("You said no and thus, have decided to exit my program!")  
                break
                
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
    city = city.lower()
    month = month.lower()
    day = day.lower()
    
    # loading pandas into the dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    #converting startime column into a more user friendly format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
        
    # making seperate colums for month day and hours of the given week from Start Time using the imported time package
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # creating a while loop to filter data  
    if month != 'all':
    # use the index of the months list to get the equivalent number associated with the month
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 
                  'october', 'november', 'december']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # filtering now by the day of week 
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    #sending values back to main program so that it can be run through the rest of the code
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nWe are now calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # displaying the most common month using the dataframe.mode function 

    top_month = df['month'].mode()[0]
    top_month_name = calendar.month_name[top_month]
    
    print ("\nThe most frequent month for travelling is:", top_month_name)
       
    # display the most common day of week
    top_day = df['day_of_week'].mode()[0]
    print ("\nThe most frequent day of the week for travelling is:", top_day)

           
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    top_start_hour = df['hour'].mode()[0]
    print ("\nThe most frequent hour for travelling is:",top_start_hour,":00 hours")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nWe are now calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    top_start_station = df['Start Station'].mode()[0]
    print("\nThe most frequently used 'start-station' for travelling is:", top_start_station,'!')


    # display most commonly used end station
    top_end_station = df['End Station'].mode()[0]
    print("\nThe most frequently used 'end-station' station for travelling is:", top_end_station,'!')


    # display most frequent combination of start station and end station trip
    df['start and end station'] = df['Start Station'] + ' and ' + df['End Station'] 
    top_start_end_station = df['start and end station'].mode()[0]
    print("\nThe most frequent combination of 'start' and 'end' stations used for travelling are:\n",top_start_end_station,'!')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    seconds = total_travel_time

    years = seconds // (365.25 * 24 * 3600)
    seconds %= (365.25 * 24 * 3600)
    days = seconds // (24 * 3600)
    seconds %= (24*3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    print('The total travel time is : ',years,' years, ',days,' days, ', hours, ' hours,', minutes, ' minutes and', seconds, ' seconds.')

    # display mean travel time
    mean_seconds = np.round(df['Trip Duration'].mean())
    mean_hours = mean_seconds // 3600
    mean_seconds %= 3600
    mean_minutes = mean_seconds // 60
    mean_seconds %= 60
    print('The mean travel time is :  ',mean_hours, ' hours,', mean_minutes, ' minutes, and', mean_seconds, ' seconds.')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_user_types = df['User Type'].value_counts()
    
    print('We are now running through Counts of user types, for example are they a suscriber:\n',counts_user_types, '\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        counts_gender = df['Gender'].value_counts()
        print('Counts of gender:\n', counts_gender, '\n')
    else:
        print('I am sorry, there is currently no information available on Gender.')


    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        earliest_year_of_b = int(df['Birth Year'].min())
        most_recent_year_of_b = int(df['Birth Year'].max())
        most_common_year_of_b = int(df['Birth Year'].mode())
        print('The earliest recorded year of birth is: ',earliest_year_of_b)
        print('The most recent year of birth is: ', most_recent_year_of_b)
        print('The most common year of birth is: ', most_common_year_of_b)
    else:
        print('I\'m sorry, there is currently no information available on Birth Year.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
# new function added   
def show_data(df):
    """
    Function to allow user to specify if they wish to  see the first 5 rows and, then any additional five rows if requested
    """
    row_count = 0
    answer = input(
        'Would you like to view the first 5 rows of your selected data? \n1-Yes\n2-No \n ').strip().lower()
    while True:
        if answer in ('yes', '1'):
            row_count += 5
            print(df.head(row_count))
            print('-'*40)
            answer = input(
                'Would you like to view an additional 5 rows? \n1-Yes\n2-No \n ').strip().lower()
            continue
        elif answer in ('no', '2'):
            break
        else:
            print('-'*40)
            print(
                f"\t({answer}) Whoops! This isn't a valid answer! Please enter a valid answer.")
            answer = input(
                'Would you like to see the next 5 rows? \n1-Yes\n2-No \n>>>  ').strip().lower()
            continue

    print('-'*40)  
    
def main():
    while True:
        city, month, day = get_filters()
        # if user said no, then city, month, and day are all ''
        if city==month==day:
            break
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
