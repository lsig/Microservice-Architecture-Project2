CREATE TABLE IF NOT EXISTS orders(
    id serial PRIMARY KEY,
    productId int not null,
    merchantId int not null,
    buyerId int not null,
    cardNumber VARCHAR(19) not null,
    totalPrice float not null
);


