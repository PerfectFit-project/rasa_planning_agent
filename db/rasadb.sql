use db;

CREATE TABLE sessiondata(prolific_id TEXT, time DATETIME, event TEXT);


CREATE TABLE users(prolific_id TEXT, time DATETIME, goal TEXT, plan_1 TEXT, plan_2 TEXT, plan_3 TEXT, reward TEXT);


CREATE TABLE state_action_state(prolific_id TEXT, time DATETIME, state_before TEXT, action TEXT, state_after TEXT);
