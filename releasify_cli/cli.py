import argparse
import logging
import os
import sys
import textwrap

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from releasify.constants import INVALD_LOG_LEVEL_ERR
from releasify.client import Client


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('owner', help='The owner of the repo')
    parser.add_argument('repo', help='The name of the repo')
    parser.add_argument('type', help='The type of release')
    parser.add_argument('-u', '--user', help='Your GitHub username')
    parser.add_argument('-p', '--password', help='Your GitHub password or personal access token')
    parser.add_argument('-b', '--branch', 
                        help='The branch on which to create the release. Defaults to whatever the target branch is set to in the repo settings')
    parser.add_argument('-d', '--dryrun', help='Perform a dry run (doesn\'t create the release)', 
                        action='store_true')
    parser.add_argument('-f', '--force', help='Create a release even if there aren\'t any commits since the last release', 
                        action='store_true')
    parser.add_argument('--draft', help='Is this a draft release?', action='store_true')                        
    parser.add_argument('--prerelease', help='Is this a prerelease?', action='store_true', default=True)                        
    parser.add_argument('-ll', '--loglevel', 
                        help='Set the logging level. One of: debug, info, warning, error, critical. Defaults to `warning`', 
                        default='warning')
    args = parser.parse_args()
    print(args)

    try:
        logging.basicConfig(level=getattr(logging, args.loglevel.upper()))
    except AttributeError:
        print(INVALD_LOG_LEVEL_ERR.format(log_level=args.loglevel))

    user = args.user or os.getenv('GITHUB_USER')
    password = args.password or os.getenv('GITHUB_PASSWORD')
    client = Client(user, password)

    try:
        result = client.create_release(
            args.owner, args.repo, args.type, args.draft, args.prerelease, args.dryrun, args.force, args.branch
        )

        if result['ok']:
            print(f'Release name: {result["tag_name"]}')
            print(f'Release body: {result["body"]}')
        else:
            # TODO: show error code & message?
            pass
    except Exception as e:
        error_msg = f"""
        An error occurred.
        Message: {str(e)}
        URL: {e.resp.url}
        Status code: {e.resp.status_code}
        """
        print(textwrap.dedent(error_msg))
    