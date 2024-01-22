function compile(){
    code = document.getElementById("editor-window").value
    $.getJSON('/compile', {
            code: code,
          }, function(data) {
            if(data.error){
                $("#decompiled-output").text("Error in compilation");
                $("#console-output").html(data.error_msg);
                $("#compiler-debug").html(data.debug);


            }else{
                $("#decompiled-output").text(data.compiled);
                $("#compiler-debug").html(data.debug);
            }
          });
}

function run(){
    bytes = document.getElementById("decompiled-output").value
    $.getJSON('/run', {
            bytes: bytes,
          }, function(data) {
            console.log(data)
            if(data.error){
                $("#decompiled-output").text("Error in compilation");
                $("#console-output").html(data.error_msg);
            }else{
                console.log("Doing it");

                $("#console-output").html(data.resp.replace("\n", "<br>").replace("app/", ""));

                // Wait for images to load before scrolling
                $("#console-output").find('img').on('load', function() {
                    // Check if all images have loaded
                    // Check if all images have loaded
                    var allImagesLoaded = $("#console-output").find('img').get().every(function(img) {
                        return img.complete && img.naturalHeight !== 0;
                    });

                    // If all images are loaded, scroll to the bottom
                    if (allImagesLoaded) {
                        $("#console").scrollTop($("#console")[0].scrollHeight);
                    }
                });


            }}
        )};

