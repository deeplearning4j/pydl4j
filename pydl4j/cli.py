#!/usr/bin python
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys
import pkg_resources
import argcomplete
import traceback
from builtins import input

import click
from click.exceptions import ClickException
from dateutil import parser


DEFAULT_DL4J_VERSION = "1.0.0-SNAPSHOT"
DEFAULT_BACKEND = "gpu"
DEFAULT_DATAVEC = 'y'
DEFAULT_SPARK = 'y'
DEFAULT_SPARK_MAJOR = "2"
DEFAULT_SCALA_VERSION = "2.10"
DEFAULT_SPARK_DETAILS = 'y'


def to_bool(string):
    return True if string[0] in ["Y", "y"] else False

class CLI(object):
    
    def __init__(self):
        self.var_args = None
        self.command = None

    def command_dispatcher(self, args=None):
        desc = ('pydl4j,  a system to manage your DL4J dependencies from Python.\n')
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument(
            '-v', '--version', action='version',
            version=pkg_resources.get_distribution("pydl4j").version,
            help='Print pydl4j version'
        )

        subparsers = parser.add_subparsers(title='subcommands', dest='command')
        subparsers.add_parser('init', help='Initialize pydl4j')

        argcomplete.autocomplete(parser)
        args = parser.parse_args(args)
        self.var_args = vars(args)

        if not args.command:
            parser.print_help()
            return

        self.command = args.command

        if self.command == 'init':
            self.init()
            return

  

    def init(self, settings_file="pydl4j.json"):

        if os.path.isfile(settings_file):
            raise ClickException("This project already has a " + click.style("{0!s} file".format(settings_file), fg="red", bold=True) + "!")

        click.echo(click.style(u"""\n██████╗ ██╗   ██╗██████╗ ██╗██╗  ██╗     ██╗
██╔══██╗╚██╗ ██╔╝██╔══██╗██║██║  ██║     ██║
██████╔╝ ╚████╔╝ ██║  ██║██║███████║     ██║
██╔═══╝   ╚██╔╝  ██║  ██║██║╚════██║██   ██║
██║        ██║   ██████╔╝███████╗██║╚█████╔╝
╚═╝        ╚═╝   ╚═════╝ ╚══════╝╚═╝ ╚════╝ \n""", fg='blue', bold=True))

        click.echo(click.style("pydl4j", bold=True) + " is a system to manage your DL4J dependencies from Python!\n")

        # DL4J version
        dl4j_version = input("Which DL4J version do you want to use for your Python projects? (default '%s'): " % DEFAULT_DL4J_VERSION) or DEFAULT_DL4J_VERSION
        # TODO: check if input is valid

        # ND4J backend
        backend = input("Which backend would you like to use ('cpu' or 'gpu')? (default '%s'): " % DEFAULT_BACKEND) or DEFAULT_BACKEND
        backend = backend.lower()

        # DataVec usage
        datavec = input("Do you need DL4J DataVec for ETL? (default 'y') [y/n]: ") or DEFAULT_DATAVEC
        datavec = to_bool(datavec)

        # DL4J core usage
        DEFAULT_DL4J = 'y'
        dl4j_core = input("Do you want to work with DeepLearning4J from Python? (default 'y') [y/n]: ") or DEFAULT_DL4J
        dl4j_core = to_bool(dl4j_core)

        # Spark
        spark = input("Do you need Spark for distributed computation in your application? (default 'y') [y/n]: ") or DEFAULT_SPARK
        spark = to_bool(spark)

        spark_details = input("We use Spark {} and Scala {} by default, is this OK for you? (default 'y') [y/n]: ".format(DEFAULT_SPARK_MAJOR,
            DEFAULT_SCALA_VERSION)) or DEFAULT_SPARK_DETAILS
        if spark_details[0] in ["Y", "y"]:
            spark_version = "2"
            scala_version = "2.10"
        else:
            spark_version = input("Which which major Spark release would you like to use? (default '%s'): " % DEFAULT_SPARK_MAJOR) or DEFAULT_SPARK_MAJOR
            scala_version = input("Which Scala version would you like to use? (default '%s'): " % DEFAULT_SCALA_VERSION) or DEFAULT_SCALA_VERSION


        pydl4j_settings = {
                'dl4j_version': dl4j_version,
                'backend': backend,
                'dl4j_core': dl4j_core,
                'datavec': datavec,
                'spark': spark,
                'spark_version': spark_version,
                'scala_version': scala_version
        }

        pydl4j_json = json.dumps(pydl4j_settings, sort_keys=False, indent=2)

        click.echo("\nThis is your current settings file " + click.style("pydl4j_settings.json", bold=True) + ":\n")
        click.echo(click.style(pydl4j_json, fg="green", bold=True))

        confirm = input("\nDoes this look good? (default 'y') [y/n]: ") or 'yes'
        if not to_bool(confirm):
            click.echo("" + click.style("Please initialize pydl4j once again", fg="red", bold=True))
            return

        with open("pydl4j_settings.json", "w") as f:
            f.write(pydl4j_json)

    def load_settings(self, settings_file="pydl4j_settings.json"):
        if not os.path.isfile(settings_file):
            raise ClickException("Configure your settings file with `pydl4j init` first.")

        with open(settings_file) as json_file:
            try:
                pydl4j_settings = json.load(json_file)
            except:
                raise ValueError("JSON file can't be loaded.")
        return pydl4j_settings

def handle():
    try:
        cli = CLI()
        sys.exit(cli.command_dispatcher())
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        click.echo(click.style("Error: ", fg='red', bold=True))
        traceback.print_exc()
        sys.exit()

if __name__ == '__main__':
    handle()
