import sys
import getpass

from . import helpformatter
from .webpassword import set_password_argon2, set_password_pam, verify_password


def add_parser(subparsers):
    help = "Set the password for the web interface."

    parser = subparsers.add_parser('password',
                                   formatter_class=helpformatter.All,
                                   help=help,
                                   description=help)

    parser.add_argument(
        '--use-pam',
        action='store_const',
        default=False,
        const=True,
        help="Configure to use PAM to verify password "
        "(Requires python-pam to be installed and is Linux only).")

    parser.add_argument(
        '--verify',
        action='store_const',
        default=False,
        const=True,
        help="Verify the password")

    parser.set_defaults(func=subcommand, config_key='view')


def subcommand(args):
    if args.verify:
        password = getpass.getpass(prompt='Password: ')
        ok = verify_password(args.storage, password)
        if ok:
            print("Password was correct")
            sys.exit(0)
        else:
            print('Wrong password')
            sys.exit(1)

    if (args.use_pam):
        set_password_pam(args.storage)
        print(f"Password hash was set use PAM")
    else:
        password1 = getpass.getpass(prompt='Password: ')
        password2 = getpass.getpass(prompt='Repeat password: ')
        if password1 != password2:
            print("Passwords don't match - please try again", file=sys.stderr)
            sys.exit(1)
        set_password_argon2(args.storage, password1)
        print("The password hash was set to an argon2 hash of your password")
        print("(So your actual password is *not* stored directly...)")
