# Glpi-ticket-automotion

Automatic ticket creation on GLPI via the API.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/HayZun/Glpi-ticket-automotion.git
    ```
2. Go to the project directory:
    ```bash
    cd Glpi-ticket-automotion
3. Install dependencies:
    ```bash
    pip3 install -r requirements.txt

4. Make the script executable:
    ```bash
    chmod +x main.py
    ```

# Configuration

Create and fill the config.json file with your GLPI server information at the root of the project.

```json
{
    "url": "http://localhost/glpi/apirest.php",
    "app_token": "XXXXXXXX",
    "user_token": "XXXXXXXX",
}
```

## Usage

```bash
usage: python3 main.py [-h] -s SUBJECT -d DESCRIPTION -e ENTITY_ID -a ASSIGN_GROUP_ID -t TYPE [-c CATEGORY_ID] [-u URGENCY]
The required arguments are:
- `-s` ou `--subject` : Ticket subject
- `-d` ou `--description` : Ticket description
- `-e` ou `--entity_id` : Entity ID
- `-a` ou `--assign_group_id` : Assign group ID
- `-t` ou `--ticket_type` : Type ticket (incident or demand)

The optional arguments are:
- `-c` ou `--category_id` : Category ID
- `-u` ou `--urgency` : Urgency ('low', 'medium', 'high', 'critical', 'major')

## Exemple

```bash
./main.py -s "Test" -d "Test" -e 0 -a 0 -t "incident" -c 0 -u "low"
```