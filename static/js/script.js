const reasonForm = document.querySelector('form');
    reasonForm.addEventListener('submit', function(event) {
        const reasonField = document.querySelector('textarea[name="reason"]');
        if (reasonField.value.trim() === '') {
            alert('Please enter a reason for deletion');
            event.preventDefault();
        }
    });

const postForm = document.querySelector('#postForm');
postForm.addEventListener('submit', function(event) {
    const description = document.querySelector('#id_description');
    if (description.value.trim() === '') {
        alert('Please provide a description for the post.');
        event.preventDefault();
    }
});