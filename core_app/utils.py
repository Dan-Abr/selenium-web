def e2e_test_action_form_to_dict(form):
    # Python supports match-case from v3.1, however
    # Microsoft VSCode isn't supporting its syntax yet.
    # Source: https://github.com/microsoft/vscode-python/issues/17745
    if(form.event_type == 1):
        # return the waiting time
        return {form.event_type: form.wait_time_in_sec}
    elif(form.event_type == 2):
        # return the CSS selector
        return {form.event_type: form.css_selector_click}