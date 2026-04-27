from schemas import AppConfig


def validate_config(config):
    errors = []

    try:
        validated = AppConfig(**config)
    except Exception as e:
        return False, [str(e)], None

    table_names = [table.name for table in validated.database_tables]

    for api in validated.api_endpoints:
        if api.entity not in table_names:
            errors.append(
                f"API endpoint {api.path} refers to missing DB table: {api.entity}"
            )

    page_routes = [page.route for page in validated.pages]
    if len(page_routes) != len(set(page_routes)):
        errors.append("Duplicate page routes found")

    if errors:
        return False, errors, validated

    return True, [], validated


def repair_config(config):
    table_names = [table["name"] for table in config.get("database_tables", [])]

    for api in config.get("api_endpoints", []):
        entity = api.get("entity")

        if entity not in table_names:
            config["database_tables"].append({
                "name": entity,
                "fields": {
                    "id": "integer",
                    "name": "string",
                    "created_at": "datetime"
                }
            })
            table_names.append(entity)

    if "assumptions" not in config:
        config["assumptions"] = ["Missing assumptions added automatically"]

    if "business_logic" not in config:
        config["business_logic"] = ["Default business logic added"]

    return config