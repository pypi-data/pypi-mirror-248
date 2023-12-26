import click
from jinja2 import Environment
import os
import re


def enviro_value(value, key):
    return os.getenv(key, value)


def find_upper_case_envs(line):
    pattern = r"\{\{ ([A-Z0-9]+) \}\}"
    matches = re.findall(pattern, line)
    return [f"{{{{ {x} }}}}" for x in matches]


def process_file(filename, strict):
    unset_vars = []
    with open(filename, 'r') as f:
        template_lines = f.readlines()
    for i in range(0, len(template_lines)):
        env_vars = find_upper_case_envs(template_lines[i])
        for e_var in env_vars:
            clean_evar = re.sub(r"[{}\s]", "", e_var)
            if not os.getenv(clean_evar):
                unset_vars.append(clean_evar)
            template_lines[i] = template_lines[i].replace(
                e_var, f"{{{{ \"\" | enviro_value('{clean_evar}') }}}}")
    if len(unset_vars) == 0 or not strict:
        return template_lines
    else:
        print("Error: Variables referenced in template are not set:")
        for u_var in unset_vars:
            print("- {}".format(u_var))
        exit(1)


@click.command()
@click.option('-f', '--filename', help='J2 Template to process')
@click.option('--trim-blocks/--no-trim-blocks', show_default=True,
              default=False,
              help="Set renderer to trim_blocks")
@click.option('--lstrip-blocks/--no-lstrip-blocks', show_default=True,
              default=True,
              help="Set renderer to lstrip_blocks")
@click.option('--strict/--no-strict', show_default=True,
              default=False,
              help="Fail if environment variable in template is not set.")
def main(filename, lstrip_blocks, trim_blocks, strict):
    env = Environment(lstrip_blocks=lstrip_blocks, trim_blocks=trim_blocks)
    env.filters['enviro_value'] = enviro_value
    if filename:
        template_lines = process_file(filename, strict)
        template = env.from_string("".join(template_lines))
        click.echo(template.render())
    else:
        click.echo("Filename to render required. See j2x --help for details.")
        exit(1)


if __name__ == '__main__':
    main()
