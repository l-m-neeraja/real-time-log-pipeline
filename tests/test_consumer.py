def should_process_log(log_event, allowed_levels):
    return log_event.get("level") in allowed_levels


def test_valid_error_log():
    log = {"level": "ERROR"}
    assert should_process_log(log, ["ERROR", "WARN"]) is True


def test_valid_warn_log():
    log = {"level": "WARN"}
    assert should_process_log(log, ["ERROR", "WARN"]) is True


def test_info_log_filtered_out():
    log = {"level": "INFO"}
    assert should_process_log(log, ["ERROR", "WARN"]) is False


def test_missing_level_field():
    log = {"service_name": "auth-service"}
    assert should_process_log(log, ["ERROR", "WARN"]) is False
