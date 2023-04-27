CREATE TABLE IF NOT EXISTS spotok_user (
  pk int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id varchar(255) not null unique,
  email varchar(255) not null unique,
  display_name varchar(255) NOT NULL,
  country varchar(50) DEFAULT 'US' NOT NULL,
  phone varchar(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  verified tinyint(1) DEFAULT 0 NOT NULL,
  origin varchar(50) not null
); 

CREATE TABLE IF NOT EXISTS auth (
  pk int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  access_token VARCHAR(255) NOT NULL unique,
  refresh_token VARCHAR(255) NOT NULL unique,
  expires_at TIMESTAMP NOT NULL,
  auth_type ENUM('basic', 'spotify') not null default 'basic',
  CONSTRAINT fk_auth_table_user_id 
    FOREIGN KEY (user_id) REFERENCES spotok_user (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS genre (
  pk int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  genre_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS track (
  pk int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id VARCHAR(255) NOT NULL UNIQUE,
  track_name VARCHAR(255) NOT NULL,
  uri VARCHAR(255),
  href VARCHAR(255) NOT NULL,
  duration_ms DOUBLE NOT NULL,
  catchy_start DOUBLE,
  origin VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS artist (
  pk int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id VARCHAR(255) NOT NULL UNIQUE,
  artist_name VARCHAR(255) NOT NULL,
  uri VARCHAR(255),
  href VARCHAR(255) NOT NULL,
  origin VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS track_image (
  pk int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  href VARCHAR(255) NOT NULL,
  width int,
  height int,
  track_id VARCHAR(255) NOT NULL,
  CONSTRAINT fk_track_image
    FOREIGN KEY (track_id) REFERENCES track (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS track_artist (
  pk int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  track_id VARCHAR(255) NOT NULL,
  artist_id VARCHAR(255) NOT NULL,
  CONSTRAINT fk_track_artist_table_track_id
    FOREIGN KEY (track_id) REFERENCES track (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_track_artist_table_artist_id
    FOREIGN KEY (artist_id) REFERENCES artist (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS user_selected_genre (
  pk int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  genre_id INT NOT NULL,
  CONSTRAINT fk_user_genre_table_user_id
    FOREIGN KEY (user_id) REFERENCES spotok_user (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_user_genre_table_genre_id
    FOREIGN KEY (genre_id) REFERENCES genre (pk) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS user_favorite_track (
  pk int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  track_id VARCHAR(255) NOT NULL,
  CONSTRAINT fk_user_favorite_table_user_id
    FOREIGN KEY (user_id) REFERENCES spotok_user (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_user_favorite_table_track_id
    FOREIGN KEY (track_id) REFERENCES track (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS track_genre (
  pk int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  track_id VARCHAR(255) NOT NULL,
  genre_id INT NOT NULL,
  CONSTRAINT fk_track_genre_table_track_id
    FOREIGN KEY (track_id) REFERENCES track (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_track_genre_table_genre_id
    FOREIGN KEY (genre_id) REFERENCES genre (pk) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS user_most_liked_genre (
  pk int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  genre_id INT NOT NULL,
  count INT NOT NULL DEFAULT 0,
  CONSTRAINT fk_user_most_liked_genre_table_user_id
    FOREIGN KEY (user_id) REFERENCES spotok_user (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_user_most_liked_genre_table_genre_id
    FOREIGN KEY (genre_id) REFERENCES genre (pk) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT uk_user_most_liked_genre_table_unique_user_and_genre
    UNIQUE KEY unique_index (user_id, genre_id)
);
