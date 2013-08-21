### New Model: language_data.AbsSyntax
CREATE TABLE "language_data_abssyntax" (
    "id" serial NOT NULL PRIMARY KEY,
    "node_id" varchar(15) NOT NULL,
    "parent_node" varchar(15),
    "category" varchar(10) NOT NULL,
    "rule" varchar(50),
    "words" text NOT NULL
)
;
