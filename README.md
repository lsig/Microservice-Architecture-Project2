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
