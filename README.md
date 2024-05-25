# Twitter Product Tracker

This repository contains a Python script designed to track product availability on a specific online store and post updates on Twitter. It uses several libraries and APIs to fetch product data, check their stock status, and tweet updates.

## Features

- Scrapes product data from an online store.
- Tracks product availability and price changes.
- Tweets updates for new products, price changes, and stock status changes.
- Stores the product catalog locally in a JSON file.

## Setup

### Prerequisites

- Python 3.x
- Dependencies listed in `requirements.txt`

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/twitter-product-tracker.git
   cd twitter-product-tracker

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt

4. Set up environment variables for Twitter API credentials:

   ```bash
   export API_KEY='your_api_key'
   export API_SECRET_KEY='your_api_secret_key'
   export ACCESS_TOKEN='your_access_token'
   export ACCESS_TOKEN_SECRET='your_access_token_secret'
   export BEARER_TOKEN='your_bearer_token'

On Windows, use set instead of export.

### Configuration

The URL of the online store to be tracked is hardcoded in the script. Modify the `url` variable as needed:

   ```python
   url = 'https://www.dragonsteelbooks.com/collections/all'

### Usage

### Running the Script

You can run the script manually or set it up as an Azure Function for scheduled execution.

#### Manually

1. Run the script:

   ```bash
   python script.py



As an Azure Function
Deploy the script as an Azure Function. The main function is designed to be triggered by a timer.
Script Overview
obtener_numero_de_paginas(url): Determines the number of pages to scrape.
obtener_productos_de_pagina(url): Scrapes product details from a single page.
buscar_sold_out_label(item): Checks if a product is sold out.
obtener_todos_los_productos(base_url): Scrapes all product pages.
cargar_catalogo(): Loads the local product catalog from catalog.json.
guardar_catalogo(catalogo): Saves the product catalog to catalog.json.
publicar_en_twitter(tweet, imagen_url): Publishes a tweet with an image.
verificar_status(productos): Verifies the status of products and tweets updates accordingly.
main(mytimer: func.TimerRequest): Azure Function entry point for scheduled execution.
License
This project is licensed under the MIT License.

Contributing
Fork the repository.
Create your feature branch (git checkout -b feature/your-feature).
Commit your changes (git commit -am 'Add some feature').
Push to the branch (git push origin feature/your-feature).
Create a new Pull Request.
Acknowledgements
Beautiful Soup
Tweepy
Azure Functions
Feel free to contribute and open issues if you find any bugs or have feature requests. Happy coding!
