import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "my_component",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("my_component", path=build_dir)

def dmg_chart(chartData=None, index_=None, styles=None, key=None):
  
    component_value = _component_func(chartData=chartData, index_=index_, styles=styles, key=key, default=0)

    return component_value


