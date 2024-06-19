CREATE TABLE
  security_user (
    id uuid NOT NULL DEFAULT gen_random_uuid (),
    name character varying(256) NOT NULL,
    sub character varying(256) NOT NULL
  );

ALTER TABLE
  security_user
ADD
  CONSTRAINT security_user_pkey PRIMARY KEY (id);

CREATE TABLE
  security_pending_user (
    id uuid NOT NULL DEFAULT gen_random_uuid (),
    sub character varying(256) NOT NULL,
    created_on timestamp without time zone NULL DEFAULT CURRENT_TIMESTAMP,
    payload jsonb NULL
  );

ALTER TABLE
  security_pending_user
ADD
  CONSTRAINT security_pending_user_pkey PRIMARY KEY (id);
