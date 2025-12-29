import time
import pandas as pd
import numpy as np

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york": "new_york_city.csv",
    "washington": "washington.csv",
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month
        filter
        (str) day - name of the day of week to filter by, or "all" to apply no
        day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = list(CITY_DATA.keys())
    while True:
        city = input(
            "Select the city you like to see data for: Chicago, New York or Washington.\n"
        ).lower()
        if city in cities:
            break
        print("Invalid input. Please try again.")
    while True:
        user_filter = (
            input('Filter by month, day, both, or none? (type "none"):\n')
            .strip()
            .lower()
        )
        if user_filter in ["month", "day", "both", "none"]:
            break
        print("Invalid input. Please try again.")
    # get user input for month (all, january, february, ... , june)
    if user_filter in ("month", "both"):
        months = ["january", "february", "march", "april", "may", "june"]
        while True:
            month = (
                input("Which month? January, February, March, April, May, or June:\n")
                .strip()
                .lower()
            )
            if month in months:
                break
            print("Invalid input. Please try again.")
    else:
        month = "all"

    if user_filter in ("day", "both"):
        days = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        while True:
            day = input("Which day? Monday, Tuesday, ... Sunday:\n").strip().lower()
            if day in days:
                break
            print("Invalid input. Please try again.")
    else:
        day = "all"
    print("-" * 40)
    return city, month, day


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    if month == "all":
        common_month = df["Month"].mode()[0]
        print("The most common month is: {}".format(common_month))

    # display the most common day of week
    if day == "all":
        common_day = df["Day of Week"].mode()[0]
        print("The most common day is: {}".format(common_day))

    # display the most common start hour
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["hour"] = df["Start Time"].dt.hour
    common_hour = df["hour"].mode()[0]
    print("The most common hour is: {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    start_station = df["Start Station"].mode()[0]
    print("The most popular start station is: {}".format(start_station))
    # display most commonly used end station
    end_station = df["End Station"].mode()[0]
    print("The most popular end station is: {}".format(end_station))

    # display most frequent combination of start station and end station trip
    trip = (df["Start Station"].str.cat(df["End Station"], sep=" - ")).mode()[0]
    print("The most popular trip is: {}".format(trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    total_time = np.sum(df["Trip Duration"])
    print("The total travel time is: {} :".format(total_time))
    # display mean travel time
    mean_time = np.mean(df["Trip Duration"])
    print("The average travel time is: {} :".format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print("The breakdown of users type is:\n{}".format(user_types))

    # Display counts of gender
    if city != "washington":
        gender = df["Gender"].value_counts()
        print("The breakdown of users gender is:\n{}".format(gender))

        # Display earliest, most recent, and most common year of birth
        oldest_birth = min(df["Birth Year"])
        youngest_birth = max(df["Birth Year"])
        common_birth = df["Birth Year"].mode()[0]
        print(
            "The oldest, youngest and most popular year of birth, respectively is:\n{}, {} and {}".format(
                int(oldest_birth), int(youngest_birth), int(common_birth)
            )
        )
    else:
        print("No data for gender and birth year")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def display_raw_data(city):
    i = 0
    while True:
        try:
            raw_data = pd.read_csv(CITY_DATA[city])
            display_data = input(
                "Would you like to preview the raw data? Enter yes or no.\n"
            ).lower()
            if display_data != "yes":
                print("Thank You")
                break
            print(raw_data[i : i + 5])
            i += 5
        except KeyboardInterrupt:
            print("Thank You")
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(city)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
