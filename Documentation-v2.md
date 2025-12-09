Copyright: Spreak https://t.me/VikendYT
<br />
Author: Sounava777 https://t.me/TrueClasher4

1. Get HTTP Toolkit Pro
2. Select Anything
3. Export CA Certificate
4. Install CA Certificate
5. Go to Proxy Settings
6. Set Proxy at 127.0.0.1:8000
7. Win + R
8. Type mmc and hit Enter
9. Go to File > Add/Remove Snap-in
10. Select Certificates and click Add
11. Choose Computer Account and click Next > Finish
12. Click OK
13. Expand Certificates (Local Computer) > Trusted Root Certification Authorities
14. Right-click Certificates and choose All Tasks > Import
15. Click Next and then click on Browse
16. Go to C:\Users\Sounava777\AppData\Local\httptoolkit\Config and select the ca.pem file
17. Click Next > Next > Finish
18. Open Craftland Studio PC
19. Login
20. In HTTP Toolkit, select View
21. Search "/MajorLogin"
22. Download RESPONSE BODY in Hex
23. Open it in any Hex Editor
24. Change the 01 to 00
25. In HTTP Toolkit, select Modify
26. Add a new rule
27. Select Match: POST requests and for url: https://client.fe.garena.com/MajorLogin
28. Click on '+' icon to add it
29. Select Then: Return a response from a file and then select the modified Hex file and then save it
30. Add another rule
31. Select Match: POST requests and for host: client.fe.garena.com
32. Click on '+' icon to add it
33. Select Then: Return a fixed response and then save it
34. Close and re-open Craftland Studio PC
