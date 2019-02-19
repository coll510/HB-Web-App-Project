--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3 (Ubuntu 10.3-1)
-- Dumped by pg_dump version 10.3 (Ubuntu 10.3-1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: classes; Type: TABLE; Schema: public; Owner: engineer
--

CREATE TABLE public.classes (
    class_id integer NOT NULL,
    class_name character varying(130) NOT NULL,
    start_time timestamp with time zone,
    end_time timestamp with time zone,
    url character varying(300)
);


ALTER TABLE public.classes OWNER TO engineer;

--
-- Name: classes_class_id_seq; Type: SEQUENCE; Schema: public; Owner: engineer
--

CREATE SEQUENCE public.classes_class_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.classes_class_id_seq OWNER TO engineer;

--
-- Name: classes_class_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: engineer
--

ALTER SEQUENCE public.classes_class_id_seq OWNED BY public.classes.class_id;


--
-- Name: user_classes; Type: TABLE; Schema: public; Owner: engineer
--

CREATE TABLE public.user_classes (
    user_class_id integer NOT NULL,
    user_id integer NOT NULL,
    class_id integer NOT NULL,
    class_saved boolean,
    class_attended boolean
);


ALTER TABLE public.user_classes OWNER TO engineer;

--
-- Name: user_classes_user_class_id_seq; Type: SEQUENCE; Schema: public; Owner: engineer
--

CREATE SEQUENCE public.user_classes_user_class_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_classes_user_class_id_seq OWNER TO engineer;

--
-- Name: user_classes_user_class_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: engineer
--

ALTER SEQUENCE public.user_classes_user_class_id_seq OWNED BY public.user_classes.user_class_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: engineer
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    user_name character varying(64) NOT NULL,
    email character varying(64) NOT NULL,
    password character varying(64) NOT NULL
);


ALTER TABLE public.users OWNER TO engineer;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: engineer
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO engineer;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: engineer
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: classes class_id; Type: DEFAULT; Schema: public; Owner: engineer
--

ALTER TABLE ONLY public.classes ALTER COLUMN class_id SET DEFAULT nextval('public.classes_class_id_seq'::regclass);


--
-- Name: user_classes user_class_id; Type: DEFAULT; Schema: public; Owner: engineer
--

ALTER TABLE ONLY public.user_classes ALTER COLUMN user_class_id SET DEFAULT nextval('public.user_classes_user_class_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: engineer
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: classes; Type: TABLE DATA; Schema: public; Owner: engineer
--

COPY public.classes (class_id, class_name, start_time, end_time, url) FROM stdin;
1	Jikilele	\N	\N	jikilele.com
\.


--
-- Data for Name: user_classes; Type: TABLE DATA; Schema: public; Owner: engineer
--

COPY public.user_classes (user_class_id, user_id, class_id, class_saved, class_attended) FROM stdin;
1	1	1	t	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: engineer
--

COPY public.users (user_id, user_name, email, password) FROM stdin;
1	Tiffany	tiffany.a@email.com	1234
2	Jackie	jackie@email.com	1234
3	Felicia	felicia@email.com	1234
6	Macy	macy.a@email.com	1234
\.


--
-- Name: classes_class_id_seq; Type: SEQUENCE SET; Schema: public; Owner: engineer
--

SELECT pg_catalog.setval('public.classes_class_id_seq', 1, true);


--
-- Name: user_classes_user_class_id_seq; Type: SEQUENCE SET; Schema: public; Owner: engineer
--

SELECT pg_catalog.setval('public.user_classes_user_class_id_seq', 1, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: engineer
--

SELECT pg_catalog.setval('public.users_user_id_seq', 6, true);


--
-- Name: classes classes_class_name_key; Type: CONSTRAINT; Schema: public; Owner: engineer
--

ALTER TABLE ONLY public.classes
    ADD CONSTRAINT classes_class_name_key UNIQUE (class_name);


--
-- Name: classes classes_pkey; Type: CONSTRAINT; Schema: public; Owner: engineer
--

ALTER TABLE ONLY public.classes
    ADD CONSTRAINT classes_pkey PRIMARY KEY (class_id);


--
-- Name: user_classes user_classes_pkey; Type: CONSTRAINT; Schema: public; Owner: engineer
--

ALTER TABLE ONLY public.user_classes
    ADD CONSTRAINT user_classes_pkey PRIMARY KEY (user_class_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: engineer
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: engineer
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_user_name_key; Type: CONSTRAINT; Schema: public; Owner: engineer
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_name_key UNIQUE (user_name);


--
-- Name: user_classes user_classes_class_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: engineer
--

ALTER TABLE ONLY public.user_classes
    ADD CONSTRAINT user_classes_class_id_fkey FOREIGN KEY (class_id) REFERENCES public.classes(class_id);


--
-- Name: user_classes user_classes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: engineer
--

ALTER TABLE ONLY public.user_classes
    ADD CONSTRAINT user_classes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

