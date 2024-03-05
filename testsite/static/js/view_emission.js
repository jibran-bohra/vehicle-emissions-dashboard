console.log("1111", 1111)
// Get the dropdown elements
var yearSelect = document.getElementById('yearDropdown');
var modelSelect = document.getElementById('modelDropdown');
var unitSelect = document.getElementById('unitsDropdown');

const submitBtn = document.querySelector(".submit-btn");


// Add event listeners
const selectedYear = yearSelect.addEventListener('change', handleSelection);
const selectedModel = modelSelect.addEventListener('change', handleSelection);
const selectedUnits = unitSelect.addEventListener('change', handleSelection);

// Event handler function
function handleSelection() {
  var selectedYear = yearSelect.value;
  var selectedModel = modelSelect.value;
  var selectedUnit = unitSelect.value;
    // Check if all fields are non-empty
if (selectedYear !== "0" && selectedModel !== "0" && selectedUnit !== "0") {
        // Do something with the selected values, e.g., log to console
  console.log('Selected Year:', selectedYear);
  console.log('Selected Model:', selectedModel);
  console.log('Selected Unit:', selectedUnit);
  submitBtn.removeAttribute("disabled")
}
}
