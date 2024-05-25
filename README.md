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

On Windows, use `set` instead of `export`.

### Configuration

The URL of the online store to be tracked is hardcoded in the script. Modify the `url` variable as needed:

   ```python
   url = 'https://www.dragonsteelbooks.com/collections/all'
