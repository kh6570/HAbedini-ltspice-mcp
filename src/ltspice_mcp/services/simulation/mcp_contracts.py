# In the name of God, the Most Gracious, the Most Merciful
"""Generated MCP contracts."""

from __future__ import annotations

MCP_CONTRACTS: dict[str, dict[str, object]] = {
    "add_library_include": {
        "title": "Add Library Include",
        "description": "Add a ``.lib`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "library_path": {"type": "string"},
            },
            "required": ["schematic_path", "library_path"],
        },
    },
    "add_model": {
        "title": "Add Model",
        "description": "Add a ``.model`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "model_text": {"type": "string"}},
            "required": ["schematic_path", "model_text"],
        },
    },
    "cancel_run": {
        "title": "Cancel Run",
        "description": "Stop a simulation started for this source path.",
        "input_schema": {
            "type": "object",
            "properties": {"source_path": {"type": "string"}},
            "required": ["source_path"],
        },
    },
    "generate_netlist": {
        "title": "Generate Netlist",
        "description": "Write a netlist with LTspice ``-netlist``, or the clean-room renderer.",
        "input_schema": {
            "type": "object",
            "properties": {"source_path": {"type": "string"}, "output_path": {"type": "string"}},
            "required": ["source_path"],
        },
    },
    "list_includes": {
        "title": "List Includes",
        "description": "List ``.lib`` and ``.include`` directives.",
        "input_schema": {
            "type": "object",
            "properties": {"source_path": {"type": "string"}},
            "required": ["source_path"],
        },
    },
    "list_plot_suggestions": {
        "title": "List Plot Suggestions",
        "description": "Suggest voltages and currents an agent can plot.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "prepare_ac": {
        "title": "Prepare Ac",
        "description": "Insert a ``.ac`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "sweep": {"type": "string"},
                "points": {"type": "integer"},
                "f_start": {"type": "string"},
                "f_end": {"type": "string"},
            },
            "required": ["schematic_path"],
        },
    },
    "prepare_dc_sweep": {
        "title": "Prepare Dc Sweep",
        "description": "Insert a ``.dc`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "source": {"type": "string"},
                "start": {"type": "string"},
                "stop": {"type": "string"},
                "step": {"type": "string"},
            },
            "required": ["schematic_path", "source", "start", "stop", "step"],
        },
    },
    "prepare_four": {
        "title": "Prepare Four",
        "description": "Insert a ``.four`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "frequency": {"type": "string"},
                "traces": {"type": "string"},
            },
            "required": ["schematic_path", "frequency", "traces"],
        },
    },
    "prepare_func": {
        "title": "Prepare Func",
        "description": "Insert a ``.func`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "definition": {"type": "string"}},
            "required": ["schematic_path", "definition"],
        },
    },
    "prepare_ic": {
        "title": "Prepare Ic",
        "description": "Insert a ``.ic`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "assignments": {"type": "string"}},
            "required": ["schematic_path", "assignments"],
        },
    },
    "prepare_loop_gain_analysis": {
        "title": "Prepare Loop Gain Analysis",
        "description": "Stage an AC loop-gain run. Use the extra-source method.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "injection_source": {"type": "string"},
                "f_start": {"type": "string"},
                "f_end": {"type": "string"},
            },
            "required": ["schematic_path"],
        },
    },
    "prepare_meas": {
        "title": "Prepare Meas",
        "description": "Insert a ``.meas`` directive. Do not replace the other measurements.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "statement": {"type": "string"}},
            "required": ["schematic_path", "statement"],
        },
    },
    "prepare_monte_carlo": {
        "title": "Prepare Monte Carlo",
        "description": "Point a component at ``mc()`` and step the run index.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "reference": {"type": "string"},
                "nominal": {"type": "string"},
                "tolerance": {"type": "string"},
                "runs": {"type": "integer"},
            },
            "required": ["schematic_path", "reference", "nominal", "tolerance"],
        },
    },
    "prepare_net": {
        "title": "Prepare Net",
        "description": "Insert a ``.net`` network-parameter directive.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "output": {"type": "string"},
                "source": {"type": "string"},
                "rin": {"type": "string"},
                "rout": {"type": "string"},
            },
            "required": ["schematic_path", "output", "source"],
        },
    },
    "prepare_nodeset": {
        "title": "Prepare Nodeset",
        "description": "Insert a ``.nodeset`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "assignments": {"type": "string"}},
            "required": ["schematic_path", "assignments"],
        },
    },
    "prepare_noise": {
        "title": "Prepare Noise",
        "description": "Insert a ``.noise`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "output": {"type": "string"},
                "source": {"type": "string"},
                "sweep": {"type": "string"},
                "points": {"type": "integer"},
                "f_start": {"type": "string"},
                "f_end": {"type": "string"},
            },
            "required": ["schematic_path", "output", "source"],
        },
    },
    "prepare_op": {
        "title": "Prepare Op",
        "description": "Insert a ``.op`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}},
            "required": ["schematic_path"],
        },
    },
    "prepare_options": {
        "title": "Prepare Options",
        "description": "Insert a ``.options`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "options": {"type": "string"}},
            "required": ["schematic_path", "options"],
        },
    },
    "prepare_param": {
        "title": "Prepare Param",
        "description": "Insert a ``.param`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "name": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["schematic_path", "name", "value"],
        },
    },
    "prepare_save": {
        "title": "Prepare Save",
        "description": "Insert a ``.save`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "traces": {"type": "string"}},
            "required": ["schematic_path", "traces"],
        },
    },
    "prepare_step": {
        "title": "Prepare Step",
        "description": "Insert a ``.step`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "statement": {"type": "string"}},
            "required": ["schematic_path", "statement"],
        },
    },
    "prepare_temperature_sweep": {
        "title": "Prepare Temperature Sweep",
        "description": "Insert a ``.step temp`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "start": {"type": "string"},
                "stop": {"type": "string"},
                "step": {"type": "string"},
            },
            "required": ["schematic_path", "start", "stop", "step"],
        },
    },
    "prepare_transfer_function": {
        "title": "Prepare Transfer Function",
        "description": "Insert a ``.tf`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "output": {"type": "string"},
                "source": {"type": "string"},
            },
            "required": ["schematic_path", "output", "source"],
        },
    },
    "prepare_transient": {
        "title": "Prepare Transient",
        "description": "Insert a ``.tran`` directive.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "t_stop": {"type": "string"},
                "t_step": {"type": "string"},
                "t_start": {"type": "string"},
                "max_step": {"type": "string"},
            },
            "required": ["schematic_path", "t_stop"],
        },
    },
    "prepare_worst_case": {
        "title": "Prepare Worst Case",
        "description": "Step a component between two corner values with ``table()``.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "reference": {"type": "string"},
                "low": {"type": "string"},
                "high": {"type": "string"},
            },
            "required": ["schematic_path", "reference", "low", "high"],
        },
    },
    "resolve_model_libraries": {
        "title": "Resolve Model Libraries",
        "description": "Search the workspace and the LTspice lib tree for a model name.",
        "input_schema": {
            "type": "object",
            "properties": {"model_name": {"type": "string"}},
            "required": ["model_name"],
        },
    },
    "run_model_sweep": {
        "title": "Run Model Sweep",
        "description": "Run once per model name.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "reference": {"type": "string"},
                "models": {"type": "string"},
            },
            "required": ["schematic_path", "reference", "models"],
        },
    },
    "run_monte_carlo": {
        "title": "Run Monte Carlo",
        "description": "Prepare a Monte Carlo ``.step`` and run it.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "reference": {"type": "string"},
                "nominal": {"type": "string"},
                "tolerance": {"type": "string"},
                "runs": {"type": "integer"},
            },
            "required": ["schematic_path", "reference", "nominal", "tolerance"],
        },
    },
    "run_param_sweep": {
        "title": "Run Param Sweep",
        "description": "Add a ``.step`` and run once. LTspice expands the steps.",
        "input_schema": {
            "type": "object",
            "properties": {"schematic_path": {"type": "string"}, "statement": {"type": "string"}},
            "required": ["schematic_path", "statement"],
        },
    },
    "run_simulation": {
        "title": "Run Simulation",
        "description": "Run one batch simulation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "source_path": {"type": "string"},
                "ascii_raw": {"type": "boolean"},
                "timeout_s": {"type": "number"},
                "extra_switches": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["source_path"],
        },
    },
    "run_value_sweep": {
        "title": "Run Value Sweep",
        "description": "Run the schematic once per component value.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "reference": {"type": "string"},
                "values": {"type": "string"},
            },
            "required": ["schematic_path", "reference", "values"],
        },
    },
    "run_worst_case": {
        "title": "Run Worst Case",
        "description": "Prepare two corners and run them.",
        "input_schema": {
            "type": "object",
            "properties": {
                "schematic_path": {"type": "string"},
                "reference": {"type": "string"},
                "low": {"type": "string"},
                "high": {"type": "string"},
            },
            "required": ["schematic_path", "reference", "low", "high"],
        },
    },
    "save_netlist_copy": {
        "title": "Save Netlist Copy",
        "description": "Copy a netlist inside the workspace.",
        "input_schema": {
            "type": "object",
            "properties": {
                "source_path": {"type": "string"},
                "destination_path": {"type": "string"},
            },
            "required": ["source_path", "destination_path"],
        },
    },
    "summarize_tolerance_analysis": {
        "title": "Summarize Tolerance Analysis",
        "description": "Summarize min, max, and mean of a stepped trace.",
        "input_schema": {
            "type": "object",
            "properties": {"raw_path": {"type": "string"}, "signal": {"type": "string"}},
            "required": ["raw_path", "signal"],
        },
    },
}
