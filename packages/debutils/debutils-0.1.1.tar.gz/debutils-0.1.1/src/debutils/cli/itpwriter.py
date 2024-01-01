# debutils -- Utilities to help Debian package maintainers.
# Copyright (C) 2023 Maytham Alsudany <maytha8thedev@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
from os.path import exists

import click
from debian.changelog import Changelog
from debian.copyright import Copyright
from debian.deb822 import Deb822
from jinja2 import Environment, PackageLoader, select_autoescape


@click.command()
@click.argument("output", type=click.File("wb"))
@click.option(
    "--name",
    envvar="DEBFULLNAME",
    help="Name of package maintainer. Uses DEBFULLNAME environment variable by default.",
)
@click.option(
    "--email",
    envvar="DEBEMAIL",
    help="Email of package maintainer. Uses DEBEMAIL environment variable by default.",
)
def itpwriter(output, name, email):
    """
    Write an ITP email based on the source tree of a Debian package.
    """
    env = Environment(
        loader=PackageLoader("debutils"),
        autoescape=select_autoescape(),
    )
    template = env.get_template("itp.jinja")

    with click.open_file("debian/control", "r") as f:
        control = Deb822(f)
        package = control["Source"]
        section = control["Section"]
        url = control["Homepage"]
        short_desc, long_desc = next(Deb822.iter_paragraphs(f))["Description"].split(
            "\n", 1
        )

    with click.open_file("debian/copyright", "r") as f:
        copyr = Copyright(f)
        upstream = copyr.header.upstream_contact
        paragraph = copyr.find_files_paragraph(".")
        if paragraph is None:
            click.secho(
                "Could not find license. Please manually input a license below.",
                fg="yellow",
                err=True,
            )
            lic = input("License:")
        else:
            lic = paragraph.license._asdict()["synopsis"]
            if lic is None or lic == "":
                click.secho(
                    "Could not find license. Please manually input a license below.",
                    fg="yellow",
                    err=True,
                )
                lic = input("License:")

    with click.open_file("debian/changelog", "r") as f:
        changelog = Changelog(f)
        deb_rev = r"\-.*$"
        deb_ext = r"[\+~](debian|dfsg|ds|deb)(\.)?(\d+)?$"
        dversion = str(changelog.version)
        version = re.sub(deb_ext, "", re.sub(deb_rev, "", dversion))

    lang = fetch_lang(section)

    cc = fetch_cc(lang)

    message = click.edit(
        template.render(
            name=name,
            email=email,
            cc=cc,
            package=package,
            license=lic,
            upstream=upstream,
            version=version,
            url=url,
            lang=lang,
            short_desc=short_desc,
            long_desc=long_desc,
        )
    )

    # action_prompt(message)
    output.write(message.encode())


# def action_prompt(message):
#     click.echo("Continue? [Nype?] ", nl=False)
#     action = click.getchar().lower()
#     click.echo("")
#     match action:
#         case "":
#             raise click.Abort
#         case "n":
#             raise click.Abort
#         case "y":
#             pass
#         case "p":
#             click.echo(message)
#             action_prompt(message)
#         case "e":
#             message = click.edit(message)
#             action_prompt(message)
#         case "?":
#             click.echo(
#                 """
# n - Quit program
# y - Send email
# p - Print email in full
# e - Edit email
# ? - Print this help message
#             """
#             )
#         case _:
#             click.echo("Invalid input")
#             action_prompt(message)


def fetch_lang(section):
    if section == "golang" or exists("go.mod"):
        return "Go"
    if section == "python" or exists("pyproject.toml") or exists("requirements.txt"):
        return "Python"
    if section == "javascript" or exists("package.json"):
        return "JavaScript"
    return input("Programming language:")


def fetch_cc(lang):
    cc = ["debian-devel@lists.debian.org"]
    if lang == "Go":
        cc.append("debian-go@lists.debian.org")
    return cc
