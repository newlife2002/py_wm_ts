#!/usr/bin/perl -w
my $title='';
my $st = 0;

while (<>) {
  chomp($_);
  if (/^\d+\.\d+$/) {
  	$title = $_;
  	$st = 1;
  } elsif (/^$/) {

  } else {
  	if ($st == 1) {
      s/'/’/g;
      s/ /_/g;
  		s/\?/？/g;
      s/(\/|\\)/-/g;
      s/&amp;/_/g;
  		print $title , $_, "\n";
  		$title = '';
  		$st = 0;
  	} else {
  		print $_, "\n";
  	}
  }
}
