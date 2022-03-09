from library import util
import os
import data.db_session as db_session

# path = "/Users/kyleking/Documents/King Family/Media Files/Original Library/2012/IMG_0808.JPG"
#
# file = os.path.dirname(os.path.splitext(path)[0])
# ext = pathlib.Path(path).suffix
# print(ext)


def main():
    setup_db()


def setup_db():
    db_file = os.path.join(os.path.dirname(__file__), 'data/db', 'digital_library.db')
    db_session.global_init(db_file)


def workflow():
    print("#############################################")
    print("            Digital Library Utility          ")
    print("#############################################")
    print("\n")
    print("Specify the source path:")
    # src_path = "/Users/kyleking/Documents/King Family/Media Files/Original Library"  # input("> ")
    src_path = "/Volumes/Data/Compressed/2006"

    print("Specify the destination path:")
    dest_path = "/Users/kyleking/Documents/King Family/Media Files/Archives/Collection"  # input("> ")

    # util.backup_files(src_path, dest_path)


if __name__ == '__main__':
    main()
