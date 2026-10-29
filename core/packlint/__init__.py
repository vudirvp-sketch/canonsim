"""The pack admission lint's implementation (the D-175 split: the
ownership stays `core/pack.py::load_pack`, the single admission gate;
these modules hold the lint bodies, one domain class each, under the
`core/pack.py::_Lint` orchestrator). No DSL, no base classes — plain
modules and functions."""
