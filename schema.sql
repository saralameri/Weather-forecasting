--
-- PostgreSQL database dump
--

-- Dumped from database version 13.9 (Ubuntu 13.9-1.pgdg20.04+1)
-- Dumped by pg_dump version 16.0

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

--
-- Name: weather_forecast; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE weather_forecast WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';


\connect weather_forecast

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

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

-- *not* creating schema, since initdb creates it


--
-- Name: btree_gin; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS btree_gin WITH SCHEMA public;


--
-- Name: EXTENSION btree_gin; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION btree_gin IS 'support for indexing common datatypes in GIN';


--
-- Name: btree_gist; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS btree_gist WITH SCHEMA public;


--
-- Name: EXTENSION btree_gist; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION btree_gist IS 'support for indexing common datatypes in GiST';


--
-- Name: citext; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA public;


--
-- Name: EXTENSION citext; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION citext IS 'data type for case-insensitive character strings';


--
-- Name: cube; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS cube WITH SCHEMA public;


--
-- Name: EXTENSION cube; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION cube IS 'data type for multidimensional cubes';


--
-- Name: dblink; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS dblink WITH SCHEMA public;


--
-- Name: EXTENSION dblink; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION dblink IS 'connect to other PostgreSQL databases from within a database';


--
-- Name: dict_int; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS dict_int WITH SCHEMA public;


--
-- Name: EXTENSION dict_int; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION dict_int IS 'text search dictionary template for integers';


--
-- Name: dict_xsyn; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS dict_xsyn WITH SCHEMA public;


--
-- Name: EXTENSION dict_xsyn; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION dict_xsyn IS 'text search dictionary template for extended synonym processing';


--
-- Name: earthdistance; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS earthdistance WITH SCHEMA public;


--
-- Name: EXTENSION earthdistance; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION earthdistance IS 'calculate great-circle distances on the surface of the Earth';


--
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- Name: hstore; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS hstore WITH SCHEMA public;


--
-- Name: EXTENSION hstore; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION hstore IS 'data type for storing sets of (key, value) pairs';


--
-- Name: intarray; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS intarray WITH SCHEMA public;


--
-- Name: EXTENSION intarray; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION intarray IS 'functions, operators, and index support for 1-D arrays of integers';


--
-- Name: ltree; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS ltree WITH SCHEMA public;


--
-- Name: EXTENSION ltree; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION ltree IS 'data type for hierarchical tree-like structures';


--
-- Name: pg_stat_statements; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA public;


--
-- Name: EXTENSION pg_stat_statements; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pg_stat_statements IS 'track planning and execution statistics of all SQL statements executed';


--
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: pgrowlocks; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgrowlocks WITH SCHEMA public;


--
-- Name: EXTENSION pgrowlocks; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pgrowlocks IS 'show row-level locking information';


--
-- Name: pgstattuple; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgstattuple WITH SCHEMA public;


--
-- Name: EXTENSION pgstattuple; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pgstattuple IS 'show tuple-level statistics';


--
-- Name: tablefunc; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS tablefunc WITH SCHEMA public;


--
-- Name: EXTENSION tablefunc; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION tablefunc IS 'functions that manipulate whole tables, including crosstab';


--
-- Name: unaccent; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public;


--
-- Name: EXTENSION unaccent; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION unaccent IS 'text search dictionary that removes accents';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: xml2; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS xml2 WITH SCHEMA public;


--
-- Name: EXTENSION xml2; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION xml2 IS 'XPath querying and XSLT';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: api_res; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.api_res (
    res_id integer NOT NULL,
    coord_lon double precision,
    coord_lat double precision,
    base text,
    main_temp double precision,
    main_feels_like double precision,
    main_temp_min double precision,
    main_temp_max double precision,
    main_pressure integer,
    main_humidity integer,
    main_sea_level double precision,
    main_grnd_level double precision,
    visibility integer,
    wind_speed double precision,
    wind_deg double precision,
    wind_gust double precision,
    dt integer,
    sys_type integer,
    sys_id integer,
    sys_message text,
    sys_country text,
    sys_sunrise integer,
    sys_sunset integer,
    timezone integer,
    id integer,
    name text,
    cod integer,
    clouds_all integer,
    rain_1h double precision,
    rain_3h double precision,
    snow_1h double precision,
    snow_3h double precision
);


--
-- Name: api_res_res_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.api_res_res_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: api_res_res_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.api_res_res_id_seq OWNED BY public.api_res.res_id;


--
-- Name: res_weather_relation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.res_weather_relation (
    res_id integer,
    weather_id integer
);


--
-- Name: weather; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.weather (
    id integer NOT NULL,
    main text,
    description text,
    icon text
);


--
-- Name: api_res res_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.api_res ALTER COLUMN res_id SET DEFAULT nextval('public.api_res_res_id_seq'::regclass);


--
-- Name: api_res api_res_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.api_res
    ADD CONSTRAINT api_res_pkey PRIMARY KEY (res_id);


--
-- Name: res_weather_relation res_weather_relation_res_id_weather_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.res_weather_relation
    ADD CONSTRAINT res_weather_relation_res_id_weather_id_key UNIQUE (res_id, weather_id);


--
-- Name: weather weather_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.weather
    ADD CONSTRAINT weather_pkey PRIMARY KEY (id);


--
-- Name: res_weather_relation res_weather_relation_res_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.res_weather_relation
    ADD CONSTRAINT res_weather_relation_res_id_fkey FOREIGN KEY (res_id) REFERENCES public.api_res(res_id);


--
-- Name: res_weather_relation res_weather_relation_weather_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.res_weather_relation
    ADD CONSTRAINT res_weather_relation_weather_id_fkey FOREIGN KEY (weather_id) REFERENCES public.weather(id);


--
-- Name: DATABASE weather_forecast; Type: ACL; Schema: -; Owner: -
--

REVOKE CONNECT,TEMPORARY ON DATABASE weather_forecast FROM PUBLIC;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: -
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

