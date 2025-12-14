#!/usr/bin/env python3
"""
Intelligent Image Resizer - Streamlit Web Interface

A modern web interface for resizing images to target file sizes.
"""

import io
import tempfile
from pathlib import Path

import streamlit as st
from PIL import Image

from image_resizer.processors import SizeModeProcessor
from image_resizer.core import ImageFormat, SIZE_MODE_FORMATS


# Page configuration
st.set_page_config(
    page_title="Intelligent Image Resizer",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern dark theme with glassmorphism
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main title styling */
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Glass card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Metric cards */
    .metric-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        text-align: center;
        flex: 1;
        min-width: 120px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #888;
        margin-top: 0.25rem;
    }
    
    /* Success/Error messages */
    .success-message {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1rem;
        color: #10b981;
        text-align: center;
    }
    
    .error-message {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 1rem;
        color: #ef4444;
        text-align: center;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        border-radius: 12px;
        border: 2px dashed rgba(102, 126, 234, 0.5);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        border-radius: 8px;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    /* Feature badges */
    .feature-badge {
        display: inline-block;
        background: rgba(102, 126, 234, 0.2);
        color: #667eea;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.25rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .footer a {
        color: #667eea;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)


def format_bytes(size: int) -> str:
    """Format bytes to human-readable string"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def get_output_format(filename: str) -> str:
    """Determine output format - keep original if supported, else convert to JPEG"""
    ext = Path(filename).suffix.lower()
    fmt = ImageFormat.from_extension(ext)
    if fmt and fmt in SIZE_MODE_FORMATS:
        return ext
    return ".jpg"


def main():
    # Header
    st.markdown('<h1 class="main-title">🖼️ Intelligent Image Resizer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Resize images to your exact target file size</p>', unsafe_allow_html=True)
    
    # Feature badges
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <span class="feature-badge">🎯 Smart Compression</span>
        <span class="feature-badge">⚡ Fast Processing</span>
        <span class="feature-badge">📦 Target Size</span>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown("### Upload Image")
    uploaded_file = st.file_uploader(
        "Drag and drop or click to upload",
        type=["jpg", "jpeg", "png", "webp", "tiff", "tif"],
        help="Supported formats: JPEG, PNG, WebP, TIFF"
    )
    
    # Target size configuration
    st.markdown("### Target Size")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        target_value = st.number_input(
            "Size value",
            min_value=1,
            max_value=10000,
            value=500,
            step=50,
            label_visibility="collapsed"
        )
    
    with col2:
        unit = st.selectbox(
            "Unit",
            options=["KB", "MB"],
            index=0,
            label_visibility="collapsed"
        )
    
    # Calculate target bytes
    if unit == "KB":
        target_bytes = int(target_value * 1024)
    else:
        target_bytes = int(target_value * 1024 * 1024)
    
    st.caption(f"Target: {format_bytes(target_bytes)}")
    
    # Process button and results
    if uploaded_file is not None:
        # Show uploaded image preview
        st.markdown("### Preview")
        
        # Load image for preview
        image = Image.open(uploaded_file)
        original_size = len(uploaded_file.getvalue())
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Original Image", use_container_width=True)
        
        # Display original image info
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-card">
                <div class="metric-value">{format_bytes(original_size)}</div>
                <div class="metric-label">Original Size</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{image.width}x{image.height}</div>
                <div class="metric-label">Dimensions</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{image.format or 'Unknown'}</div>
                <div class="metric-label">Format</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Resize button
        if st.button("🚀 Resize Image", use_container_width=True):
            with st.spinner("Processing... Finding optimal quality..."):
                # Reset file position
                uploaded_file.seek(0)
                
                # Save uploaded file to temp location
                with tempfile.NamedTemporaryFile(
                    delete=False, 
                    suffix=Path(uploaded_file.name).suffix
                ) as tmp_input:
                    tmp_input.write(uploaded_file.getvalue())
                    input_path = Path(tmp_input.name)
                
                # Determine output format and path
                output_ext = get_output_format(uploaded_file.name)
                output_path = input_path.with_suffix(output_ext)
                
                # Process image
                processor = SizeModeProcessor()
                result = processor.process(input_path, output_path, target_bytes)
                
                # Store result in session state
                st.session_state.result = result
                st.session_state.output_path = output_path
                st.session_state.input_path = input_path
                st.session_state.original_size = original_size
                st.session_state.target_bytes = target_bytes
                st.session_state.original_filename = uploaded_file.name
    
    # Display results if available
    if hasattr(st.session_state, 'result') and st.session_state.result is not None:
        result = st.session_state.result
        output_path = st.session_state.output_path
        original_size = st.session_state.original_size
        target_bytes = st.session_state.target_bytes
        
        st.markdown("### Results")
        
        if result.success:
            st.markdown(f"""
            <div class="success-message">
                ✅ Successfully resized to {format_bytes(result.output_size)}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="error-message">
                ⚠️ {result.message}
            </div>
            """, unsafe_allow_html=True)
        
        # Display metrics
        if result.output_size:
            reduction = ((original_size - result.output_size) / original_size) * 100
            accuracy = 100 - abs((result.output_size - target_bytes) / target_bytes * 100)
            
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-card">
                    <div class="metric-value">{format_bytes(result.output_size)}</div>
                    <div class="metric-label">Output Size</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{reduction:.1f}%</div>
                    <div class="metric-label">Size Reduction</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{result.quality or 'N/A'}</div>
                    <div class="metric-label">Quality Level</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{accuracy:.1f}%</div>
                    <div class="metric-label">Target Accuracy</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show output image preview
            if output_path.exists():
                col1, col2 = st.columns(2)
                with col2:
                    output_image = Image.open(output_path)
                    st.image(output_image, caption="Resized Image", use_container_width=True)
                
                # Download button
                with open(output_path, 'rb') as f:
                    output_bytes = f.read()
                
                original_filename = st.session_state.get('original_filename', 'image')
                output_filename = f"resized_{Path(original_filename).stem}{output_path.suffix}"
                st.download_button(
                    label="📥 Download Resized Image",
                    data=output_bytes,
                    file_name=output_filename,
                    mime=f"image/{output_path.suffix[1:]}",
                    use_container_width=True
                )
        
        # Processing time
        if result.processing_time:
            st.caption(f"⏱️ Processed in {result.processing_time:.2f} seconds")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Built By kavindamihiran using <a href="https://streamlit.io" target="_blank">Streamlit</a></p>
        <p>
            <a href="https://github.com/kavindamihiran/Intelligent-Image-Resizer" target="_blank">
                GitHub Repository
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
