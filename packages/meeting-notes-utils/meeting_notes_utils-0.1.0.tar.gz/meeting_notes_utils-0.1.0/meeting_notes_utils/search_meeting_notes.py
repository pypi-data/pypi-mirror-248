"""Search meeting notes .yaml files."""
import datetime
import os
import sys
import click
import pathlib
import logging
import yaml

from pathlib import Path
from datetime import datetime
from rich.console import Console
from typing import List

from .file_utils import check_indir_status, check_infile_status

DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    "meeting-notes-utils",
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))
)

DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False

error_console = Console(stderr=True, style="bold red")

console = Console()


def get_infiles(indir: str, infile: str) -> List[str]:
    """Get candidate meeting notes .yaml files.

    Args:
        indir (str): input directory containing some meeting notes .yaml files
        infile (str): input meeting notes .yaml file

    Raises:
        Exception: If neither indir nor infile were specified

    Returns:
        List[str]: list of meeting notes .yaml files
    """
    infiles = []
    if indir is not None:
        infiles = [os.path.join(indir, f) for f in os.listdir(indir) if os.path.isfile(os.path.join(indir, f)) and os.path.join(indir, f).endswith(".yaml")]
    elif infile is not None and infile.endswith(".yaml"):
        infiles = [infile]
    else:
        raise Exception("Neither indir nor infile were specified")
    return infiles

def search_meeting_notes(
        logfile: str,
        outdir: str,
        outfile: str,
        indir: str = None,
        infile: str = None,
        keywords: str = None,
        topics: str = None,
    ) -> None:
    """Search meeting notes .yaml files."""

    infiles = get_infiles(indir, infile)

    topic_list = None
    if topics is not None:
        topic_list = [t.strip() for t in topics.strip().split(",")]

    keyword_list = None
    if keywords is not None:
        keyword_list = [k.strip() for k in keywords.strip().split(",")]

    topic_to_file_lookup = {}
    topic_found_ctr = 0

    keyword_to_file_lookup = {}
    keyword_found_ctr = 0

    file_ctr = 0
    for meeting_file in infiles:
        file_ctr += 1

        logging.info(f"Will load contents of meeting notes file '{meeting_file}'")
        lookup = yaml.safe_load(Path(meeting_file).read_text())
        if "topic" not in lookup:
            error_console.print(f"[bold red]The meeting notes file '{meeting_file}' does not contain a 'topic' key[/]")
            continue

        if topic_list is not None:
            for topic in topic_list:
                if topic in lookup["topic"]:
                    if topic not in topic_to_file_lookup:
                        topic_to_file_lookup[topic] = []
                    topic_to_file_lookup[topic].append(meeting_file)
                    topic_found_ctr += 1
                else:
                    logging.info(f"The meeting notes file '{meeting_file}' does not contain the topic '{topic}'[/]")
                    continue

        if "keywords" not in lookup:
            logging.info(f"Did not find 'keywords' in meeting notes file '{meeting_file}'")
            continue

        if keyword_list is not None:
            for keyword in keyword_list:
                if keyword in lookup["keywords"]:
                    if keyword not in keyword_to_file_lookup:
                        keyword_to_file_lookup[keyword] = []
                    keyword_to_file_lookup[keyword].append(meeting_file)
                    keyword_found_ctr += 1
                else:
                    logging.info(f"The meeting notes file '{meeting_file}' does not contain the keyword '{keyword}'[/]")
                    continue

    if topic_found_ctr == 0 and keyword_found_ctr == 0:
        error_console.print(f"[bold red]No topics or keywords were found among all '{file_ctr}' files searched:[/]")
        logging.info(f"No topics or keywords were found among all '{file_ctr}' files searched:")
        for meeting_file in infiles:
            print(f"{meeting_file}")
            logging.info(f"{meeting_file}")
        return None

    generate_topic_report(topic_list, topic_found_ctr, topic_to_file_lookup, file_ctr, infiles)
    generate_keyword_report(keyword_list, keyword_found_ctr, keyword_to_file_lookup, file_ctr, infiles)

def generate_topic_report(topic_list, topic_found_ctr, topic_to_file_lookup, file_ctr, infiles) -> None:
    """Generate a report of topics found in meeting notes .yaml files.

    Args:
        topic_list (List[str]): List of topics searched for.
        topic_found_ctr (int): Number of topics found.
        topic_to_file_lookup (Dict[str, str]): Topic to file found in lookup.
        file_ctr (int): Number of files searched.
        infiles (List[str]): The list of meeting notes .yaml files searched.
    """
    if topic_list is not None:
        if topic_found_ctr == 0:
            error_console.print(f"[bold red]No topics were found among all {file_ctr} files searched:[/]")
            logging.info(f"No topics were found among all '{file_ctr}' files searched:")
            for meeting_file in infiles:
                console.print(f"{meeting_file}")
                logging.info(f"{meeting_file}")
        else:
            if topic_found_ctr > 0:
                console.print(f"Found {topic_found_ctr} topics among {file_ctr} files searched:")
                logging.info(f"Found {topic_found_ctr} topics among '{file_ctr}' files searched:")
                for topic, file_list in topic_to_file_lookup.items():
                    count = len(file_list)
                    console.print(f"\nFound topic '{topic}' in the following {count} files:")
                    logging.info(f"Found topic '{topic}' in the following '{count}' files:")
                    for f in file_list:
                        console.print(f"{f}")
                        logging.info(f"{f}")
    # else:
    #     error_console.print(f"[bold red]No topics were found among all '{file_ctr}' files searched:[/]")
    #     logging.info(f"No topics were found among all '{file_ctr}' files searched:")
    #     for meeting_file in infiles:
    #         print(f"{meeting_file}")
    #         logging.info(f"{meeting_file}")


def generate_keyword_report(keyword_list, keyword_found_ctr, keyword_to_file_lookup, file_ctr, infiles) -> None:
    """Generate a report of keywords found in meeting notes .yaml files.

    Args:
        keyword_list (List[str]): List of keywords searched for.
        keyword_found_ctr (int): Number of keywords found.
        keyword_to_file_lookup (Dict[str, str]): keyword to file found in lookup.
        file_ctr (int): Number of files searched.
        infiles (List[str]): The list of meeting notes .yaml files searched.
    """
    if keyword_list is not None:
        if keyword_found_ctr == 0:
            error_console.print(f"[bold red]No keywords were found among all {file_ctr} files searched:[/]")
            logging.info(f"No keywords were found among all '{file_ctr}' files searched:")
            for meeting_file in infiles:
                console.print(f"{meeting_file}")
                logging.info(f"{meeting_file}")
        elif keyword_found_ctr > 0:
            console.print(f"Found {keyword_found_ctr} keywords among {file_ctr} files searched:")
            logging.info(f"Found {keyword_found_ctr} keywords among '{file_ctr}' files searched:")
            for keyword, file_list in keyword_to_file_lookup.items():
                count = len(file_list)
                console.print(f"\nFound keyword '{keyword}' in the following {count} files:")
                logging.info(f"Found keyword '{keyword}' in the following '{count}' files:")
                for f in file_list:
                    console.print(f"{f}")
                    logging.info(f"{f}")
        # else:
        #     print(f"Did not find any keywords among '{file_ctr}' files searched:")
        #     for meeting_file in infiles:
        #         print(f"{meeting_file}")
        #         logging.info(f"{meeting_file}")

    print("")


def validate_verbose(ctx, param, value):
    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return DEFAULT_VERBOSE
    return value


@click.command()
@click.option('--indir', help="Optional: The directory containing meeting notes .yaml files.")
@click.option('--infile', help="Optional: The meeting notes .yaml file to be searched.")
@click.option('--keywords', help="Optional: Some keywords to search for.")
@click.option('--logfile', help="Optional: The log file.")
@click.option('--outdir', help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'.")
@click.option('--outfile', help="Optional: The output search results file.")
@click.option('--topics',  help="Optional: Some topics to search for.")
@click.option('--verbose', is_flag=True, help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(indir: str, infile: str, keywords: str, logfile: str, outdir: str, outfile: str, topics: str, verbose: bool):
    """Search meeting notes .yaml files."""
    error_ctr = 0

    if indir is None and infile is None:
        error_console.print("[bold red]--indir and --infile were not specified[/]")
        error_ctr += 1

    if indir is not None:
        check_indir_status(indir)

    if infile is not None:
        check_infile_status(infile)

    if keywords is None and topics is None:
        error_console.print("[bold red]--keywords and --topics were not specified[/]")
        error_ctr += 1

    if error_ctr > 0:
        sys.exit(1)

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        console.print(f"[yellow]--outdir was not specified and therefore was set to '{outdir}'[/]")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        console.print(f"[yellow]Created output directory '{outdir}'[/]")

    if logfile is None:
        logfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.log'
        )
        console.print(f"[yellow]--logfile was not specified and therefore was set to '{logfile}'[/]")

    if outfile is None:
        outfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.report.txt'
        )
        console.print(f"[yellow]--outfile was not specified and therefore was set to '{outfile}'[/]")

    if verbose is None:
        verbose = DEFAULT_VERBOSE
        console.print(f"[yellow]--verbose was not specified and therefore was set to '{verbose}'[/]")

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    search_meeting_notes(
        logfile,
        outdir,
        outfile,
        indir,
        infile,
        keywords,
        topics,
    )

    print(f"The log file is '{logfile}'")
    console.print(f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]")
    sys.exit(0)

if __name__ == "__main__":
    main()

