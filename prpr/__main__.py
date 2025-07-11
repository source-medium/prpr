"""CLI entry point for prpr."""

import json
import sys

import click

from prpr.classifier import CommentClassifier
from prpr.config import Config
from prpr.gh import GitHubAPI
from prpr.io import ThreadsIO


@click.group()
@click.help_option("--help", "-h")
def cli():
    """CLI tool for managing GitHub pull request comments."""


@cli.command()
def sync():
    """Fetch all threads/comments for the current PR and write .prpr/threads.json."""
    try:
        # Check if gh CLI is available
        gh_api = GitHubAPI()
        if not gh_api.is_available():
            click.echo("GitHub CLI not found", err=True)
            sys.exit(9)

        # Get PR number from current branch
        pr_number = gh_api.get_current_pr_number()
        if not pr_number:
            click.echo("Not in a PR branch", err=True)
            sys.exit(11)

        # Fetch PR comments
        raw_comments = gh_api.get_pr_comments(pr_number)

        # Initialize classifier with config
        config = Config()
        classifier = CommentClassifier(config)

        # Classify comments
        classified_comments = classifier.classify_comments(raw_comments)

        # Write to .prpr/threads.json
        threads_io = ThreadsIO()
        threads_io.write_threads(pr_number, classified_comments)

        click.echo(f"Synced {len(classified_comments)} threads for PR #{pr_number}")

    except Exception as e:
        click.echo(f"API failure: {e}", err=True)
        sys.exit(10)


@cli.command()
@click.option("--author", help="Filter by author type")
@click.option("--open", "open_only", is_flag=True, help="Show only open threads")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
def ls(author: str | None, open_only: bool, json_output: bool):
    """Emit a filtered JSON list to stdout."""
    try:
        threads_io = ThreadsIO()
        threads_data = threads_io.read_threads()

        # Filter threads
        filtered_threads = threads_data["threads"]

        if author:
            filtered_threads = [
                t for t in filtered_threads if t["author_type"] == author
            ]

        if open_only:
            filtered_threads = [t for t in filtered_threads if t["state"] == "open"]

        if json_output:
            click.echo(json.dumps(filtered_threads, indent=2))
        else:
            for thread in filtered_threads:
                click.echo(f"{thread['id']}: {thread['body'][:50]}...")

    except Exception as e:
        click.echo(f"Failed to read threads: {e}", err=True)
        sys.exit(10)


@cli.command()
@click.argument("thread_id")
@click.argument("message")
def reply(thread_id: str, message: str):
    """Post a reply to a specific thread."""
    try:
        gh_api = GitHubAPI()
        if not gh_api.is_available():
            click.echo("GitHub CLI not found", err=True)
            sys.exit(9)

        # Post reply
        comment_id = gh_api.post_reply(thread_id, message)
        click.echo(comment_id)

    except Exception as e:
        click.echo(f"Failed to post reply: {e}", err=True)
        sys.exit(10)


@cli.command()
@click.option("--since", required=True, help="ISO timestamp to check from")
def check_new(since: str):
    """List comments newer than timestamp."""
    try:
        threads_io = ThreadsIO()
        threads_data = threads_io.read_threads()

        # Filter by timestamp
        from datetime import datetime

        since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))

        new_threads = []
        for thread in threads_data["threads"]:
            thread_dt = datetime.fromisoformat(
                thread["created_at"].replace("Z", "+00:00")
            )
            if thread_dt > since_dt:
                new_threads.append(thread)

        click.echo(json.dumps(new_threads, indent=2))

    except Exception as e:
        click.echo(f"Failed to check new comments: {e}", err=True)
        sys.exit(10)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
