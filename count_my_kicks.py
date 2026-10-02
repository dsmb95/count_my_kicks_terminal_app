from datetime import datetime, date
import csv
import os

# VARIABLES THAT WILL OBTAIN DATA FROM THE CSV FILE
# A list of dictionaries containing the number of kicks of the baby per day(date). Populated by the populate_dict() function.
kicks_date_data = []
# A list of dates recorded during the kicks. Populated through the csv file.
recorded_dates = []
# Lists the kick counts in order. Populated through the csv file.
kick_count_list = []

# Reads data from the csv file and to reference the lists.
if os.path.exists('kicks_data.csv'):
    with open('kicks_data.csv') as kicks_data:
        kick_data = csv.DictReader(kicks_data)
        for row in kick_data:
            kick_count_list.append(int(row['count']))
            recorded_dates.append(row['date'])


# VARIABLES THAT WILL MANIPULATE DATA IN CSV
# Records today's kick count
date_today_str = str(date.today())
if len(recorded_dates) > 0 and recorded_dates[-1] == date_today_str:
    kick_count_today = kick_count_list[-1]
else:
    kick_count_today = 0


# Function that ensure the current date is up to date.
# Updates the recorded_date and kick_count_list lists to ensure up to date.
def record_current_date():
    today = str(date.today())
    if len(recorded_dates) == 0 or recorded_dates[-1] != today:
       recorded_dates.append(date.today())
       kick_count_list.append(0)
       return recorded_dates[-1]  
    return recorded_dates[-1]

# Function that updates the kick counts per day.
def kick_counter():
    global kick_count_today
    current_date = record_current_date()
    current_time = datetime.now().strftime("%H:%M")
    
    prompt = input("Did you feel a kick just now? (Y/N) ")
    
    if prompt.lower() == 'y':   
        kick_count_today += 1
        kick_count_list[-1] = kick_count_today
        print("You just recorded a kick on {date} {time}, you have logged {kicks} kicks today!".format(date=current_date, time=current_time, kicks=kick_count_list[-1]))
        return kick_count_today

def update_file(date_data, count_data):
    for row in kicks_date_data:
        if row['date'] == date_data:
            row['count'] = count_data
            return
    kicks_date_data.append({'date': date_data, 'count': count_data})
    
kick_counter()

for i in range(len(recorded_dates)):
    update_file(recorded_dates[i], kick_count_list[i])

# Writes updated data to csv file.
with open('kicks_data.csv', 'w', newline='') as kicks_data:
    fields = ['date', 'count']
    kick_data_writer = csv.DictWriter(kicks_data, fieldnames=fields)
    kick_data_writer.writeheader()
    for item in kicks_date_data:
        kick_data_writer.writerow(item)

print("\n --- Final Data State ---")
print("Dictionary: ", kicks_date_data)
print("Dates List: ", recorded_dates)
print("Kick Counts List: ", kick_count_list)