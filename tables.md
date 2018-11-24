CREATE EXTENSION chkpass;

CREATE TABLE users (
  id              SERIAL PRIMARY KEY,
  username        VARCHAR(255) NOT NULL UNIQUE,
  password        chkpass NOT NULL,
  email           VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE messages (
  id              SERIAL PRIMARY KEY,
  sender_id       INTEGER NOT NULL,
  recipient_id    INTEGER NOT NULL,
  message         VARCHAR,
  created         TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  read            BOOLEAN NOT NULL DEFAULT FALSE,
  FOREIGN KEY (sender_id) REFERENCES users (id),
  FOREIGN KEY (recipient_id) REFERENCES users (id)
);

CREATE TABLE tokens (
  token         VARCHAR(64) PRIMARY KEY UNIQUE,
  user_id       INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
