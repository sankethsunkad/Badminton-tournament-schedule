import json
def check_player_participation(input_json):
    player_categories = {}

    for category, players_or_teams in input_json.items():
      if isinstance(players_or_teams[0], list):
          for team in players_or_teams:
              for player in team:
                  if player not in player_categories:
                      player_categories[player] = {category}
                  else:
                      player_categories[player].add(category)
      else:
          for player in players_or_teams:
              if player not in player_categories:
                  player_categories[player] = {category}
              else:
                  player_categories[player].add(category)

    for player, categories in player_categories.items():
        if len(categories) > 2:
            return False, f'{player} is participating in more than two categories: {categories}'

    return True, 'All players are participating in two or fewer categories.'

def read_input(input_string):
    input_json = json.loads(input_string)
    check_result, message = check_player_participation(input_json)

    if not check_result:
        print(message)
    else:
        print('Participation check passed: ', message)
