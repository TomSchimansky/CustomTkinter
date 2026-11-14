# Tests

The tests use pytest and need Pillow for screenshots and CTkImage:

```
pip install pytest pillow
```

Run all unit and integration tests from the repository root:

```
python -m pytest
```

On Linux without a desktop (for example in CI or over SSH), run them in a virtual X server:

```
xvfb-run -a python -m pytest
```

The tests open real windows. Don't move the mouse over them while they run, some tests check hover colors.

## Folders

- `unit_tests/`: options, methods and events of every widget, windows and dialogs, fonts, images, themes, appearance mode, scaling and the drawing engine.
- `integration_tests/`: screenshots of the rendered widgets for every drawing method, mouse and keyboard interaction, runtime changes of appearance mode, scaling and window size, the Linux HiDPI scaling in a separate X server (needs `Xvfb` and `xrdb`), and starts all examples and manual test scripts.
- `manual_integration_tests/`: scripts to look at and try out by hand.

Screenshots are not possible on macOS without the screen recording permission for the terminal, those tests are skipped then.

Run only some tests with `-k`, for example `python -m pytest -k "slider or scaling"`.
