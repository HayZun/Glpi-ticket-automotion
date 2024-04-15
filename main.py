#!/home/paul/.work/2022134222/venv/bin/python3
"""
Description: Create a ticket in GLPI
Author: Paul Durieux
Date: 11/04/2024
Version: 1.0
"""

import argparse
import logging
import json
from glpi import Glpi

class Main:
    def __init__(self, glpi, ticket_data):
        self.glpi = glpi
        self.ticket_data = ticket_data

    def action(self):
        try:
            self.glpi.init_session_glpi()
            self.glpi.creation_ticket(self.ticket_data)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
        finally:
            self.glpi.kill_session_glpi()

def setup_logger():
    """
    Configure logging.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

def validate_urgency(value):
    """
    Validate the urgency argument.
    """
    if value.lower() not in {'low', 'medium', 'high', 'critical', 'major'}:
        raise argparse.ArgumentTypeError("Urgency must be one of: low, medium, high, critical, major")
    return value

def validate_ticket_type(value):
    """
    Validate the ticket type argument.
    """
    if value.lower() not in {'demand', 'incident'}:
        raise argparse.ArgumentTypeError("Ticket type must be one of: demand, incident")
    return value

def config_parser():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Create a ticket in GLPI")
    parser.add_argument(
        "-s",
        "--subject",
        type=str,
        required=True,
        help="Subject of the ticket",
    )
    parser.add_argument(
        "-d",
        "--description",
        type=str,
        required=True,
        help="Description of the ticket",
    )
    parser.add_argument(
        "-e",
        "--entity_id",
        type=int,
        required=True,
        help="Entity ID of the ticket",
    )
    parser.add_argument(
        "-a",
        "--assign_group_id",
        type=int,
        required=True,
        help="Assign group ID of the ticket",
    )
    parser.add_argument(
        "-t",
        "--ticket_type",
        type=validate_ticket_type,
        required=False,
        help="Type of the ticket",
    )
    parser.add_argument(
        "-c",
        "--category_id",
        type=int,
        required=False,
        help="Category ID of the ticket",
    )
    parser.add_argument(
        "-u",
        "--urgency",
        type=validate_urgency,
        required=False,
        help="Urgency of the ticket",
    )

    args = parser.parse_args()
    return args

def configure_ticket_data(args):
    """
    Configure ticket data based on command line arguments.
    """
    ticket_data = {
        "subject": args.subject,
        "description": args.description,
        "entity_id": args.entity_id,
        "assign_group_id": args.assign_group_id
    }
    if args.category_id:
        ticket_data["category_id"] = args.category_id
    if args.urgency:
        ticket_data["urgency"] = args.urgency
    return ticket_data

def main():
    setup_logger()  # Configure the logger

    # Configure GLPI instance
    with open("config.json") as f:
        config = json.load(f)

    # Parse command line arguments
    args = config_parser()

    # Configure ticket data
    ticket_data = configure_ticket_data(args)

    # Create GLPI object
    glpi = Glpi(config)

    # Create Main object
    main = Main(glpi, ticket_data)

    # Execute the action
    main.action()

if __name__ == "__main__":
    main()
