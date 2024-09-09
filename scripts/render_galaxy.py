import sys

import jinja2


def main() -> None:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))
    tpl = env.get_template('galaxy.yml.j2')
    version = "0.0.0"
    if len(sys.argv) > 1:
        version = sys.argv[1]
        if version.startswith('v'):
            version = version[1:]
    output = tpl.render({'collection_version': version})

    with open('galaxy.yml', 'w') as f:
        f.write(output)


if __name__ == '__main__':
    main()
