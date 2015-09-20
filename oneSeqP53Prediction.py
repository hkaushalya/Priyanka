#!/usr/bin/env python
__author__ = 'shewamanage'

# this program is for making tata wt matrix
# For Web version Saran's Changes

DIR = "/home/priyankara/TT/Input"
HOME = "/home/priyankara/TT"
LOG = "/home/priyankara/TT/Log"
HTML = "/home/priyankara/TT/html"



##############################################################################

# code added by saran for Web version
#?????

read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});

############################################################
# Reading the input from the form and putting it in a file
############################################################
$buffer =~ s/\-+\d+//g;
$buffer =~ s/\n//g;
#$buffer =~ s/\d+//g;
$buffer =~ s/\-+//g;
$buffer =~ s/^Content.*//g;
$buffer =~ s/^Predict.*//g;
$buffer =~ s/\r/\t/g;

	&get_date_time;
	$ext = "log";
    $filename = "$datetimenow"."."."$ext";
	$inter1 = "human.INTER1.$filename";
	$inter2= "mouse.INTER2.$filename";
	$final = "final.$filename"."."."txt";

	chdir($LOG);
	open(FILE,">$filename");
	print FILE $buffer;
	close(FILE);
	open(BUFFER, "$filename") || "File cannot be opened";
	$h = "";
	$m = "";
	while ($buffer1 = <BUFFER>) {
		$buffer1 =~ s/\s+/\t/g;
#		if($buffer1 =~ /name\=\"human\"\s+(\>.*)\s+ContentDisposition.*\s+name\=\"mouse\"\s+(\>.*)\s+ContentDisposition.*/) {
		($h) = $buffer1 =~ /name=\"human\"\s+(\>.*)\s+ContentDisposition/;
		($m) = $buffer1 =~ /name=\"mouse\"\s+(\>.*)\s+ContentDisposition/;
		 if($h =~ /(\>\S+)\s+(.*)/) {
			$header1 = $1;
			$hSeq = $2;
			$hSeq =~ s/\s+//g;
			open (INTER1,">$inter1");
			print INTER1 "$header1\t$hSeq\n";
			close(INTER1);
		  }
		  if($m =~ /(\>\S+)\s+(.*)/) {
			 $header2 = $1;
			 $mSeq = $2;
			 $mSeq =~ s/\s+//g;
		  	 open (INTER2,">$inter2");
			 print INTER2 "$header2\t$mSeq\n";
			 close(INTER2);
		  }
	 }
	chdir($HOME);

###################### End of reading the Input ###############################
$head1 = "";
$head2 = "";
if($header1 =~/\>(\S+)/) {
	$head1 = $1;
}
if($header2 =~/\>(\S+)/) {
	$head2 = $1;
}

print $header1."\n";

################################################################################
#       executing the prediction program
################################################################################

if ( $head1 ne "" )
{
	`perl p53PredictWeb.pl $LOG/$inter1 $LOG/$head1`;
}

if ( $head2 ne "" )
{
	`perl p53PredictWeb.pl $LOG/$inter2 $LOG/$head2`;
}

if ( $head1 ne ""  && $head2 ne "" )
{
	`perl p53Filter.pl $LOG/$head1 $LOG/$head2 > $HTML/$final`;
}
elsif ( $head1 ne "" )
{
	`cp $LOG/$head1 $HTML/$final`;
}
elsif ( $head2 ne "" )
{
	`cp $LOG/$head2 $HTML/$final`;
}


###################### end of execution phase ##################################

##################################################################################
# Sending output back to the webpage
# *****************************************************************************

########### Printing the header of the page ######################################
open(FILE,"html/header.html") || "File cannot be opened";
while(<FILE>) {
	$head .= $_ ;
}

$OUT = "OUT.$filename.html";
open(OUT, "> html/$OUT") || "File cannnot be opened";
print OUT "$head";

########### End of Printing the header of the page ####################################

########### Printing the formatted predictions on the page ############################

open(RES, "html/$final") || "File cannot be opened";



	print OUT "
	<div align=center>
	<table border = 1 align = center>
	<tr>
     <td>Species</td>
";
	if ( $head1 ne "" && $head2 ne "" )
	{
	  print OUT "
	  <td>Count</td>
	  ";
	}
	print OUT "
	  <td>MotifBegin</td>
	  <td>MotifEnd</td>
	  <td>Motif</td>
	  <td>Score</td>
	  <td>Difference</td>
	  <td>Motif</td>
	  <td>Score</td>
	  <td>Confidence</td>
	  <td>Mismatches</td>
	  </tr>
	 ";

while($IN = <RES>) {
#	$data .= $_ ;
	if($IN =~ /(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)/)
	{
		$id = $1;
		$count = $2;
		$motifSt = $3;
		$motifEnd = $4;
		$motif = $5;
		$score1 = $6;
		$diff =$7;
		$motif2 = $8;
		$score2 = $9;
		$confidence = $10;
		$mismatches = $11;
	}
	elsif($IN =~ /(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)/)
	{
		if ( $head1 ne "" )
		{
			$id = $head1;
		}
		elsif ( $head2 ne "" )
		{
			 $id = $head2;
		}
		$motifSt = $1;
		$motifEnd = $2;
		$motif = $3;
		$score1 = $4;
		$diff =$5;
		$motif2 = $6;
		$score2 = $7;
		$confidence = $8;
		$mismatches = $9;
	}

		 print OUT "
		  <tr>
		  <td>$id</td>";
		if ( $head1 ne "" && $head2 ne "" )
		{
			print OUT "<td>$count</td>
";
		}
		print OUT "
		  <td>$motifSt</td>
		  <td>$motifEnd</td>
		  <td>$motif</td>
		  <td>$score1</td>
		  <td>$diff</td>
		  <td>$motif2</td>
		  <td>$score2</td>
		  <td>$confidence</td>
		  <td>$mismatches</td>
		  </tr>
		 ";
}
		print OUT "
			</table>
			</div>
			";
############ End of Formatted Predictions on the page ##################################

########## Printing footer of the page #################################################

open(AND, "html/footer.html") || "File cannot be opened";
while(<AND>) {
	$tail .= $_ ;
}

print OUT "$tail";
close(OUT);

############# End of Printing the footer of the page #####################################


##################### Printing the entire content on the web browser #####################

open(HTML,"html/$OUT") || " File cannot be opened";
print "Content-type: text/html\n\n";
while(<HTML>) {
	print;
}
close(HTML);

################## End of printing on the web browser ####################################


##########################################################################################

##########################################################################################


###################################### subroutine for date and time#####################################

sub get_date_time {

        # Get the all the values for current time
        ($Second, $Minute, $Hour, $Day, $Month, $Year, $WeekDay, $DayOfYear, $IsDST) = localtime(time);


        $RealMonth = $Month + 1; # Months of the year are not zero-based

        if($RealMonth < 10)
        {
           $RealMonth = "0" . $RealMonth; # add a leading zero to one-digit months
        }

        if($Day < 10)
        {
           $Day = "0" . $Day; # add a leading zero to one-digit days
        }

        $Fixed_Year = $Year + 1900;

        if($Minute<10)
        {
                $Minute = "0".$Minute;
        }

        if($Hour<10)
        {
                $Hour = "0".$Hour;
        }

	$datetimenow = "$Fixed_Year$RealMonth$Day"."_"."$Hour$Minute";
}

################################ end of subroutine for date #########################################
