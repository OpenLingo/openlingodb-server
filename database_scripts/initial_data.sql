USE OpenLingo;

-- Instantiate strong entities:
INSERT INTO `language` -- [id, code, title, is_gendered]
    (code, title, is_gendered)
VALUES 
    ('ENG', 'English', 0),
    ('GER', 'German', 1);

INSERT INTO user -- [id, email, password, role, timezone]
    (email, `password`, `role`, timezone)
VALUES
    -- test dummy users 
    ('user.user@openlingo.com', 'user_password', 'user', 'UTC+10'),
    ('user.contributor@openlingo.com', 'contributor_password', 'contributor', 'UTC+10'),
    ('user.admin@openlingo.com', 'admin_password', 'admin', 'UTC+10');


-- Instantiate entities with one foreign key:
INSERT INTO dialect -- [id, language_id, code, title]
    (language_id, code, title)
VALUES 
    (1, 'en-AU', 'Australian English'),
    (1, 'en-GB', 'British English'),
    (1, 'en-US', 'American English'),
    (1, 'en-CA', 'Canadian English'),
    (2, 'de-DE', 'High German'),
    (2, 'de-AT', 'Austrian German'),
    (2, 'de-CH', 'Swiss German');

INSERT INTO `level` -- [id, language_id, code, title]
    (language_id, code, title)
VALUES
    -- English levels:
    (1, 'FUNC', 'Functional'), 
    (1, 'VOC', 'Vocational'),
    (1, 'COMP', 'Competent'),
    (1, 'PROF', 'Proficient'),
    (1, 'SUP', 'Superior'),
    -- German levels:
    (2, 'A1', 'Beginner'),
    (2, 'A2', 'Elementary'),
    (2, 'B1', 'Intermediate'),
    (2, 'B2', 'Upper Intermediate'),
    (2, 'C1', 'Advanced'),
    (2, 'C2', 'Highly Competent');

-- Instantiate entities with two foreign keys:
-- English words
INSERT INTO noun
    (language_id, word)
VALUES
    (1, 'Mother'),
    (1, 'Father'),
    (1, 'Sister'),
    (1, 'Brother'),
    (1, 'Child'),
    (1, 'Aunt'),
    (1, 'Uncle'),
    (1, 'Grandmother'),
    (1, 'GrandFather');
-- German words
INSERT INTO noun -- [id, language_id, level_id, gender, word]
    (language_id, gender, word)
VALUES
    (2, 'f', 'Mutter'),
    (2, 'm', 'Vater'),
    (2, 'f', 'Schwester'),
    (2, 'm', 'Bruder'),
    (2, 'n', 'Kind'),
    (2, 'f', 'Tante'),
    (2, 'm', 'Onkel'),
    (2, 'f', 'Großmutter'),
    (2, 'm', 'Großvater'),
    (2, 'f', 'Mutti');

INSERT INTO noun_translation -- [id, noun_from, noun_to, accuracy]
    (from_noun_id, to_noun_id, accuracy)
VALUES
    (1, 10, 100),
    (1, 19, 50),
    (2, 11, 100),
    (3, 12, 100),
    (4, 13, 100),
    (5, 14, 100),
    (6, 15, 100),
    (7, 16, 100),
    (8, 17, 100),
    (9, 18, 100);
-- Instantiate entities with three foreign keys:
INSERT INTO user_language -- [id, dialect_id, level_id, user_id, is_native, qual_level]
    (dialect_id, level_id, user_id, is_native, qual_level)
VALUES 
    (1, 5, 2, 1, 'EXP'),
    (5, 11, 2, 0, 'EXP'),
    (3, 5, 1, 1, 'EXP'),
    (6, 9, 1, 0, 'INT'),
    (2, 5, 3, 1, 'EXP');

