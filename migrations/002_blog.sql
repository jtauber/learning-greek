### New Model: biblion.Post
CREATE TABLE "biblion_post" (
    "id" serial NOT NULL PRIMARY KEY,
    "section" integer NOT NULL,
    "title" varchar(90) NOT NULL,
    "slug" varchar(50) NOT NULL,
    "author_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "teaser_html" text NOT NULL,
    "content_html" text NOT NULL,
    "tweet_text" varchar(140) NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "updated" timestamp with time zone,
    "published" timestamp with time zone,
    "view_count" integer NOT NULL
)
;
### New Model: biblion.Revision
CREATE TABLE "biblion_revision" (
    "id" serial NOT NULL PRIMARY KEY,
    "post_id" integer NOT NULL REFERENCES "biblion_post" ("id") DEFERRABLE INITIALLY DEFERRED,
    "title" varchar(90) NOT NULL,
    "teaser" text NOT NULL,
    "content" text NOT NULL,
    "author_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "updated" timestamp with time zone NOT NULL,
    "published" timestamp with time zone,
    "view_count" integer NOT NULL
)
;
### New Model: biblion.Image
CREATE TABLE "biblion_image" (
    "id" serial NOT NULL PRIMARY KEY,
    "post_id" integer NOT NULL REFERENCES "biblion_post" ("id") DEFERRABLE INITIALLY DEFERRED,
    "image_path" varchar(100) NOT NULL,
    "url" varchar(150) NOT NULL,
    "timestamp" timestamp with time zone NOT NULL
)
;
### New Model: biblion.FeedHit
CREATE TABLE "biblion_feedhit" (
    "id" serial NOT NULL PRIMARY KEY,
    "request_data" text NOT NULL,
    "created" timestamp with time zone NOT NULL
)
;
CREATE INDEX "biblion_post_slug" ON "biblion_post" ("slug");
CREATE INDEX "biblion_post_slug_like" ON "biblion_post" ("slug" varchar_pattern_ops);
CREATE INDEX "biblion_post_author_id" ON "biblion_post" ("author_id");
CREATE INDEX "biblion_revision_post_id" ON "biblion_revision" ("post_id");
CREATE INDEX "biblion_revision_author_id" ON "biblion_revision" ("author_id");
CREATE INDEX "biblion_image_post_id" ON "biblion_image" ("post_id");
