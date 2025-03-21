# PlateNotify

PlateNotify is a Telegram bot that allows users to register their vehicle plate numbers and receive notifications when their plate is mentioned in specific chat groups.

## Features

- **Plate Registration:** Users can register a vehicle plate number with their Telegram ID.
- **Plate Normalization & Validation:** Incoming plate strings are normalized (uppercase, remove special characters) and validated against the format (3 letters + 1-3 digits).
- **Alert Notifications:** When a registered plate is mentioned in an allowed chat, the owner is notified via a Telegram message.
- **Alert Logging:** Alerts are recorded in a PostgreSQL database for historical tracking.

## Prerequisites

- Python 3.12+
- PostgreSQL database
- Telegram Bot Token

## Setup

1. **Clone the Repository & Create a Virtual Environment:**

   ```shell
   cd c:\PlateNotify
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install Dependencies:**

   ```shell
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**

   - Create or update the `.env` file in the project root with your credentials:
     - `BOT_TOKEN`: Your Telegram Bot token.
     - `DB_URL`: PostgreSQL connection string.

4. **Initialize the Database:**

   When the bot starts, it creates the required tables. Ensure your PostgreSQL instance is running and accessible.

## File Structure

```
PlateNotify
├── .env                      # Environment variables file (ignored by Git)
├── .gitignore                # Git ignore rules
├── Procfile                  # Process file for deployment platforms
├── main.py                   # Entry point for the Telegram bot
├── requirements.txt          # Python package dependencies
└── app
    ├── handlers.py           # Telegram bot command and message handlers
    ├── utils.py              # Utility functions (plate normalization and registration)
    └── database
        ├── database.py       # Database connection and session creation
        └── models.py         # SQLAlchemy models (User, Plate, Alert)
```

## Module Overviews

### main.py

- **Purpose:**  
  Initializes environment variables, creates database tables, starts the Telegram bot, and begins polling for messages.

- **Key Functions:**  
  - `main()`: Loads configuration, sets up the bot, and starts polling for updates.
  
### app/database/database.py

- **Purpose:**  
  Configures the SQLAlchemy engine and session factory using the connection URL from the `.env` file.

- **Key Exports:**  
  - `engine`: SQLAlchemy engine to interact with the PostgreSQL database.
  - `SessionLocal`: A session factory for creating sessions.

### app/database/models.py

- **Purpose:**  
  Defines the database models using SQLAlchemy.

- **Key Models:**
  - `User`: Represents a Telegram user.
  - `Plate`: Stores vehicle plate numbers linked to a user.
  - `Alert`: Records alerts when a plate is mentioned in a specified chat.

### app/utils.py

- **Purpose:**  
  Provides helper functions for plate normalization, registration, and plate lookup.

- **Key Functions:**
  - `normalize_plate(plate: str) -> str or None`:  
    Normalizes the plate by converting to uppercase, removing invalid characters, and validates against a specific format. Returns the normalized plate or `None` if invalid.
  - `register_plate(user_telegram_id: int, plate_number: str) -> bool`:  
    Registers a plate number for a Telegram user. If the user does not exist, a new user record is created. Returns `False` if the plate is already registered.
  - `get_user_by_plate(plate_number: str) -> int or None`:  
    Looks up a plate number, joining with the user table, and returns the associated Telegram user ID if found.

### app/handlers.py

- **Purpose:**  
  Contains the command and message handlers for the Telegram bot using the Aiogram framework.

- **Key Handlers:**
  - `/start`:  
    Welcomes the user and provides usage instructions.
  - `/register <plate_number>`:  
    Allows a user to register a vehicle plate number. If used in a non-private chat, informs the user to switch to a private conversation.
  - **Plate Mention Checker:**  
    Monitors messages in a specific chat (identified by `ALLOWED_CHAT_ID`) and checks if any registered plate numbers are mentioned. If a match is found, the bot sends a notification to the corresponding user and logs an alert in the database.

## Running the Bot

- **Local Execution:**

  ```shell
  python main.py
  ```

- **Using Procfile (for platforms like Heroku):**

  The `Procfile` specifies the worker command:

  ```plaintext
  worker: python main.py
  ```

## Contributing

Contributions and suggestions are welcome. Please open an issue or submit a pull request for enhancements and bug fixes.

## License

This project is provided for educational purposes.