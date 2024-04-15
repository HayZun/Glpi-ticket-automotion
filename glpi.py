#!/usr/bin/python3

import json
import logging

import requests


class Glpi:

    def __init__(self, config):
        self.url_glpi = config["url_glpi"]
        self.url_api_glpi = self.url_glpi + "/apirest.php"
        self.app_token = config["app_token"]
        self.user_token = config["user_token"]
        self.logger = logging.getLogger(__name__)  # Initialisation du logger
        self._session = None
        self._id_ticket = None
        self.logger.info("GLPI object created.")  # Log d'information

    def init_session_glpi(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "user_token " + self.user_token,
            "App-Token": self.app_token,
        }
        response = requests.request(
            "GET", self.url_api_glpi + "/initSession", headers=headers
        )
        response = json.loads(response.text)
        if "session_token" not in response:
            self.logger.error(response)
            raise Exception("Error while initializing session.")
        else:
            self._session = response["session_token"]
            self.logger.info("Session GLPI initialized.")  # Log d'information

    # get user id with session token
    def get_user_id(self):
        self.logger.info("Get user id with session token")  # Log d'information
        headers = {
            "Content-Type": "application/json",
            "Session-Token": self._session,
            "App-Token": self.app_token,
        }
        response = requests.request(
            "GET", self.url_api_glpi + "/getFullSession/", headers=headers
        )
        response = json.loads(response.text)
        user_id = response["session"]["glpiID"]
        self.logger.info("User id retrieved (id: %s)" % user_id)  # Log d'information
        return user_id

    def creation_ticket(
        self,
        ticket_data,
    ):
        self.logger.info("Creation of a ticket in GLPI")  # Log d'information

        dict_type_ticket = {"demand": 1, "incident": 2}

        # Required data
        subject = ticket_data["subject"]
        description = ticket_data["description"]
        entity_id = ticket_data["entity_id"]
        assign_group_id = ticket_data["assign_group_id"]
        type_ticket = dict_type_ticket[ticket_data["type"]]

        # Optional data
        optional_data = {}
        if "urgency" in ticket_data:
            dict_urgency = {"low": 2, "medium": 3, "high": 4, "critical": 5, "major": 6}
            optional_data["urgency"] = dict_urgency[ticket_data["urgency"]]
        if "category_id" in ticket_data:
            optional_data["category_id"] = ticket_data["category_id"]

        # Construction du payload JSON
        payload = {
            "input": {
                "entities_id": entity_id,
                "name": subject,
                "status": "1",
                "type": type_ticket,
                "content": description,
                "_users_id_requester": self.get_user_id(),
                "_groups_id_assign": assign_group_id,
            }
        }

        if optional_data == {}:
            self.logger.info("No optional data provided")
        else:
            self.logger.info("Optional data provided: %s" % optional_data)
            if "category_id" in optional_data:
                payload["input"]["itilcategories_id"] = optional_data["category_id"]
            if "urgency" in optional_data:
                payload["input"]["priority"] = optional_data["urgency"]
        
        # Envoi de la requête POST
        headers = {
            "Content-Type": "application/json",
            "Session-Token": self._session,
            "App-Token": self.app_token,
        }
        print(payload)
        # response = requests.post(
        #     self.url_api_glpi + "/Ticket/", headers=headers, json=payload
        # )

        # # Log de l'envoi du ticket
        # if response.status_code == 201:
        #     self._id_ticket = response.json()["id"]
        #     self.logger.info(
        #         f"Ticket created successfully, url: {self.url_glpi}/front/ticket.form.php?id={self._id_ticket}"
        #     )
        # else:
        #     self.logger.error("Error while creating ticket")

    def kill_session_glpi(self):
        headers = {
            "Content-Type": "application/json",
            "Session-Token": self._session,
            "App-Token": self.app_token,
        }
        response = requests.request(
            "GET", self.url_api_glpi + "/killSession", headers=headers
        )
        if response.status_code == 200:
            self.logger.info("Session GLPI killed.")
        else:
            self.logger.error(response.json())
            self.logger.error("Error while killing session.")
