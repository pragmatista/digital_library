from library import util


def main():
    print("#############################################")
    print("            Digital Library Utility          ")
    print("#############################################")
    print("\n")
    print("Specify the source path:")
    src_path = input("> ")

    print("Specify the destination path")
    dest_path = input("> ")

    # util.backup_files(src_path, dest_path)


if __name__ == '__main__':
    main()
