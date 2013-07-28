### New Model: admin.LogEntry
CREATE TABLE "django_admin_log" (
    "id" serial NOT NULL PRIMARY KEY,
    "action_time" timestamp with time zone NOT NULL,
    "user_id" integer NOT NULL,
    "content_type_id" integer,
    "object_id" text,
    "object_repr" varchar(200) NOT NULL,
    "action_flag" smallint CHECK ("action_flag" >= 0) NOT NULL,
    "change_message" text NOT NULL
)
;
### New Model: auth.Permission
CREATE TABLE "auth_permission" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
)
;
### New Model: auth.Group_permissions
CREATE TABLE "auth_group_permissions" (
    "id" serial NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("group_id", "permission_id")
)
;
### New Model: auth.Group
CREATE TABLE "auth_group" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(80) NOT NULL UNIQUE
)
;
ALTER TABLE "auth_group_permissions" ADD CONSTRAINT "group_id_refs_id_f4b32aac" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: auth.User_groups
CREATE TABLE "auth_user_groups" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "group_id")
)
;
### New Model: auth.User_user_permissions
CREATE TABLE "auth_user_user_permissions" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "permission_id")
)
;
### New Model: auth.User
CREATE TABLE "auth_user" (
    "id" serial NOT NULL PRIMARY KEY,
    "password" varchar(128) NOT NULL,
    "last_login" timestamp with time zone NOT NULL,
    "is_superuser" boolean NOT NULL,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "is_staff" boolean NOT NULL,
    "is_active" boolean NOT NULL,
    "date_joined" timestamp with time zone NOT NULL
)
;
ALTER TABLE "django_admin_log" ADD CONSTRAINT "user_id_refs_id_c0d12874" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "auth_user_groups" ADD CONSTRAINT "user_id_refs_id_40c41112" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "auth_user_user_permissions" ADD CONSTRAINT "user_id_refs_id_4dc23c39" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: contenttypes.ContentType
CREATE TABLE "django_content_type" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
)
;
ALTER TABLE "django_admin_log" ADD CONSTRAINT "content_type_id_refs_id_93d2d1f8" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "auth_permission" ADD CONSTRAINT "content_type_id_refs_id_d043b34a" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: sessions.Session
CREATE TABLE "django_session" (
    "session_key" varchar(40) NOT NULL PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" timestamp with time zone NOT NULL
)
;
### New Model: sites.Site
CREATE TABLE "django_site" (
    "id" serial NOT NULL PRIMARY KEY,
    "domain" varchar(100) NOT NULL,
    "name" varchar(50) NOT NULL
)
;
### New Model: account.Account
CREATE TABLE "account_account" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "timezone" varchar(100) NOT NULL,
    "language" varchar(10) NOT NULL
)
;
### New Model: account.SignupCode
CREATE TABLE "account_signupcode" (
    "id" serial NOT NULL PRIMARY KEY,
    "code" varchar(64) NOT NULL UNIQUE,
    "max_uses" integer CHECK ("max_uses" >= 0) NOT NULL,
    "expiry" timestamp with time zone,
    "inviter_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "email" varchar(75) NOT NULL,
    "notes" text NOT NULL,
    "sent" timestamp with time zone,
    "created" timestamp with time zone NOT NULL,
    "use_count" integer CHECK ("use_count" >= 0) NOT NULL
)
;
### New Model: account.SignupCodeResult
CREATE TABLE "account_signupcoderesult" (
    "id" serial NOT NULL PRIMARY KEY,
    "signup_code_id" integer NOT NULL REFERENCES "account_signupcode" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "timestamp" timestamp with time zone NOT NULL
)
;
### New Model: account.EmailAddress
CREATE TABLE "account_emailaddress" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "email" varchar(75) NOT NULL UNIQUE,
    "verified" boolean NOT NULL,
    "primary" boolean NOT NULL
)
;
### New Model: account.EmailConfirmation
CREATE TABLE "account_emailconfirmation" (
    "id" serial NOT NULL PRIMARY KEY,
    "email_address_id" integer NOT NULL REFERENCES "account_emailaddress" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created" timestamp with time zone NOT NULL,
    "sent" timestamp with time zone,
    "key" varchar(64) NOT NULL UNIQUE
)
;
### New Model: account.AccountDeletion
CREATE TABLE "account_accountdeletion" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "email" varchar(75) NOT NULL,
    "date_requested" timestamp with time zone NOT NULL,
    "date_expunged" timestamp with time zone
)
;
### New Model: eventlog.Log
CREATE TABLE "eventlog_log" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "timestamp" timestamp with time zone NOT NULL,
    "action" varchar(50) NOT NULL,
    "extra" text NOT NULL
)
;
### New Model: learning_greek.Preference
CREATE TABLE "learning_greek_preference" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "adoption_level" varchar(20) NOT NULL
)
;
### New Model: activities.UserState
CREATE TABLE "activities_userstate" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "data" text NOT NULL
)
;
### New Model: activities.ActivityState
CREATE TABLE "activities_activitystate" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "activity_slug" varchar(50) NOT NULL,
    "completed_count" integer NOT NULL,
    "data" text NOT NULL,
    UNIQUE ("user_id", "activity_slug")
)
;
### New Model: activities.ActivityOccurrenceState
CREATE TABLE "activities_activityoccurrencestate" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "activity_slug" varchar(50) NOT NULL,
    "started" timestamp with time zone NOT NULL,
    "completed" timestamp with time zone,
    "data" text NOT NULL,
    UNIQUE ("user_id", "activity_slug", "started")
)
;
### New Model: language_data.NounCumulativeCount
CREATE TABLE "language_data_nouncumulativecount" (
    "id" serial NOT NULL PRIMARY KEY,
    "lemma" varchar(50) NOT NULL,
    "cumulative_count" integer NOT NULL
)
;
### New Model: language_data.NounCaseNumberGender
CREATE TABLE "language_data_nouncasenumbergender" (
    "id" serial NOT NULL PRIMARY KEY,
    "lemma" varchar(50) NOT NULL,
    "case" varchar(1) NOT NULL,
    "number" varchar(1) NOT NULL,
    "gender" varchar(1) NOT NULL
)
;
### New Model: language_data.DickinsonCoreList
CREATE TABLE "language_data_dickinsoncorelist" (
    "id" serial NOT NULL PRIMARY KEY,
    "lemma" varchar(50) NOT NULL,
    "headword" text NOT NULL,
    "definition" text NOT NULL,
    "pos" varchar(20) NOT NULL,
    "pos_detail" varchar(50) NOT NULL,
    "semantic_group" varchar(50) NOT NULL
)
;
CREATE INDEX "django_admin_log_user_id" ON "django_admin_log" ("user_id");
CREATE INDEX "django_admin_log_content_type_id" ON "django_admin_log" ("content_type_id");
CREATE INDEX "auth_permission_content_type_id" ON "auth_permission" ("content_type_id");
CREATE INDEX "auth_group_permissions_group_id" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id" ON "auth_group_permissions" ("permission_id");
CREATE INDEX "auth_group_name_like" ON "auth_group" ("name" varchar_pattern_ops);
CREATE INDEX "auth_user_groups_user_id" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_group_id" ON "auth_user_groups" ("group_id");
CREATE INDEX "auth_user_user_permissions_user_id" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "auth_user_user_permissions_permission_id" ON "auth_user_user_permissions" ("permission_id");
CREATE INDEX "auth_user_username_like" ON "auth_user" ("username" varchar_pattern_ops);
CREATE INDEX "django_session_session_key_like" ON "django_session" ("session_key" varchar_pattern_ops);
CREATE INDEX "django_session_expire_date" ON "django_session" ("expire_date");
CREATE INDEX "account_signupcode_code_like" ON "account_signupcode" ("code" varchar_pattern_ops);
CREATE INDEX "account_signupcode_inviter_id" ON "account_signupcode" ("inviter_id");
CREATE INDEX "account_signupcoderesult_signup_code_id" ON "account_signupcoderesult" ("signup_code_id");
CREATE INDEX "account_signupcoderesult_user_id" ON "account_signupcoderesult" ("user_id");
CREATE INDEX "account_emailaddress_user_id" ON "account_emailaddress" ("user_id");
CREATE INDEX "account_emailaddress_email_like" ON "account_emailaddress" ("email" varchar_pattern_ops);
CREATE INDEX "account_emailconfirmation_email_address_id" ON "account_emailconfirmation" ("email_address_id");
CREATE INDEX "account_emailconfirmation_key_like" ON "account_emailconfirmation" ("key" varchar_pattern_ops);
CREATE INDEX "account_accountdeletion_user_id" ON "account_accountdeletion" ("user_id");
CREATE INDEX "eventlog_log_user_id" ON "eventlog_log" ("user_id");
CREATE INDEX "activities_activitystate_user_id" ON "activities_activitystate" ("user_id");
CREATE INDEX "activities_activityoccurrencestate_user_id" ON "activities_activityoccurrencestate" ("user_id");
