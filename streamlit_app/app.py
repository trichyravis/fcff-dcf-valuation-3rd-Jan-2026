
[12:34:59] 🐍 Python dependencies were installed from /mount/src/fcff-dcf-valuation-3rd-jan-2026/requirements.txt using uv.

Check if streamlit is installed

Streamlit is already installed

[12:35:00] 📦 Processed dependencies!




2026-01-03 12:35:24.168 `label` got an empty value. This is discouraged for accessibility reasons and may be disallowed in the future by raising an exception. Please provide a non-empty label and hide it with label_visibility if needed.

Stack (most recent call last):

  File "/usr/local/lib/python3.13/threading.py", line 1014, in _bootstrap

    self._bootstrap_inner()

  File "/usr/local/lib/python3.13/threading.py", line 1043, in _bootstrap_inner

    self.run()

  File "/usr/local/lib/python3.13/threading.py", line 994, in run

    self._target(*self._args, **self._kwargs)

  File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 378, in _run_script_thread

    self._run_script(request.rerun_data)

  File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 687, in _run_script

    ) = exec_func_with_error_handling(code_to_exec, ctx)

  File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 129, in exec_func_with_error_handling

    result = func()

  File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 671, in code_to_exec

    exec(code, module.__dict__)  # noqa: S102

  File "/mount/src/fcff-dcf-valuation-3rd-jan-2026/app.py", line 15, in <module>

    from streamlit_app.app import *

  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load

  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked

  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked

  File "<frozen importlib._bootstrap_external>", line 1027, in exec_module

  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed

  File "/mount/src/fcff-dcf-valuation-3rd-jan-2026/streamlit_app/app.py", line 99, in <module>

    page = st.radio("", options=list(pages.keys()), label_visibility="collapsed")

  File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/runtime/metrics_util.py", line 531, in wrapped_func

    result = non_optional_func(*args, **kwargs)

  File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/widgets/radio.py", line 318, in radio

    return self._radio(

  File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/widgets/radio.py", line 363, in _radio

    maybe_raise_label_warnings(label, label_visibility)

  File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/lib/policies.py", line 184, in maybe_raise_label_warnings

    _LOGGER.warning(
