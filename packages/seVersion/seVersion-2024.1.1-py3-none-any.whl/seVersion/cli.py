from __future__ import absolute_import, division
from ._version import __version__

import click
import datetime
import os

from typing import Dict, Optional, Callable
from seCore.filepath import FilePath
from seVersion import Version

_VERSIONPY_TEMPLATE = '''"""
Provides `{package}` version information.
"""
# This file is auto-generated! Do not edit!
# Use `seVersion {package}` to change this file.

from seVersion import Version
__version__ = {version_repr}
__setuptools__ = __version__.public()
__all__ = ["__version__"]
'''

_YEAR_START = 0


def currentVersion(ctx, param, value):
    """Output current version"""
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'{__version__}')
    ctx.exit()


class ClickColorLogger:

    def __init__(self):
        self.pre = "seVersion"

    @staticmethod
    def echo(msg):
        click.echo(f'{msg}')

    def info(self, msg):
        click.secho(self.pre, fg='blue', nl=False)
        click.secho(" | ", fg='white', nl=False)
        click.secho(f'{"INFO": <8}', nl=False)
        click.secho(" | ", fg='white', nl=False)
        click.secho(f'{msg}', fg='cyan')

    def error(self, msg):
        click.secho(self.pre, fg='blue', nl=False)
        click.secho(" | ", fg='white', nl=False)
        click.secho(f'{"ERROR": <8}', fg='red', nl=False)
        click.secho(" | ", fg='white', nl=False)
        click.secho(f'{msg}', fg='red')

    def warning(self, msg):
        click.secho(self.pre, fg='blue', nl=False)
        click.secho(" | ", fg='white', nl=False)
        click.secho(f'{"WARNING": <8}', fg='yellow', nl=False)
        click.secho(" | ", fg='white', nl=False)
        click.secho(f'{msg}', fg='yellow')


loggerColor = ClickColorLogger()
loggerColor.echo(f'{"":-<100}')


def _findPath(path, package, create):  # type: (str, str, bool) -> FilePath
    cwd = FilePath(path)
    src_dir = cwd.child("src").child(package.lower())
    current_dir = cwd.child(package.lower())

    if src_dir.isdir():
        return src_dir  # pragma: no cover
    elif current_dir.isdir():
        return current_dir
    else:
        if create:
            loggerColor.info(f'{"Creating": >17}: {cwd.child(package.lower())}')
            FilePath.makedirs(cwd.child(package.lower()))
            return current_dir
        else:
            _SE_01100_1 = f'''Can't find `{package}` under `./src` or `./`'''
            _SE_01100_2 = f'''Check the package name is right (note that we expect your package name to be lower cased), or pass it using '--path' '''
            _SE_01100_3 = f'''or add `--cdne` to automatically initialize the project to create folder and files'''
            loggerColor.warning(f'{"SE-01100": >17}: {_SE_01100_1}')
            loggerColor.warning(f'{"": >18} {_SE_01100_2}')
            loggerColor.warning(f'{"": >18} {_SE_01100_3}')
            exit(1100)


def _existing_version(path):  # type: (FilePath) -> Version
    version_info = {}  # type: Dict[str, Version]
    try:
        with path.child("_version.py").open("r") as f:
            exec(f.read(), version_info)
        return version_info["__version__"]
    except FileNotFoundError:
        loggerColor.error(f'{"SE-01311": >17}: Could not find {path.child("_version.py")}')
        exit(1311)


def _run(
        package,  # type: str
        firstparam,  # type: str
        path,  # type: Optional[str]
        newversion,  # type: Optional[str]
        patch,  # type: bool
        rc,  # type: bool
        post,  # type: bool
        dev,  # type: bool
        create,  # type: bool
        release,  # type: bool
        minor,  # type: bool
        major,  # type: bool
        build,  # type: bool
        clean,  # type: bool
        cdne,  # type: bool
        _date=None,  # type: Optional[datetime.date]
        _getcwd=None,  # type: Optional[Callable[[], str]]
):  # type: (...) -> list[str]

    if not _getcwd:
        _getcwd = os.getcwd

    if not _date:
        _date = datetime.date.today()

    if str != type(package):
        package = package.encode("utf8")  # pragma: no cover

    _path = FilePath(path) if path else _findPath(_getcwd(), package, cdne)

    # cmdExcludeList = [create, newversion, dev, post, rc, patch, release, major, minor, clean, cdne, build]

    # -- create
    if create:
        cmdExcludeList = [newversion, dev, post, rc, patch, release, major, minor, clean, build]
        if any(cmdExcludeList):
            loggerColor.error(f'{"SE-01300": >17}: --create error, only --cdne is allowed to be used with this command to create ''package\\project'' folder if does not exist')
            exit(1300)
        else:
            v = Version(package,
                        _date.year - _YEAR_START,  # major
                        _date.month,  # minor
                        0,  # micro
                        0  # build
                        )

            loggerColor.info(f'{"Creating codebase": >17}: {v.public()}')
            # existing = v

    # --newversion
    elif newversion:
        cmdExcludeList = [create, dev, post, rc, patch, release, major, minor, clean, cdne, build]
        if any(cmdExcludeList) or "--" in newversion:
            loggerColor.error(f'{"SE-01301": >17}: --newversion=?.?.? error, no other commands need to be used')
            exit(1301)
        else:
            from pkg_resources import parse_version
            existing = _existing_version(_path)
            st_version = parse_version(newversion)  # type: ignore[attr-defined]
            release = list(st_version.release)
            minor = _date.month
            micro = 0
            if len(release) == 1:
                (major,) = release
            elif len(release) == 2:
                major, minor = release
            else:
                major, minor, micro = release

            v = Version(
                package,
                major,
                minor,
                micro,
                existing.build,
                release_candidate=st_version.pre[1] if st_version.pre else None,
                post=None if st_version.post is None else st_version.post,
                dev=None if st_version.dev is None else st_version.dev,
            )
            loggerColor.info(f'{"Updating codebase": >17}: {v.public()}')

    # --dev
    elif dev:
        cmdExcludeList = [create, newversion, post, rc, patch, release, major, minor, clean, cdne, build]
        if any(cmdExcludeList):
            loggerColor.error(f'{"SE-01302": >17}: --dev error, no other commands need to be used')
            exit(1302)
        else:
            existing = _existing_version(_path)
            loggerColor.info(f'{"Current codebase": >17}: {existing.public()}')

            if existing.dev is None:
                _dev = 0
            else:
                _dev = existing.dev + 1

            v = Version(
                package,
                existing.major,
                existing.minor,
                existing.micro,
                existing.build,
                # existing.release_candidate,
                dev=_dev,
            )
            loggerColor.info(f'{"Updating codebase": >17}: {v.public()}')

    # --rc
    elif rc:
        cmdExcludeList = [create, newversion, dev, post, patch, release, major, minor, clean, cdne, build]
        if any(cmdExcludeList):
            loggerColor.error(f'{"SE-01303": >17}: --rc error, no other commands need to be used')
            exit(1303)
        else:
            existing = _existing_version(_path)
            loggerColor.info(f'{"Current codebase": >17}: {existing.public()}')
            if existing.release_candidate:
                v = Version(
                    package,
                    existing.major,
                    existing.minor,
                    existing.micro,
                    existing.build,
                    existing.release_candidate + 1,
                )
            else:
                # v = Version(package, _date.year - _YEAR_START, _date.month, 0, 1)
                v = Version(
                    package,
                    existing.major,
                    existing.minor,
                    existing.micro,
                    existing.build,
                    1,
                )
            loggerColor.info(f'{"Updating codebase": >17}: {v.public()}')

    # --patch
    elif patch:
        cmdExcludeList = [create, newversion, dev, post, rc, release, major, minor, clean, cdne, build]
        if any(cmdExcludeList):
            loggerColor.error(f'{"SE-01304": >17}: --patch error, no other commands need to be used')
            exit(1304)
        else:
            existing = _existing_version(_path)
            loggerColor.info(f'{"Current codebase": >17}: {existing.public()}')
            v = Version(
                package,
                existing.major,
                existing.minor,
                existing.micro + 1,
                existing.build,
                1 if rc else None,
            )
            loggerColor.info(f'{"Updating codebase": >17}: {v.public()}')

    # -- major
    elif major:
        cmdExcludeList = [create, newversion, dev, post, rc, patch, release, minor, clean, cdne, build]
        if any(cmdExcludeList):
            loggerColor.error(f'{"SE-01305": >17}: --major error, no other commands need to be used')
            exit(1305)
        else:
            existing = _existing_version(_path)
            v = existing
            loggerColor.info(f'{"Current codebase": >17}: {existing.public()}')

            if existing.major:
                _major = existing.major + 1
                v = Version(package, _major, _date.month, 0, existing.build)
            loggerColor.info(f'{"Updating codebase": >17}: {v.public()}')

    # --minor
    elif minor:
        cmdExcludeList = [create, newversion, dev, post, rc, patch, release, major, clean, cdne, build]
        if any(cmdExcludeList):
            loggerColor.error(f'{"SE-01306": >17}: --minor error, no other commands need to be used')
            exit(1306)
        else:
            existing = _existing_version(_path)
            v = existing
            loggerColor.info(f'{"Current codebase": >17}: {existing.public()}')

            if existing.minor:
                _minor = existing.minor + 1
                v = Version(package, existing.major, _minor, 0, existing.build)
            loggerColor.info(f'{"Updating codebase": >17}: {v.public()}')

    # --build
    elif build:
        cmdExcludeList = [create, newversion, dev, post, rc, patch, release, major, minor, clean, cdne]
        if any(cmdExcludeList):
            loggerColor.error(f'{"SE-01307": >17}: --build error, no other commands need to be used')
            exit(1307)
        else:
            existing = _existing_version(_path)
            v = existing
            loggerColor.info(f'{"Current codebase": >17}: {existing.public_build()}')
            if isinstance(existing.build, int):
                _build = existing.build + 1
                v = Version(package,
                            existing.major,
                            existing.minor,
                            existing.micro,
                            _build,
                            release_candidate=existing.release_candidate if existing.release_candidate else None,
                            post=existing.post if existing.post else None,
                            dev=existing.dev if existing.dev else None
                            )
            loggerColor.info(f'{"Updating codebase": >17}: {v.public_build()}')

    # --post
    elif post:
        cmdExcludeList = [create, newversion, dev, rc, patch, release, major, minor, clean, cdne, build]
        if any(cmdExcludeList):
            loggerColor.error(f'{"SE-01308": >17}: --post error, no other commands need to be used')
            exit(1308)
        else:
            existing = _existing_version(_path)
            loggerColor.info(f'{"Current codebase": >17}: {existing.public()}')

            if existing.post is None:
                _post = 0
            else:
                _post = existing.post + 1

            v = Version(
                package,
                existing.major,
                existing.minor,
                existing.micro,
                existing.build,
                post=_post)
            loggerColor.info(f'{"Updating codebase": >17}: {v.public()}')

    elif release:
        cmdExcludeList = [create, newversion, dev, post, rc, patch, major, minor, clean, cdne, build]
        if any(cmdExcludeList):
            loggerColor.error(f'{"SE-01309": >17}: --release error, no other commands need to be used')
            exit(1309)
        else:
            existing = _existing_version(_path)
            v = existing
            if existing.release_candidate or existing.dev or existing.post:
                loggerColor.info(f'{"Current codebase": >17}: {existing.public()}')
                v = Version(package,
                            existing.major,
                            existing.minor,
                            existing.micro,
                            existing.build
                            )
            loggerColor.info(f'{"Current Release": >17}: {v.public()}')

    elif clean:
        loggerColor.info(f'Cleaning codebase: Removing {_path.child("_version.py")}')
        try:
            FilePath.remove(_path.child("_version.py"))
        except FileNotFoundError:
            loggerColor.error(f'{"SE-01310": >17}: {_path.child("_version.py")} not found')
            exit(1310)
        exit()

    else:
        loggerColor.info(f'{"Project Path": >17}: ./{package}/_version.py')
        existing = _existing_version(_path)
        loggerColor.info(f'{"Current Release": >17}: {existing.public()}')
        loggerColor.info(f'{"Build Release": >17}: {existing.public_build()}')

        exit()

    # ---------------------------------------------------------------------------------
    # existing_version_repr = repr(existing).split("#")[0].replace("'", '"')
    version_repr = repr(v).split("#")[0].replace("'", '"')

    loggerColor.info(f'{"Updating": >17}: ./{package}/_version.py')
    # loggerColor.info(f'{existing_version_repr} == {version_repr}: {existing_version_repr == version_repr}')

    with _path.child("_version.py").open("w") as f:
        f.write((_VERSIONPY_TEMPLATE.format(package=package, version_repr=version_repr)).encode("utf8"))
    return [firstparam, v.public(), v.public_build()]


class OrderedParamsCommand(click.Command):
    _options = []

    def parse_args(self, ctx, args):
        # run the parser for ourselves to preserve the passed order
        parser = self.make_parser(ctx)
        opts, _, param_order = parser.parse_args(args=list(args))
        for param in param_order:
            # Type check
            option = opts[param.name]
            if option is not None:
                type(self)._options.append((param, option))
        return super().parse_args(ctx, args)


@click.command(cls=OrderedParamsCommand)
@click.option('-v', '--version', is_flag=True, callback=currentVersion, expose_value=False, is_eager=True)
@click.argument("package")
@click.option("--path", default=None)
@click.option("--newversion", default=None)
@click.option("--patch", is_flag=True)
@click.option("--rc", is_flag=True)
@click.option("--post", is_flag=True)
@click.option("--dev", is_flag=True)
@click.option("--create", is_flag=True)
@click.option("--release", is_flag=True)
@click.option("--major", is_flag=True)
@click.option("--minor", is_flag=True)
@click.option("--clean", is_flag=True)
@click.option("--cdne", is_flag=True)
@click.option("--build", is_flag=True)
def cli(
        package,  # type: str
        path,  # type: Optional[str]
        newversion,  # type: Optional[str]
        patch,  # type: bool
        rc,  # type: bool
        post,  # type: bool
        dev,  # type: bool
        create,  # type: bool
        release,  # type: bool
        minor,  # type: bool
        major,  # type: bool
        clean,  # type: bool
        cdne,  # type: bool
        build,  # type: bool
):
    # noinspection PyProtectedMember
    options = OrderedParamsCommand._options
    option = str(options[0][0].name)
    _run(
        package=package,
        firstparam=option,
        path=path,
        newversion=newversion,
        patch=patch,
        rc=rc,
        post=post,
        dev=dev,
        create=create,
        release=release,
        minor=minor,
        major=major,
        build=build,
        clean=clean,
        cdne=cdne,
    )

# if __name__ == '_main_':
#     cli(["seVersioning", "--path=./"])
