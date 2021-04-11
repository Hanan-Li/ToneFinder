CREATE TABLE users(
	username VARCHAR(20),
	password VARCHAR(256) NOT NULL,
	created DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (username)
);

CREATE TABLE ir(
	irid INTEGER AUTO_INCREMENT,
	name VARCHAR(20) NOT NULL,
	irfile VARCHAR(64) NOT NULL,
	owner VARCHAR(20) NOT NULL,
	created DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY(owner) REFERENCES users(username) ON DELETE CASCADE,
	PRIMARY KEY (irid)
);

CREATE TABLE guitar(
	gid INTEGER AUTO_INCREMENT,
	name VARCHAR(20) NOT NULL,
	guitarfile VARCHAR(64) NOT NULL,
	owner VARCHAR(20) NOT NULL,
	created DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY(owner) REFERENCES users(username) ON DELETE CASCADE,
	PRIMARY KEY (gid)
);
