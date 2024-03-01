$('.remove-item').on('click', function() {
    const issue_id = $(this).data('id');
    console.log(issue_id);
    var element = document.getElementById('delete');
    element.setAttribute('value', issue_id);
});

$('#delete_form').on('submit', function(event) {
  event.preventDefault();
  $.ajax({
    url: '/remove_record',
    type: 'POST',
    data: $(this).serialize(),
    success: function(data) {
        var element = document.getElementById(data['id']);
        element.setAttribute("hidden", "");
    }
  });
});