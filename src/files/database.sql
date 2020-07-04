CREATE TYPE "playerrole" AS ENUM (
  'spectator',
  'player',
  'player_gm',
  'gm'
);

CREATE TABLE "users" (
  "id" uuid PRIMARY KEY,
  "login" varchar(50) UNIQUE NOT NULL,
  "username" varchar(50) NOT NULL,
  "email" varchar(255) UNIQUE NOT NULL,
  "password" varchar(255) NOT NULL,
  "role" int,
  "created_at" timestamp
);

CREATE TABLE "groups" (
  "id" uuid PRIMARY KEY,
  "name" varchar(255) NOT NULL
);

CREATE TABLE "m_users_groups" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid NOT NULL,
  "group_id" uuid NOT NULL,
  "role" playerrole NOT NULL
);

CREATE TABLE "characters" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid NOT NULL,
  "group_id" uuid,
  "name" varchar(255)
);

CREATE TABLE "l_head" (
  "id" uuid PRIMARY KEY,
  "title" varchar(255) NOT NULL,
  "description" text
);

CREATE TABLE "c_head" (
  "id" uuid PRIMARY KEY,
  "list_id" uuid NOT NULL,
  "character_id" uuid NOT NULL,
  "value_id" uuid NOT NULL
);

CREATE TABLE "v_head" (
  "id" uuid PRIMARY KEY,
  "value" varchar(255) NOT NULL,
  "list_id" uuid NOT NULL
);

CREATE TABLE "l_attributes" (
  "id" uuid PRIMARY KEY,
  "title" varchar(255) NOT NULL,
  "description" text
);

CREATE TABLE "c_attributes" (
  "id" uuid PRIMARY KEY,
  "list_id" uuid NOT NULL,
  "character_id" uuid NOT NULL,
  "value" int NOT NULL
);

CREATE TABLE "l_advantages" (
  "id" uuid PRIMARY KEY,
  "title" varchar(255) UNIQUE NOT NULL,
  "description" text
);

CREATE TABLE "c_advantages" (
  "id" uuid PRIMARY KEY,
  "list_id" uuid NOT NULL,
  "character_id" uuid NOT NULL,
  "value_id" uuid
);

CREATE TABLE "v_advantages" (
  "id" uuid PRIMARY KEY,
  "list_id" uuid NOT NULL,
  "value" varchar(255) NOT NULL
);

CREATE TABLE "experiences" (
  "id" uuid PRIMARY KEY,
  "character_id" uuid NOT NULL,
  "experience_rank_id" uuid NOT NULL
);

CREATE TABLE "experience_ranks" (
  "id" uuid PRIMARY KEY,
  "title" varchar(255) UNIQUE NOT NULL,
  "experience_points" int NOT NULL
);

CREATE TABLE "l_skills" (
  "id" uuid PRIMARY KEY,
  "title" varchar(255) UNIQUE NOT NULL,
  "description" text,
  "attribute_1_id" uuid NOT NULL,
  "attribute_2_id" uuid NOT NULL,
  "attribute_3_id" uuid NOT NULL
);

CREATE TABLE "c_skills" (
  "id" uuid PRIMARY KEY,
  "list_id" uuid NOT NULL,
  "character_id" uuid NOT NULL,
  "value" int NOT NULL
);

CREATE TABLE "l_languages" (
  "id" uuid PRIMARY KEY,
  "title" varchar(255) UNIQUE NOT NULL,
  "description" text
);

CREATE TABLE "c_languages" (
  "id" uuid PRIMARY KEY,
  "list_id" uuid NOT NULL,
  "character_id" uuid NOT NULL,
  "value" int NOT NULL
);

CREATE TABLE "l_scripts" (
  "id" uuid PRIMARY KEY,
  "title" varchar(255) UNIQUE NOT NULL,
  "description" text
);

CREATE TABLE "c_scripts" (
  "id" uuid PRIMARY KEY,
  "list_id" uuid NOT NULL,
  "character_id" uuid NOT NULL,
  "value" int NOT NULL
);

ALTER TABLE "m_users_groups" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "m_users_groups" ADD FOREIGN KEY ("group_id") REFERENCES "groups" ("id");

ALTER TABLE "characters" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "characters" ADD FOREIGN KEY ("group_id") REFERENCES "groups" ("id");

ALTER TABLE "c_head" ADD FOREIGN KEY ("list_id") REFERENCES "l_head" ("id");

ALTER TABLE "c_head" ADD FOREIGN KEY ("character_id") REFERENCES "characters" ("id");

ALTER TABLE "c_head" ADD FOREIGN KEY ("value_id") REFERENCES "v_head" ("id");

ALTER TABLE "v_head" ADD FOREIGN KEY ("list_id") REFERENCES "l_head" ("id");

ALTER TABLE "c_attributes" ADD FOREIGN KEY ("list_id") REFERENCES "l_attributes" ("id");

ALTER TABLE "c_attributes" ADD FOREIGN KEY ("character_id") REFERENCES "characters" ("id");

ALTER TABLE "c_advantages" ADD FOREIGN KEY ("list_id") REFERENCES "l_advantages" ("id");

ALTER TABLE "c_advantages" ADD FOREIGN KEY ("character_id") REFERENCES "characters" ("id");

ALTER TABLE "c_advantages" ADD FOREIGN KEY ("value_id") REFERENCES "v_advantages" ("id");

ALTER TABLE "v_advantages" ADD FOREIGN KEY ("list_id") REFERENCES "l_advantages" ("id");

ALTER TABLE "experiences" ADD FOREIGN KEY ("character_id") REFERENCES "characters" ("id");

ALTER TABLE "experiences" ADD FOREIGN KEY ("experience_rank_id") REFERENCES "experience_ranks" ("id");

ALTER TABLE "l_skills" ADD FOREIGN KEY ("attribute_1_id") REFERENCES "l_attributes" ("id");

ALTER TABLE "l_skills" ADD FOREIGN KEY ("attribute_2_id") REFERENCES "l_attributes" ("id");

ALTER TABLE "l_skills" ADD FOREIGN KEY ("attribute_3_id") REFERENCES "l_attributes" ("id");

ALTER TABLE "c_skills" ADD FOREIGN KEY ("list_id") REFERENCES "l_skills" ("id");

ALTER TABLE "c_skills" ADD FOREIGN KEY ("character_id") REFERENCES "characters" ("id");

ALTER TABLE "c_languages" ADD FOREIGN KEY ("list_id") REFERENCES "l_languages" ("id");

ALTER TABLE "c_languages" ADD FOREIGN KEY ("character_id") REFERENCES "characters" ("id");

ALTER TABLE "c_scripts" ADD FOREIGN KEY ("list_id") REFERENCES "l_scripts" ("id");

ALTER TABLE "c_scripts" ADD FOREIGN KEY ("character_id") REFERENCES "characters" ("id");

COMMENT ON COLUMN "users"."password" IS 'password-function';
