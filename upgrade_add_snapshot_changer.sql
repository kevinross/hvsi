alter table snapshot add column (changer_id int);
alter table snapshot add foreign key(changer_id) references player(id);