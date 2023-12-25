import sys
import re
from os.path import exists
from typing import get_origin
import click
from debian.copyright import Copyright
from debian.deb822 import Deb822
from debian.changelog import Changelog
from jinja2 import Environment, PackageLoader, select_autoescape


@click.command(help="Write an ITP email based on the source tree of a Debian package.")
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
def cli(name, email):
    env = Environment(
        loader=PackageLoader("itpwriter"),
        autoescape=select_autoescape(),
    )
    template = env.get_template("itp.jinja")

    with open("debian/control") as f:
        control = Deb822(f)
        package = control["Source"]
        section = control["Section"]
        url = control["Homepage"]
        short_desc, long_desc = list(Deb822.iter_paragraphs(f))[0]["Description"].split(
            "\n", 1
        )

    with open("debian/copyright") as f:
        copyright = Copyright(f)
        upstream = copyright.header.upstream_contact
        paragraph = copyright.find_files_paragraph(".")
        if paragraph == None:
            eprint("Could not find license. Please manually input a license below.")
            license = input("License:")
        else:
            license = paragraph.license._asdict()["synopsis"]
            if license == None or len(license) == 0:
                eprint("Could not find license. Please manually input a license below.")
                license = input("License:")

    with open("debian/changelog") as f:
        changelog = Changelog(f)
        deb_rev = r"\-.*$"
        deb_ext = r"[\+~](debian|dfsg|ds|deb)(\.)?(\d+)?$"
        dversion = str(changelog.version)
        version = re.sub(deb_ext, "", re.sub(deb_rev, "", dversion))

    lang = fetch_lang(section)

    cc = fetch_cc(lang)

    eprint(
        """
Enter a comment to be added to the ITP, usually reasoning for the package, as
well as other details such as whether the package will be team maintained and
if you will need a sponsor. End with three newlines in a row, or an EOF
(Ctrl-D).
"""
    )
    comment = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if len(comment) > 1 and comment[-1] == "" and line == "":
            comment.pop()
            break
        comment.append(line)
    comment = "\n".join(comment)

    print(
        template.render(
            name=name,
            email=email,
            cc=cc,
            package=package,
            license=license,
            upstream=upstream,
            version=version,
            url=url,
            lang=lang,
            short_desc=short_desc,
            long_desc=long_desc,
            comment=comment,
        )
    )


def fetch_lang(section):
    if section == "golang" or exists("go.mod"):
        return "Go"
    if section == "python" or exists("pyproject.toml") or exists("requirements.txt"):
        return "Python"
    return input("Programming language:")


def fetch_cc(lang):
    cc = ["debian-devel@lists.debian.org"]
    if lang == "Go":
        cc.append("debian-go@lists.debian.org")
    return cc


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
