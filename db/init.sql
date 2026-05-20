CREATE DATABASE IF NOT EXISTS yarnlogic_calculate;

CREATE SCHEMA IF NOT EXISTS yarnlogic_calculate;

CREATE TABLE yarnlogic_calculate.stitch_type (
    name TEXT PRIMARY KEY,
    description TEXT,
    image BYTEA
);

CREATE TABLE yarnlogic_calculate.relation_type (
    name TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE yarnlogic_calculate.tool (
    name TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE yarnlogic_calculate.pattern (
    id SERIAL PRIMARY KEY,
    name TEXT
);