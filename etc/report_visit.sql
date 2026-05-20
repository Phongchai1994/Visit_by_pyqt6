--
-- PostgreSQL database dump
--

\restrict rqghyIGqPmfHHTLn2VtLSjNWwtWLdJDYl2APfDiKrIo2hDzSPQFQhYTe8YQRluN

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-05-20 16:25:34

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 230 (class 1259 OID 16878)
-- Name: check_; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.check_ (
    id integer NOT NULL,
    key text
);


ALTER TABLE public.check_ OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16877)
-- Name: check__id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.check__id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.check__id_seq OWNER TO postgres;

--
-- TOC entry 4944 (class 0 OID 0)
-- Dependencies: 229
-- Name: check__id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.check__id_seq OWNED BY public.check_.id;


--
-- TOC entry 232 (class 1259 OID 16888)
-- Name: holidays; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.holidays (
    id integer NOT NULL,
    date text NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.holidays OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16887)
-- Name: holidays_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.holidays_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.holidays_id_seq OWNER TO postgres;

--
-- TOC entry 4945 (class 0 OID 0)
-- Dependencies: 231
-- Name: holidays_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.holidays_id_seq OWNED BY public.holidays.id;


--
-- TOC entry 238 (class 1259 OID 16925)
-- Name: log_error; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.log_error (
    log_id integer NOT NULL,
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    function_name text,
    error_message text,
    extra_info text
);


ALTER TABLE public.log_error OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16924)
-- Name: log_error_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.log_error_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.log_error_log_id_seq OWNER TO postgres;

--
-- TOC entry 4946 (class 0 OID 0)
-- Dependencies: 237
-- Name: log_error_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.log_error_log_id_seq OWNED BY public.log_error.log_id;


--
-- TOC entry 236 (class 1259 OID 16914)
-- Name: log_realtime; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.log_realtime (
    id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    prisoner_id bigint,
    relative_id bigint,
    result text,
    detail text,
    device text,
    channel integer,
    visit_date text,
    time_visit text
);


ALTER TABLE public.log_realtime OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16913)
-- Name: log_realtime_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.log_realtime_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.log_realtime_id_seq OWNER TO postgres;

--
-- TOC entry 4947 (class 0 OID 0)
-- Dependencies: 235
-- Name: log_realtime_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.log_realtime_id_seq OWNED BY public.log_realtime.id;


--
-- TOC entry 219 (class 1259 OID 16764)
-- Name: prisoners_; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prisoners_ (
    prisoner_id bigint NOT NULL,
    sex text NOT NULL,
    f_name text NOT NULL,
    l_name text NOT NULL,
    lawsuit text NOT NULL,
    level text NOT NULL,
    dan text NOT NULL,
    type text,
    status text,
    disciplinary text,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.prisoners_ OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16795)
-- Name: relations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.relations (
    id integer NOT NULL,
    prisoner_id bigint NOT NULL,
    relative_id bigint NOT NULL,
    relation text NOT NULL,
    is_active boolean DEFAULT true,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.relations OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16794)
-- Name: relations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.relations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.relations_id_seq OWNER TO postgres;

--
-- TOC entry 4948 (class 0 OID 0)
-- Dependencies: 221
-- Name: relations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.relations_id_seq OWNED BY public.relations.id;


--
-- TOC entry 220 (class 1259 OID 16779)
-- Name: relatives; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.relatives (
    relative_id bigint NOT NULL,
    title text NOT NULL,
    f_name text NOT NULL,
    l_name text NOT NULL,
    address text NOT NULL,
    tel text NOT NULL,
    fingerprint bytea,
    is_active boolean DEFAULT true,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.relatives OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 16902)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username text,
    password bytea,
    user_type text,
    fullname text
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16901)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4949 (class 0 OID 0)
-- Dependencies: 233
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 226 (class 1259 OID 16840)
-- Name: visit_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.visit_history (
    id integer NOT NULL,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    visit_date text NOT NULL,
    time_visit text NOT NULL,
    prisoner_id bigint NOT NULL,
    relative_id_1 bigint,
    relative_id_2 bigint,
    relative_id_3 bigint,
    relative_id_4 bigint,
    relative_id_5 bigint,
    channel integer,
    "desc" text
);


ALTER TABLE public.visit_history OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16839)
-- Name: visit_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.visit_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.visit_history_id_seq OWNER TO postgres;

--
-- TOC entry 4950 (class 0 OID 0)
-- Dependencies: 225
-- Name: visit_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.visit_history_id_seq OWNED BY public.visit_history.id;


--
-- TOC entry 228 (class 1259 OID 16859)
-- Name: visit_spacial; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.visit_spacial (
    visit_id integer NOT NULL,
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    date_visit text NOT NULL,
    time_visit text NOT NULL,
    prisoner_id bigint NOT NULL,
    relative_id_1 bigint,
    relative_id_2 bigint,
    relative_id_3 bigint,
    relative_id_4 bigint,
    relative_id_5 bigint,
    channel integer
);


ALTER TABLE public.visit_spacial OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16858)
-- Name: visit_spacial_visit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.visit_spacial_visit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.visit_spacial_visit_id_seq OWNER TO postgres;

--
-- TOC entry 4951 (class 0 OID 0)
-- Dependencies: 227
-- Name: visit_spacial_visit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.visit_spacial_visit_id_seq OWNED BY public.visit_spacial.visit_id;


--
-- TOC entry 224 (class 1259 OID 16820)
-- Name: visits; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.visits (
    visit_id integer NOT NULL,
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    date_visit text NOT NULL,
    time_visit text NOT NULL,
    prisoner_id bigint NOT NULL,
    relative_id_1 bigint,
    relative_id_2 bigint,
    relative_id_3 bigint,
    relative_id_4 bigint,
    relative_id_5 bigint,
    channel integer,
    visit_status text DEFAULT 'pending'::text
);


ALTER TABLE public.visits OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16819)
-- Name: visits_visit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.visits_visit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.visits_visit_id_seq OWNER TO postgres;

--
-- TOC entry 4952 (class 0 OID 0)
-- Dependencies: 223
-- Name: visits_visit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.visits_visit_id_seq OWNED BY public.visits.visit_id;


--
-- TOC entry 4754 (class 2604 OID 16881)
-- Name: check_ id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.check_ ALTER COLUMN id SET DEFAULT nextval('public.check__id_seq'::regclass);


--
-- TOC entry 4755 (class 2604 OID 16891)
-- Name: holidays id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holidays ALTER COLUMN id SET DEFAULT nextval('public.holidays_id_seq'::regclass);


--
-- TOC entry 4759 (class 2604 OID 16928)
-- Name: log_error log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.log_error ALTER COLUMN log_id SET DEFAULT nextval('public.log_error_log_id_seq'::regclass);


--
-- TOC entry 4757 (class 2604 OID 16917)
-- Name: log_realtime id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.log_realtime ALTER COLUMN id SET DEFAULT nextval('public.log_realtime_id_seq'::regclass);


--
-- TOC entry 4744 (class 2604 OID 16798)
-- Name: relations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relations ALTER COLUMN id SET DEFAULT nextval('public.relations_id_seq'::regclass);


--
-- TOC entry 4756 (class 2604 OID 16905)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4750 (class 2604 OID 16843)
-- Name: visit_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visit_history ALTER COLUMN id SET DEFAULT nextval('public.visit_history_id_seq'::regclass);


--
-- TOC entry 4752 (class 2604 OID 16862)
-- Name: visit_spacial visit_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visit_spacial ALTER COLUMN visit_id SET DEFAULT nextval('public.visit_spacial_visit_id_seq'::regclass);


--
-- TOC entry 4747 (class 2604 OID 16823)
-- Name: visits visit_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visits ALTER COLUMN visit_id SET DEFAULT nextval('public.visits_visit_id_seq'::regclass);


--
-- TOC entry 4774 (class 2606 OID 16886)
-- Name: check_ check__pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.check_
    ADD CONSTRAINT check__pkey PRIMARY KEY (id);


--
-- TOC entry 4776 (class 2606 OID 16900)
-- Name: holidays holidays_date_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holidays
    ADD CONSTRAINT holidays_date_key UNIQUE (date);


--
-- TOC entry 4778 (class 2606 OID 16898)
-- Name: holidays holidays_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holidays
    ADD CONSTRAINT holidays_pkey PRIMARY KEY (id);


--
-- TOC entry 4786 (class 2606 OID 16934)
-- Name: log_error log_error_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.log_error
    ADD CONSTRAINT log_error_pkey PRIMARY KEY (log_id);


--
-- TOC entry 4784 (class 2606 OID 16923)
-- Name: log_realtime log_realtime_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.log_realtime
    ADD CONSTRAINT log_realtime_pkey PRIMARY KEY (id);


--
-- TOC entry 4762 (class 2606 OID 16778)
-- Name: prisoners_ prisoners__pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prisoners_
    ADD CONSTRAINT prisoners__pkey PRIMARY KEY (prisoner_id);


--
-- TOC entry 4766 (class 2606 OID 16808)
-- Name: relations relations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relations
    ADD CONSTRAINT relations_pkey PRIMARY KEY (id);


--
-- TOC entry 4764 (class 2606 OID 16793)
-- Name: relatives relatives_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relatives
    ADD CONSTRAINT relatives_pkey PRIMARY KEY (relative_id);


--
-- TOC entry 4780 (class 2606 OID 16910)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4782 (class 2606 OID 16912)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4770 (class 2606 OID 16852)
-- Name: visit_history visit_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visit_history
    ADD CONSTRAINT visit_history_pkey PRIMARY KEY (id);


--
-- TOC entry 4772 (class 2606 OID 16871)
-- Name: visit_spacial visit_spacial_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visit_spacial
    ADD CONSTRAINT visit_spacial_pkey PRIMARY KEY (visit_id);


--
-- TOC entry 4768 (class 2606 OID 16833)
-- Name: visits visits_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visits
    ADD CONSTRAINT visits_pkey PRIMARY KEY (visit_id);


--
-- TOC entry 4787 (class 2606 OID 16809)
-- Name: relations relations_prisoner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relations
    ADD CONSTRAINT relations_prisoner_id_fkey FOREIGN KEY (prisoner_id) REFERENCES public.prisoners_(prisoner_id) ON DELETE RESTRICT;


--
-- TOC entry 4788 (class 2606 OID 16814)
-- Name: relations relations_relative_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relations
    ADD CONSTRAINT relations_relative_id_fkey FOREIGN KEY (relative_id) REFERENCES public.relatives(relative_id) ON DELETE RESTRICT;


--
-- TOC entry 4790 (class 2606 OID 16853)
-- Name: visit_history visit_history_prisoner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visit_history
    ADD CONSTRAINT visit_history_prisoner_id_fkey FOREIGN KEY (prisoner_id) REFERENCES public.prisoners_(prisoner_id) ON DELETE RESTRICT;


--
-- TOC entry 4791 (class 2606 OID 16872)
-- Name: visit_spacial visit_spacial_prisoner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visit_spacial
    ADD CONSTRAINT visit_spacial_prisoner_id_fkey FOREIGN KEY (prisoner_id) REFERENCES public.prisoners_(prisoner_id) ON DELETE RESTRICT;


--
-- TOC entry 4789 (class 2606 OID 16834)
-- Name: visits visits_prisoner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visits
    ADD CONSTRAINT visits_prisoner_id_fkey FOREIGN KEY (prisoner_id) REFERENCES public.prisoners_(prisoner_id) ON DELETE RESTRICT;


-- Completed on 2026-05-20 16:25:34

--
-- PostgreSQL database dump complete
--

\unrestrict rqghyIGqPmfHHTLn2VtLSjNWwtWLdJDYl2APfDiKrIo2hDzSPQFQhYTe8YQRluN

