"""
Intialising firebase admin ,firestore client and stripe
"""
import firebase_admin
import stripe
from firebase_admin import firestore
from google.cloud import tasks_v2

CT_CLIENT = tasks_v2.CloudTasksClient()

FB_APP = firebase_admin.initialize_app()

FS_CLIENT = firestore.client()

stripe.api_key = "sk_test_51MyTwDSHKZRFQ2mqKuh7R0bavcJIPXGJkF5e9mtDUoBD1PufUUAWl15cxversk5d07RefdzxooeqkehSPi20Gr2C00wkNfIgXd"
