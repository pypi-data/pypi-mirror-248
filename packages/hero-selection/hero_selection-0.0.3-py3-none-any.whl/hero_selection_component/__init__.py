import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _hero_selection_component = components.declare_component(
        "hero_selection_component",
        url="http://localhost:3001", 
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _hero_selection_component = components.declare_component("hero_selection_component", path=build_dir)

def hero_selection_slider(heroData=None, styles=None, currentSelectedIndex=None, key=None):
  
    component_value = _hero_selection_component(heroData=heroData, styles=styles, currentSelectedIndex=currentSelectedIndex, key=key, default=0)

    return component_value
