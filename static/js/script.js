document.addEventListener('DOMContentLoaded', function() {
  const reasonForm = document.querySelector('#deleteForm');
  if (reasonForm) {
    reasonForm.addEventListener('submit', function(event) {
      const reasonField = document.querySelector('textarea[name="reason"]');
      if (reasonField.value.trim() === '') {
          alert('Please enter a reason for deletion');
          event.preventDefault();
      }
    });
  }
})

const acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    const panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
  });
}