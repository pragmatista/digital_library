import os
import data.db_session as db_session
import workflow


def main():
    setup_db()
    workflow.main_menu()


def setup_db():
    db_file = os.path.join(os.path.dirname(__file__), 'data/db', 'digital_library.db')
    db_session.global_init(db_file)


if __name__ == '__main__':
    main()



