# nimboapp/schema.py

from ariadne import QueryType, MutationType, make_executable_schema, gql
from django.db import connection
from datetime import datetime

# GraphQL Schema Definition
type_defs = gql("""
    type Query {
        _empty: String
        symptoms: [Symptom!]!
        diagnosis: [Diagnosis!]!
    }

    type Mutation {
        registerUserWithEmail(email: String!): UserEmailRegistrationResponse!
    }

    type UserEmailRegistrationResponse {
        success: Boolean!
        message: String!
        user: User
    }

    type User {
        email: String!
        is_email_verified: Boolean!
        created_at: String!
        updated_at: String!
    }

    type Symptom {
        id: ID!
        user_id: String!
        title: String!
        status: Boolean!
        soft_delete: Boolean!
        created_at: String!
        updated_at: String!
    }

    type Diagnosis {
        id: ID!
        user_id: String!
        title: String!
        status: Boolean!
        soft_delete: Boolean!
        created_at: String!
        updated_at: String!
    }
""")

query = QueryType()
mutation = MutationType()

# Mutation Resolver (registerUserWithEmail)
@mutation.field("registerUserWithEmail")
def resolve_register_user_with_email(_, info, email):
    try:
        with connection.cursor() as cursor:
            # Check if the email already exists
            cursor.execute("""
                SELECT user_id FROM users_shard WHERE email = %s
            """, [email])
            existing_user = cursor.fetchone()

            if existing_user:
                return {
                    "success": False,
                    "message": "Email already in use",
                    "user": None
                }

            # Insert new user if email does not exist
            created_at = updated_at = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO users_shard (email, is_email_verified, created_at, updated_at)
                VALUES (%s, %s, %s, %s)
                RETURNING email, is_email_verified, created_at, updated_at
            """, [email, False, created_at, updated_at])
            user = cursor.fetchone()
        
        if user:
            return {
                "success": True,
                "message": "User email registered successfully",
                "user": {
                    "email": user[0],
                    "is_email_verified": user[1],
                    "created_at": user[2],
                    "updated_at": user[3]
                }
            }
        else:
            return {
                "success": False,
                "message": "User email registration failed",
                "user": None
            }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "user": None
        }

# Query Resolver for symptoms
@query.field("symptoms")
def resolve_symptoms(_, info):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, user_id, title, status, soft_delete, created_at, updated_at
                FROM symptoms
            """)
            symptoms = []
            for row in cursor.fetchall():
                symptom = {
                    "id": row[0],
                    "user_id": row[1],
                    "title": row[2],
                    "status": row[3],
                    "soft_delete": row[4],
                    "created_at": row[5].isoformat(),
                    "updated_at": row[6].isoformat(),
                }
                symptoms.append(symptom)
        return symptoms
    except Exception as e:
        return []

# Query Resolver for diagnoses
@query.field("diagnosis")
def resolve_diagnosis(_, info):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, user_id, title, status, soft_delete, created_at, updated_at
                FROM diagnosis
            """)
            diagnoses = []
            for row in cursor.fetchall():
                diagnosis = {
                    "id": row[0],
                    "user_id": row[1],
                    "title": row[2],
                    "status": row[3],
                    "soft_delete": row[4],
                    "created_at": row[5].isoformat(),
                    "updated_at": row[6].isoformat(),
                }
                diagnoses.append(diagnosis)
        return diagnoses
    except Exception as e:
        return []

# Create executable schema
schema = make_executable_schema(type_defs, query, mutation)
