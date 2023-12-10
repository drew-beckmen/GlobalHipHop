from sys import argv, exit, stderr
from hhapp import app
from utils import initialize_argparse


def main():
    parser = initialize_argparse(
        "Hip Hop Artist Discovery Game",
        positionals=[("port", "the port at which the server should listen.")],
    )
    args = parser.parse_args()
    port = args.port

    try:
        port = int(argv[1])
    except Exception:
        print("Port must be an integer.", file=stderr)
        exit(1)

    try:
        app.run(host="0.0.0.0", port=port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)


if __name__ == "__main__":
    main()
