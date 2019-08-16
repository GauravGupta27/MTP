import subprocess
import sys

def main():
	file_name   = sys.argv[1]
	receiver_ip = sys.argv[2]
	stream_dur  = sys.argv[3]	
	port_num    = sys.argv[4]
	port_num1   = "5005"
	cmd_str = 'cvlc %s --sout "#transcode{vcodec=h264,acodec=mpga,ab=128,channels=2,samplerate=44100}:duplicate{dst=rtp{dst=%s,port=%s,mux=ts}}" --run-time %s --stop-time %s vlc://quit &' % (file_name, receiver_ip, port_num, stream_dur, stream_dur)	
	#print cmd_str
	cmd_str1 = 'ffmpeg -re -thread_queue_size 4 -i %s -strict -2 -vcodec copy -an -f rtp rtp://%s:%s -acodec copy -vn -sdp_file saved_sdp_file.txt -f rtp rtp://%s:%s' % (file_name, receiver_ip, port_num, receiver_ip, port_num1)
	subprocess.call(cmd_str, shell=True)

if __name__ == '__main__':
	main()
