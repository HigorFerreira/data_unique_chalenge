window.onload = function(evt){
    setTimeout(() => {
        document.querySelector('#output-data').addEventListener("change", function(evt){
            console.log(evt.target.value)
        });
    }, 200);
}