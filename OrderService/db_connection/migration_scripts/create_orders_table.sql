CREATE TABLE IF NOT EXISTS orders(
    id int PRIMARY KEY,
    productId int not null,
    buyerId int not null,
    cardNumber VARCHAR not null,
    totalPrice float not null
)