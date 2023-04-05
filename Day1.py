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
    return 'Noob'


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


@app.route('/create-product', methods=['POST'])
def create_product():
    endpoint = f'{site_domain}/admin/api/2023-01/products.json'
    params = {"product": {"title": "Burton Custom Freestyle 151", "body_html": "<strong>Good snowboard!</strong>",
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


@app.route('/update-product-price',methods = ['GET','PATCH'])
def update_product_price():
    products_list = requests.get(url=f'{site_domain}/admin/api/2023-01/products.json',headers=header).json()['products']
    product_1_id = products_list[-1]['id']
    product_2_id = products_list[-2]['id']

    products_list[-1]['variants'][0]['price'] = '100'
    products_list[-2]['variants'][0]['price'] = '100'
    requests.patch(url=f'{site_domain}/admin/api/2023-01/products/{product_1_id}.json',headers=header,data={'products':products_list})
    requests.patch(url=f'{site_domain}/admin/api/2023-01/products/{product_2_id}.json',headers=header,data={'products':products_list})
    return jsonify({'data':[products_list[-1],products_list[-2]]})


@app.route('/update-product-image',methods = ['GET','PATCH'])
def update_product_image():
    products_list = requests.get(url=f'{site_domain}/admin/api/2023-01/products.json',headers=header).json()['products']
    product_1_id = products_list[-1]['id']
    product_2_id = products_list[-2]['id']
    products_list[-1]['image'] = 'https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg'
    products_list[-2]['image'] = 'https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg'

    requests.patch(url=f'{site_domain}/admin/api/2023-01/products/{product_1_id}.json',headers=header,data={'products':products_list})
    requests.patch(url=f'{site_domain}/admin/api/2023-01/products/{product_2_id}.json',headers=header,data={'products':products_list})
    print(products_list[-1])
    return jsonify({'data':[products_list[-1],products_list[-2]]})


@app.route('/update-product-quantity',methods = ['GET','PATCH'])
def update_product_quantity():
    products_list = requests.get(url=f'{site_domain}/admin/api/2023-01/products.json',headers=header).json()['products']
    product_1_id = products_list[-1]['id']
    product_2_id = products_list[-2]['id']

    products_list[-1]['variants'][0]['inventory_quantity'] = 50
    products_list[-2]['variants'][0]['inventory_quantity'] = 50
    requests.patch(url=f'{site_domain}/admin/api/2023-01/products/{product_1_id}.json',headers=header,data={'products':products_list})
    requests.patch(url=f'{site_domain}/admin/api/2023-01/products/{product_2_id}.json',headers=header,data={'products':products_list})

    return jsonify({'data':[products_list[-1],products_list[-2]]})


@app.route('/delete-product',methods = ['DELETE'])
def delete_product():
    products_list = requests.get(url=f'{site_domain}/admin/api/2023-01/products.json',headers=header).json()['products']
    product_id = products_list[0]['id']
    response = requests.delete(url=f'{site_domain}/admin/api/2023-01/products/{product_id}.json',headers=header)
    return response.json()
    
    


if __name__ == '__main__':
    app.run(debug=True)
