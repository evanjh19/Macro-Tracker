import os
from datetime import datetime

# Define file paths for various trackers
goal_tracker = 'records/goal.txt'
year_tracker = 'records/year.txt'
month_counter = 'records/month_counter.txt'
month_tracker = 'records/month.txt'
week_tracker = 'records/week.txt'
day_tracker = 'records/day.txt'
macro_records = 'records/macro_records.txt'
weight = 'records/weight_tracker.txt'

def check_quit(input_str):
    # Function to exit the program if the user inputs 'quit'
    if input_str.lower() == 'quit':
        exit()

def print_welcome_message():
    # Function to print the welcome message in a formatted box
    print("\n")
    message_length = len("Macro Tracker")
    box_width = message_length + 6
    print("+" + "-" * box_width + "+")
    print("|" + " " * box_width + "|")
    print("|  " + " Macro Tracker " + "  |")
    print("|" + " " * box_width + "|")
    print("+" + "-" * box_width + "+")
    print("\n")

def load_macro_dict():
    # Function to load the macro records into a dictionary
    macro_dict = {}
    with open(macro_records) as r:
        for line in r:
            first_split = line.split('\t')
            second_split = first_split[1].split()
            second_split = [int(i) for i in second_split]
            macro_dict[first_split[0]] = second_split
    return macro_dict

def get_user_input(prompt, valid_inputs=None, case_sensitive=False, input_type=str):
    while True:
        user_input = input(prompt).strip()
        check_quit(user_input)
        try:
            user_input = input_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")
            continue
        if valid_inputs:
            if case_sensitive:
                if user_input in valid_inputs:
                    return user_input
            else:
                if user_input.lower() in [v.lower() for v in valid_inputs]:
                    return user_input.lower()
            print(f"Invalid input. Please enter one of the following: {', '.join(valid_inputs)}")
        else:
            return user_input

def sanitize_input(input_str):
    # Function to remove any unwanted characters from the input, including tabs, spaces, and returns
    return ''.join(e for e in input_str if e.isalnum())

# Print welcome message and load macro dictionary
print_welcome_message()
macro_dict = load_macro_dict()

running = 'no'
while running != 'yes':
    # Main loop to handle user input and navigate the app
    mode = get_user_input("Which would you like to do? (d: display, t: track, l: log_weight, s: set_goal) ", ['d', 'display', 't', 'track', 'l', 'log_weight', 's', 'set_goal'])

    if mode in ['s', 'set_goal']:
        # Set macro goals
        print('\nSet your macro goals!')
        print('---------------------------------\n')
        print("If you need help determining your macro goals, try visiting https://www.iifym.com/macro-calculator/ and filling out the questionnaire for an estimate of macros that fit your goals.\n")

        carb_goal = get_user_input("What is your daily carb goal? ", input_type=int)
        protein_goal = get_user_input("What is your daily protein goal? ", input_type=int)
        fat_goal = get_user_input("What is your daily fat goal? ", input_type=int)
        calorie_goal = get_user_input("What is your daily calorie goal? ", input_type=int)

        # Write the goals to the goal_tracker file
        with open(goal_tracker, 'w') as gt:
            gt.write(f"{carb_goal} {protein_goal} {fat_goal} {calorie_goal}")

        # Ask if the user is finished tracking macros
        running = get_user_input("Are you finished tracking your macros? (yes or no) ", ['yes', 'no'])

    if mode in ['d', 'display']:
        # Display various tracked data
        print('\nDisplay tracked macros and weight!')
        print('---------------------------------\n')
        show = get_user_input("What would you like to display? (y: yearly_macros, m: monthly_macros, w: weekly_macros, d: daily_macros, g: goal, p: macro_progress, c: weight_change) ", 
                             ['y', 'yearly_macros', 'm', 'monthly_macros', 'w', 'weekly_macros', 'd', 'daily_macros', 'g', 'goal', 'p', 'macro_progress', 'c', 'weight_change'])

        if show in ['g', 'goal']:
            # Display macro goals
            with open(goal_tracker, 'r') as gtd_read:
                for line in gtd_read:
                    line = line.split()
                print('Carbs', 'Protein', 'Fats', 'Calories')
                print(f"{line[0]}\t{line[1]}\t{line[2]}\t{line[3]}")

        if show in ['p', 'macro_progress']:
            # Display progress towards macro goals
            day_totals = [0, 0, 0, 0]
            with open(day_tracker, 'r') as dt_read:
                for line in dt_read:
                    line = line.split()
                    del line[0]
                    line = [int(i) for i in line]
                    day_totals = [x + y for x, y in zip(line, day_totals)]

            if os.path.getsize(goal_tracker) == 0:
                print('You have no macro goals recorded.')
            else:
                with open(goal_tracker) as gt:
                    for line in gt:
                        goals = line.split()

                # Print daily goal progress
                print('\nDaily goal progress')
                print('---------------------------------')
                print(f"carbs: {day_totals[0]}/{goals[0]}\nprotein: {day_totals[1]}/{goals[1]}\nfat: {day_totals[2]}/{goals[2]}\ncalories: {day_totals[3]}/{goals[3]}")

        if show in ['y', 'yearly_macros']:
            # Display yearly macros
            year_totals = [0, 0, 0, 0]
            with open(year_tracker, 'r') as yt_read:
                for line in yt_read:
                    line = line.split()
                    del line[0]
                    line = [int(i) for i in line]
                    year_totals = [x + y for x, y in zip(line, year_totals)]
                print('Carbs', 'Protein', 'Fats', 'Calories')
                print(f"{year_totals[0]}\t{year_totals[1]}\t{year_totals[2]}\t{year_totals[3]}")

        if show in ['m', 'monthly_macros']:
            # Display monthly macros
            month_totals = [0, 0, 0, 0]
            with open(month_tracker, 'r') as mt_read:
                for line in mt_read:
                    line = line.split()
                    del line[0]
                    line = [int(i) for i in line]
                    month_totals = [x + y for x, y in zip(line, month_totals)]
                print('Carbs', 'Protein', 'Fats', 'Calories')
                print(f"{month_totals[0]}\t{month_totals[1]}\t{month_totals[2]}\t{month_totals[3]}")

        if show in ['w', 'weekly_macros']:
            # Display weekly macros
            week_totals = [0, 0, 0, 0]
            with open(week_tracker, 'r') as wt_read:
                for line in wt_read:
                    line = line.split()
                    del line[0]
                    line = [int(i) for i in line]
                    week_totals = [x + y for x, y in zip(line, week_totals)]
                print('Carbs', 'Protein', 'Fats', 'Calories')
                print(f"{week_totals[0]}\t{week_totals[1]}\t{week_totals[2]}\t{week_totals[3]}")

        if show in ['d', 'daily_macros']:
            # Display daily macros
            day_totals = [0, 0, 0, 0]
            with open(day_tracker, 'r') as dt_read:
                for line in dt_read:
                    line = line.split()
                    del line[0]
                    line = [int(i) for i in line]
                    day_totals = [x + y for x, y in zip(line, day_totals)]
                print('Carbs', 'Protein', 'Fats', 'Calories')
                print(f"{day_totals[0]}\t{day_totals[1]}\t{day_totals[2]}\t{day_totals[3]}")

        if show in ['c', 'weight_change']:
            # Display weight change
            if os.path.getsize(weight) == 0:
                print('You have no weights logged.')
            else:
                all_weights = []

                weights = get_user_input("From how many entries back would you like to see your change in weight? ", input_type=int)

                with open(weight, 'r') as wtr:
                    for line in wtr:
                        split_line = line.split()
                        weight = split_line[2]
                        all_weights.append(weight)

                numeric_all_weights = [float(i) for i in all_weights]

                if weights >= len(numeric_all_weights):
                    # Calculate and display statistics for all recorded weights
                    mean = sum(numeric_all_weights) / len(numeric_all_weights)
                    variance = sum((i - mean) ** 2 for i in numeric_all_weights) / len(numeric_all_weights)
                    change = numeric_all_weights[-1] - numeric_all_weights[0]

                    print(f"Average: {mean}")
                    print(f"Variance: {variance}")
                    print(f"Change: {change}")

                if weights < len(numeric_all_weights):
                    # Calculate and display statistics for the specified number of recent weights
                    weight_range = numeric_all_weights[-weights:]
                    mean = sum(weight_range) / len(weight_range)
                    variance = sum((i - mean) ** 2 for i in weight_range) / len(weight_range)
                    change = weight_range[-1] - weight_range[0]

                    print(f"Average: {mean}")
                    print(f"Variance: {variance}")
                    print(f"Change: {change}")

        # Ask if the user is finished tracking macros
        running = get_user_input("Are you finished tracking your macros? (yes or no) ", ['yes', 'no'])

    if mode in ['l', 'log_weight']:
        # Log weight
        print('\nRecord your weight!')
        print('---------------------------------\n')

        now = datetime.now()  # Get current date and time
        lbs = get_user_input("What is your measured weight? ", input_type=float)

        # Append the recorded weight to the weight tracker file
        with open(weight, 'a') as wta:
            wta.write(f"{now.strftime('%d/%m/%Y %H:%M:%S')} {lbs}\n")

        # Ask if the user is finished tracking macros
        running = get_user_input("Are you finished tracking your macros? (yes or no) ", ['yes', 'no'])

    if mode in ['t', 'track']:
        # Track macros
        print('\nTrack your macros!')
        print('---------------------------------\n')

        # Check if it's a new month and update month counter and files if needed
        month = get_user_input("Use the skip shortcut if you are continuing macro tracking for the same day.\nIs this a new month? (yes, no, or skip) ", ['yes', 'no', 'skip'])

        if month == 'yes':
            if os.path.getsize(month_counter) == 0:
                month_count = 0
            else:
                with open(month_counter, 'r') as mt_read:
                    for line in mt_read:
                        month_count = int(line)

            month_count += 1
            if month_count >= 12:
                # If a year has passed, archive month data to year file
                month_count = 0
                with open(month_tracker) as month:
                    with open(year_tracker, 'a') as year:
                        for line in month:
                            year.write(line)
                with open(month_tracker, 'r+') as month_empty:
                    month_empty.truncate(0)  # Clear month tracker file
            else:
                with open(month_tracker, 'a') as month:
                    month.write('\n')

            # Update the month counter file
            with open(month_counter, 'w') as mc:
                mc.write(str(month_count))

        if month in ['yes', 'no']:
            # Check if it's a new week and update week tracker file if needed
            week = get_user_input("Is this a new week? (yes or no) ", ['yes', 'no'])

            if week == 'yes':
                with open(week_tracker) as week:
                    with open(month_tracker, 'a') as month:
                        for line in week:
                            month.write(line)
                with open(week_tracker, 'r+') as week_empty:
                    week_empty.truncate(0)  # Clear week tracker file
                    
        if month in ['yes', 'no']:
        	# Check if it's a new day and update day tracker file if needed
        	day = get_user_input("Is this a new day? (yes or no) ", ['yes', 'no'])
        	if day == 'yes':
        		with open(day_tracker) as day:
        			with open(week_tracker, 'a') as week:
        				for line in day:
        					week.write(line)
        		with open(day_tracker, 'r+') as day_empty:
        			day_empty.truncate(0)  # Clear day tracker file

        entry_totals = [0, 0, 0, 0]  # Initialize total macros for the day
        option = 'yes'
        while option != 'no':
            # Loop to enter individual food items
            print("To see a list of the items with macros recorded, input 'records'")
            entry = get_user_input("What would you like to enter? ")

            if entry == 'records':
                # Display list of items with macros recorded
                for i in macro_dict:
                    print(i)
            else:
                entry = sanitize_input(entry)  # Sanitize the entry to remove any unwanted characters
                if entry in macro_dict:
                    # If the item is in the macro dictionary, record its macros
                    times = int(get_user_input("How many of this item would you like to enter? ", input_type=int))
                    entered = f"{entry} {macro_dict[entry][0] * times} {macro_dict[entry][1] * times} {macro_dict[entry][2] * times} {macro_dict[entry][3] * times}\n"
                    custom_entry = [int(macro_dict[entry][0] * times), int(macro_dict[entry][1] * times), int(macro_dict[entry][2] * times), int(macro_dict[entry][3] * times)]
                    entry_totals = [x + y for x, y in zip(custom_entry, entry_totals)]
                    # Append the entered item to the day tracker file
                    with open(day_tracker, "a") as day_append:
                        day_append.write(entered)
                else:
                    # If the item is not in the macro dictionary, enter its macros manually
                    print('You will need to enter details for this item manually...')
                    custom_carb = get_user_input("What is the total carb content? ", input_type=int)
                    custom_protein = get_user_input("What is the total protein content? ", input_type=int)
                    custom_fat = get_user_input("What is the total fat content? ", input_type=int)
                    custom_calorie = get_user_input("What is the total calorie content? ", input_type=int)

                    save = get_user_input("Would you like to save this to your records? (yes or no) ", ['yes', 'no'])

                    if save == 'yes':
                        # Save the custom item to the macro records
                        data = f"{sanitize_input(entry)}\t{custom_carb} {custom_protein} {custom_fat} {custom_calorie}\n"
                        with open(macro_records, 'a') as file:
                            file.write(data)

                    times = int(get_user_input("How many of this item would you like to enter? ", input_type=int))
                    custom_carb = str(int(custom_carb) * times)
                    custom_protein = str(int(custom_protein) * times)
                    custom_fat = str(int(custom_fat) * times)
                    custom_calorie = str(int(custom_calorie) * times)

                    entered = f"{sanitize_input(entry)} {custom_carb} {custom_protein} {custom_fat} {custom_calorie}\n"
                    custom_entry = [int(custom_carb), int(custom_protein), int(custom_fat), int(custom_calorie)]
                    entry_totals = [x + y for x, y in zip(custom_entry, entry_totals)]
                    
                    # Append the entered item to the day tracker file
                    with open(day_tracker, "a") as day_append:
                        day_append.write(entered)

            # Ask if the user wants to enter another item
            option = get_user_input("Would you like to enter another item? (yes or no) ", ['yes', 'no'])

        # Print the total macros entered for the day
        print('Total macros entered:')
        print('Carbs', 'Protein', 'Fats', 'Calories')
        print(f"{entry_totals[0]}\t{entry_totals[1]}\t{entry_totals[2]}\t{entry_totals[3]}")

        # Update the day's total macros by summing up all entries in the day tracker
        day_totals = [0, 0, 0, 0]
        with open(day_tracker, 'r') as dt_read:
            for line in dt_read:
                line = line.split()
                del line[0]
                line = [int(i) for i in line]
                day_totals = [x + y for x, y in zip(line, day_totals)]

        if os.path.getsize(goal_tracker) == 0:
            print('You have no macro goals recorded.')
        else:
            with open(goal_tracker) as gt:
                for line in gt:
                    goals = line.split()

        # Ask if the user is finished tracking macros
        running = get_user_input("Are you finished tracking your macros? (yes or no) ", ['yes', 'no'])
