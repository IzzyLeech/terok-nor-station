document.addEventListener('DOMContentLoaded', function() {
  var reasonForm = document.querySelector('#deleteForm');
  if (reasonForm) {
    reasonForm.addEventListener('submit', function(event) {
      var reasonField = document.querySelector('textarea[name="reason"]');
      if (reasonField.value.trim() === '') {
          alert('Please enter a reason for deletion');
          event.preventDefault();
      }
    });
  }
})

var acc = document.getElementsByClassName("accordion");
var i;
for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
  });
}

