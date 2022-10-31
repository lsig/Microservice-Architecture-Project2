CREATE TABLE IF NOT EXISTS orders(
    id serial PRIMARY KEY,
    productId int not null,
    buyerId int not null,
    cardNumber CHAR(16) not null,
    totalPrice float not null
);


