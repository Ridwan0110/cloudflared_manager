# **Cloudflared Manager**



This script is designed to work with Linux distros to tunnel a network using Cloudflared and manage it all from a simple Python script. This script is for those who does not own a domain and still want to use Cloudflared but somehow manage using the random **trycloudflare.com** domain given by Cloudflare. 



This script manages:



* Which Cloudflared version is compatible with your Linux architecture.
* Downloads the correct version of Cloudflared automatically.
* Start a tunnel using the server URL from the config.json.
* Grabs the temporary domain given by Cloudflare and save it in memory.
* Sends that domain to a remote server to keep track of the current temporary domain.



### Description:



If your network is behind CGNAT/not-a-public-ip-address but you still want to host something from your computer and access it using the internet from anywhere in the world, your options are to use network tunneling as it is the best. ZeroTier covers it pretty well and I love it but you need everyone to be on a virtual network to access your hosted things from the outside world. This is where Cloudflared and NGROK comes in as it does not need the end user to be in a virtual network or use any kind of app to access your hosted thing. They give you a domain which is accessible publicly. I prefer Cloudflared over NGROK for a number of reasons. But one drawback with Cloudflared is you need to own a domain to have a static public domain which NGROK gives to you free (a subdomain). Cloudflared does give free subdomains but it is not static. This is why I made this script. This script is made to work with Linux but you can use it in any operating system as long as you have Python on it and the correct version of Cloudflared on it.



This script grabs the temporary subdomain given by Cloudflare to you during setting up a tunnel and sends that URL to a server. You can even use your own Discord webhook if you don't have any server or VPS.

