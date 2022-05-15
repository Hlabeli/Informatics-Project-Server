/*  Project event handling */
// Edit button click
$("#edit-Project-icon").click(function(){
  //hide edit button and show save/close/select buttons
  $(this).addClass("d-none");
  $("#close-Project-icon").removeClass("d-none");
  $("#save-Project-icon").removeClass("d-none");
  $("#change-image").removeClass("d-none");
  $("#category-div").removeClass("d-none").addClass("edit-element");

  //show the file field
  $("#Project-cover").removeClass("d-none");

  //make Project fields editable
  $("#Project-title").prop('contenteditable', 'true').addClass("edit-element").focus();
  $("#Project-subtitle").prop('contenteditable', 'true').addClass("edit-element");
  $("#Project-content").prop('contenteditable', 'true').addClass("edit-element");
});


/* Project cover image form submit event */
$("#Project-image-form").submit(function(e){
  e.preventDefault();
  var data = new FormData($(this)[0]);
  // make post ajax call
  $.ajax({
      type: 'POST',
      url: update_Project_url,
      headers: {
        'X-CSRFToken': csrftoken
      },
      data: data,
      processData: false,
      contentType: false,
      cache: false,
      success: function (response) {
        $("#Project-cover-image").attr("src", response.photo);
        $('#image_modal').modal('toggle');
      },
      error: function (response) {
          // alert the error if any error occured
          var err_msg = response["responseJSON"]["error"]
          $("#alert-Project-msg").text(err_msg).removeClass("d-none");
      }
  })
});


//Save button click
$("#save-Project-icon").click(function(){
  //get the title, subtitle and content
  var title = $("#Project-title").text();
  var subtitle = $("#Project-subtitle").text();
  var content = $("#Project-content").text();
  var Project_cover = $("#Project-cover").val();

  //get the category value selected
  var category_id = $("#select-Project-category").val();
  var category = $("#select-Project-category option:selected").text()

  if(title === ""){
    $("#alert-Project-msg").text("Title field cannot be left blank").removeClass("d-none");
    return;
  }

  if(subtitle === ""){
    $("#alert-Project-msg").text("Subtitle field cannot be left blank").removeClass("d-none");
    return;
  }

  if(content === ""){
    $("#alert-Project-msg").text("Content field cannot be left blank").removeClass("d-none");
    return;
  }

  if(Project_cover === ""){
    $("#alert-Project-msg").text("Project_cover field cannot be left blank").removeClass("d-none");
    return;
  }

  //send a put request to view (backend)
  $.ajax({
    type: 'PUT',
    url: edit_Project_url,
    headers: {
      'Content-Type':'application/json',
      'X-CSRFToken': csrftoken
    },
    data: JSON.stringify({
      'title': title,
      'subtitle' : subtitle,
      'content' : content,
      'category' : category_id,
      'Project_cover': Project_cover
    }),
    success: function (response) {
      // updated elements
      let date = new Date(Date.parse(response.updated_at));
      $("#Project-updated-at").text("Last updated: " + date.toUTCString());
      $("#Project-title").text(title);
      $("#Project-subtitle").text(subtitle);
      $("#Project-content").text(content);
      $("#Project-category").text(category)


      //Hide save and close button and category select and show edit button also remove class and turn off editing
      $("#close-Project-icon").addClass("d-none");
      $("#save-Project-icon").addClass("d-none");
      $("#edit-Project-icon").removeClass("d-none");
      $("#category-div").addClass("d-none");
      $("#Project-cover").addClass("d-none");
      $("#change-image").addClass("d-none");

      $("#Project-title").prop('contenteditable', 'false').removeClass("edit-element").focus();
      $("#Project-subtitle").prop('contenteditable', 'false').removeClass("edit-element");
      $("#Project-content").prop('contenteditable', 'false').removeClass("edit-element");

    },
    error: function (response) {
        // alert the error if any error occured
        var err_msg = response["responseJSON"]["error"]
        $("#alert-Project-msg").text(err_msg).removeClass("d-none");
     }
  })


});

// Handle close button event
$("#close-Project-icon").click(function(){

  //if user clicks edit then types in something and then click close. We want to show the old text not the unsaved one
  //we need to do a GET request

  $.ajax({
    type: 'GET',
    url: edit_Project_url,
    headers: {
      'Content-Type':'application/json',
      'X-CSRFToken': csrftoken
    },
    success: function (response) {
      // updated elements
      let date = new Date(Date.parse(response.updated_at));
      $("#Project-updated-at").text("Last updated: " + date.toUTCString());
      $("#Project-title").text(response.title);
      $("#Project-subtitle").text(response.subtitle);
      $("#Project-content").text(response.content);

      //Hide save and close button and category select and show edit button also remove class and turn off editing
      $("#close-Project-icon").addClass("d-none");
      $("#save-Project-icon").addClass("d-none");
      $("#edit-Project-icon").removeClass("d-none");
      $("#category-div").addClass("d-none");
      $("#Project-cover").addClass("d-none");
      $("#change-image").addClass("d-none");

      $("#Project-title").prop('contenteditable', 'false').removeClass("edit-element").focus();
      $("#Project-subtitle").prop('contenteditable', 'false').removeClass("edit-element");
      $("#Project-content").prop('contenteditable', 'false').removeClass("edit-element");


    },
    error: function (response) {
        // alert the error if any error occured
        var err_msg = response["responseJSON"]["error"]
        $("#alert-Project-msg").text(err_msg).removeClass("d-none");
     }
  })

  return false; //to prevent button click event from firing twice

});


/* Project event ends */
