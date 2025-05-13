#!/usr/bin/env bash

SAMPLE=$(echo $1 | cut -d'.' -f1)


samtools depth -a $SAMPLE.sort.bam > $SAMPLE.LRvsMTBanc.coverage


#Assessment of basic stats

POSITION0=$(grep -c -w '0' $SAMPLE.LRvsMTBanc.coverage)

GENOME=4411532.0

COVER_POS=$(echo $GENOME-$POSITION0 | bc)

COVERAGE=$(echo "scale=2; $COVER_POS*100.0/$GENOME" | bc -l)

MEAN=$(awk '{ sum += $3; n++ } END { if (n > 0) print sum / n; }' $SAMPLE.LRvsMTBanc.coverage)

MEDIAN=$(cut -f3 $SAMPLE.LRvsMTBanc.coverage | sort -n | awk ' { a[i++]=$1; } END { print a[int(i/2)]; }')

rm $SAMPLE.LRvsMTBanc.coverage

echo $SAMPLE,$COVERAGE,$MEAN,$MEDIAN > $SAMPLE.LRvsMTBanc.stats
