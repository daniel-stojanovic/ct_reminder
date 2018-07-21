CREATE TABLE jobs(
    id              serial,
    job_title  text                         NOT NULL,
    er_id           int                     UNIQUE,
    client_id       int                     NOT NULL,
    recruiter_id    int,
    creation_date   timestamp               NOT NULL    default CURRENT_TIMESTAMP,
    briefing_on     timestamp,
    status          text,
    min_salary      int,
    max_salary      int,
    exp_salary      int,
    dayzee_link     text
);

CREATE TABLE staff(
    number          serial,
    first_name      text                    NOT NULL,
    last_name       text                    NOT NULL,
    position        text,
    created_on      timestamp                       NOT NULL    default CURRENT_TIMESTAMP
);

CREATE TABLE candidates(
    id              serial,
    er_id           int                             NOT NULL,
    first_name      text                    NOT NULL,
    last_name       text                    NOT NULL,
    phone_number    text,
    email           text,
    dob             date,
    xing_link       text,
    linkedin_link   text,
    added_on        timestamp               NOT NULL    default CURRENT_TIMESTAMP,
    approachable    boolean                             default TRUE,
    referrer        text
);

CREATE TABLE applications(
    id                          serial,
    candidate_id                int         NOT NULL,
    job_id                      int         NOT NULL,
    status                      text        NOT NULL,
    added_on                    timestamp   NOT NULL    default CURRENT_TIMESTAMP,
    contacted_on                timestamp,
    contact_version             text,
    replied_on                  timestamp,
    interview_on                timestamp,
    contract_negotiations_on    timestamp
);

CREATE TABLE clients(
    id                          serial,
    internal_name               text        NOT NULL,
    full_name                   text,
    street                      text,
    street_number               text,
    zip                         int,
    city                        text,
    main_contact                text
);