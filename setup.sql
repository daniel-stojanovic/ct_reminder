CREATE TABLE jobs(
    id              serial,
    position_title  varchar(255)                NOT NULL,
    er_id           int                         UNIQUE,
    client_id       int                         NOT NULL,
    recruiter_id    int,
    creation_date   date                        NOT NULL    default CURRENT_TIMESTAMP,
    briefing_on     date,
    status          varchar(255),
    min_salary      int,
    max_salary      int,
    exp_salary      int
);

CREATE TABLE staff(
    number          int,
    first_name      varchar(255)                NOT NULL,
    last_name       varchar(255)                NOT NULL,
    position        varchar(255),
    created_on      date                        NOT NULL    default CURRENT_TIMESTAMP
);

CREATE TABLE candidates(
    id              serial,
    er_id           int                         NOT NULL,
    first_name      varchar(255)                NOT NULL,
    last_name       varchar(255)                NOT NULL,
    phone_number    varchar(255),
    email           varchar(255),
    dob             date,
    xing_link       varchar(255),
    linkedin_link   varchar(255),
    added_on        date                        NOT NULL    default CURRENT_TIMESTAMP
);

CREATE TABLE applications(
    id                          serial,
    candidate_id                int             NOT NULL,
    job_id                      int             NOT NULL,
    status                      varchar(255)    NOT NULL,
    added_on                    date            NOT NULL,
    contacted_on                date,
    contact_version             varchar(255),
    replied_on                  date,
    interview_on                date,
    contract_negotiations_on    date
);

CREATE TABLE clients(
    id                          serial,
    internal_name               varchar(255)    NOT NULL,
    full_name                   varchar(255),
    address                     varchar(255),
    main_contact                varchar(255)
);