import { createSlice } from "@reduxjs/toolkit";

const interactionSlice = createSlice({
  name: "interaction",
  initialState: {
    form: {
      hcp_name: "",
      topics: "",
      sentiment: "Neutral",
      outcomes: "",
      follow_up: "",
      date: "",
      time: ""
    }
  },
  reducers: {
    setFormData: (state, action) => {
      state.form = { ...state.form, ...action.payload };
    }
  }
});

export const { setFormData } = interactionSlice.actions;
export default interactionSlice.reducer;