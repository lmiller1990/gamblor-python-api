def map_market_short_to_long_with_id(short_name):
    """
    maps a market name to the relevant column on the games table

    Parameters:
        short_name: 'fb' | 'ft' | 'fd' | 'fbaron'

    Returns:
        attribute which maps to column in the games table.

    Example:
        map_market_short_to_long_with_id('fb') #=> 'first_blood_team_id'
    """

    market_map = {
            'fbaron': 'first_baron_team_id',
            'fb': 'first_blood_team_id',
            'fd': 'first_dragon_team_id',
            'ft': 'first_turret_team_id'
            }
    return market_map[short_name]


def map_team_and_market_to_odds(game, side, market):
    """
    Description:
        maps a market name to the relevant column on the games table

    Parameters:
        game: schema.Game
        side: 'red' | 'blue'
        market: 'fb' | 'ft' | 'fd' | 'fbaron'

    Returns:
        attribute which maps to column in the games table.

    Example:
        map_team_and_market_to_odds(Game.select().first(), 'red', 'fb') 
            #=> SELECT red_side_team_fb_odds FROM game;
            #=> 1.2
    """
    return getattr(game, side + '_side_team_' + market + '_odds')


