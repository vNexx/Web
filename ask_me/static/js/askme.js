$('#likebutton1').click(function(){
      $.ajax({
               var pk = $(this).attr('dataid');
               type: "POST",
               url: "/like/question1/",
               data: {'id': $(this).attr('dataid'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
               dataType: "json",
               success: function(response) {
                      $('#count' + pk).html(response.user) 
                      alert(response.message);                      
                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          }); 
    })
