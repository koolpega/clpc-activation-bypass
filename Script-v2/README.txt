1. Install Python (Check the box saying "Add Python.exe to PATH")
2. Install MITM Proxy
3. Go to Windows Proxy Settings and enable proxy at 127.0.0.1:8080
4. Open Terminal and type: "mitmdump" and hit Enter
5. Open your browser and go to http://mitm.it
6. Download the certificate for Windows
7. Open the certificate and select Store Location: Local Machine and click on Next
8. Click Next again, then leave Password blank and click Next again
9. Select "Place all certificates in the following store" and click on Browse
10. Select "Trusted Root Certification Authorities" and click OK
11. Click Next and Finish
12. Close all previously open Terminals and open a new Terminal
13. Type "python app.py" and hit Enter