"""add player rushing table

Revision ID: a9646922c3aa
Revises: 
Create Date: 2019-11-11 13:58:33.915049

"""
from alembic import op
import sqlalchemy as sa
import json

from nflrushing.utils.units import parse_yards


# revision identifiers, used by Alembic.
revision = 'a9646922c3aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    player_rushing_table = op.create_table('player_rushing',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('team', sa.String(length=50), nullable=False),
        sa.Column('position', sa.String(length=50), nullable=False),
        sa.Column('rushing_attempts_per_game_average', sa.Float(), nullable=False),
        sa.Column('rushing_attempts', sa.Integer(), nullable=False),
        sa.Column('total_rushing_yards', sa.Integer(), nullable=False),
        sa.Column('rushing_average_yards_per_attempt', sa.Float(), nullable=False),
        sa.Column('rushing_yards_per_game', sa.Float(), nullable=False),
        sa.Column('total_rushing_touchdowns', sa.Integer(), nullable=False),
        sa.Column('longest_rush', sa.Integer(), nullable=False),
        sa.Column('longest_rush_touchdown', sa.Boolean(), nullable=False),
        sa.Column('rushing_first_downs', sa.Integer(), nullable=False),
        sa.Column('rushing_first_down_percentage', sa.Float(), nullable=False),
        sa.Column('rushing_20_plus_yards_each', sa.Integer(), nullable=False),
        sa.Column('rushing_40_plus_yards_each', sa.Integer(), nullable=False),
        sa.Column('rushing_fumbles', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    data = [{
        'name': player['Player'],
        'team': player['Team'],
        'position': player['Pos'],
        'rushing_attempts_per_game_average': player['Att/G'],
        'rushing_attempts': player['Att'],
        'total_rushing_yards': parse_yards(str(player['Yds']))[0],
        'rushing_average_yards_per_attempt': player['Avg'],
        'rushing_yards_per_game': player['Yds/G'],
        'total_rushing_touchdowns': player['TD'],
        'longest_rush': parse_yards(str(player['Lng']))[0],
        'longest_rush_touchdown': parse_yards(str(player['Lng']))[1],
        'rushing_first_downs': player['1st'],
        'rushing_first_down_percentage': player['1st%'],
        'rushing_20_plus_yards_each': player['20+'],
        'rushing_40_plus_yards_each': player['40+'],
        'rushing_fumbles': player['FUM'],
    } for player in json.load(open('./rushing.json'))]

    # transfer data from rushing.json to a DB table
    op.bulk_insert(player_rushing_table, data)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player_rushing')
    # ### end Alembic commands ###
