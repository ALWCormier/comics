$('.issue-select').on('submit', function(event) {
  event.preventDefault();
  $.ajax({
    url: '/create_record',
    type: 'POST',
    data: $(this).serialize(),
    success: function(data) {
        var element = document.getElementById(data['id']);
        element.setAttribute("hidden", "");
    }
  });
});