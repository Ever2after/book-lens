import streamlit as st 
from ai import *

st.set_page_config(
    page_title="북렌즈",
    page_icon="📋",
)

st.title('북렌즈')

if 'filename' not in st.session_state:
    st.session_state['filename'] = ''

img_file_buffer = st.camera_input("책을 촬영해주세요!")

if img_file_buffer is not None:
    result = {}
    with st.spinner('waiting...'):
        # To read image file buffer as bytes:
        bytes_data = img_file_buffer.getvalue()
        # Check the type of bytes_data:
        data = base64.b64encode(bytes_data).decode('utf-8')
        
        text, _ = directocr(data)
    
        # chatgpt logic
        keyword = 'aws' # getKeywords(text)
        
        col3, col4 = st.columns(2)
        with col3:
            st.write('OCR 결과: ')
            st.write(text)
        with col4:
            st.write('교정 결과: ')
            st.write(keyword)
        
        result = bookSearch(keyword)
    if result['total']:
        st.balloons()
        book = result['items'][0]
        st.subheader('검색 결과:')
    
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(book['image'], caption='Sunrise by the mountains')
            st.write(f"저자: {book['author'].replace('^', ', ')}")
            st.write(f"출판사: {book['publisher']}")
            st.write(book['link'])
        with col2:
            st.subheader(book['title'])
            st.write(book['description'])
    else:
        st.write('검색된 책이 없습니다!')
    

