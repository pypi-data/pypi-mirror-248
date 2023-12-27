import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component("streamlit_input_box",url="http://localhost:3001")
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_input_box", path=build_dir)

def input_box(min_lines=1, max_lines=5,just_once=False,on_submit=None,args=(),kwargs={},key=None):
    if not '_last_input_box_id' in st.session_state:
        st.session_state._last_input_box_id=0
    output = _component_func(min_lines=min_lines,max_lines=max_lines,key=key,default=None)
    if not output:
        return None
    else:
        id=output['id']
        text=output['text']
        if not id==st.session_state._last_input_box_id or just_once==False:
            if not id==st.session_state._last_input_box_id and on_submit:
                on_submit(*args,**kwargs)
            st.session_state._last_input_box_id=id
            return text
        else:
            return None

if not _RELEASE:
    import streamlit as st

    state=st.session_state

    if 'texts' not in state:
        state.texts=[]

    def on_submit():
        st.write("success!")

    text=input_box(min_lines=3,max_lines=10,just_once=True,on_submit=on_submit,key='inputbox')
      
    if text:
        state.texts.append(text)

    for text in state.texts:
        st.text(text)

