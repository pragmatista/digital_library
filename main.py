import os
import data.db_session as db_session
import services.inventory
import workflow
from services import library

import json

def main():
    setup_db()

    results = services.inventory.get_inventory_by_classification()
    if results:
        for result in results:
            print(result)
            print(type(result['classification_json']), result['classification_json'])
            print(result['classification']['tags'])
            print(result['classification']['tags'][0])
            # result['classification'] = json.loads(result['classification'])
            # print(result['classification']['tags'])

    pre_populate_db()
    workflow.main_menu()


def setup_db():
    db_file = os.path.join(os.path.dirname(__file__), 'data/db', 'digital_library.db')
    db_session.global_init(db_file)


def pre_populate_db():
    add_model_library()


def add_model_library():
    lib = library.get_model_library()
    if not lib:
        data = {
            'library_name': 'Object Recognition Training Model',
            'description': 'Created by the program to store images used to train an ML object recognition model',
            'base_path': 'tests/samples/ml/train/',
            'user_defined': False
        }

        library.add_library(**data)


if __name__ == '__main__':
    main()



