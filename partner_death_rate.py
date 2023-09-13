import numpy as np
import pandas as pd

def suv_mean_partner_death_rate(year):

    df = pd.read_csv(f'data/{year}/Vehicle.CSV', encoding ="ISO-8859-1", low_memory=False)

    two_vehicle_cases = df.groupby("ST_CASE").filter(lambda x: len(x) == 2)

    two_vehicle_cases_ampute = two_vehicle_cases[["DEATHS", "ST_CASE", "MOD_YEAR", "BODY_TYP"]]

    grouped = two_vehicle_cases_ampute.groupby('ST_CASE')

    def filter_suv_group(group, year):
        # Check if both vehicles in the group are SUVs.
        if year < 1991:
            if any(group['BODY_TYP'].isin([12, 56, 67])):
                return group
        else:
            if any(group['BODY_TYP'].isin([14, 15, 16, 19])):
                return group

    suv_crashes  = pd.concat([group for _, group in grouped if filter_suv_group(group, year) is not None])




    suv_group = suv_crashes.groupby("ST_CASE")

    def filter_out_when_suv_old(group, year):
        if year < 1991:
            suv_condition = (group['BODY_TYP'].isin([12, 56, 67]))
        else:
            suv_condition = (group['BODY_TYP'].isin([14, 15, 16, 19]))

        if year < 1998:
            year_2_dig = year % 100
            year_condition = (group['MOD_YEAR'].isin( [year_2_dig, year_2_dig-1,year_2_dig-2,year_2_dig-3,
                                                       year_2_dig-4]))
        else:
            year_condition = (group['MOD_YEAR'].isin( [year, year-1, year-2, year-3, year-4]))

        combined_condition = suv_condition & year_condition
        if combined_condition.any():
            return group


    suv_new_model = pd.concat(
        [group for _, group in suv_group if filter_out_when_suv_old(group, year) is not None])

    if year<1998:
        year_2_dig = year % 100

        suv_new_model['Death_Rate'] = suv_new_model['DEATHS'] / \
                                                        np.maximum(0.5, year_2_dig - suv_new_model['MOD_YEAR'] )
        suv_new_model['Registration_Years'] = year_2_dig - suv_new_model['MOD_YEAR']

    else:
        suv_new_model['Death_Rate'] = suv_new_model['DEATHS'] /\
                                                        np.maximum(0.5, year - suv_new_model['MOD_YEAR'] )

        suv_new_model['Registration_Years'] = year - suv_new_model['MOD_YEAR']

    if year < 1991:
        suv_new_model = suv_new_model[~suv_new_model['BODY_TYP'].isin([12, 56, 67])]

    else:
        suv_new_model = suv_new_model[~suv_new_model['BODY_TYP'].isin([14, 15, 16, 19])]

    average_partner_death_rate_suv = suv_new_model['Death_Rate'].mean()

    print(f"suv crashes partner death rate: {average_partner_death_rate_suv}")
    return average_partner_death_rate_suv

def pass_car_average_partner_death_rate(year):

    df = pd.read_csv(f'data/{year}/Vehicle.CSV', encoding ="ISO-8859-1", low_memory=False)

    two_vehicle_cases = df.groupby("ST_CASE").filter(lambda x: len(x) == 2)

    two_vehicle_cases_ampute = two_vehicle_cases[["DEATHS", "ST_CASE", "MOD_YEAR", "BODY_TYP"]]

    grouped = two_vehicle_cases_ampute.groupby('ST_CASE')

    def filter_passenger_group(group, year):
        # Check if both vehicles in the group are SUVs.
        if year < 1991:
            if any(group['BODY_TYP'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9 , 17 ])):
                return group
        else:
            if any(group['BODY_TYP'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9 , 17 ])):
                return group

    passenger_crashes  = pd.concat([group for _, group in grouped if filter_passenger_group(group, year) is not None])




    passenger_group = passenger_crashes.groupby("ST_CASE")

    def filter_out_when_passenger_old(group, year):
        if year < 1991:
            passenger_condition = (group['BODY_TYP'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9 , 17 ]))
        else:
            passenger_condition = (group['BODY_TYP'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9 , 17 ]))

        if year < 1998:
            year_2_dig = year % 100
            year_condition = (group['MOD_YEAR'].isin([year_2_dig, year_2_dig - 1, year_2_dig - 2, year_2_dig - 3,
                                                      year_2_dig - 4]))
        else:
            year_condition = (group['MOD_YEAR'].isin([year, year - 1, year - 2, year - 3, year - 4]))

        combined_condition = passenger_condition & year_condition
        if combined_condition.any():
            return group


    passenger_new_model = pd.concat(
        [group for _, group in passenger_group if filter_out_when_passenger_old(group, year) is not None])

    if year<1998:
        year_2_dig = year % 100

        passenger_new_model['Death_Rate'] = passenger_new_model['DEATHS'] / \
                                                        np.maximum(0.5, year_2_dig - passenger_new_model['MOD_YEAR'] )
        passenger_new_model['Registration_Years'] = year_2_dig - passenger_new_model['MOD_YEAR']

    else:
        passenger_new_model['Death_Rate'] = passenger_new_model['DEATHS'] /\
                                                        np.maximum(0.5, year - passenger_new_model['MOD_YEAR'] )

        passenger_new_model['Registration_Years'] = year - passenger_new_model['MOD_YEAR']

    if year < 1991:
        passenger_new_model = passenger_new_model[~passenger_new_model['BODY_TYP'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9 , 17 ])]

    else:
        passenger_new_model = passenger_new_model[~passenger_new_model['BODY_TYP'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9 , 17 ])]

    average_partner_death_rate_passenger = passenger_new_model['Death_Rate'].mean()

    print(f"passenger crashes partner death rate: {average_partner_death_rate_passenger}")
    return average_partner_death_rate_passenger





year_groups = [[2017, 2018, 2019, 2020], [2013, 2014, 2015, 2016], [2009, 2010, 2011, 2012], [2005, 2006, 2007, 2008],
               [2001, 2002, 2003, 2004], [1997, 1998, 1999, 2000], [1993, 1994, 1995, 1996],  [1989, 1990, 1991, 1992]
               ]

# year_groups = [[1997, 1998, 1999, 2000], [1993, 1994, 1995, 1996],  [1989, 1990, 1991, 1992]
#                ]
#

pass_avg_death_rate_year_groups = []
suv_avg_death_rate_year_groups = []

for year_group in year_groups:
    pass_avg_death_rate = []
    suv_avg_death_rate = []
    for year in year_group:
        suv_mean_death = suv_mean_partner_death_rate(year)
        pass_mean_death = pass_car_average_partner_death_rate(year)
        if suv_mean_death !=0:
            suv_avg_death_rate.append(suv_mean_death)
        if pass_mean_death != 0:
            pass_avg_death_rate.append(pass_mean_death)

    group_suv_death_rate =  np.mean(np.array(suv_avg_death_rate))
    group_passenger_car_death_rate =  np.mean(np.array(pass_avg_death_rate))
    print(f"average SUV partner death rate between {year_group}:", group_suv_death_rate )
    print(f"average Passanger car partner death rate between {year_group}:",group_passenger_car_death_rate)

    pass_avg_death_rate_year_groups.append(group_passenger_car_death_rate)
    suv_avg_death_rate_year_groups.append(group_suv_death_rate)


print("pass_avg_death_rate_by_years:", pass_avg_death_rate_year_groups)
print("suv_avg_death_rate_by_years:", suv_avg_death_rate_year_groups)





import matplotlib.pyplot as plt

years = ['1989-1992', '1993-1996', '1997-2000', '2001-2004', '2005-2008', '2009-2012', '2013-2016', '2017-2020']

plt.figure(figsize=(8, 6))
plt.plot(years, np.flip(suv_avg_death_rate_year_groups), label='SUV partner death rate', marker='s', color = 'green')
plt.plot(years, np.flip(pass_avg_death_rate_year_groups), label='Passanger car partner death rate', marker='s', color = 'blue')

plt.title('Partner Death Rate graph for SUVs and Passanger cars')
plt.xlabel('Years')
plt.ylabel('Rate')
plt.legend()

plt.xticks(rotation=45)


plt.tight_layout()
plt.savefig('plots/partner_death_rate.png')

plt.show()




