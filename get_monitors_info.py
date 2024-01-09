"""
Returns the model name and input source for each detected monitor.
"""

from monitorcontrol import get_monitors


def main():
    for idx, monitor in enumerate(get_monitors()):
        with monitor:
            print(f"Monitor {idx + 1}:")
            name = monitor.get_vcp_capabilities()["model"]
            print(f" - model: {name}")
            print(f" - input source: {monitor.get_input_source().name}")


if __name__ == "__main__":
    main()
