--
-- PostgreSQL database dump
--

\restrict 83qgmFD1yj7B0U37uYgEW172pvNZoTjDbsrR2bSReaawNwPG5o2zjAukdoHBdci

-- Dumped from database version 13.22 (Debian 13.22-1.pgdg13+1)
-- Dumped by pg_dump version 13.22 (Debian 13.22-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY core."user" DROP CONSTRAINT user_unique;
ALTER TABLE ONLY core."user" DROP CONSTRAINT user_pk;
ALTER TABLE ONLY core.organization DROP CONSTRAINT organization_unique;
ALTER TABLE ONLY core.organization DROP CONSTRAINT organization_pk;
ALTER TABLE ONLY core.org_user DROP CONSTRAINT org_user_pk;
DROP TABLE core."user";
DROP TABLE core.organization;
DROP TABLE core.org_user;
DROP EXTENSION "uuid-ossp";
DROP SCHEMA core;
--
-- Name: core; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA core;


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: org_user; Type: TABLE; Schema: core; Owner: -
--

CREATE TABLE core.org_user (
    org_id uuid NOT NULL,
    user_id uuid NOT NULL,
    type character varying NOT NULL,
    role character varying,
    status character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    finished_at timestamp with time zone
);


--
-- Name: organization; Type: TABLE; Schema: core; Owner: -
--

CREATE TABLE core.organization (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name character varying NOT NULL,
    supervisor_max_amount smallint NOT NULL,
    cnpj character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: user; Type: TABLE; Schema: core; Owner: -
--

CREATE TABLE core."user" (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name character varying NOT NULL,
    surname character varying,
    email character varying NOT NULL,
    password character varying NOT NULL,
    type character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: org_user org_user_pk; Type: CONSTRAINT; Schema: core; Owner: -
--

ALTER TABLE ONLY core.org_user
    ADD CONSTRAINT org_user_pk PRIMARY KEY (org_id, user_id, type);


--
-- Name: organization organization_pk; Type: CONSTRAINT; Schema: core; Owner: -
--

ALTER TABLE ONLY core.organization
    ADD CONSTRAINT organization_pk PRIMARY KEY (id);


--
-- Name: organization organization_unique; Type: CONSTRAINT; Schema: core; Owner: -
--

ALTER TABLE ONLY core.organization
    ADD CONSTRAINT organization_unique UNIQUE (cnpj);


--
-- Name: user user_pk; Type: CONSTRAINT; Schema: core; Owner: -
--

ALTER TABLE ONLY core."user"
    ADD CONSTRAINT user_pk PRIMARY KEY (id);


--
-- Name: user user_unique; Type: CONSTRAINT; Schema: core; Owner: -
--

ALTER TABLE ONLY core."user"
    ADD CONSTRAINT user_unique UNIQUE (email);


--
-- PostgreSQL database dump complete
--

\unrestrict 83qgmFD1yj7B0U37uYgEW172pvNZoTjDbsrR2bSReaawNwPG5o2zjAukdoHBdci

