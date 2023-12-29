import argparse
from workflows.services.file_service import download_file_from_s3


def main():
    parser = argparse.ArgumentParser(description="Process args.")

    parser.add_argument('--bucket', type=str, help='S3 bucket name', required=True)
    parser.add_argument('--file-key', type=str, help='S3 file key', required=True)
    parser.add_argument('--path-to-save', type=str, help='S3 file content type', required=True)

    args = parser.parse_args()

    try:
        download_file_from_s3(bucket=args.bucket, file_key=args.file_key, path_to_save=args.path_to_save)
    except Exception as e:
        print(f'Error downloading file: {e}')

    print('File downloaded successfully')


if __name__ == "__main__":
    main()
