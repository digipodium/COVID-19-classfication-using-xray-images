import os
from fastai.basic_train import load_learner
from fastai.vision.image import open_image
import streamlit as st
from db import Image,Predictions
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


st.title("Covid detection using AI")

def opendb():
    engine = create_engine('sqlite:///db.sqlite3') # connect
    Session =  sessionmaker(bind=engine)
    return Session()

def save_file(file,path):
    try:
        db = opendb()
        ext = file.type.split('/')[1] # second piece
        img = Image(filename=file.name,extension=ext,filepath=path)
        db.add(img)
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.write("database error:",e)
        return False

info ={
    'covid':'''covid-19 pneumonia causes the density of the lungs to increase. This may be seen as whiteness in the lungs on radiography which, depending on the severity of the pneumonia, obscures the lung markings that are normally seen; however, this may be delayed in appearing or absent.''',
    'pneumonia':'''When interpreting the x-ray, the AI will look for white spots in the lungs (called infiltrates) that identify an infection. This exam will also help determine if you have any complications related to pneumonia such as abscesses or pleural effusions (fluid surrounding the lungs).''',
    'no finding':'the xray image does not show symptoms of pneumonia or covid-19'
}

learner = None

with st.spinner("please wait, while model loads"):
    learner = load_learner(path='covid_classifier_model',file='model.pkl')
    st.info('model loaded into memory')

choice = st.sidebar.selectbox("select option",['intro','classify image','upload new content','manage uploads'])

if choice == 'intro':
    with open('intro.md') as file:
        cols = st.beta_columns(3)
        cols[0].image('images/c.jpeg',use_column_width=True)
        cols[1].image('images/p.png',use_column_width=True)
        cols[2].image('images/n.png',use_column_width=True)
        st.markdown(f'{file.read()}')

if choice == 'upload new content':
    file = st.file_uploader("select a x-ray image of patient",type=['jpg','png'])
    if file:
        path = os.path.join('uploads',file.name)
        with open(path,'wb') as f:
            f.write(file.getbuffer())
            status = save_file(file,path)
            if status:
                st.sidebar.success("file uploaded")
                st.sidebar.image(path,use_column_width=True)
            else:
                st.sidebar.error('upload failed')

if choice == 'classify image':
    db = opendb()
    results = db.query(Image).all()
    db.close()
    img = st.sidebar.radio('select image',results)
    if img and os.path.exists(img.filepath):
        st.sidebar.info("img loaded")
        col1,col2 = st.beta_columns(2)
        col1.image(img.filepath, use_column_width=True)
        if st.sidebar.button("classifiy X-ray image") and learner:
            img = open_image(img.filepath)
            cat,tensor,probs=learner.predict(img)
            col2.success(cat)
            if str(cat) == 'Covid-19':
                col2.success(info['covid'])
            elif str(cat) == 'Pneumonia':
                col2.success(info['pneumonia'])
            elif str(cat) == 'No_findings':
                col2.success(info['no finding'])
            
        

if choice == 'manage uploads':
    db = opendb()
    # results = db.query(Image).filter(Image.uploader == 'admin') if u want to use where query
    results = db.query(Image).all()
    db.close()
    img = st.sidebar.radio('select image to remove',results)
    if img:
        st.error("img to be deleted")
        if os.path.exists(img.filepath):
            st.image(img.filepath, use_column_width=True)
        if st.sidebar.button("delete"): 
            try:
                db = opendb()
                db.query(Image).filter(Image.id == img.id).delete()
                if os.path.exists(img.filepath):
                    os.unlink(img.filepath)
                db.commit()
                db.close()
                st.info("image deleted")
            except Exception as e:
                st.error("image not deleted")
                st.error(e)
    
