import re


def extract_intent(user_prompt):
    prompt = user_prompt.lower()

    intent = {
        "app_type": "web application",
        "features": [],
        "roles": [],
        "entities": []
    }

    keywords = {
        "login": "Authentication",
        "dashboard": "Dashboard",
        "payment": "Payments",
        "payments": "Payments",
        "analytics": "Analytics",
        "premium": "Premium Plan",
        "contacts": "Contacts Management",
        "crm": "CRM"
    }

    for word, feature in keywords.items():
        if word in prompt:
            intent["features"].append(feature)

    if "admin" in prompt:
        intent["roles"].append("admin")
    if "user" in prompt or "customer" in prompt:
        intent["roles"].append("user")

    if "contacts" in prompt:
        intent["entities"].append("contacts")
    if "payment" in prompt or "premium" in prompt:
        intent["entities"].append("subscriptions")

    if not intent["roles"]:
        intent["roles"] = ["user", "admin"]

    if not intent["entities"]:
        intent["entities"] = ["users"]

    return intent


def system_design(intent):
    return {
        "architecture": "Frontend + API + Database + Auth",
        "entities": intent["entities"],
        "roles": intent["roles"],
        "flows": [
            "User registers or logs in",
            "User accesses dashboard",
            "Role permissions are checked",
            "Business rules are applied"
        ]
    }


def generate_schema(intent, design):
    pages = [
        {
            "name": "Login",
            "route": "/login",
            "components": ["EmailInput", "PasswordInput", "LoginButton"]
        },
        {
            "name": "Dashboard",
            "route": "/dashboard",
            "components": ["Sidebar", "StatsCards", "MainContent"]
        }
    ]

    if "Contacts Management" in intent["features"]:
        pages.append({
            "name": "Contacts",
            "route": "/contacts",
            "components": ["ContactForm", "ContactTable"]
        })

    if "Analytics" in intent["features"]:
        pages.append({
            "name": "Analytics",
            "route": "/analytics",
            "components": ["Charts", "Reports"]
        })

    api_endpoints = [
        {"path": "/api/login", "method": "POST", "entity": "users"},
        {"path": "/api/register", "method": "POST", "entity": "users"}
    ]

    for entity in design["entities"]:
        api_endpoints.append({
            "path": f"/api/{entity}",
            "method": "GET",
            "entity": entity
        })
        api_endpoints.append({
            "path": f"/api/{entity}",
            "method": "POST",
            "entity": entity
        })

    database_tables = [
        {
            "name": "users",
            "fields": {
                "id": "integer",
                "name": "string",
                "email": "string",
                "password": "string",
                "role": "string"
            }
        }
    ]

    for entity in design["entities"]:
        if entity != "users":
            database_tables.append({
                "name": entity,
                "fields": {
                    "id": "integer",
                    "user_id": "integer",
                    "name": "string",
                    "created_at": "datetime"
                }
            })

    roles = []
    for role in design["roles"]:
        if role == "admin":
            roles.append({
                "name": "admin",
                "permissions": ["read", "write", "delete", "analytics"]
            })
        else:
            roles.append({
                "name": role,
                "permissions": ["read", "write"]
            })

    return {
        "app_name": "Generated SaaS App",
        "assumptions": [
            "Default database is relational",
            "Authentication uses email and password",
            "Admin role has higher permissions"
        ],
        "pages": pages,
        "api_endpoints": api_endpoints,
        "database_tables": database_tables,
        "roles": roles,
        "business_logic": [
            "Users must login before accessing dashboard",
            "Premium features require active subscription",
            "Admins can access analytics"
        ]
    }