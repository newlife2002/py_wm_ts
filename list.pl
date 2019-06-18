#!/usr/bin/perl -w
while (<>) {
  s/\<.*?\>/\n/g;
  print $_;
}
