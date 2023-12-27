import streamlit as st
from __init__ import dmg_chart

# st.write("HI")

chartData = [
    {
      "index": 0,
      "title": "All Damage",
      "skills": [
        {
          "id": 1,
          "link": "https://static.wikia.nocookie.net/mobile-legends/images/0/0e/Moon_Arrow.png",
          "name": "Moon Arrow",
          "value":100,
          "indicator": "26%",
        },
        {
          "id": 2,
          "link": "https://static.wikia.nocookie.net/mobile-legends/images/7/73/Arrow_of_Eclipse.png",
          "name": "Arrow of Eclipse",
          "value":100,
          "indicator": "56%",
        },
        {
          "id": 3,
          "link": "https://static.wikia.nocookie.net/mobile-legends/images/e/ec/Hidden_Moonlight.png",
          "name": "Hidden Moonlight",
          "value":100,
          "indicator": "30%",
        },
      ],
    },
    { "index": 1, "title": "Base Damage" },
    { "index": 2, "title": "Additive Damage" },
    { "index": 3, "title": "Passive Damage" },
  ]

index_ = [
    { "index": 0, "title": "skill 1" },
    { "index": 1, "title": "skill 2" },
    { "index": 2, "title": "skill 3" },
  ]

st.set_page_config(
    layout="wide"
)

dmg_chart(chartData=chartData, index_=index_)