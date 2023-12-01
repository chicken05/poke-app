import streamlit as st
import requests


if "yresult" not in st.session_state:
    st.session_state.yresult = []
if "nresult" not in st.session_state:
    st.session_state.nresult = []

def title():
    st.title(":red[Which Pokemons can _you_ lift?]")#new
    st.divider()#new
title()

def weight():
    st.header("First, let's figure out how much you can lift.")
    user_weight = st.number_input(label="Your Weight (lbs):", min_value=0)
    kgs = round(user_weight * 0.453592, 2)
    max_lift = round(kgs * 1.2, 2)
    if user_weight > 0:
        st.subheader(f"According to :blue[G]:red[o]:orange[o]:blue[g]:green[l]:red[e] the average person can lift 1.2 times their body weight, so you can lift up to {max_lift} kgs.")
    else:
        st.subheader("Please enter in your weight.")
    st.divider()
    return max_lift
max_lift = weight() 

def can_lift(max_lift, weight, name):
    if max_lift >= weight:
        st.balloons() #new
        st.write(f"{name} is only {weight} kgs. Very liftable :)")
        st.image("yes.gif", caption="RAAHH, you are SO strong!!", use_column_width=True)
        st.session_state.yresult.append("yes")
    else:
        st.write(f"{name} is {weight} kgs. A little too heavy...")
        st.image("sad.gif", caption=f"You can't lift {name} now. More training required.", use_column_width=True)
        st.session_state.nresult.append("no")
    
    st.subheader("How many Pokemons can you lift?:")
    chart_info = {"Can Lift": len(st.session_state.yresult), "Can't Lift": len(st.session_state.nresult)}
    st.bar_chart(chart_info)
        
    
def get_poke():
    name = ""
    result = False
    try:
        st.header("Which Pokemon are you trying to lift?")
        poke = st.text_input("Pokemon Name (or National Pokedex Number):")
        url = f"https://pokeapi.co/api/v2/pokemon/{poke.lower()}"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            name = data['name'].capitalize()
            weight = round((data['weight'])/10, 2)
            if "sprites" in data and "official-artwork" in data["sprites"]["other"]:
                image_url = data['sprites']["other"]["official-artwork"]["front_default"]
                st.markdown(f'<div style="text-align: center;"><img src="{image_url}" alt="{name}" width="250"></div>', unsafe_allow_html=True)
                if st.button(f"Let's see if you can lift {name}..."):
                    result = True
                    can_lift(max_lift, weight, name)
            else:
                st.warning("No official art :(")
        else:
            st.error("That Pokemon can't be found. Check your input again.")
    except:
        st.write("Please enter in a valid pokemon name.")
    if not result:
        st.subheader(f"So can you lift {name}?")

get_poke()




