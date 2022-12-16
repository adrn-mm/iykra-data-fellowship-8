-- # 2. Table Creation
create table kdrama_list (
    list_id int primary key,
    drama_name varchar(150),
    episodes int,
    orig_network varchar(75),
    score_list float,
    scored_by int,
    watchers float,
    imdb_desc varchar(255)
    );

-- # 3. Data insertion
insert into kdrama_list values 
    (1, 'Move to Heaven', 10, 'Netflix', 9.2, 26058, 51979, 'Working as trauma cleaners, both Gu-ru and Sang-gu uncover various stories of the deceased while exp...'),
    (2, 'Extraordinary Attorney Woo', 16, 'Netflix', 9.2, 8535, 33699, 'About an autistic 27-year-old lawyer. Due to her high IQ of 164, impressive memory, and creative tho...'),
    (3, 'Hospital Playlist', 12, 'Netlix-TVN', 9.1, 32842, 72138, 'Hospital Playlist tells the story of five doctors who have been friends since they entered medical s...'),
    (4, 'Its Okay to Not be Okay', 16, 'Netflix-TVN', 9, 71704, 129299, 'An extraordinary road to emotional healing opens up for an selfish antisocial children s book writer...'),
    (5, 'Guardian: The Lonely and Great God - Goblin', 16, 'TVN', 8.8, 91993, 173027, 'In his quest for a bride to break his immortal curse, Dokkaebi, a 939-year-old guardian of souls, me...'),
    (6, 'Mouse', 20, 'TVN', 8.8, 13640, 37206, 'A suspenseful story that will center around the key question, What if we could sort out psychopaths...'),
    (7, 'Start Up', 16, 'Netflix-TVN', 8.1, 36309, 70484, 'Young entrepreneurs aspiring to launch virtual dreams into reality compete for success and love in t...'),
    (8, 'Descendants of the Sun', 16, 'KBS2', 8.7, 77045, 146812, 'This drama tells of the love story that develops between a surgeon and a special forces officer...'),
    (9, 'Dr Romantic', 20, 'SBS', 8.7, 22827, 48508, 'Romantic Doctor Kim is a real doctor story set in a small, humble hospital called Dol Dam Hospit...'),
    (10, 'Vincenzo', 20, 'Netflix-TVN', 9, 51495, 92974, 'During a visit to his motherland, a Korean-Italian mafia lawyer gives an unrivaled conglomerate a ta...');

-- 6. Streaming Insertion
insert into kdrama_list values (11, 'Hospital Playlist', 12, '...', 8.5, 3, 7, '...');
insert into kdrama_list values (12, 'Hospital Playlist', 12, '...', 9.5, 1, 3, '...');
insert into kdrama_list values (13, 'Descendants of the Sun', 16, '...', 8.8, 6, 10, '...');
insert into kdrama_list values (14, 'Mouse', 20, '...', 9, 10, 10, '...');
insert into kdrama_list values (15, 'Vincenzo', 12, '...', 9.3, 13, 25, '...');
insert into kdrama_list values (16, 'Extraordinary Attorney Woo', 16, '...', 9.6, 4, 7, '...');
insert into kdrama_list values (17, 'Extraordinary Attorney Woo', 16, '...', 9.0, 8, 8, '...');