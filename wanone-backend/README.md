# WanOne AI API

This project is a Flask-based API that uses a fine-tuned AI model based on Google's GEMMA-2B to provide conversational AI services.
Features

Custom AI model integration using Hugging Face Transformers
RESTful API endpoints for AI interactions
Database integration for storing conversations and messages
CORS support for cross-origin requests

Prerequisites

Python 3.10+
MySQL Database

Installation

Clone the repository:

'''
Copygit clone <https://github.com/alexcclo/wanone.git>
cd wanone-backend
'''

Create a virtual environment and activate it:

'''
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
'''

Install the required packages:
'''
pip install -r requirements.txt
'''

Set up your environment variables by creating a .env file in the project root:

'''
SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@host/database_name
'''

## Usage

To run the server:
python app.py

The API will be available at <http://localhost:8087/gen/api/>.
API documentation can be accessed at <http://localhost:8087/gen/api/docs/>.

## API Endpoints

POST /gen/api/agent/AI/Reply: Send a message to the AI agent and receive a reply.