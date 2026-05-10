CREATE DATABASE IF NOT EXISTS yarnlogic_calculate;

CREATE TABLE stitch_type (
    name TEXT PRIMARY KEY,
    description TEXT,
    image BYTEA
);

CREATE TABLE relation_type (
    name TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE tool (
    name TEXT PRIMARY KEY,
    description TEXT
);