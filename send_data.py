import os
import requests
import argparse


def upload_to_bhtom(file_path, token, target_name, filter_name, observatory_name):
    
    url = 'https://uploadsvc2.astrolabs.pl/upload/'

    with open(file_path, 'rb') as f:
        data = {
            'target': target_name,
            'filter': filter_name,
            'data_product_type': 'fits_file',
            'dry_run': 'False',
            'observatory': observatory_name
        }

        headers = {
            'Authorization': f'Token {token}'
        }

        response = requests.post(
            url=url,
            headers=headers,
            data=data,
            files={'files': f}
        )

    return response.json()
