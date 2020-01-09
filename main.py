import argparse

from devrandomclone import simulate


def main() -> None:
    """
    Main function that will deploy the /dev/random clone with the arguments passed to the script.
    :return: Nothing
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--bytes', help='The number of random bytes to receive at a time.')
    parser.add_argument('--force', help='Force reads of entropy pool, despite bytes available. 0 = False, 1 = True.')
    parser.add_argument('--chunks', help='How many chunks of reddit posts to hash for generating entropy.')
    args = parser.parse_args()
    kwargs = {'bytes_read': None, 'force': None, 'chunks': None}
    if not args.bytes:
        del kwargs['bytes_read']
    else:
        kwargs['bytes_read'] = int(args.bytes)
    if not args.force:
        del kwargs['force']
    else:
        kwargs['force'] = bool(int(args.force))
    if not args.chunks:
        del kwargs['chunks']
    else:
        kwargs['chunks'] = int(args.chunks)
    simulate(**kwargs)


if __name__ == '__main__':
    main()
