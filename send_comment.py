#!/usr/bin/env python3
""" This is a short python script for sending comments to Github Pull Requsets.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys

from github import Github


def delete_old_comments(issue, user):
    for c in issue.get_comments():
        if c.user.login == user.login:
            c.delete()


def main(access_token, args):
    try:
        gh = Github(os.environ['GITHUB_ACCESS_TOKEN'])
        repo = gh.get_repo(args[1])
        number = int(args[2])
        message = args[3]
        issue = repo.get_issue(number)
        delete_old_comments(issue, gh.get_user())
        print('Adding comment {}'.format(message))
        issue.create_comment(message)
    except Exception as e:
        print('Error: Comment could not be created '
              'on {} PR #{} ({})'.format(repo.full_name, number, repr(e)))


if 'GITHUB_ACCESS_TOKEN' in os.environ:
    main(os.environ['GITHUB_ACCESS_TOKEN'], sys.argv)
    sys.exit(0)
else:
    print('Please set the GITHUB_ACCESS_TOKEN environment variable')
    sys.exit(1)
