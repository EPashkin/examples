#!/bin/python3

import sys

def write_msg(msg):
    sys.stdout.write('{}\n'.format(msg))

def get_file_content(file_path):
    try:
        with open(file_path, 'r') as fd:
            return fd.read()
    except Exception as e:
        write_error('get_file_content failed: "{}": {}'.format(file_path, e))
    return None

def write_into_file(file_path, content):
    try:
        with open(file_path, 'w') as fd:
            fd.write(content)
            return True
    except Exception as e:
        write_error('write_into_file failed: "{}": {}'.format(file_path, e))
    return False

def get_replacements(crate):
    temp = ['gtk', 'glib']
    single = ['gtk', 'gdk', 'gdk-pixbuf', 'gio', 'glib', 'pango', 'pangocairo']
    if crate in temp:
        repl_from = '{} = {{ git = "https://github.com/EPashkin/{}" }}'.format(crate, crate)
        repl_to = '{} = {{ path = ".." }}'.format(crate)
        return [[repl_from, repl_to]]
    elif crate in single:
        repl_from = '{} = {{ git = "https://github.com/gtk-rs/{}" }}'.format(crate, crate)
        repl_to = '{} = {{ path = ".." }}'.format(crate)
        return [[repl_from, repl_to]]
    elif crate == 'sys':
        list = []
        for name in ['glib-sys', 'gobject-sys', 'gio-sys', 'atk-sys', 'gdk-pixbuf-sys',
                     'pango-sys', 'pangocairo-sys', 'gdk-sys', 'gtk-sys']:
            repl_from = '{} = {{ git = "https://github.com/EPashkin/rust-gnome-sys" }}'.format(name)
            repl_to = '{} = {{ path = "../{}" }}'.format(name, name)
            list.append([repl_from, repl_to])
        return list
    elif crate == 'cairo':
        list = []
        repl_from = '{}-rs = {{ git = "https://github.com/EPashkin/{}" }}'.format(crate, crate)
        repl_to = '{}-rs = {{ path = ".." }}'.format(crate)
        list.append([repl_from, repl_to])
        repl_from = '{}-sys-rs = {{ git = "https://github.com/EPashkin/{}" }}'.format(crate, crate)
        repl_to = '{}-sys-rs = {{ path = "../{}-sys-rs" }}'.format(crate,crate)
        list.append([repl_from, repl_to])
        return list
    else:
        return None

def fix_line(line, repl_from, repl_to):
    try:
        index = repl_from.index(line)
        write_msg(line)
        return repl_to[index]
    except ValueError:
        return line

def fix_patchs(content, repl_from, repl_to):
    new_content = [];
    skipping = True
    for line in content.split('\n'):
        if line.startswith('[patch.'):
            write_msg(line)
            skipping = False
        elif line.startswith('['):
            skipping = True
        elif not skipping:
            line = fix_line(line, repl_from, repl_to)
        new_content.append(line)

    return '\n'.join(new_content)

def main(argv):
    if len(argv) < 1:
        write_msg('usage: replace_patchs.py crate_name')
        sys.exit(2)
    crate = argv[0]
    replacements = get_replacements(crate)
    repl_from = [r[0] for r in replacements]
    repl_to = [r[1] for r in replacements]
    #write_msg(repl_from)
    #write_msg(repl_to)

    if replacements is None:
        write_msg('unsupported crate {}'.format(crate))
        sys.exit(4)
    write_msg('starting for crate {}'.format(crate))
    file_path = 'Cargo.toml'
    content = get_file_content(file_path)
    if content is None:
        sys.exit(4)
    new_content = fix_patchs(content, repl_from, repl_to)
    write_into_file(file_path, new_content)
    #write_msg(new_content)

# Beginning of the script
if __name__ == "__main__":
    main(sys.argv[1:])
