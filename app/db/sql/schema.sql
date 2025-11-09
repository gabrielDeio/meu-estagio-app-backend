-- core.organization definition

-- Drop table

-- DROP TABLE core.organization;

CREATE TABLE core.organization (
	id uuid DEFAULT uuid_generate_v4() NOT NULL,
	"name" varchar NOT NULL,
	supervisor_max_amount int2 NOT NULL,
	cnpj varchar NOT NULL,
	created_at timestamptz DEFAULT now() NOT NULL,
	code varchar NOT NULL,
	CONSTRAINT organization_pk PRIMARY KEY (id),
	CONSTRAINT organization_unique UNIQUE (cnpj),
	CONSTRAINT organization_unique_1 UNIQUE (code)
);


-- core.users definition

-- Drop table

-- DROP TABLE core.users;

CREATE TABLE core.users (
	id uuid DEFAULT uuid_generate_v4() NOT NULL,
	"name" varchar NOT NULL,
	surname varchar NULL,
	email varchar NOT NULL,
	"password" varchar NOT NULL,
	"type" varchar NOT NULL,
	created_at timestamptz DEFAULT now() NOT NULL,
	CONSTRAINT user_pk PRIMARY KEY (id),
	CONSTRAINT user_unique UNIQUE (email)
);


-- core.org_user definition

-- Drop table

-- DROP TABLE core.org_user;

CREATE TABLE core.org_user (
	org_id uuid NOT NULL,
	user_id uuid NOT NULL,
	"type" varchar NOT NULL,
	"role" varchar NULL,
	status varchar NOT NULL,
	created_at timestamptz DEFAULT now() NOT NULL,
	finished_at timestamptz NULL,
	CONSTRAINT org_user_pk PRIMARY KEY (org_id, user_id, type),
	CONSTRAINT org_user_organization_fk FOREIGN KEY (org_id) REFERENCES core.organization(id),
	CONSTRAINT org_user_users_fk FOREIGN KEY (user_id) REFERENCES core.users(id)
);