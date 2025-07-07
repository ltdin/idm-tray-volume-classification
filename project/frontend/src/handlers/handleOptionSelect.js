const handleOptionSelect = (option, setActiveTab) => {
  console.log("Option selected:", option);

  if (
    option.section === 'masterprogram' &&
    option.title === 'IDM Inventory Management' &&
    option.item === 'Validation'
  ) {
    setActiveTab('tray');
  } else if (
    option.section === 'masterprogram' &&
    option.title === '5S Auto Audit' &&
    option.item === 'Validation'
  ) {
    setActiveTab('kanban');
  } else if (option.item === 'home') {
    setActiveTab('home');
  } else {
    alert(`Bạn vừa bấm vào: ${option.item}`);
  }
};

export default handleOptionSelect;
