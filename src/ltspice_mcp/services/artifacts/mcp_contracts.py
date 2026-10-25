# In the name of God, the Most Gracious, the Most Merciful
"""Generated MCP contracts."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "compare_waveforms": {
        "title": "Compare Waveforms",
        "description": "Compare the means of one signal in two raw files.",
        "input_schema": {
            "type": "object",
            "properties": {
                "left_path": {"type": "string"},
                "right_path": {"type": "string"},
                "signal": {"type": "string"},
            },
            "required": ["left_path", "right_path", "signal"],
        },
    },
    "export_derived_raw": {
        "title": "Export Derived Raw",
        "description": "Write a small ASCII raw file that contains one trace.",
        "input_schema": {
            "type": "object",
            "properties": {
                "raw_path": {"type": "string"},
                "signal": {"type": "string"},
                "output_path": {"type": "string"},
            },
            "required": ["raw_path", "signal"],
        },
    },
    "export_measures_csv": {
        "title": "Export Measures Csv",
        "description": "Write ``.meas`` rows to CSV.",
        "input_schema": {
            "type": "object",
            "properties": {"log_path": {"type": "string"}, "output_path": {"type": "string"}},
            "required": ["log_path"],
        },
    },
    "export_touchstone_s2p": {
        "title": "Export Touchstone S2p",
        "description": "Write a one-port-style S2P. Set S21 equal to output/reference. Set the other terms to 0.",
        "input_schema": {
            "type": "object",
            "properties": {
                "raw_path": {"type": "string"},
                "output_signal": {"type": "string"},
                "reference_signal": {"type": "string"},
                "output_path": {"type": "string"},
                "z0": {"type": "number"},
            },
            "required": ["raw_path", "output_signal", "reference_signal"],
        },
    },
    "export_waveform_ascii": {
        "title": "Export Waveform Ascii",
        "description": "Write one signal as whitespace-separated text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "raw_path": {"type": "string"},
                "signal": {"type": "string"},
                "output_path": {"type": "string"},
            },
            "required": ["raw_path", "signal"],
        },
    },
    "export_waveform_csv": {
        "title": "Export Waveform Csv",
        "description": "Write selected signals to CSV.",
        "input_schema": {
            "type": "object",
            "properties": {
                "raw_path": {"type": "string"},
                "signals": {"type": "string"},
                "output_path": {"type": "string"},
            },
            "required": ["raw_path", "signals"],
        },
    },
    "export_waveform_spice": {
        "title": "Export Waveform Spice",
        "description": "Write a PWL statement for one real trace.",
        "input_schema": {
            "type": "object",
            "properties": {
                "raw_path": {"type": "string"},
                "signal": {"type": "string"},
                "output_path": {"type": "string"},
            },
            "required": ["raw_path", "signal"],
        },
    },
    "merge_waveforms": {
        "title": "Merge Waveforms",
        "description": "Return two traces side by side. Do not write a combined raw file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "left_path": {"type": "string"},
                "right_path": {"type": "string"},
                "signal": {"type": "string"},
            },
            "required": ["left_path", "right_path", "signal"],
        },
    },
    "summarize_batch": {
        "title": "Summarize Batch",
        "description": "Summarize the raw files in a batch directory.",
        "input_schema": {
            "type": "object",
            "properties": {"batch_dir": {"type": "string"}},
            "required": ["batch_dir"],
        },
    },
}
