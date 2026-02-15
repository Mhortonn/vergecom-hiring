# ── THE MASTER DATA GRID (DSI SYSTEMS STYLE) ──
if not df.empty:
    f_df = df.copy()
    
    # ... (your existing search/filter logic here) ...

    # 1. DEFINE ALL POTENTIAL COLUMNS
    all_requested_cols = [
        'id', 'name', 'phone', 'state', 'counties', 'radius', 
        'experience', 'exp_types', 'vehicle', 'ladder', 
        'tools', 'insurance', 'status', 'notes', 'created_at'
    ]

    # 2. CRITICAL FIX: Only keep columns that actually exist in the database
    # This prevents the KeyError crash
    existing_cols = [col for col in all_requested_cols if col in f_df.columns]

    st.write(f"**Technicians Loaded:** {len(f_df)}")
    
    # 3. RENDER THE GRID SAFELY
    edited_df = st.data_editor(
        f_df[existing_cols], # Use the filtered list of columns
        use_container_width=True,
        height=600,
        hide_index=True,
        column_config={
            "id": None, 
            "name": st.column_config.TextColumn("Name", width="medium"),
            "phone": "Contact",
            "state": "State",
            "counties": st.column_config.TextColumn("Counties Covered", width="medium"),
            "radius": st.column_config.NumberColumn("Radius", format="%d mi"),
            "experience": "Years",
            "exp_types": st.column_config.TextColumn("Skills", width="medium"),
            "vehicle": "Truck?",
            "ladder": "Ladder?",
            "tools": "Tools?",
            "insurance": "Insured?",
            "status": st.column_config.SelectboxColumn("Status", options=["NEW", "REVIEWED", "CONTACTED", "HIRED", "REJECTED"], required=True),
            "notes": st.column_config.TextColumn("Operational Notes (Edit Here)", width="large"),
            "created_at": st.column_config.DatetimeColumn("Joined", format="MM/DD/YY"),
        }
    )
