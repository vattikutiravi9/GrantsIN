# Grants In

Grants In is a SaaS platform that allows private companies to post grants, and users can apply for those grants by submitting detailed proposals. The platform provides a seamless experience for both grant providers and applicants, making it easy to manage grant opportunities and applications.

## Features

- User authentication and role-based access control (admins, applicants).
- Grant management (create, update, delete grants).
- Application submission with document uploads.
- Search and filter functionality for grants.
- Application status tracking (submitted, pending review, approved, rejected).
- Notifications and audit logs.

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL (SQLite is used here for simplicity)
- A virtual environment tool (optional but recommended)


### Project Setup

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/vattikutiravi9/GrantsIN.git
    cd grantsin
    ```

2. **Set Up a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\\Scripts\\activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Database:**

The application is configured to use SQLite by default.

5. **Run the Application:**
    ```bash
    uvicorn main:app --reload
    ```

6. **Access the Application:**
    Open your browser and navigate to:
    ```
    http://127.0.0.1:8000
    ```

7. **API Documentation:**
    - The interactive API documentation (Swagger UI) is available at:
      ```
      http://127.0.0.1:8000/docs
      ```

## Endpoint Implemented

Currently, only one endpoint is implemented in this application:

### Apply for a Grant

- **Route:** `POST /grants/{grant_id}/apply`
- **Functionality:**
  - Authenticated users can submit their applications for a specific grant.
  - The route handles the following:
    - **Document Uploads:** Users can upload required documents for the grant.
    - **Validation:** Ensures that all required fields are completed before submission.
    - **Status Updates:** Tracks the application status (e.g., submitted, pending review).
    - **Error Handling:** Gracefully handles errors such as missing fields or invalid document formats.

## Running Tests

To run unit tests, use:
```bash
pytest
```

## System architecture
The system design and other services used for the application can be found in the SystemDesign.drawio pdf file
