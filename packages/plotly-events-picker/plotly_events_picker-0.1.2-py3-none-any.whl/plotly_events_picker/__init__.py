from __future__ import annotations
import json
from plotly.graph_objects import Figure
import streamlit.components.v1 as components
import base64
from io import BytesIO
from pathlib import Path

import numpy as np
import streamlit as st
import streamlit.components.v1 as components

frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "plotly_events_picker", path=str(frontend_dir)
)

def plotly_events(fig: Figure):
    # spec = json.dumps(fig, cls=PlotlyJSONEncoder)
    spec = fig.to_json()
    component_value = _component_func(spec = spec, default = None)
    return component_value