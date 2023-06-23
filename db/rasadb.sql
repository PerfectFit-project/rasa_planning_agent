use db;

CREATE TABLE sessiondata(prolific_id TEXT, time DATETIME, event TEXT);


CREATE TABLE users(prolific_id TEXT, time DATETIME, goal TEXT, plan_1 TEXT, plan_2 TEXT, plan_3 TEXT, reward TEXT, testimonial_1 TEXT, takeaway_1 TEXT, testimonial_2 TEXT, takeaway_2 TEXT, identified_barrier TEXT, barrier_descripion TEXT, barrier_strategy_1 TEXT, barrier_strategy_2 TEXT, planning_relevance TEXT, planning_importance_explanation TEXT);


CREATE TABLE state_action_state(prolific_id TEXT, time DATETIME, state_before TEXT, action TEXT, state_after TEXT);
