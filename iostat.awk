##################################
### script give the average tps for an iostat output file.
### iostat 5 20 > iostat.out
### usage: awk -f iostat.awk iostat.out

BEGIN { printf("%10s ;%10s","Dev","tps")
	}
	( NF==6 && !/isk/ && !/cd0/ && !/^[ ]/ ) {
	TPS+=$2
	COUNT++
	printf("\n%10s ;%10f ", $1, $2) }

	/hdisk/{ printf("%10f ;",$2) }

END { printf("\n\nAverage tansactions per-seconds(tps) = %5.2f\n", TPS/COUNT) } 
