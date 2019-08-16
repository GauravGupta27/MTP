import subprocess
import sys

def main():
	output_file_name = sys.argv[1]
	stream_dur       = sys.argv[2]
	port_num         = sys.argv[3]
	
	cmd_str = 'cvlc rtp://@:%s --sout=file/ts:%s --run-time %s --stop-time %s vlc://quit &' % (port_num, output_file_name, stream_dur, stream_dur)

	cmd_str1 = 'ffmpeg protocol_whitelist file,rtp,udp,http,https,tcp,tls -safe "0" -i rx_sdp.txt -strict -2 %s' % (output_file_name)
	cmd_str3='ffmpeg -f "concat" -safe "0" -protocol_whitelist "file,http,https,tcp,tls" -i rx_sdp -codec "copy" %s '% (output_file_name) 
	subprocess.call(cmd_str, shell=True)

if __name__ == '__main__':
	main()

