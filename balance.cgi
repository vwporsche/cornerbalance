#!/var/www/vhosts/rennlight.com/bin/perl
# calculate corner balances
# 07/20/2002 Thom Fitzpatrick & Sherwood Lee

use strict 'refs';
use strict;
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser/;
my $LOG="/var/www/vhosts/rennlight.com/www/cgi-bin/log/balance.log";

my $TF;
my $TR;
my $TW;
my $LW;
my $RW;
my $LSPCT;
my $RSPCT;
my $FPCT;
my $RPCT;
my $DWLFRR;
my $DWRFLR;
my $ILF;
my $IRF;
my $ILR;
my $IRR;
my $LF;
my $RF;
my $LR;
my $RR;
my $weight;
my $dist;
my $name;
my $notes;
my $car;

print header();
print "<head>\n";
print "<link rel=stylesheet href=http://www.rennlight.com/rennlight.css TYPE=text/css>\n";
print title("Corner Balance Calculator");
print "<body>\n";
print "<center>\n";
print h4("Corner Balance Calculator");

# slurp values from form
$LF=param('LF'); 
$RF=param('RF'); 
$LR=param('LR'); 
$RR=param('RR'); 
$weight=param('weight'); 
$dist=param('dist'); 
$name=param('name'); 
$car=param('car'); 
$notes=param('notes'); 

if (param('multiply')) {
	$LF *= 4;
	$RF *= 4;
	$LR *= 4;
	$RR *= 4;
}

if ($weight == 0 && $LF > 0 && $RF > 0 && $LR > 0 && $RR > 0) {
	$weight = ($LF + $RF + $LR + $RR);
}

if ($weight >0 && $LF > 0 && $RF > 0 && $LR > 0 && $RR > 0) {
	if (($weight) != ($LF + $RF + $LR + $RR)) {
		print "<p><b><font color=blue>Note: there is a discrepancy between the measured weight and the corner weights</font></b>\n";
	}
}

print "<table border=0 cellpading=10 cellspacing=10>\n";

print "<tr>\n";
print "<td align=top>\n";
ShowForm();
print "</td>\n";


print "<td align=center>\n";
CalcDisp();
print "</td>\n";

print "</tr>\n";

print "</table>\n";

print "</center>\n";

#Images();
Trailer();

sub CalcDisp {

return if ($LF <= 0 || $RF <= 0 || $LR <= 0 || $RR <= 0);

$TF = $LF + $RF;
$TR = $LR + $RR;
$TW = $TF + $TR;
$LW = $LF + $LR;
$RW = $RF + $RR;

$LSPCT = ($LW / $TW);
$RSPCT = ($RW / $TW);

$RPCT = ($TR / $TW);
$FPCT = ($TF / $TW);

$DWLFRR = $LF + $RR;
$DWRFLR = $RF + $LR;

$ILF = $FPCT * $LW;
$IRF = $FPCT * $RW;
$ILR = $RPCT * $LW;
$IRR = $RPCT * $RW;

# dump results

#print "<table border = 0>\n";
#print "<tr>\n";
#print "<th>Calculations Based on Existing Corner Weights</th>\n";
#print "</tr>\n";
#print "</table>\n";

print "<table border=1>\n";
print "<tr>\n";
print "<th colspan=3>Ideal Corner Weights</th>\n";
print "</tr>\n";

print "<tr>\n";
print "<td>&nbsp;</td>\n";
print "<th>Left</th>\n";
print "<th>Right</th>\n";
print "</tr>\n";

print "<tr>\n";
print "<th>Front</th>\n";
printf "<td align=center><font color=green><b>%d</font> <font size=-2>(%s%d)</font></td>\n", $ILF, ($LF > $ILF ? "-" : "+"), abs($LF - $ILF) ;
printf "<td align=center><font color=green><b>%d</font> <font size=-2>(%s%d)</font></td>\n", $IRF, 
($RF > $IRF ?  "-" : "+"), abs($RF - $IRF);
print "</tr>\n";

print "<tr>\n";
print "<th>Rear</th>\n";
printf "<td align=center><font color=green><b>%d</font> <font size=-2>(%s%d)</font></td>\n", $ILR, 
($LR > $ILR ?  "-" : "+"), abs($LR - $ILR);
printf "<td align=center><font color=green><b>%d</font> <font size=-2>(%s%d)</font></td>\n", $IRR, 
($RR > $IRR ?  "-" : "+"), abs($RR - $IRR);
print "</tr>\n";

print "</table>\n";

print "<p>\n";
print "<table border=1>\n";
print "<tr>\n";
print "<th colspan=2>Ratios</th>\n";
print "</tr><tr>\n";
print "<td align=center>LF / LR</td>\n";
printf "<td align=center>%.3f\n", $LF / $LR;
print "</tr><tr>\n";
print "<td align=center>RF / RR</td>\n";
printf "<td align=center>%.3f\n", $RF / $RR;
print "</tr><tr>\n";
print "<td colspan=2><font size=-1>These two values should be close to equal</td>\n";
print "</table>\n";

print "<p>\n";
print "<table border=1>\n";

print "<tr>\n";
print "<th colspan=3>Measured Weight Distribution</th>\n";
print "</tr>\n";

print "<tr>\n";
print "<th colspan=2>Total Weight</th>\n";
print "<td align=center>$TW</td>\n";
print "</tr>\n";

print "<tr>\n";
print "<th colspan=3>Front-to-Rear</th>\n";
print "</tr>\n";

print "<tr>\n";
print "<td>Front</td>\n";
print "<td align=center>$TF</td>\n";
printf "<td align=center>%.2f %</td>\n", $FPCT * 100;
print "</tr>\n";

print "<tr>\n";
print "<td>Rear</td>\n";
print "<td align=center>$TR</td>\n";
printf "<td align=center>%.2f %</td>\n", $RPCT * 100;
print "</tr>\n";


print "<tr>\n";
print "<th colspan=3>Side-to-Side</th>\n";
print "</tr>\n";

print "<tr>\n";
print "<td>Left</td>\n";
print "<td align=center>$LW</td>\n";
printf "<td align=center>%.2f %</td>\n", $LSPCT * 100;
print "</tr>\n";

print "<tr>\n";
print "<td>Right</td>\n";
print "<td align=center>$RW</td>\n";
printf "<td align=center>%.2f %</td>\n", $RSPCT * 100;
print "</tr>\n";

print "<tr>\n";
print "<th colspan=3>Diagonal Weight</th>\n";
print "</tr>\n";
print "<tr>\n";
print "<td colspan=2>Left Front / Right Rear</td>\n";
print "<td colspan=2 align=center>$DWLFRR</td>\n";
print "</tr>\n";
print "<tr>\n";
print "<td colspan=2>Right Front / Left Rear</td>\n";
print "<td colspan=2 align=center>$DWRFLR</td>\n";
print "</tr>\n";

print "</table>\n";

$name =~ s/:/ /g;
$notes =~ s/:/ /g;
$car =~ s/:/ /g;
Log("$LF:$RF:$RF:$RR:$name:$car:$notes");
}

sub ShowForm () {
print <<EOF;
<form action=http://rennlight.com/cgi-bin/balance.cgi method=get>

<table border=1>

<tr>
<th colspan=2>Car Details</th>
</tr>

<tr>
<td>Name</td>
<td><input type=text size=40 name="name" value="$name" ></td>
</tr>

<tr>
<td>Car <font size=-2 color=blue>(year, make, model))</td>
<td><input type=text size=40 name="car" value="$car" ></td>
</tr>

<tr>
<td>Notes</td>
<td><input type=text size=50 name="notes" value="$notes" ></td>
</tr>

</table> 


<center>

<p>
<table border=1 width=100%>
<th colspan=3>Measured Corner Weights</th>
<tr>
<td>&nbsp;</td>
<th>Left</th>
<th>Right</th>
</tr>

<tr>
<th>Front</th>
<td align=center><input type=text size=5 name="LF" value=$LF ></td>
<td align=center><input type=text size=5 name="RF" value=$RF ></td>
</tr>

<tr>
<th>Rear</td>
<td align=center><input type=text size=5 name="LR" value=$LR ></td>
<td align=center><input type=text size=5 name="RR" value=$RR ></td>
</tr>

<tr>
<td colspan=3 align=center><input type=checkbox name=multiply>4:1 Scales <font color=blue size=-1>(When using Ruggles scales)</font></td>
</tr>

</table>

<table border=0 >
<tr>
<td colspan=2 align=absmiddle><input type="submit" value="Submit"><input type="reset" value="Clear Form" name="clear"></td>
</tr>
</table>
EOF

}

sub Trailer () {
print "</center>\n";
print "<p><b><a href=http://rennlight.com><< Home</a></b>\n";

print "<p>Technical questions about this web page and/or script can be directed to <a href=mailto:thom\@calweb.com?SUBJECT=Corner%20Balance%20Calculator>Thom Fitzpatrick</a>\n";
print end_html;

}

sub Images () {
my $com;
my $ERR="balance.err";
my $FONT="-font helvetica -fill blue";
my $tmp="/var/www/vhosts/rennlight.com/www/tmp";
my $diag="911-diag.jpg";
my $side="911-side.jpg";
my $rear="911-rear.jpg";
my $top="911-top.jpg";
my $tmp_side="$$-911-side.jpg";
my $tmp_top="$$-911-top.jpg";
my $tmp_rear="$$-911-rear.jpg";
my $tmp_diag="$$-911-diag.jpg";

# top
my $LFT="-draw \"text 0,10 \'$LF\'\"";
my $RFT="-draw \"text 185,10 \'$RF\'\"";
my $LRT="-draw \"text 0,450 \'$LR\'\"";
my $RRT="-draw \"text 180,450 \'$RR\'\"";
$com="convert $FONT $LFT $RFT $RRT $LRT $top $tmp/$tmp_top";
#system ("echo \'$com\' >> $ERR");
#system("$com >> $ERR 2>&1");

# side
my $FRONT="-draw \"text 95,170 \'$TF\'\"";
my $REAR="-draw \"text 325,170 \'$TR\'\"";
$com="convert $FONT $FRONT $REAR $side $tmp/$tmp_side";
#system("$com >> $ERR 2>&1");

# rear
my $LEFT="-draw \"text 25,170 \'$LW\'\"";
my $RIGHT="-draw \"text 167,170 \'$RW\'\"";
my $com="convert $FONT $LEFT $RIGHT $rear $tmp/$tmp_rear";
#print "$com\n";
#system("$com >> $ERR 2>&1");

# diagonal
my $LINE1="-draw \"line 0,0,210,457 \"";
my $LINE2="-draw \"line 0,457,210,0 \"";
my $LFRR="-draw \"text 175,455 \'$DWLFRR\'\"";
my $RFLR="-draw \"text 10,455 \'$DWRFLR\'\"";
my $com="convert $FONT $LINE1 $LINE2 $LFRR $RFLR $diag $tmp/$tmp_diag";
#print "$com\n";
#system("$com >> $ERR 2>&1");

#print "<center>\n";
#print "<table border=0 cellspacing=15>\n";
#print "<tr>\n";
#print "<th colspan=2>Measured Weight Distribution</th>\n";
#print "</tr>\n";
#print "<tr>\n";
#print "<th>Front-to-Rear Distribution<br clear=left><p><img src=http://rennlight.com/tmp/$tmp_side></th>\n";
#print "<th>Side-to-Side Distribution<br clear=left><p><img src=http://rennlight.com/tmp/$tmp_rear></th>\n";
#print "</tr>\n";
#print "<tr>\n";
#print "<th>Per-Corner Distribution<br clear=left><p><img src=http://rennlight.com/tmp/$tmp_top></th>\n";
#print "<th>Diagonal Distribution<br clear=left><p><img src=http://rennlight.com/tmp/$tmp_diag></th>\n";
#print "<tr>\n";
#print "</table>\n";
#
#system ("chmod 666 /var/www/vhosts/rennlight.com/www/tmp/*.jpg");

}

sub Log() {
	my $DATE=`date "+%Y-%m-%d %H:%M"`;
	chomp($DATE);
	
	open(LOG, ">>$LOG") || warn "Couldn't update log file ($LOG) [$!]\n";
	print LOG "$DATE|$ENV{'REMOTE_ADDR'}|@_\n";
	close(LOG);	
}

exit 0;
