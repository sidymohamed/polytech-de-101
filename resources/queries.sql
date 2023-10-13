create schema consolidate;

drop table if exists consolidate.consolidate_gists;
create table consolidate.consolidate_gists(
   "url"          VARCHAR(256) 
  ,"forks_url"    VARCHAR(256) 
  ,"commits_url"  VARCHAR(256)
  ,"id"           VARCHAR(256)  primary KEY
  ,"node_id"      VARCHAR(256) 
  ,"public"       BOOL 
  ,"created_at"   TIMESTAMP 
  ,"updated_at"   TIMESTAMP 
  ,"description"  VARCHAR(256)
  ,"comments"     INTEGER 
  ,"user"         VARCHAR(256)
  ,"comments_url" VARCHAR(256) 
  ,"owner_login"  VARCHAR(256) 
  ,"owner_id"     INTEGER 
  ,"truncated"    BOOL
);

drop table if exists consolidate.consolidate_repositories;
create table consolidate.consolidate_repositories(
  "id"            VARCHAR(256)  primary key,
  "name"		  VARCHAR(256),
  "full_name"     VARCHAR(256),
  "description"   VARCHAR(256),
  "size"              INTEGER,
  "stargazers_count"  INTEGER,
  "watchers_count"    INTEGER,
  "forks_count"       INTEGER,
  "open_issues_count" INTEGER,
  "visibility"    VARCHAR(256),
  "html_url"      VARCHAR(256),
  "forks_url"     VARCHAR(256),
  "commits_url"   VARCHAR(256),
  "languages_url" VARCHAR(256),
  "issues_url"    VARCHAR(256)
);
