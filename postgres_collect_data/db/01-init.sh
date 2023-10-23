#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';
  CREATE DATABASE $APP_DB_NAME;
  GRANT ALL PRIVILEGES ON DATABASE $APP_DB_NAME TO $APP_DB_USER;

  \connect $APP_DB_NAME;

  CREATE TABLE IF NOT EXISTS random_cannabis
  (
      uid                      uuid primary key,
      id                       bigint,
      strain                   text,
      cannabinoid_abbreviation text,
      cannabinoid              text,
      terpene                  text,
      medical_use              text,
      health_benefit           text,
      category                 text,
      type                     text,
      buzzword                 text,
      brand                    text,
      load_date                timestamp not null default now()
  );

  alter table random_cannabis
    owner to $APP_DB_USER;

  CREATE TABLE IF NOT EXISTS team
  (
      uid uuid,
      id  bigint,
      load_date timestamp not null default now()
  );

  alter table team
    owner to $APP_DB_USER;

  CREATE TABLE IF NOT EXISTS stats
  (
      team_uid    uuid,
      uid         uuid,
      load_date   timestamp not null default now(),
      display_name text,
      game_type    jsonb
  );

  alter table stats
    owner to $APP_DB_USER;

  CREATE TABLE IF NOT EXISTS splits
  (
      stat_uid                 uuid,
      uid                      uuid,
      load_date                timestamp not null default now(),
      games_played             text,
      wins                     text,
      losses                   text,
      ot                       text,
      pts                      text,
      ptpctg                   text,
      goals_pergame            text,
      goals_against_pergame    text,
      evgga_ratio              text,
      power_play_percentage    text,
      power_play_goals         text,
      power_play_goals_against text,
      power_play_opportunities text,
      penalty_kill_percentage  text,
      shots_pergame            text,
      shots_allowed            text,
      win_score_first          text,
      win_opp_score_first      text,
      win_lead_first_per       text,
      win_lead_second_per      text,
      win_out_shootopp         text,
      win_out_shotbyopp        text,
      face_offs_taken          text,
      face_offs_won            text,
      face_offs_lost           text,
      face_off_win_percentage  text,
      shooting_pctg              text,
      save_pctg                  text,
      penalty_kill_opportunities text,
      save_pct_rank              text,
      shooting_pct_rank          text
  );

  alter table splits
    owner to $APP_DB_USER;

EOSQL
