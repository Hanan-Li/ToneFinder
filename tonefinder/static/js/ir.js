
function addToIRProfile(name, filename){
    let g_profile = `<div class="card">
        <div class="card-body">
            <h5 class="card-title">${name}</h5>
            <p class="card-text">Download your IR Plugin below!</p>
            <a href="/ir_file/${filename} " class="card-link" download>Download!</a>
        </div>
    </div>`;
    $('#ir_profile').append(g_profile);
}

document.addEventListener("DOMContentLoaded", function(){
    fetch('/api/v1/get_ir')
    .then(response => response.json())
    .then(data => {
            console.log('Success:', data);
            if(data['ir_files'].length === 0){
                let inner = `<p class="lead text-center">No available plugin profiles.</p>`;
                $('#ir_profile').append(inner);
            }
          for(var i = 0; i < data["ir_files"].length; i++){
            addToIRProfile(data["ir_files"][i]["name"], data["ir_files"][i]["irfile"])
          }
        })

});
