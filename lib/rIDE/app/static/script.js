function compile(){
    code = document.getElementById("editor-window").value
    $.getJSON('/compile', {
            code: code,
          }, function(data) {
            if(data.error){
                $("#decompiled-output").text("Error in compilation");
                $("#console-output").text(data.error_msg);
            }else{
                $("#decompiled-output").text(data.compiled);
            }
          });
}

function run(){
    bytes = document.getElementById("decompiled-output").innerText
    $.getJSON('/run', {
            bytes: bytes,
          }, function(data) {
            console.log(data)
            if(data.error){
                $("#decompiled-output").text("Error in compilation");
                $("#console-output").text(data.error_msg);
            }else{
                console.log("Doing it");
                $("#console-output").text(data.resp);

            }
          });
}