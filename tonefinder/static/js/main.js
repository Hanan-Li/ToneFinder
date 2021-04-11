
$('#more_info').change(function() {
    if(this.checked != true){
          $("#conditional_part").hide();

     }
  else{
        $("#conditional_part").show();
  }
});

const irform = document.getElementById('irform')
irform.addEventListener('submit', event => {
  // submit event detected
  event.preventDefault();
  let name = event.target["ir_profile_name"].value;
  let ir_file = event.target["ir_filename"].value;
  console.log(name);
  console.log(ir_file);
  let data = { name: name, ir_file: ir_file };
  fetch('/api/v1/save_ir',{
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data) // body data type must match "Content-Type" header
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      $("#hidden").text("Successfully created IR Profile! Check it at the IR Profile Page");
    })
})

document.addEventListener("DOMContentLoaded", function(){
      fetch('/api/v1/get_guitar_profile')
      .then(response => response.json())
      .then(data => {
            console.log('Success:', data);
            let inner = "";
            for(var i = 0; i < data["guitar_files"].length; i++){
                  inner += `<option value=\"${i}\">${data["guitar_files"][i]["name"]}/</option>\n`;
            }
            $('#guitar_select').append(inner);
          })

  });