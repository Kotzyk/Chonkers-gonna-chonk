CREATE TABLE Users(
   UserId INTEGER PRIMARY KEY,
   Username TEXT,
   Password TEXT
);

CREATE TABLE Ratings(
    Id INTEGER PRIMARY KEY,
    UserId INTEGER ,
    ImageId INTEGER,
    Score INTEGER
);