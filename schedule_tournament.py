def schedule_matches(players_list, start_time, match_duration, rest_duration, courts):
    schedule = []
    court_index = 0

    for i in range(0, len(players_list), 2):
        if i > 0 and players_list[i] == players_list[i - 2]:
            start_time += rest_duration

        match = {"court": courts[court_index], "player1": players_list[i], "player2": players_list[i + 1],
                 "start_time": start_time}
        schedule.append(match)
        start_time += match_duration

        # Move to the next court
        court_index = (court_index + 1) % len(courts)

    return schedule