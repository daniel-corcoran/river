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
                $("#console-output").text(data.resp);

            }
          });
}
