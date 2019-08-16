#!/bin/bash
python plt_tcp_rtt.py 0
python plt_tcp_rtt.py 1

for i in {0..3}
do
	echo $i
	python plt_udp_delay.py $i
	python plt_udp_loss.py $i
	python plt_vid_psnr.py $i
	python plt_vid_jain.py $i
	python plt_all_tput.py $i
	python plt_vid_shjain.py $i
done

scp *.pdf xavier666@10.5.20.114:~/Documents/git_stuff/2016-sdn-sumitro/ICNP_2017/plots/
mv *.pdf ../stats/plots/
