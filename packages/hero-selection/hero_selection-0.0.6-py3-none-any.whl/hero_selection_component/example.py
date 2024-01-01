import streamlit as st
from __init__ import hero_selection_slider

# st.write("HI")

st.set_page_config(layout="wide")

heroData = [
    {
      "id": 0,
      "link": "https://static.wikia.nocookie.net/mobile-legends/images/d/d8/Moon_Blessing.png",
      "gif": "TBC",
      "heroName": "Miya",
    },
    {
      "id": 1,
      "link": "https://static.wikia.nocookie.net/mobile-legends/images/0/0e/Moon_Arrow.png",
      "gif": "TBC",
      "heroName": "Miya",
    },
    {
      "id": 2,
      "link": "https://static.wikia.nocookie.net/mobile-legends/images/7/73/Arrow_of_Eclipse.png",
      "gif": "TBC",
      "heroName": "Miya",
    },
    {
      "id": 3,
      "link": "https://static.wikia.nocookie.net/mobile-legends/images/e/ec/Hidden_Moonlight.png",
      "gif": "TBC",
      "heroName": "Miya",
    },
    {
      "id": 4,
      "link": "https://static.wikia.nocookie.net/mobile-legends/images/d/d8/Moon_Blessing.png",
      "gif": "TBC",
      "heroName": "Miya",
    },
    {
      "id": 5,
      "link": "https://static.wikia.nocookie.net/mobile-legends/images/0/0e/Moon_Arrow.png",
      "gif": "TBC",
      "heroName": "Miya",
    },
    {
      "id": 6,
      "link": "https://static.wikia.nocookie.net/mobile-legends/images/7/73/Arrow_of_Eclipse.png",
      "gif": "TBC",
      "heroName": "Miya",
    },
    {
      "id": 7,
      "link": "https://static.wikia.nocookie.net/mobile-legends/images/e/ec/Hidden_Moonlight.png",
      "gif": "TBC",
      "heroName": "Miya",
    }
]

hero_selection_slider(heroData=heroData)