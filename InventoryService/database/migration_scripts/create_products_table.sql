CREATE TABLE IF NOT EXISTS products(
    id serial PRIMARY KEY,
    merchantId int not null,
    productName VARCHAR(50) not null,
    price float not null,
    quantity int not null,
    reserved int not null
);
