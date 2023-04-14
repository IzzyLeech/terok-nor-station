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
/*  const postForm = document.querySelector('#postForm');
  if (postForm) {
    postForm.addEventListener('submit', function(event) {
      const description = document.querySelector('#id_description');
      if (description.value.trim() === '') {
          alert('Please provide a description for the post.');
          event.preventDefault();
      }
    });
  }


/*const postForm = document.querySelector('#postForm');
if (postForm) {
  const description = document.querySelector('#id_description');
  const submitButton = document.querySelector('input[type="submit"]');

  // Disable the submit button initially
  submitButton.disabled = true;

  // Enable the submit button if the description field is not empty
  description.addEventListener('input', function(event) {
    if (description.value.trim() !== '') {
      submitButton.disabled = false;
    } else {
      submitButton.disabled = true;
    }
  });

  postForm.addEventListener('submit', function(event) {
    if (description.value.trim() === '') {
      alert('Please provide a description for the post.');
      event.preventDefault();
    }
  });
}*/