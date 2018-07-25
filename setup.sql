CREATE TABLE jobs(
    id              SERIAL,
    job_title  TEXT                         NOT NULL,
    er_id           INTEGER                     UNIQUE,
    client_id       INTEGER                     NOT NULL,
    recruiter_id    INTEGER,
    creation_date   TIMESTAMP               NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    briefing_on     TIMESTAMP,
    status          TEXT,
    min_salary      INTEGER,
    max_salary      INTEGER,
    exp_salary      INTEGER,
    dayzee_link     TEXT
);

CREATE TABLE staff(
    number          SERIAL,
    first_name      TEXT                    NOT NULL,
    last_name       TEXT                    NOT NULL,
    position        TEXT,
    created_on      TIMESTAMP                       NOT NULL    DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE candidates(
    id              SERIAL,
    er_id           INTEGER                             NOT NULL,
    first_name      TEXT                    NOT NULL,
    last_name       TEXT                    NOT NULL,
    phone_number    TEXT,
    email           TEXT,
    dob             date,
    xing_link       TEXT,
    linkedin_link   TEXT,
    added_on        TIMESTAMP               NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    approachable    BOOLEAN                             DEFAULT TRUE,
    referrer        TEXT
);

CREATE TABLE applications(
    id                          SERIAL,
    candidate_id                INTEGER         NOT NULL,
    job_id                      INTEGER         NOT NULL,
    status                      TEXT        NOT NULL,
    added_on                    TIMESTAMP   NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    contacted_on                TIMESTAMP,
    contact_version             TEXT,
    replied_on                  TIMESTAMP,
    INTEGERerview_on                TIMESTAMP,
    contract_negotiations_on    TIMESTAMP
);

CREATE TABLE clients(
    id                          SERIAL,
    name                        TEXT        NOT NULL,
    street                      TEXT,
    street_number               TEXT,
    zip                         INTEGER,
    city                        TEXT,
    main_contact                TEXT
);

CREATE TABLE matches(
    id                          SERIAL,
    candidate_id                INTEGER,
    job_id                      INTEGER,
    er_id                       BIGINT,
    creation_date               TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    last_status_change          TIMESTAMP,
    rating                      CHAR(1),
    candidate_decline_reason    TEXT,
    client_decline_reason       TEXT
);