'''Root of the hiking journal'''


#@fapp.route ('/')
def _root() -> bytes:
    return b'''
<!DOCTYPE html>
<html>
  <head>
    <script> 
      function frontEndShutdown()
      {
        document.getElementById("stop_server").submit();
        window.close();
      } 
    </script>
    <title>Hiking Journal</title>
  </head>
  <body>
    <form action="/pages/cover" style="float:left ; margin-right:10px" target="workspace"><input type="submit" value="Home"/></form>
    <form action="/import" style="float:left ; margin-right:10px" target="workspace"><input type="submit" value="Import"/></form>
    <form action="/scribe" style="float:left ; margin-right:10px" target="workspace"><input type="submit" value="Scribe Entry"/></form>
    <form action="/setup" style="float:left ; margin-right:10px" target="workspace"><input type="submit" value="Settup"/></form>
    <input style="float:left" type="button" value="Quit" onclick="frontEndShutdown();"/>
    <form id="stop_server" action="/stop"><input type="hidden" value="Stop"/></form>
    <iframe id="workspace"
            name="workspace"
            src="/pages/cover"
            style="border:medium solid black; height:95vh; width:90%;"/>
  </body>
</html>
'''

