import requests
# import shopify
from flask import Flask, jsonify
# import json

app = Flask(__name__)
header = {"X-Shopify-Access-Token": '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'}


site_domain = 'https://testerguinea.myshopify.com'
# API_KEY e925af3243b2e9cb035d5ceb390755f2
# API_SECRET ccc79ec781c709ee62b41aef40568604


@app.route('/')
def index():
    return 'Hello'


@app.route('/create-smart-collection', methods=['POST'])
def create_smart_product():
    endpoint = f'{site_domain}/admin/api/2023-04/smart_collections.json'
    params = {
        "smart_collection": {
            "title": "Macbooks",
            "rules": [
                {
                    "column": "vendor",
                    "relation": "equals",
                    "condition": "Apple"
                }
            ],
            "image": {
                "attachment": "R0lGODlhAQABAIAAAAAAAAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==\n",
                "alt": "iPod"
            }
        }
    }
    response = requests.post(url=endpoint, json=params, headers=header)
    return response.json()


@app.route('/create-custom-collection', methods=['POST'])
def create_custom_collection():
    endpoint = f'{site_domain}/admin/api/2023-01/custom_collections.json'
    params = {"custom_collection": {"title": "Macbooks"}}
    response = requests.post(url=endpoint, headers=header, json=params)
    return response.json()


@app.route('/create-product', methods=['GET', 'POST'])
def create_product():
    endpoint = f'{site_domain}/admin/api/2023-01/products.json'
    params = {"product": {"title": "Goods", "body_html": "<strong>Good snowboard!</strong>",
                          "vendor": "Burton", "product_type": "Snowboard"}}
    response = requests.post(url=endpoint, headers=header, json=params)
    return response.json()


@app.route('/create-custom-product', methods=['POST'])
def create_custom_product():
    endpoint = f'{site_domain}/admin/api/2023-01/products.json'
    params = {"product": {"title": "Burton Custom Freestyle 152", "body_html": "<strong>Good snowboard!</strong>", "vendor": "Burton", "product_type": "Snowboard", "variants": [
        {"option1": "Blue", "option2": "155"}, {"option1": "Black", "option2": "159"}], "options": [{"name": "Color", "values": ["Blue", "Black"]}, {"name": "Size", "values": ["155", "159"]}]}}
    response = requests.post(url=endpoint, headers=header, json=params)
    return response.json()


@app.route('/create-customer', methods=['POST'])
def create_customer():
    endpoint = f'{site_domain}/admin/api/2023-01/customers.json'
    params = {"customer": {"first_name": "Steve", "last_name": "Lastnameson", "email": "steve.lastnameson@example.com", "phone": "+15142546011", "verified_email": true, "addresses": [
        {"address1": "123 Oak St", "city": "Ottawa", "province": "ON", "phone": "555-1212", "zip": "123 ABC", "last_name": "Lastnameson", "first_name": "Mother", "country": "CA"}], "password": "newpass", "password_confirmation": "newpass", "send_email_welcome": false}}
    response = requests.post(url=endpoint, headers=header, json=params)
    return response.json()


@app.route('/create-order', methods=['POST'])
def create_order():
    endpoint = f'{site_domain}/admin/api/2023-01/orders.json'
    params = {"order": {"line_items": [{"title": "Big Brown Bear Boots", "price": 74.99, "grams": "1300", "quantity": 3, "tax_lines": [
        {"price": 13.5, "rate": 0.06, "title": "State tax"}]}], "transactions": [{"kind": "sale", "status": "success", "amount": 238.47}], "total_tax": 13.5, "currency": "EUR"}}
    response = requests.post(url=endpoint, headers=header, json=params)
    return response.json()


@app.route('/update-product-price', methods=['GET', 'PATCH'])
def update_product_price():
    products_list = requests.get(
        url=f'{site_domain}/admin/api/2023-01/products.json', headers=header).json()['products']
    
    product_id = products_list[0]['id']

    products_list[0]['variants'][0]['price'] = '200'
    
    requests.patch(
        url=f'{site_domain}/admin/api/2023-01/products/{productid}.json', headers=header)
    
    return jsonify({'data':products_list[0]})


@app.route('/update-product-image', methods=['GET', 'PUT', 'POST'])
def update_product_image():
    products_list = requests.get(
        url=f'{site_domain}/admin/api/2023-01/products.json', headers=header).json()['products']
    product_id = products_list[0]['id']
    
    
    images_list = requests.get(
        f'{site_domain}/admin/api/2023-04/products/{product_id}/images.json', headers=header).json()
    image_id = images_list['images'][0]['id']
    
    payload = {
    "product": {
        "id": product_id,
        "images": [
            {
                "src": "https://i.gifer.com/origin/c3/c320e774393ce5869b6b348b546c23d0_w200.gif"
            }
        ]
    }
}

    response = requests.put(f"{site_domain}/admin/api/2023-04/products/{product_id}.json", headers=header, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return jsonify({'error': 'Noob'})

    

    
    


    


@app.route('/update-product-quantity', methods=['GET', 'POST'])
def update_product_quantity():
    products_list = requests.get(
        url=f'{site_domain}/admin/api/2023-04/products.json', headers=header).json()['products']
    product_id = products_list[0]['id']
    inventory_item_id = requests.get(f'{site_domain}/admin/api/2023-04/products/{product_id}/variants.json',
                                     headers=header).json()['variants'][0]['inventory_item_id']
    inventory_level = requests.get(f'{site_domain}/admin/api/2023-04/inventory_levels.json',
                                   headers=header, params={'inventory_item_ids': inventory_item_id}).json()
    location_id = inventory_level['inventory_levels'][0]['location_id']
    params = {"location_id": f"{location_id}",
              "inventory_item_id": f"{inventory_item_id}",
              "available_adjustment": 10}
    return requests.post(f'{site_domain}/admin/api/2023-04/inventory_levels/adjust.json', headers=header, json=params).json()


@app.route('/delete-product', methods=['DELETE'])
def delete_product():
    products_list = requests.get(
        url=f'{site_domain}/admin/api/2023-01/products.json', headers=header).json()['products']
    product_id = products_list[0]['id']
    requests.delete(
        url=f'{site_domain}/admin/api/2023-01/products/{product_id}.json', headers=header)
    return jsonify({'success': 'Delete successfully'})


if __name__ == '__main__':
    app.run(debug=True)
