from __future__ import annotations

import logging
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

from typing import Optional
import pandas as pd

from player_performance_ratings.data_structures import MatchTeam, ColumnNames, MatchPerformance, \
    MatchPlayer, Match
from player_performance_ratings.ratings.league_identifier import LeagueIdentifier

HOUR_NUMBER_COLUMN_NAME = "hour_number"


def convert_df_to_matches(df: pd.DataFrame, column_names: ColumnNames,
                          league_identifier: Optional[LeagueIdentifier] = None) -> list[Match]:
    """
    Converts a dataframe to a list of matches.
    Each dataframe row needs to be a unique combination of match_id and player_id.
    The dataframe needs to contain the following columns:
        * player_id
        * team_id
        * match_id
        * start_date
        * performance


    Dataframe needs to be sorted by date, game_id, team_id in ascending order.

    Optionally a column for participation_weight and league can be passed.
    The participation_weight indicates the percentage (as a ratio) of the time played by the player in the match.
    The league column indicates the league of the match.
    If the league_identifier is passed it will identify the league of the match by the players past matches played.
    If not the  league of the match will be equal to the league of the current match
    """

    df_sorted = df.sort_values(
        by=[column_names.start_date, column_names.match_id,
            column_names.team_id, column_names.player_id])

    if not df.equals(df_sorted):
        raise ValueError("df needs to be sorted by date, game_id, team_id in ascending order")

    col_names = column_names
    df[col_names.start_date] = pd.to_datetime(df[col_names.start_date], format='%Y-%m-%d %H:%M:%S')
    try:
        date_time = df[col_names.start_date].dt.tz_convert('UTC')
    except TypeError:
        date_time = df[col_names.start_date].dt.tz_localize('UTC')
    df[HOUR_NUMBER_COLUMN_NAME] = (date_time - pd.Timestamp("1970-01-01").tz_localize('UTC')) // pd.Timedelta(
        '1h')

    league_in_df = False
    if col_names.league in df.columns.tolist():
        if league_identifier is None:
            logging.warning("League column passed but no league_identifier passed. league will be set to None")
        else:
            league_in_df = True

    prev_match_id = None

    data_dict = df.to_dict('records')

    matches = []

    prev_team_id = None
    prev_row: Optional[None, pd.Series] = None
    match_teams = []
    match_team_players = []
    team_league_counts = {}

    for row in data_dict:
        match_id = row[col_names.match_id]
        team_id = row[col_names.team_id]
        if team_id != prev_team_id and prev_team_id != None or prev_match_id != match_id and prev_match_id != None:
            match_team = _create_match_team(team_league_counts=team_league_counts, team_id=prev_team_id,
                                            match_team_players=match_team_players)
            match_teams.append(match_team)
            match_team_players = []
            team_league_counts = {}

        if match_id != prev_match_id and prev_match_id != None:
            match = _create_match(league_in_df=league_in_df, row=prev_row, match_teams=match_teams,
                                  column_names=column_names)
            matches.append(match)
            match_teams = []

        participation_weight = 1.0
        if col_names.participation_weight:
            participation_weight = row[col_names.participation_weight]

        player_id = row[col_names.team_id]
        if col_names.player_id is not None:
            player_id = row[col_names.player_id]


        if col_names.position is not None:
            position = row[col_names.position]
        else:
            position = None

        if league_in_df:
            match_league = row[column_names.league]
            if team_id not in team_league_counts:
                team_league_counts[team_id] = {}
            player_league = league_identifier.identify(player_id=player_id,
                                                       league_match=match_league)
            if player_league not in team_league_counts[team_id]:
                team_league_counts[team_id][player_league] = 0

            team_league_counts[team_id][player_league] += 1
        else:
            player_league = None

        performance = MatchPerformance(
            performance_value=row[col_names.performance],
            participation_weight=participation_weight,
        )

        match_player = MatchPlayer(
            id=player_id,
            league=player_league,
            performance=performance,
            position=position,
        )
        match_team_players.append(match_player)

        prev_match_id = match_id
        prev_team_id = team_id
        prev_row = row

    match_team = _create_match_team(team_league_counts=team_league_counts, team_id=prev_team_id,
                                    match_team_players=match_team_players)
    match_teams.append(match_team)
    match = _create_match(league_in_df=league_in_df, row=df.iloc[len(df) - 1],
                          match_teams=match_teams, column_names=column_names)
    matches.append(match)

    return matches


def _create_match(league_in_df, row: pd.Series, match_teams: list[MatchTeam], column_names: ColumnNames) -> Match:
    match_id = row[column_names.match_id]
    if league_in_df:
        match_league = row[column_names.league]
    else:
        match_league = None

    return Match(
        id=match_id,
        teams=match_teams,
        day_number=int(row[HOUR_NUMBER_COLUMN_NAME] / 24),
        league=match_league,
        update_id=row[column_names.rating_update_id]
    )


def _create_match_team(team_league_counts: dict, team_id: str,
                       match_team_players: list[MatchPlayer]) -> MatchTeam:
    if team_league_counts:
        team_league = max(team_league_counts[team_id], key=team_league_counts[team_id].get)
    else:
        team_league = None
    return MatchTeam(
        id=team_id,
        players=match_team_players,
        league=team_league
    )
