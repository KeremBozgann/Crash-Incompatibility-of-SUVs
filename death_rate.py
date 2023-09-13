
import numpy as np
import pandas as pd

def suv_mean_average_death_rate(year):

    df = pd.read_csv(f'data/{year}/Vehicle.CSV', encoding ="ISO-8859-1", low_memory=False)

    two_vehicle_cases = df.groupby("ST_CASE").filter(lambda x: len(x) == 2)

    two_vehicle_cases_ampute = two_vehicle_cases[["DEATHS", "ST_CASE", "MOD_YEAR", "BODY_TYP"]]

    if year < 1991:
        two_vehicle_cases_ampute_suv = two_vehicle_cases_ampute[two_vehicle_cases_ampute['BODY_TYP'].isin([12, 56, 67])]

    else:
        two_vehicle_cases_ampute_suv = two_vehicle_cases_ampute[two_vehicle_cases_ampute['BODY_TYP'].isin([14, 15, 16, 19])]

    if year < 1998:
        year_2_digit = year %100
        suv_entries_new_model = two_vehicle_cases_ampute_suv[two_vehicle_cases_ampute_suv['MOD_YEAR'] > (year_2_digit - 4)]

    else:
        suv_entries_new_model = two_vehicle_cases_ampute_suv[two_vehicle_cases_ampute_suv['MOD_YEAR'] > (year - 4)]

    if year<1998:
        year_2_dig = year % 100

        suv_entries_new_model['Death_Rate'] = suv_entries_new_model['DEATHS'] / np.maximum(0.5, year_2_dig - suv_entries_new_model['MOD_YEAR'] )
        # suv_suv_crashes_new_model['Registration_Years'] = year_2_dig - suv_suv_crashes_new_model['MOD_YEAR']

    else:
        suv_entries_new_model['Death_Rate'] = suv_entries_new_model['DEATHS'] / np.maximum(0.5, year - suv_entries_new_model['MOD_YEAR'] )

        # suv_suv_crashes_new_model['Registration_Years'] = year - suv_suv_crashes_new_model['MOD_YEAR']

    average_death_rate = suv_entries_new_model['Death_Rate'].mean()

    print(f"suv death rate: {average_death_rate}")
    return average_death_rate


def pass_car_average_death_rate(year):

    df = pd.read_csv(f'data/{year}/Vehicle.CSV', encoding ="ISO-8859-1", low_memory=False)

    two_vehicle_cases = df.groupby("ST_CASE").filter(lambda x: len(x) == 2)

    two_vehicle_cases_ampute = two_vehicle_cases[["DEATHS", "ST_CASE", "MOD_YEAR", "BODY_TYP"]]


    if year < 1991:
        two_vehicle_cases_ampute_passenger = two_vehicle_cases_ampute[two_vehicle_cases_ampute['BODY_TYP'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9 , 17 ])]

    else:
        two_vehicle_cases_ampute_passenger = two_vehicle_cases_ampute[two_vehicle_cases_ampute['BODY_TYP'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9 , 17 ])]




    if year < 1998:
        year_2_digit = year %100
        passenger_entries_new_model = two_vehicle_cases_ampute_passenger[
                                two_vehicle_cases_ampute_passenger['MOD_YEAR'] > (year_2_digit - 4)]

    else:
        passenger_entries_new_model = two_vehicle_cases_ampute_passenger[
                                two_vehicle_cases_ampute_passenger['MOD_YEAR'] > (year - 4)]




    if year<1998:
        year_2_dig = year % 100

        passenger_entries_new_model['Death_Rate'] =  passenger_entries_new_model['DEATHS'] / np.maximum(0.5, year_2_dig -  passenger_entries_new_model['MOD_YEAR'] )
        # suv_suv_crashes_new_model['Registration_Years'] = year_2_dig - suv_suv_crashes_new_model['MOD_YEAR']

    else:
        passenger_entries_new_model['Death_Rate'] =  passenger_entries_new_model['DEATHS'] / np.maximum(0.5, year -  passenger_entries_new_model['MOD_YEAR'] )

        # suv_suv_crashes_new_model['Registration_Years'] = year - suv_suv_crashes_new_model['MOD_YEAR']

    average_death_rate_passenger =  passenger_entries_new_model['Death_Rate'].mean()

    print(f"passenger death rate: {average_death_rate_passenger}")
    return average_death_rate_passenger





year_groups = [[2017, 2018, 2019, 2020], [2013, 2014, 2015, 2016], [2009, 2010, 2011, 2012], [2005, 2006, 2007, 2008],
               [2001, 2002, 2003, 2004], [1997, 1998, 1999, 2000], [1993, 1994, 1995, 1996],  [1989, 1990, 1991, 1992]
               ]

pass_avg_death_rate_year_groups = []
suv_avg_death_rate_year_groups = []

for year_group in year_groups:
    pass_avg_death_rate = []
    suv_avg_death_rate = []
    for year in year_group:
        suv_mean_death = suv_mean_average_death_rate(year)
        pass_mean_death = pass_car_average_death_rate(year)
        if suv_mean_death !=0:
            suv_avg_death_rate.append(suv_mean_death)
        if pass_mean_death != 0:
            pass_avg_death_rate.append(pass_mean_death)

    group_suv_death_rate =  np.mean(np.array(suv_avg_death_rate))
    group_passenger_car_death_rate =  np.mean(np.array(pass_avg_death_rate))
    print(f"average SUV death rate between {year_group}:", group_suv_death_rate )
    print(f"average Passanger car death rate between {year_group}:",group_passenger_car_death_rate)

    pass_avg_death_rate_year_groups.append(group_passenger_car_death_rate)
    suv_avg_death_rate_year_groups.append(group_suv_death_rate)


print("pass_avg_death_rate_by_years:", pass_avg_death_rate_year_groups)
print("suv_avg_death_rate_by_years:", suv_avg_death_rate_year_groups)



import matplotlib.pyplot as plt

years = ['1989-1992', '1993-1996', '1997-2000', '2001-2004', '2005-2008', '2009-2012', '2013-2016', '2017-2020']

plt.figure(figsize=(8, 6))
plt.plot(years, np.flip(suv_avg_death_rate_year_groups), label='SUV death rate', marker='s', color = 'green')
plt.plot(years, np.flip(pass_avg_death_rate_year_groups), label='Passanger car death rate', marker='s', color = 'blue')

plt.title('Death Rate graph for SUVs and Passanger cars')
plt.xlabel('Years')
plt.ylabel('Rate')
plt.legend()

plt.xticks(rotation=45)


plt.tight_layout()
plt.savefig('plots/death_rate.png')

plt.show()


