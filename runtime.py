def simulate_runtime(config):
    pages = config.get("pages", [])
    api_endpoints = config.get("api_endpoints", [])
    database_tables = config.get("database_tables", [])

    if not pages:
        return False, "Runtime failed: No UI pages found"

    if not api_endpoints:
        return False, "Runtime failed: No API endpoints found"

    if not database_tables:
        return False, "Runtime failed: No database tables found"

    return True, "Runtime simulation successful: App can be generated from this config"