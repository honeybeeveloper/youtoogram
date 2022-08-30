-- CREATE DATABASE youtoogram;
-- \c youtoogram;

-- create schema public;

comment on schema public is 'standard public schema';

alter schema public owner to postgres;

grant create, usage on schema public to public;

-- users
-- drop table users cascade;
create table users
(
    id serial,
    user_id varchar(60),
    password varchar(60),
    name varchar(30),
    nickname varchar(50),
    email varchar(50),
    phone varchar(30),
    profile varchar default null,
    created_at timestamp default now(),
    modified_at timestamp default null,
    constraint users_pk primary key (id),
    constraint users_user_id_key unique (user_id)
);
comment on table users is '사용자 테이블';
comment on column users.id is '사용자 정보 id';
comment on column users.user_id is '사용자 아이디';
comment on column users.password is '비밀번호';
comment on column users.name is '이름';
comment on column users.nickname is '애칭';
comment on column users.email is '이메일';
comment on column users.phone is '휴대전화번호';
comment on column users.profile is '자기소개';
comment on column users.created_at is '등록 일시';
comment on column users.modified_at is '수정 일시';

-- post
-- drop table post cascade;
create table post
(
    id serial,
    user_id varchar(60),
    gram varchar(1000),
    photo_1 varchar default null,
    photo_2 varchar default null,
    photo_3 varchar default null,
    photo_4 varchar default null,
    photo_5 varchar default null,
	created_at timestamp default now(),
	modified_at timestamp default null,
	constraint post_pk primary key (id),
	constraint post_user_id_fk foreign key (user_id) references users (user_id) on delete cascade on update cascade
);
comment on table post is '게시물 테이블';
comment on column post.id is '게시물 정보 id';
comment on column post.user_id is '게시글 작성 아이디';
comment on column post.gram is '게시글';
comment on column post.photo_1 is '사진 경로 1';
comment on column post.photo_2 is '사진 경로 2';
comment on column post.photo_3 is '사진 경로 3';
comment on column post.photo_4 is '사진 경로 4';
comment on column post.photo_5 is '사진 경로 5';
comment on column post.created_at is '등록 일시';
comment on column post.modified_at is '수정 일시';

-- follow
-- drop table follow cascade;
create table follow
(
	id serial,
    user_id varchar(60),
    follow_id varchar(60),
	created_at timestamp default now(),
	constraint follow_pk primary key (id),
	constraint follow_user_id_follow_id_key UNIQUE (user_id, follow_id),
	constraint follow_user_id_fk foreign key (user_id) references users (user_id) on delete cascade on update cascade
);
comment on table follow is '팔로우 테이블';
comment on column follow.id is '팔로우 정보 id';
comment on column follow.user_id is '사용자 아이디';
comment on column follow.follow_id is '팔로우 대상 아이디';
comment on column follow.created_at is '등록 일시';


-- sequence initialization
ALTER SEQUENCE users_id_seq RESTART WITH 1;
ALTER SEQUENCE post_id_seq RESTART WITH 1;
ALTER SEQUENCE follow_id_seq RESTART WITH 1;


commit;