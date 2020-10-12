import click

from .. import fs
from .ctx import Context
from remote_fs.mount.settings import MountSettings


@click.group()
@click.pass_context
@click.option(
    "--smbfs",
    "filesystem",
    flag_value="smbfs",
    default=False,
    help="mounts via mount_smbfs (darwin only)",
)
@click.option(
    "--sshfs", "filesystem", flag_value="sshfs", default=True, help="mounts via sshfs"
)
def cli(click_ctx, filesystem):
    click_ctx.obj = Context("remote-fs", settings={"filesystem": filesystem})


@cli.command()
@click.pass_context
@click.argument("mount_point", required=True)
@click.option("--load", is_flag=True, default=False)
@click.option("--save", required=False)
@click.option(
    "--remote", required=False, help="full hostname string, e.g. user@hostname:dir"
)
@click.option("--hostname", required=False)
@click.option("--user", required=False)
@click.option("--dir", required=False)
@click.option(
    "--option",
    "-o",
    multiple=True,
    default=["reconnect,ServerAliveInterval=15,ServerAliveCountMax=3"],
)
def mount(click_ctx, mount_point, load, save, **kwargs):
    ctx: Context = click_ctx.obj

    mount_settings = MountSettings(
        filesystem=ctx.settings.filesystem, mount_point=mount_point, **kwargs
    )

    if save is not None:
        mount_settings.save(save, ctx.app_dir)
        return
    elif load:
        mount_settings.load(mount_point, ctx.app_dir)

    if mount_settings.filesystem == "sshfs":
        filesystem = fs.SSHFS(mount_settings)

    print(filesystem.format_cmd())
    # filesystem.mount()

    # if cli_options.filesystem == "sshfs":
    #     mount_sshfs(cli_ctx, mount_options)

    # if cli_options.filesystem == "sshfs":
    #     filesystem = fs.SSHFS(hostname, mount_point, user=user, dir=dir, options=option)
    # else:
    #     raise ValueError(f"{cli_options.filesystem} is not supported")

    # if remote is not None:
    #     filesystem.parse_remote(remote)

    # if save is not None:
    #     filesystem.save(save, cli_ctx.app_dir)
    # else:
    #     filesystem.mount()


@cli.command()
@click.argument("mount_point")
def unmount(mount_point):
    click.echo(mount_point)


@cli.command()
@click.pass_context
@click.argument("resource")
def ls(click_ctx, resource):
    ctx: Context = click_ctx.obj
    if resource == "names":
        for name in MountSettings.ls(ctx.app_dir):
            click.echo(name)
    # click.echo(MountSettings.list_saved(ctx.app_dir))