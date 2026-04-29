import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  hcp_name: "",
  interaction_type: "Meeting",
  date: "",
  time: "",
  topics: "",
  materials: "",
  samples: "",
  sentiment: "",
  outcomes: "",
  follow_up: ""
};

const interactionSlice = createSlice({
  name: "interaction",
  initialState,
  reducers: {
    setFormData: (state, action) => {
      Object.assign(state, action.payload); // ✅ IMPORTANT FIX
    },
    resetForm: () => initialState
  }
});

export const { setFormData, resetForm } = interactionSlice.actions;
export default interactionSlice.reducer;