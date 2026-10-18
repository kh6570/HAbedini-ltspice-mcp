In the name of God, the Most Gracious, the Most Merciful

# Tool reference

Each tool is one module under `services/<group>/`. File arguments are resolved inside `--workspace-root`.

145 tools are implemented. Sections follow the first word of the tool name. Each entry is the one-line contract and the arguments you must pass.

## add

### add_component

Place a primitive component.

Required arguments: schematic_path, kind, reference.

### add_component_from_asy

Place a symbol using the file name of an .asy in the workspace.

Required arguments: schematic_path, asy_path, reference.

### add_component_symbol_drawing

Append a LINE, RECTANGLE, CIRCLE, or ARC to a symbol.

Required arguments: asy_path, kind, coords.

### add_instruction

Add a SPICE directive or a comment.

Required arguments: schematic_path, text.

### add_junction

Split a wire so a coordinate becomes a junction.

Required arguments: schematic_path, x, y.

### add_library_component

Place a library symbol by name.

Required arguments: schematic_path, symbol_name, reference.

### add_net_label

Add a net label.

Required arguments: schematic_path, x, y, name.

### add_wire

Add a wire. Exposed as add_wire by the tool module.

Required arguments: schematic_path, x1, y1, x2, y2.

### add_library_include

Add a .lib directive.

Required arguments: schematic_path, library_path.

### add_model

Add a .model directive.

Required arguments: schematic_path, model_text.

### add_hierarchical_block

Create a child sheet with In/Out pins and place it on the parent.

Required arguments: schematic_path, block_name, reference.

## apply

### apply_schematic_layout_spec

Replace a schematic with a built-in layout.

Required arguments: schematic_path.

## cancel

### cancel_run

Stop a simulation started for this source path.

Required arguments: source_path.

### cancel_batch

Mark a batch cancelled. A finished batch stays completed.

Required arguments: batch_id.

## check

### check_schematic

Report structural problems without running LTspice.

Required arguments: schematic_path.

## close

### close_remote_session

Drop a session from memory. Files on disk are left in place.

Required arguments: session_id.

### close_live_gui_session

Stop a GUI process this server launched.

Required arguments: schematic_path.

## collect

### collect_batch_results

Return the stored batch result.

Required arguments: batch_id.

## compare

### compare_schematics

Compare component values between two schematics.

Required arguments: left_path, right_path.

### compare_waveforms

Compare the means of one signal in two raw files.

Required arguments: left_path, right_path, signal.

## compute

### compute_thd

Total harmonic distortion.

Required arguments: raw_path, signal, fundamental_hz.

## create

### create_schematic

Create an empty schematic.

Required arguments: schematic_path.

### create_starter_schematic

Create a divider, RC, or buck starter schematic.

Required arguments: schematic_path.

### create_asy_symbol

Write a two-pin .asy symbol.

Required arguments: output_path.

## describe

### describe_server_capabilities

Report the LTspice engine, tool groups, and feature flags.

Required arguments: none.

### describe_edit_capability

Describe which edits the clean-room editor performs.

Required arguments: none.

### describe_schematic_edit_support

Describe schematic edit support for clients.

Required arguments: none.

### describe_schematic_layout_spec

Describe a built-in layout spec.

Required arguments: none.

### describe_mixed_signal_support

State what mixed-signal authoring LTspice can and cannot do.

Required arguments: none.

### describe_protocol_support

State that I2C and SPI scaffolds here are behavioral teaching circuits.

Required arguments: none.

### describe_live_gui_support

Describe the GUI launch support.

Required arguments: none.

### describe_reference_circuit_recipe

Describe one reference circuit.

Required arguments: recipe_id.

### describe_topology_authoring_support

Describe the topology note format.

Required arguments: none.

### describe_topology_block

Return one topology note.

Required arguments: block_id.

## download

### download_remote_artifacts

Return artifact paths recorded for a finished session.

Required arguments: session_id.

## evaluate

### evaluate_waveform_expression

Evaluate an expression built from raw signal names.

Required arguments: raw_path, expression.

## export

### export_symbol_to_asy

Write a two-pin .asy named for a placed component.

Required arguments: schematic_path, reference, output_path.

### export_fft_spectrum

Write an FFT magnitude CSV.

Required arguments: raw_path, signal.

### export_derived_raw

Write a small ASCII raw file containing one trace.

Required arguments: raw_path, signal.

### export_measures_csv

Write .meas rows to CSV.

Required arguments: log_path.

### export_touchstone_s2p

Write a one-port-style S2P using S21 = output/reference and the other terms at 0.

Required arguments: raw_path, output_signal, reference_signal.

### export_waveform_ascii

Write one signal as whitespace-separated text.

Required arguments: raw_path, signal.

### export_waveform_csv

Write selected signals to CSV.

Required arguments: raw_path, signals.

### export_waveform_spice

Write a PWL statement for one real trace.

Required arguments: raw_path, signal.

## filter

### filter_device_operating_points

Keep operating-point rows whose name contains device.

Required arguments: log_path, device.

## generate

### generate_netlist

Write a netlist with LTspice -netlist, or the clean-room renderer.

Required arguments: source_path.

## get

### get_batch_status

Return a batch manifest summary.

Required arguments: batch_id.

## import

### import_circuit_bundle

Unpack a zip of schematics into the workspace, or copy one .asc.

Required arguments: bundle_path.

## ingest

### ingest_topology_contribution

Store a validated contribution under the workspace.

Required arguments: payload.

## inspect

### inspect_schematic

Summarize a schematic.

Required arguments: schematic_path.

## list

### list_components

List placed components.

Required arguments: schematic_path.

### list_subcircuits

List .subckt blocks and hierarchical symbols.

Required arguments: source_path.

### list_includes

List .lib and .include directives.

Required arguments: source_path.

### list_plot_suggestions

Suggest voltages and currents an agent can plot.

Required arguments: schematic_path.

### list_measures

List .meas names.

Required arguments: log_path.

### list_signals

List signals in a raw file.

Required arguments: raw_path.

### list_steps

List stepped runs from a raw file and, when given, the log.

Required arguments: raw_path.

### list_workflow_instructions

List bundled workflow notes.

Required arguments: none.

### list_reference_circuit_recipes

List bundled reference circuits.

Required arguments: none.

### list_topology_blocks

List topology notes.

Required arguments: none.

## materialize

### materialize_reference_circuit

Write a built-in reference circuit.

Required arguments: recipe_id, destination_path.

### materialize_recipe

Write a recipe schematic into the workspace.

Required arguments: recipe_id, destination_path.

## measure

### measure_bode_response

Bode magnitude and phase of output/reference.

Required arguments: raw_path, output, reference.

### measure_efficiency

Average output power over average input power.

Required arguments: raw_path, v_in, i_in, v_out, i_out.

### measure_stability_margins

Gain and phase margins.

Required arguments: raw_path, output, reference.

### measure_step_response

Step-response scalars.

Required arguments: raw_path, signal.

### measure_waveform

Measure avg, rms, max, min, pp, or peak.

Required arguments: raw_path, signal, method.

## merge

### merge_waveforms

Return two traces side by side without writing a combined raw file.

Required arguments: left_path, right_path, signal.

## normalize

### normalize_component_text_rotation

Reset attribute windows to left-justified text.

Required arguments: schematic_path.

## open

### open_schematic_in_gui

Launch LTspice on a schematic without -b.

Required arguments: schematic_path.

## plot

### plot_waveforms

Plot one or more comma-separated signals to a PNG.

Required arguments: raw_path, signals.

## poll

### poll_remote_run

Return the status of a background session.

Required arguments: session_id.

### poll_live_gui_session

Report that polling a GUI session is unsupported.

Required arguments: schematic_path.

### poll_live_gui_session_events

Report that GUI events are unsupported.

Required arguments: schematic_path.

## prepare

### prepare_ac

Insert a .ac directive.

Required arguments: schematic_path.

### prepare_dc_sweep

Insert a .dc directive.

Required arguments: schematic_path, source, start, stop, step.

### prepare_four

Insert a .four directive.

Required arguments: schematic_path, frequency, traces.

### prepare_func

Insert a .func directive.

Required arguments: schematic_path, definition.

### prepare_ic

Insert a .ic directive.

Required arguments: schematic_path, assignments.

### prepare_loop_gain_analysis

Stage an AC loop-gain run using the extra-source method.

Required arguments: schematic_path.

### prepare_meas

Insert a .meas directive without replacing other measurements.

Required arguments: schematic_path, statement.

### prepare_monte_carlo

Point a component at mc() and step the run index.

Required arguments: schematic_path, reference, nominal, tolerance.

### prepare_net

Insert a .net network-parameter directive.

Required arguments: schematic_path, output, source.

### prepare_nodeset

Insert a .nodeset directive.

Required arguments: schematic_path, assignments.

### prepare_noise

Insert a .noise directive.

Required arguments: schematic_path, output, source.

### prepare_op

Insert a .op directive.

Required arguments: schematic_path.

### prepare_options

Insert a .options directive.

Required arguments: schematic_path, options.

### prepare_param

Insert a .param directive.

Required arguments: schematic_path, name, value.

### prepare_save

Insert a .save directive.

Required arguments: schematic_path, traces.

### prepare_step

Insert a .step directive.

Required arguments: schematic_path, statement.

### prepare_temperature_sweep

Insert a .step temp directive.

Required arguments: schematic_path, start, stop, step.

### prepare_transfer_function

Insert a .tf directive.

Required arguments: schematic_path, output, source.

### prepare_transient

Insert a .tran directive.

Required arguments: schematic_path, t_stop.

### prepare_worst_case

Step a component between two corner values with table().

Required arguments: schematic_path, reference, low, high.

## read

### read_component

Read one component.

Required arguments: schematic_path, reference.

### read_component_symbol

Read an .asy symbol.

Required arguments: symbol_path.

### read_net_connectivity

Return primitive pin-to-net connectivity.

Required arguments: schematic_path.

### read_subcircuit

Return one .subckt body or a hierarchical sheet.

Required arguments: source_path, name.

### read_device_operating_points

Read operating-point rows from a log.

Required arguments: log_path.

### read_fourier

Read the Fourier section of a log.

Required arguments: log_path.

### read_log

Summarize a simulation log.

Required arguments: log_path.

### read_measures

Read .meas results.

Required arguments: log_path.

### read_noise

Read noise lines from a log.

Required arguments: log_path.

### read_waveform

Read one budgeted waveform.

Required arguments: raw_path, signal.

### read_workflow_instruction

Read one bundled workflow note.

Required arguments: name.

## refresh

### refresh_schematic_in_gui

Close and reopen the schematic so the GUI reloads the file.

Required arguments: schematic_path.

## remove

### remove_component

Remove a component.

Required arguments: schematic_path, reference.

### remove_component_symbol_drawing

Remove one symbol drawing by index.

Required arguments: asy_path, index.

### remove_instruction

Remove a directive or comment containing text.

Required arguments: schematic_path, text.

### remove_junction

Explain that LTspice junctions are implicit.

Required arguments: schematic_path, x, y.

### remove_net_label

Remove a net label.

Required arguments: schematic_path, x, y.

### remove_wire

Remove a wire.

Required arguments: schematic_path, x1, y1, x2, y2.

## rename

### rename_component_reference

Rename InstName.

Required arguments: schematic_path, reference, new_reference.

## render

### render_schematic_image

Draw a simple schematic preview.

Required arguments: schematic_path.

## resolve

### resolve_model_libraries

Search the workspace and the LTspice lib tree for a model name.

Required arguments: model_name.

## run

### run_model_sweep

Run once per model name.

Required arguments: schematic_path, reference, models.

### run_monte_carlo

Prepare a Monte Carlo .step and run it.

Required arguments: schematic_path, reference, nominal, tolerance.

### run_param_sweep

Add a .step and run once. LTspice expands the steps.

Required arguments: schematic_path, statement.

### run_simulation

Run one batch simulation.

Required arguments: source_path.

### run_value_sweep

Run the schematic once per component value.

Required arguments: schematic_path, reference, values.

### run_worst_case

Prepare two corners and run them.

Required arguments: schematic_path, reference, low, high.

## save

### save_schematic_as

Copy a schematic to a new path.

Required arguments: schematic_path, destination_path.

### save_netlist_copy

Copy a netlist inside the workspace.

Required arguments: source_path, destination_path.

## scaffold

### scaffold_behavioral_subcircuit

Write a schematic whose only active device is a behavioral source.

Required arguments: output_path.

### scaffold_i2c_device

Write a behavioral sketch of an I2C open-drain pull-up, not a protocol engine.

Required arguments: output_path.

### scaffold_spi_device

Write a behavioral sketch of a SPI data latch, not a protocol engine.

Required arguments: output_path.

## search

### search_topology_blocks

Search titles and summaries.

Required arguments: query.

## send

### send_live_gui_session_command

Report that GUI commands are unsupported.

Required arguments: schematic_path, command.

## set

### set_component_parameters

Set SpiceLine attributes.

Required arguments: schematic_path, reference, spice_line.

### set_component_position

Move a component and wires that ended on its pins.

Required arguments: schematic_path, reference, x, y.

### set_component_symbol_pin

Move or add a symbol pin.

Required arguments: asy_path, pin_name, x, y, spice_order.

### set_component_symbol_text

Set one .asy attribute.

Required arguments: asy_path, attribute, value.

### set_component_value

Set a component value.

Required arguments: schematic_path, reference, value.

### set_element_model

Set a component model.

Required arguments: schematic_path, reference, model.

### set_parameter

Add or replace a .param directive.

Required arguments: schematic_path, name, value.

### set_subcircuit_component_parameters

Set SpiceLine on a component inside a schematic subcircuit file.

Required arguments: schematic_path, reference, spice_line.

### set_subcircuit_component_value

Set a value on a component inside a schematic subcircuit file.

Required arguments: schematic_path, reference, value.

## submit

### submit_batch

Run one schematic and keep a manifest of the artifacts.

Required arguments: source_path.

### submit_remote_simulation

Start a background local simulation and return a session id.

Required arguments: source_path.

## suggest

### suggest_component_placement

Suggest the next free grid point to the right of existing parts.

Required arguments: schematic_path, kind.

## summarize

### summarize_tolerance_analysis

Summarize min, max, and mean of a stepped trace.

Required arguments: raw_path, signal.

### summarize_device_operating_points

Count operating-point rows by unit.

Required arguments: log_path.

### summarize_batch

Summarize raw files sitting in a batch directory.

Required arguments: batch_dir.

## validate

### validate_topology_contribution

Check that a contribution JSON object has the required keys.

Required arguments: payload.

## write

### write_workspace_text_file

Write a text file inside the workspace.

Required arguments: relative_path, content.
