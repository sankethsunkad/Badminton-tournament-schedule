from collect_sheet_data import import_csv
import pandas as pd
import json
from check_duplicate import read_input
from schedule_tournament import schedule
import datetime
import random


def collect_fluid_pronouns(data):
    filtered_data = [record['Email Address'] for record in data if record['pronouns'] == 'they/them']
    return filtered_data


def collect_singles_list(data, pronoun):
    str = 'Singles'
    filtered_data = [record['Email Address'] for record in data if record['pronouns'] == pronoun and (str in record["Alright, folks, it's decision time! Pick your poison - which badminton battlegrounds will you conquer? "])]
    return filtered_data


def collect_doubles_list(data, pronoun):
    filtered_data = [[record['Email Address'], record["Ready to double up with a partner who shares your pronouns? Go ahead and drop their email ID, and let's hit the badminton court together for some fun!"]] for record in data if record['pronouns'] == pronoun and (record['Feeling up for some epic doubles action with a partner who shares your pronouns?']=='Yes' and record["Ready to double up with a partner who shares your pronouns? Go ahead and drop their email ID, and let's hit the badminton court together for some fun!"]!='')]
    return filtered_data


def collect_mixed_doubles_list(data):
    filtered_data = [[record['Email Address'], record["Who's your mixed doubles dance partner? Drop their email ID so we can groove together on the badminton court!"]] for record in data if (record['Feeling up for some epic doubles action with a partner who shares your pronouns?']=='Yes' and record["Who's your mixed doubles dance partner? Drop their email ID so we can groove together on the badminton court!"]!='')]
    return filtered_data


def check_doubles_null(data, pronoun):
    filtered_data = [record['Email Address'] for record in data if record['pronouns'] == pronoun and  record['Feeling up for some epic doubles action with a partner who shares your pronouns?']=='Yes' and record["Ready to double up with a partner who shares your pronouns? Go ahead and drop their email ID, and let's hit the badminton court together for some fun!"]=='']
    return filtered_data


def check_mixed_doubles_null(data, pronoun):
    filtered_data = [record['Email Address'] for record in data if record['pronouns'] == pronoun and (record["Feeling like mixing it up on the court? Ready to bring the 'mixed' to 'doubles'? Sign up and let's see if you've got the perfect partner in crime!"]=='Yes' and record["Who's your mixed doubles dance partner? Drop their email ID so we can groove together on the badminton court!"]=='')]
    return filtered_data


def remove_duplicate_nested_lists(original_list):
    tuple_list = [tuple(inner) for inner in original_list]
    deduplicated = list(dict.fromkeys(tuple_list).keys())
    return [list(inner) for inner in deduplicated]

def sort_list(lst):
    for i in range(len(lst)):
        lst[i] = sorted(lst[i])
    return lst


def remove_items(single_list, nested_list):
    return [item for item in single_list if not any(item in sublist for sublist in nested_list)]


def remove_duplicatesublists(nested_list):
    filtered_list = [sub_list for sub_list in nested_list if len(set(sub_list)) > 1]
    single_list = [item for sub_list in nested_list if len(set(sub_list)) == 1 for item in sub_list]
    return filtered_list, single_list


def random_team_generator(single_list, nested_list):
    while(len(single_list)!=0):
        if(len(single_list) > 1):
            team1 = single_list.pop(random.randint(0, len(single_list)-1))
            team2 = single_list.pop(random.randint(0, len(single_list)-1))
            team = [team1, team2]
            nested_list.append(team)
    return nested_list, single_list


def mixed_random_team_geenrator(men_mixed, women_mixed):
    append_list = []
    while (len(women_mixed) != 0):
        team1 = women_mixed.pop(random.randint(0, len(women_mixed)-1))
        team2 = men_mixed.pop(random.randint(0, len(men_mixed)-1))
        team = [team1, team2]
        append_list.append(team)
    return men_mixed, append_list


def remove_single_list_duplicates_nested_list(single_list, nested_list):
    lst_to_remove = [item for sublist in nested_list for item in sublist]
    lst_result = [item for item in single_list if item not in lst_to_remove]
    return lst_result


def fetch_data():
    data = import_csv()
    df = pd.DataFrame(data)
    df = df.fillna('')
    processed_data = df.T.to_dict().values()

    fluid_pronoun_list = collect_fluid_pronouns(data)
    print("fluid_pronoun_list : ",fluid_pronoun_list)

    men_singles_list = collect_singles_list(data, 'he/him')
    print("mens single list : ",men_singles_list)

    women_singles_list = collect_singles_list(data, 'she/her')
    print("women single list :",women_singles_list)

    men_doubles_list = collect_doubles_list(data, 'he/him')
    men_doubles_list = sort_list(men_doubles_list)
    mens_doubles_list_final = remove_duplicate_nested_lists(men_doubles_list)
    mens_doubles_list_final, men_doubles_append_list = remove_duplicatesublists(mens_doubles_list_final)
    #print("mens doubles final list : ",mens_doubles_list_final)

    women_doubles_list = collect_doubles_list(data, 'she/her')
    women_doubles_list = sort_list(women_doubles_list)
    womens_doubles_list_final = remove_duplicate_nested_lists(women_doubles_list)
    womens_doubles_list_final, women_doubles_append_list = remove_duplicatesublists(womens_doubles_list_final)
    print("women doubles list : ",womens_doubles_list_final)

    mixed_doubles_list = collect_mixed_doubles_list(processed_data)
    mixed_doubles_list = sort_list(mixed_doubles_list)
    mixed_doubles_list_final = remove_duplicate_nested_lists(mixed_doubles_list)
    mixed_doubles_list_final, men_mixed_doubles_append_list = remove_duplicatesublists(mixed_doubles_list_final)
    print("mixed doubles list : ", mixed_doubles_list_final)

    men_doubles_null = check_doubles_null(data, 'he/him')
    men_doubles_null = men_doubles_null + men_doubles_append_list
    men_doubles_null = remove_items(men_doubles_null, mens_doubles_list_final)
    men_doubles_null = remove_single_list_duplicates_nested_list(men_doubles_null, mens_doubles_list_final)
    #men_doubles_null = list(set(men_doubles_null))
    #mens_doubles_list_final, men_doubles_null = random_team_generator(men_doubles_null, mens_doubles_list_final)
    #print("men doubles with no partner : ",men_doubles_null)

    #print("men doubles after random pairing: ", mens_doubles_list_final)

    women_doubles_null = check_doubles_null(data, 'she/her')
    women_doubles_null = women_doubles_null + women_doubles_append_list
    women_doubles_null = remove_items(women_doubles_null, womens_doubles_list_final)
    women_doubles_null = remove_single_list_duplicates_nested_list(women_doubles_null, womens_doubles_list_final)
    women_doubles_null = list(set(women_doubles_null))
    womens_doubles_list_final, women_doubles_null = random_team_generator(women_doubles_null, womens_doubles_list_final)
    print("women doubles with no partner : ",women_doubles_null)
    print("women doubles after random pairing : ", womens_doubles_list_final)

    men_mixed_null = check_mixed_doubles_null(processed_data, 'he/him')
    men_mixed_null = men_mixed_null+men_mixed_doubles_append_list
    men_mixed_null = remove_items(men_mixed_null, mixed_doubles_list_final)
    men_mixed_null = remove_single_list_duplicates_nested_list(men_mixed_null, mixed_doubles_list_final)
    men_mixed_null = list(set(men_mixed_null))

    women_mixed_null = check_mixed_doubles_null(processed_data, 'she/her')
    women_mixed_null = remove_items(women_mixed_null, mixed_doubles_list_final)
    women_mixed_null = remove_single_list_duplicates_nested_list(women_mixed_null, mixed_doubles_list_final)
    women_mixed_null = list(set(women_mixed_null))
    men_mixed_null, append_list = mixed_random_team_geenrator(men_mixed_null, women_mixed_null)
    mixed_doubles_list_final = mixed_doubles_list_final + append_list
    print("List of men who opted for mixed doubles with no female partner : ",men_mixed_null)
    print("List of women who opted for mixed doubles with no male partner : ",women_mixed_null)
    print("mixed doubles final list : ", mixed_doubles_list_final)

    men_doubles_append_null = remove_single_list_duplicates_nested_list(men_mixed_null, mens_doubles_list_final)
    men_doubles_null = men_doubles_null + men_doubles_append_null
    men_doubles_null = list(set(men_doubles_null))
    mens_doubles_list_final, men_doubles_null = random_team_generator(men_doubles_null, mens_doubles_list_final)
    print("men doubles with no partner : ", men_doubles_null)
    print("men doubles after random pairing: ", mens_doubles_list_final)


    data = {
        "singles": men_singles_list,
        "doubles": mens_doubles_list_final,
        "mixed": mixed_doubles_list_final
    }
    json_data = json.dumps(data)
    read_input(json_data)

    json_final_data = {
        "men_singles": men_singles_list,
        "women_singles": women_singles_list,
        "men_doubles": mens_doubles_list_final,
        "women_doubles": womens_doubles_list_final,
        "mixed": mixed_doubles_list_final
    }
    print(json_final_data)
    courts = ['Premium Hybrid Court 1','Premium Hybrid Court 2','Premium Hybrid Court 3','Premium Hybrid Court 4','Premium Hybrid Court 5','Premium Hybrid Court 6', 'Synthetic Court 1','Synthetic Court 2','Synthetic Court 3']
    court = ['Premium Hybrid Court 1','Premium Hybrid Court 3','Premium Hybrid Court 5','Synthetic Court 1']
    schedule(men_singles_list, court)
    court = ['Premium Hybrid Court 2','Synthetic Court 3']
    schedule(mens_doubles_list_final, court)
    court = ['Premium Hybrid Court 4']
    schedule(women_singles_list, court)
    court = ['Premium Hybrid Court 6']
    schedule(womens_doubles_list_final, court)
    court = ['Synthetic Court 1']
    schedule(mixed_doubles_list_final, court)

if __name__ == '__main__':
    fetch_data()
