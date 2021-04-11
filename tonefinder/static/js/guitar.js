
function addToGuitarProfile(name, filename){
    let g_profile = `<div class="card">
        <div class="card-body">
            <h5 class="card-title">${name}</h5>
            <p class="card-text">Download your guitar sample below!</p>
            <a href="/guitar/${name}.wav" class="card-link">Download!</a>
        </div>
    </div>`;
    $('#guitar_profile').append(g_profile);
}

document.addEventListener("DOMContentLoaded", function(){
    fetch('/api/v1/get_guitar_profile')
    .then(response => response.json())
    .then(data => {
            console.log('Success:', data);
            if(data['guitar_files'].length === 0){
                let inner = `<p class="lead text-center">No available guitar profiles. Create one below!</p>`;
                $('#guitar_profile').append(inner);
            }
          for(var i = 0; i < data["guitar_files"].length; i++){
                addToGuitarProfile(data["guitar_files"][i]["name"], data["guitar_files"][i]["guitarfile"])
          }
        })

});

$("#add-guitar-button").on('click', function(event) {
    event.preventDefault();
    if(event.target.classList.length === 3){
        event.target.classList.remove("active");
        console.log($('#guitar-form'));
        $('#guitar-form')[0].style.visibility="hidden"; 
    }
    else{
        event.target.classList.add("active");
        $('#guitar-form')[0].style.visibility="visible"; 
    }
});
