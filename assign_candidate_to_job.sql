UPDATE candidates SET approachable=FALSE WHERE id=%(candidate_id)s;

INSERT INTO applications (candidate_id, job_id, status)
VALUES (%(candidate_id)s, %(job_id)s, 'new') returning id;

