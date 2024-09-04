
---

# Job-Bot: Automated LinkedIn Easy Apply

Job-Bot is a Python-based automation tool that uses Selenium to help users automatically apply for jobs on LinkedIn using the Easy Apply feature. The bot fills out application forms based on the user's pre-configured details, saving time and ensuring consistency across applications.

## Features

- **Automated Applications:** Apply for jobs on LinkedIn with the Easy Apply feature automatically.
- **Customizable Configurations:** Set up your application preferences, including job keywords, location, and required details.
- **Secure Login:** Safely store and use your LinkedIn credentials for automation.
- **User-Friendly Setup:** Simple configuration through a `config.py` file.

## Prerequisites

Before running Job-Bot, ensure you have the following installed:

- Python 3.x
- Pip (Python package installer)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/job-bot.git
   cd job-bot
   ```

2. **Install Required Packages:**
   Install the dependencies listed in `requirements.yaml` using pip:
   ```bash
   pip install -r requirements.yaml
   ```

   *The following packages will be installed:*
   - `selenium`
   - `webdriver_manager`

## Configuration

Job-Bot requires user-specific details to function correctly. These details are configured in the `config.py` file.

### Required Details

Open the `config.py` file and fill in the following information:

- **LinkedIn Credentials:**
  - `LINKEDIN_USERNAME`: Your LinkedIn email or username.
  - `LINKEDIN_PASSWORD`: Your LinkedIn password.

- **Job Preferences:**
  - `JOB_KEYWORDS`: Keywords for the types of jobs you're interested in.
  - `LOCATION`: Desired job location.

- **Personal Information:**
  - `PHONE_NUMBER`: Your phone number.
  - `EXPERIENCE`: Brief summary of your experience (if required).
  - **Additional Fields:** Include any other details that may be required by the company during the application process (e.g., resume, cover letter, portfolio links).

Example `config.py`:

```python
LINKEDIN_USERNAME = 'your_email@example.com'
LINKEDIN_PASSWORD = 'your_password'
JOB_KEYWORDS = ['Software Engineer', 'Data Scientist']
LOCATION = 'New York, NY'
PHONE_NUMBER = '+1234567890'
EXPERIENCE = '3 years in software development'
```

## Usage

1. **Run the Bot:**
   Once the configuration is complete, run the bot using the following command:
   ```bash
   python job_bot.py
   ```

2. **Monitoring:**
   - The bot will automatically log in to LinkedIn and start applying to jobs that match your criteria.
   - You can monitor the process through the command line interface.

## Limitations

- The bot is designed to work only with LinkedIn's Easy Apply feature.
- Ensure that your internet connection is stable to avoid disruptions.
- Review and test the bot's functionality in a controlled environment before running it extensively.

## Disclaimer

Use this tool responsibly and be aware of LinkedIn's terms of service. Automating job applications could potentially violate these terms, so proceed at your own risk.

---
