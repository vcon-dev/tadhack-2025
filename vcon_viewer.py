import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="VCON Viewer", page_icon="📞", layout="wide")

st.title("VCON Conversation Viewer")
st.markdown("Browse and explore VCON conversation data from TADHack 2025")

@st.cache_data
def load_vcon_files():
    """Load all VCON files from the numbered directories"""
    vcon_data = []
    base_path = Path(".")
    
    # Look for numbered directories
    for day_dir in sorted(base_path.glob("[0-9]*")):
        if day_dir.is_dir():
            # Find all VCON JSON files in this directory
            for vcon_file in sorted(day_dir.glob("*.vcon.json")):
                try:
                    with open(vcon_file, 'r') as f:
                        data = json.load(f)
                        data['file_path'] = str(vcon_file)
                        data['day'] = day_dir.name
                        vcon_data.append(data)
                except Exception as e:
                    st.error(f"Error loading {vcon_file}: {e}")
    
    return vcon_data

# Load all VCON files
vcon_files = load_vcon_files()

if not vcon_files:
    st.warning("No VCON files found in the current directory")
else:
    # Sidebar for filtering
    st.sidebar.header("Filters")
    
    # Get unique days
    days = sorted(set(vcon['day'] for vcon in vcon_files))
    selected_days = st.sidebar.multiselect("Select Days", days, default=days)
    
    # Filter by selected days
    filtered_vcons = [vcon for vcon in vcon_files if vcon['day'] in selected_days]
    
    # Main content area
    st.subheader(f"Found {len(filtered_vcons)} conversations")
    
    # Create overview dataframe
    overview_data = []
    for vcon in filtered_vcons:
        created_at = datetime.fromisoformat(vcon['created_at'].replace('Z', '+00:00'))
        duration = vcon['dialog'][0]['duration'] if vcon.get('dialog') else 0
        num_parties = len(vcon.get('parties', []))
        
        overview_data.append({
            'Day': vcon['day'],
            'UUID': vcon['uuid'],
            'Created': created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'Duration (s)': duration,
            'Parties': num_parties,
            'File': os.path.basename(vcon['file_path'])
        })
    
    df = pd.DataFrame(overview_data)
    
    # Display overview table
    st.dataframe(df, use_container_width=True)
    
    # Detailed view
    st.subheader("Conversation Details")
    
    # Let user select a conversation
    conversation_options = {f"Day {vcon['day']} - {vcon['uuid'][:8]}... ({datetime.fromisoformat(vcon['created_at'].replace('Z', '+00:00')).strftime('%H:%M:%S')})": idx 
                           for idx, vcon in enumerate(filtered_vcons)}
    
    if conversation_options:
        selected_conv = st.selectbox("Select a conversation to view details", 
                                    options=list(conversation_options.keys()))
        
        if selected_conv:
            selected_idx = conversation_options[selected_conv]
            vcon = filtered_vcons[selected_idx]
            
            # Display conversation details
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Metadata")
                st.json({
                    "UUID": vcon['uuid'],
                    "Version": vcon['vcon'],
                    "Created": vcon['created_at'],
                    "Day": vcon['day']
                })
                
                st.markdown("### Parties")
                for party in vcon.get('parties', []):
                    with st.expander(f"{party.get('name', 'Unknown')} ({party.get('role', 'Unknown')})"):
                        st.json(party)
            
            with col2:
                st.markdown("### Dialog")
                if vcon.get('dialog'):
                    dialog = vcon['dialog'][0]
                    st.write(f"**Duration:** {dialog['duration']} seconds")
                    st.write(f"**Start:** {dialog['start']}")
                    st.write(f"**Parties:** {', '.join(str(p) for p in dialog['parties'])}")
                    
                    # Audio player
                    audio_file = vcon['file_path'].replace('.vcon.json', '.mp3')
                    if os.path.exists(audio_file):
                        st.audio(audio_file)
                    else:
                        st.info("Audio file not found locally")
            
            # Analysis section
            st.markdown("### Analysis")
            if vcon.get('analysis'):
                for analysis in vcon['analysis']:
                    analysis_type = analysis.get('type', 'Unknown')
                    
                    if analysis_type == 'transcript':
                        with st.expander("Transcript", expanded=True):
                            st.text(analysis.get('body', 'No transcript available'))
                    
                    elif analysis_type == 'summary':
                        with st.expander("Summary"):
                            st.write(analysis.get('body', 'No summary available'))
                    
                    elif analysis_type == 'diarized':
                        with st.expander("Diarized Conversation"):
                            diarized_text = analysis.get('body', '')
                            # Format diarized text for better readability
                            lines = diarized_text.split('\n')
                            for line in lines:
                                if line.strip():
                                    if line.startswith('Customer:'):
                                        st.markdown(f"**{line}**")
                                    elif line.startswith('Agent:'):
                                        st.markdown(f"*{line}*")
                                    else:
                                        st.write(line)
            
            # Raw JSON view
            with st.expander("Raw VCON JSON"):
                st.json(vcon)

# Add refresh button
if st.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()