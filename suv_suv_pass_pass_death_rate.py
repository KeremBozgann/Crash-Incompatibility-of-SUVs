import numpy as np
import pandas as pd


def suv_suv_mean_average_death_rate(year, filter_old = True):

    df = pd.read_csv(f'data/{year}/Vehicle.CSV', encoding ="ISO-8859-1", low_memory=False)

    two_vehicle_cases = df.groupby("ST_CASE").filter(lambda x: len(x) == 2)

    two_vehicle_cases_ampute = two_vehicle_cases[["DEATHS", "ST_CASE", "MOD_YEAR", "BODY_TYP"]]

    grouped = two_vehicle_cases_ampute.groupby('ST_CASE')

    def filter_non_suv_group(group, year):
        if year < 1991:
            if all(group['BODY_TYP'].isin([12, 56, 67])):
                return group
        else:
            if all(group['BODY_TYP'].isin([14, 15, 16, 19])):
                return group

    suv_suv_crashes  = pd.concat([group for _, group in grouped if filter_non_suv_group(group, year) is not None])



    suv_suv_group = suv_suv_crashes.groupby("ST_CASE")
    def filter_out_when_both_suvs_old(group, year):
        if year< 1998:
            year_2_dig = year%100
            if any(group['MOD_YEAR'].isin([year_2_dig,year_2_dig-1, year_2_dig-2, year_2_dig-3,year_2_dig-4])):
                return group
        else:
            if any(group['MOD_YEAR'].isin([year, year-1, year-2, year-3, year-4])):
                return group

    try:
        if filter_old:
            suv_suv_crashes_new_model  = pd.concat([group for _, group in suv_suv_group if filter_out_when_both_suvs_old(group, year) is not None])
        else:
            suv_suv_crashes_new_model = suv_suv_crashes
        print(f"Number of SUV-SUV crashes in the year {year}: ", len(suv_suv_crashes_new_model))
    except:
        print("No suv crashes with new model")
        return 0


    if year<1998:
        year_2_dig = year % 100

        suv_suv_crashes_new_model['Death_Rate'] = suv_suv_crashes_new_model['DEATHS'] / (0.5 + year_2_dig - suv_suv_crashes['MOD_YEAR'] )
        suv_suv_crashes_new_model['Registration_Years'] = year_2_dig - suv_suv_crashes_new_model['MOD_YEAR']

    else:
        suv_suv_crashes_new_model['Death_Rate'] = suv_suv_crashes_new_model['DEATHS'] / (0.5 + year - suv_suv_crashes['MOD_YEAR'] )

        suv_suv_crashes_new_model['Registration_Years'] = year - suv_suv_crashes_new_model['MOD_YEAR']

    average_death_rate = suv_suv_crashes_new_model['Death_Rate'].mean()

    print(f"SUV-SUV crashes death rate: {average_death_rate} in year {year}")
    return average_death_rate

def pass_car_pass_car_average_death_rate(year, filter_old = True):

    df = pd.read_csv(f'data/{year}/Vehicle.CSV', encoding ="ISO-8859-1", low_memory=False)

    two_vehicle_cases = df.groupby("ST_CASE").filter(lambda x: len(x) == 2)

    two_vehicle_cases_ampute = two_vehicle_cases[["DEATHS", "ST_CASE", "MOD_YEAR", "BODY_TYP"]]

    grouped = two_vehicle_cases_ampute.groupby('ST_CASE')

    def filter_non_passenger_car_group(group):
        if all(group['BODY_TYP'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9 , 17 ])):
            return group

    pass_pass_crashes  = pd.concat([group for _, group in grouped if filter_non_passenger_car_group(group) is not None])



    pass_pass_group = pass_pass_crashes.groupby("ST_CASE")
    def filter_out_when_both_pass_old(group, year):
        if year< 1998:
            year_2_dig = year%100
            if any(group['MOD_YEAR'].isin([year_2_dig,year_2_dig-1, year_2_dig-2, year_2_dig-3,year_2_dig-4])):
                return group
        else:
            if any(group['MOD_YEAR'].isin([year, year-1, year-2, year-3, year-4])):
                return group
    if filter_old:
        pass_pass_crashes_new_model  = pd.concat([group for _, group in pass_pass_group if filter_out_when_both_pass_old(group, year) is not None])
    else:
        pass_pass_crashes_new_model  = pass_pass_crashes
    print(f"Number of Passenger-Passenger crashes in the year {year}: ", len(pass_pass_crashes_new_model))

    if year<1998:
        year_2_dig = year % 100

        pass_pass_crashes_new_model['Death_Rate'] = pass_pass_crashes_new_model['DEATHS'] / (0.5 + year_2_dig - pass_pass_crashes_new_model['MOD_YEAR'] )
        pass_pass_crashes_new_model['Registration_Years'] = year_2_dig - pass_pass_crashes_new_model['MOD_YEAR']

    else:
        pass_pass_crashes_new_model['Death_Rate'] = pass_pass_crashes_new_model['DEATHS'] / (0.5 + year - pass_pass_crashes_new_model['MOD_YEAR'] )
        pass_pass_crashes_new_model['Registration_Years'] = year - pass_pass_crashes_new_model['MOD_YEAR']

    average_death_rate_pass = pass_pass_crashes_new_model['Death_Rate'].mean()

    print(f"Passenger car-passenger car crashes death rate: {average_death_rate_pass} in the year {year}")

    return average_death_rate_pass

# year_groups = [[2017, 2018, 2019, 2020], [2013, 2014, 2015, 2016], [2009, 2010, 2011, 2012], [2005, 2006, 2007, 2008],
#                [2001, 2002, 2003, 2004]]
# year_groups  = [[1997, 1998, 1999, 2000], [1993, 1994, 1995, 1996],  [1989, 1990, 1991, 1992]]
# year_groups  = [ [1989, 1990, 1991, 1992]]
# years =[2017, 2018, 2019]



year_groups = [[2017, 2018, 2019, 2020], [2013, 2014, 2015, 2016], [2009, 2010, 2011, 2012], [2005, 2006, 2007, 2008],
               [2001, 2002, 2003, 2004], [1997, 1998, 1999, 2000], [1993, 1994, 1995, 1996],  [1989, 1990, 1991, 1992]
               ]

pass_avg_death_rate_year_groups = []
suv_avg_death_rate_year_groups = []

for year_group in year_groups:
    pass_avg_death_rate = []
    suv_avg_death_rate = []
    for year in year_group:
        suv_suv_mean_death = suv_suv_mean_average_death_rate(year, filter_old = False)
        pass_pass_mean_death = pass_car_pass_car_average_death_rate(year, filter_old= False)
        if suv_suv_mean_death !=0:
            suv_avg_death_rate.append(suv_suv_mean_death)
        if pass_pass_mean_death != 0:
            pass_avg_death_rate.append(pass_pass_mean_death)

    group_suv_death_rate =  np.mean(np.array(suv_avg_death_rate))
    group_passenger_car_death_rate =  np.mean(np.array(pass_avg_death_rate))
    print(f"average SUV-SUV death rate between {year_group}:", group_suv_death_rate )
    print(f"average Passanger car- Passanger car death rate between {year_group}:",group_passenger_car_death_rate)

    pass_avg_death_rate_year_groups.append(group_passenger_car_death_rate)
    suv_avg_death_rate_year_groups.append(group_suv_death_rate)


print("pass_avg_death_rate_by_years:", pass_avg_death_rate_year_groups)
print("suv_avg_death_rate_by_years:", suv_avg_death_rate_year_groups)


import matplotlib.pyplot as plt

years = ['1989-1992', '1993-1996', '1997-2000', '2001-2004', '2005-2008', '2009-2012', '2013-2016', '2017-2020']

plt.figure(figsize=(8, 6))
plt.plot(years, np.flip(suv_avg_death_rate_year_groups), label='SUV-SUV', marker='s', color = 'green')
plt.plot(years, np.flip(pass_avg_death_rate_year_groups), label='Passanger car-Passanger car', marker='s', color = 'blue')

plt.title('Death Rate in crashes between the same type vehiclew')
plt.xlabel('Years')
plt.ylabel('Rate')
plt.legend()

plt.xticks(rotation=45)


plt.tight_layout()
plt.savefig('plots/death_rate_between_same_type.png')

plt.show()




