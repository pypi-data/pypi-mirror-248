import argparse

from workflows.services.processor_service import process_file


def main():
    parser = argparse.ArgumentParser(description="Process args.")

    parser.add_argument('--path-file', type=str, help='file path', required=True)
    parser.add_argument('--content-type', type=str, help='file content type', required=True)
    parser.add_argument('--path-save-parquet', type=str, help='path to save parquet', required=True)

    args = parser.parse_args()

    try:
        process_file(path_file=args.path_file, content_type=args.content_type, path_save_parquet=args.path_save_parquet)
    except Exception as e:
        print(f'Error downloading file: {e}')

    print('File downloaded successfully')


if __name__ == "__main__":
    main()
