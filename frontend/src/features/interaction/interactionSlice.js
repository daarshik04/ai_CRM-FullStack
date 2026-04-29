import { createSlice } from "@reduxjs/toolkit";

const interactionSlice = createSlice({
  name: "interaction",
  initialState: {
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
},
  reducers: {
    setFormData: (state, action) => {
  Object.assign(state, action.payload);
}
  }
});

export const { setFormData } = interactionSlice.actions;
export default interactionSlice.reducer;