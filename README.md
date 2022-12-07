Project 2
lets go


## Notkun

Kerfið er keyrt upp með docker-compose up í root skránni, þaðan er farið inn á *http://localhost:8000/docs* þar sem FastAPI tekur við leiðbeiningum.

Þar er hægt að tala við 

- OrderService (/orders)
Þjónusta ofan á PostgreSQL gagnagrunn

- MerchantService (/merchants)
Þjónusta ofan á MongoDB gagnagrunn

- BuyerService (/buyers)
Þjónusta ofan á MongoDB gagnagrunn

- InventoryService (/products)
Þjónusta ofan á PostgreSQL gagnagrunn


Einnig eru þjónusturnar PaymentService og EmailService, sem átt er samskipti við með **RabbitMQ** events, sem vinna úr greiðslum og tilkynningum.

## Use case (Microservice Architecture)

Start the system up with the docker-compose.yaml file in the root directory, from there got to *http://localhost:8000/docs* to interact with the FastAPI UI.

You can send requests to

- OrderService (/orders)
Microservice with PostgreSQL database

- MerchantService (/merchants)
Microservice with a MongoDB database

- BuyerService (/buyers)
Microservice with a MongoDB database

- InventoryService (/products)
Microservice with PostgreSQL database

Also the system has to additional microservices, which interact with events sent from **RabbitMQ**, which process payments and confirmations.


