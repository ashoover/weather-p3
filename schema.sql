-- noinspection SqlDialectInspectionForFile

-- noinspection SqlNoDataSourceInspectionForFile

-- Schema for weather data.

create table weather (
    name        text primary key,
    description text,
    deadline    date
);
