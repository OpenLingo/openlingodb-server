CREATE DATABASE IF NOT EXISTS OpenLingo;
USE OpenLingo;

-- Strong entities
CREATE TABLE IF NOT EXISTS `language` (
    id INT NOT NULL AUTO_INCREMENT,
    code VARCHAR(10) NOT NULL,
    title VARCHAR(50) NOT NULL,
    is_gendered TINYINT(1),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS user (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL,
    `password` VARCHAR(50) NOT NULL,
    `role` ENUM('Contributor', 'Moderator', 'Admin') NOT NULL,
    timezone VARCHAR(10) NOT NULL,
    PRIMARY KEY(id)
);

-- Entities with one foreign Key
CREATE TABLE IF NOT EXISTS app_log (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT, -- must be nullable in case a user chooses to delete their acc
    log_level INT NOT NULL,
    `message` VARCHAR(1000) NOT NULL,
    date_time DATETIME NOT NULL,
    creator VARCHAR(32) NOT NULL,
    source VARCHAR(160) NOT NULL,
    request VARCHAR(160) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT `fk_log_author`
        FOREIGN KEY(user_id) 
        REFERENCES user(id)
        ON DELETE SET NULL -- log remains with anonymous author if user is deleted
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS dialect (
    id INT NOT NULL AUTO_INCREMENT,
    language_id INT NOT NULL,
    code VARCHAR(20) NOT NULL, -- IETF Standard
    title VARCHAR(50) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT `fk_dialect_language`
        FOREIGN KEY(language_id) 
        REFERENCES `language`(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS feedback (
    id INT NOT NULL AUTO_INCREMENT, 
    user_id NULL, -- must be nullable in case a user chooses to delete their acc
    comment VARCHAR(1000) NOT NULL,
    json_data VARCHAR(200),
    entity VARCHAR(50),
    entity_id INT,
    is_approved TINYINT(1),
    PRIMARY KEY(id),
    CONSTRAINT `fk_feedback_author`
        FOREIGN KEY(user_id) 
        REFERENCES user(id)
        ON DELETE SET NULL -- feedback remains with anonymous author if user is deleted
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `level` (
    id INT NOT NULL AUTO_INCREMENT,
    language_id INT NOT NULL,
    code VARCHAR(10) NOT NULL,
    title VARCHAR(50) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT `fk_level_language`
        FOREIGN KEY(language_id) 
        REFERENCES `language`(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS note (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    comment VARCHAR(1000) NOT NULL,
    json_data VARCHAR(200),
    entity VARCHAR(50),
    entity_id INT,
    is_public TINYINT(1),
    PRIMARY KEY(id),
    CONSTRAINT `fk_note_author`
        FOREIGN KEY(user_id) 
        REFERENCES user(id)
        ON DELETE CASCADE -- user notes do not remain if the user is deleted
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS topic (
    id INT NOT NULL AUTO_INCREMENT,
    level_id INT,  -- must be nullable in case a level is deleted 
    title VARCHAR(50) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT `fk_topic_level`
        FOREIGN KEY(level_id) 
        REFERENCES `level`(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Entities with two foreign keys
CREATE TABLE IF NOT EXISTS noun (
    id INT NOT NULL AUTO_INCREMENT,
    language_id INT NOT NULL,
    level_id INT, -- must be nullable in case a level is deleted, and for pre-release use
    gender VARCHAR(1),
    word VARCHAR(50) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT `fk_noun_language`
        FOREIGN KEY(language_id) 
        REFERENCES `language`(id)
        ON DELETE RESTRICT -- prevents admins from accidentally deleting a language
        ON UPDATE CASCADE,
    CONSTRAINT `fk_noun_level`
        FOREIGN KEY(level_id) 
        REFERENCES `level`(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CHECK(gender IN ('f', 'm', 'n', NULL))
);

CREATE TABLE IF NOT EXISTS `definition` (
    -- Potential normalistion gains: 
    -- > could split definition dialect into an interstitial table to facilitate
    --   multiple dialects explicitly having the same definition of a word.
    -- > could remove the dialect attribute entirely and inject the dependency 
    --   elsewhere.
    id INT NOT NULL AUTO_INCREMENT,
    dialect_id INT,
    noun_id INT NOT NULL,
    `text` VARCHAR(400) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT `fk_definition_dialect` 
        FOREIGN KEY(dialect_id) 
        REFERENCES dialect(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT `fk_definition_noun`
        FOREIGN KEY(noun_id) 
        REFERENCES noun(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS noun_dialect (
    id INT NOT NULL AUTO_INCREMENT,
    dialect_id INT NOT NULL,
    noun_id INT NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT `fk_noun_dialect_dialect`
        FOREIGN KEY(dialect_id) 
        REFERENCES dialect(id)
        ON DELETE RESTRICT -- prevents admins from accidentally deleting a dialect
        ON UPDATE CASCADE,
    CONSTRAINT `fk_noun_dialect_noun`
        FOREIGN KEY(noun_id) 
        REFERENCES noun(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS noun_topic (
    id INT NOT NULL AUTO_INCREMENT,
    noun_id INT NOT NULL,
    topic_id INT NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT `fk_noun_topic_noun`
        FOREIGN KEY(noun_id) 
        REFERENCES noun(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT `fk_noun_topic_topic`
        FOREIGN KEY(topic_id) 
        REFERENCES topic(id)
        ON DELETE RESTRICT -- prevents admins from accidentally deleting a topic
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS noun_translation (
    id INT NOT NULL AUTO_INCREMENT,
    from_noun_id INT NOT NULL,
    to_noun_id INT NOT NULL,
    accuracy TINYINT NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT `fk_translation_from`
        FOREIGN KEY(from_noun_id) 
        REFERENCES noun(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT `fk_traslation_to`
        FOREIGN KEY(to_noun_id) 
        REFERENCES noun(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS recording (
    id INT NOT NULL AUTO_INCREMENT,
    noun_id INT NOT NULL,
    user_id INT,
    date_time_recorded DATETIME NOT NULL,
    `filename` VARCHAR(45) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT `fk_recording_noun`
        FOREIGN KEY(noun_id) 
        REFERENCES noun(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT `fk_recording_author`
        FOREIGN KEY(user_id) 
        REFERENCES user(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE

);

CREATE TABLE IF NOT EXISTS topic_child (
    id INT NOT NULL AUTO_INCREMENT,
    child_topic_id INT NOT NULL,
    parent_topic_id INT NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT `fk_topic_child_child`
        FOREIGN KEY(child_topic_id) 
        REFERENCES topic(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT `fk_topic_child_parent`
        FOREIGN KEY(parent_topic_id) 
        REFERENCES topic(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Entities with three foreign keys
CREATE TABLE IF NOT EXISTS user_language (
    id INT NOT NULL AUTO_INCREMENT,
    dialect_id INT NOT NULL,
    level_id INT,
    user_id INT NOT NULL,
    is_native TINYINT(1) NOT NULL,
    qual_level VARCHAR(4) NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT `fk_user_language_dialect`
        FOREIGN KEY(dialect_id) 
        REFERENCES dialect(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT `fk_user_language_level`
        FOREIGN KEY(level_id) 
        REFERENCES `level`(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT `fk_user_language_user`
        FOREIGN KEY(user_id) 
        REFERENCES user(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CHECK(qual_level IN ('BEG', 'INT', 'COMP', 'PROF', 'EXP'))
);