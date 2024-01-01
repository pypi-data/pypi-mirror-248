import os
import streamlit as st
import streamlit.components.v1 as components
from hero_selection_component.streamlit_callback import register 

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

def hero_selection_slider(heroData=None, styles=None, currentSelectedIndex=None, key=None, on_change=None, args=None, kwargs=None, default=None):

    if on_change is not None:
        if key is None:
            st.error("You must pass a key if you want to use the on_change callback for the option menu")
        else:
            register(key=key, callback=on_change, args=args, kwargs=kwargs)
  
    component_value = _hero_selection_component(heroData=heroData, styles=styles, currentSelectedIndex=currentSelectedIndex, key=key, default=default)

    return component_value
