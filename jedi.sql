USE testdb;

CREATE TABLE jedi (
    id_jedi INT AUTO_INCREMENT PRIMARY KEY,
    nombre_jedi VARCHAR(100) NOT NULL,
    email_jedi VARCHAR(100) UNIQUE NOT NULL
);
