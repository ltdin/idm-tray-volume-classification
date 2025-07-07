export const handleYoloLabelChange = (e, setYoloLabels) => {
  setYoloLabels(Array.from(e.target.files));
};
