from app import app
import subprocess
subprocess.call("C:\\Users\\WorkSeeNote\\Desktop\\lights\\startlocaltunnel.vbs", shell=True)
app.run(host='0.0.0.0', port=5005)
