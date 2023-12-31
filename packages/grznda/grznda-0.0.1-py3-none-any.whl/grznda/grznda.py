from vt100logging import vt100logging_init, I, E

DEFAULT_BUILD_DIR = 'build'
DEFAULT_CONFIG_FILE = 'config.toml'


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False, help='verbose output')
    subparsers = parser.add_subparsers(
        dest='command', help='sub-command help', required=True)

    create_parser = subparsers.add_parser('create', help='create new project')
    create_parser.add_argument('project', help='project name')

    build_subparser = subparsers.add_parser(
        'build', help='build project at current directory')
    build_subparser.add_argument(
        '-o', '--output', help=f'output directory (default: {DEFAULT_BUILD_DIR})', default=DEFAULT_BUILD_DIR)
    build_subparser.add_argument(
        '-c', '--clean', help='clean output directory', action='store_true', default=False)

    return parser.parse_args()


def main():
    try:
        args = parse_args()
        vt100logging_init('grznda', args.verbose)
        I('Done')
    except Exception as e:
        E(e)
        exit(1)


if __name__ == '__main__':
    main()
