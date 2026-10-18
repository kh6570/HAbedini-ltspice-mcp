# In the name of God, the Most Gracious, the Most Merciful
"""Generated MCP contracts."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "compute_thd": {
        "title": "Compute Thd",
        "description": "Total harmonic distortion.",
        "input_schema": {
            "type": "object",
            "properties": {
                "raw_path": {"type": "string"},
                "signal": {"type": "string"},
                "fundamental_hz": {"type": "number"},
            },
            "required": ["raw_path", "signal", "fundamental_hz"],
        },
    },
    "evaluate_waveform_expression": {
        "title": "Evaluate Waveform Expression",
        "description": "Evaluate an expression built from raw signal names.",
        "input_schema": {
            "type": "object",
            "properties": {
                "raw_path": {"type": "string"},
                "expression": {"type": "string"},
                "max_points": {"type": "integer"},
            },
            "required": ["raw_path", "expression"],
        },
    },
    "export_fft_spectrum": {
        "title": "Export Fft Spectrum",
        "description": "Write an FFT magnitude CSV.",
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
    "filter_device_operating_points": {
        "title": "Filter Device Operating Points",
        "description": "Keep operating-point rows whose name contains ``device``.",
        "input_schema": {
            "type": "object",
            "properties": {"log_path": {"type": "string"}, "device": {"type": "string"}},
            "required": ["log_path", "device"],
        },
    },
    "list_measures": {
        "title": "List Measures",
        "description": "List ``.meas`` names.",
        "input_schema": {
            "type": "object",
            "properties": {"log_path": {"type": "string"}},
            "required": ["log_path"],
        },
    },
    "list_signals": {
        "title": "List Signals",
        "description": "List signals in a raw file.",
        "input_schema": {
            "type": "object",
            "properties": {"raw_path": {"type": "string"}},
            "required": ["raw_path"],
        },
    },
    "list_steps": {
        "title": "List Steps",
        "description": "List stepped runs from a raw file and, when given, the log.",
        "input_schema": {
            "type": "object",
            "properties": {"raw_path": {"type": "string"}, "log_path": {"type": "string"}},
            "required": ["raw_path"],
        },
    },
    "measure_bode_response": {
        "title": "Measure Bode Response",
        "description": "Bode magnitude and phase of output/reference.",
        "input_schema": {
            "type": "object",
            "properties": {
                "raw_path": {"type": "string"},
                "output": {"type": "string"},
                "reference": {"type": "string"},
            },
            "required": ["raw_path", "output", "reference"],
        },
    },
    "measure_efficiency": {
        "title": "Measure Efficiency",
        "description": "Average output power over average input power.",
        "input_schema": {
            "type": "object",
            "properties": {
                "raw_path": {"type": "string"},
                "v_in": {"type": "string"},
                "i_in": {"type": "string"},
                "v_out": {"type": "string"},
                "i_out": {"type": "string"},
            },
            "required": ["raw_path", "v_in", "i_in", "v_out", "i_out"],
        },
    },
    "measure_stability_margins": {
        "title": "Measure Stability Margins",
        "description": "Gain and phase margins.",
        "input_schema": {
            "type": "object",
            "properties": {
                "raw_path": {"type": "string"},
                "output": {"type": "string"},
                "reference": {"type": "string"},
            },
            "required": ["raw_path", "output", "reference"],
        },
    },
    "measure_step_response": {
        "title": "Measure Step Response",
        "description": "Step-response scalars.",
        "input_schema": {
            "type": "object",
            "properties": {"raw_path": {"type": "string"}, "signal": {"type": "string"}},
            "required": ["raw_path", "signal"],
        },
    },
    "measure_waveform": {
        "title": "Measure Waveform",
        "description": "Measure avg, rms, max, min, pp, or peak.",
        "input_schema": {
            "type": "object",
            "properties": {
                "raw_path": {"type": "string"},
                "signal": {"type": "string"},
                "method": {"type": "string"},
            },
            "required": ["raw_path", "signal", "method"],
        },
    },
    "plot_waveforms": {
        "title": "Plot Waveforms",
        "description": "Plot one or more comma-separated signals to a PNG.",
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
    "read_device_operating_points": {
        "title": "Read Device Operating Points",
        "description": "Read operating-point rows from a log.",
        "input_schema": {
            "type": "object",
            "properties": {"log_path": {"type": "string"}},
            "required": ["log_path"],
        },
    },
    "read_fourier": {
        "title": "Read Fourier",
        "description": "Read the Fourier section of a log.",
        "input_schema": {
            "type": "object",
            "properties": {"log_path": {"type": "string"}},
            "required": ["log_path"],
        },
    },
    "read_log": {
        "title": "Read Log",
        "description": "Summarize a simulation log.",
        "input_schema": {
            "type": "object",
            "properties": {"log_path": {"type": "string"}},
            "required": ["log_path"],
        },
    },
    "read_measures": {
        "title": "Read Measures",
        "description": "Read ``.meas`` results.",
        "input_schema": {
            "type": "object",
            "properties": {"log_path": {"type": "string"}},
            "required": ["log_path"],
        },
    },
    "read_noise": {
        "title": "Read Noise",
        "description": "Read noise lines from a log.",
        "input_schema": {
            "type": "object",
            "properties": {"log_path": {"type": "string"}},
            "required": ["log_path"],
        },
    },
    "read_waveform": {
        "title": "Read Waveform",
        "description": "Read one budgeted waveform.",
        "input_schema": {
            "type": "object",
            "properties": {
                "raw_path": {"type": "string"},
                "signal": {"type": "string"},
                "t_start": {"type": "number"},
                "t_end": {"type": "number"},
                "max_points": {"type": "integer"},
            },
            "required": ["raw_path", "signal"],
        },
    },
    "summarize_device_operating_points": {
        "title": "Summarize Device Operating Points",
        "description": "Count operating-point rows by unit.",
        "input_schema": {
            "type": "object",
            "properties": {"log_path": {"type": "string"}},
            "required": ["log_path"],
        },
    },
}
