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
  } else if (option.section === 'masterprogram' &&
    option.title === 'IDM Inventory Management' &&
    option.item === 'Fine Tune Model') {
    setActiveTab('fine-tune');
  } else {
    alert(`You are clicking to: ${option.item}`);
  }
};

export default handleOptionSelect;
