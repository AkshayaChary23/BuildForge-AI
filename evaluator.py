import time
from pipeline import extract_intent, system_design, generate_schema
from validator import validate_config, repair_config
from runtime import simulate_runtime


def evaluate_prompt(prompt):
    start = time.time()
    retries = 0
    failure_types = []

    intent = extract_intent(prompt)
    design = system_design(intent)
    config = generate_schema(intent, design)

    is_valid, errors, _ = validate_config(config)

    if not is_valid:
        failure_types.extend(errors)
        config = repair_config(config)
        retries += 1

    is_valid, errors, _ = validate_config(config)

    runtime_ok, runtime_message = simulate_runtime(config)

    end = time.time()

    return {
        "prompt": prompt,
        "success": is_valid and runtime_ok,
        "retries": retries,
        "failure_types": failure_types,
        "latency_seconds": round(end - start, 4),
        "runtime_message": runtime_message
    }