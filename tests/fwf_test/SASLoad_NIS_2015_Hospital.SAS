/*****************************************************************************
* SASload_NIS_2015_Hospital.SAS
* This program will load the NIS_2015_Hospital ASCII File into SAS.
*****************************************************************************/

*** Create SAS informats for missing values ***;
PROC FORMAT;
  INVALUE N2PF
    '-9' = .
    '-8' = .A
    '-6' = .C
    '-5' = .N
    OTHER = (|2.|)
  ;
  INVALUE N3PF
    '-99' = .
    '-88' = .A
    '-66' = .C
    OTHER = (|3.|)
  ;
  INVALUE N4PF
    '-999' = .
    '-888' = .A
    '-666' = .C
    OTHER = (|4.|)
  ;
  INVALUE N4P1F
    '-9.9' = .
    '-8.8' = .A
    '-6.6' = .C
    OTHER = (|4.1|)
  ;
  INVALUE N5PF
    '-9999' = .
    '-8888' = .A
    '-6666' = .C
    OTHER = (|5.|)
  ;
  INVALUE N5P2F
    '-9.99' = .
    '-8.88' = .A
    '-6.66' = .C
    OTHER = (|5.2|)
  ;
  INVALUE N6PF
    '-99999' = .
    '-88888' = .A
    '-66666' = .C
    OTHER = (|6.|)
  ;
  INVALUE N6P2F
    '-99.99' = .
    '-88.88' = .A
    '-66.66' = .C
    OTHER = (|6.2|)
  ;
  INVALUE N7P2F
    '-999.99' = .
    '-888.88' = .A
    '-666.66' = .C
    OTHER = (|7.2|)
  ;
  INVALUE N8PF
    '-9999999' = .
    '-8888888' = .A
    '-6666666' = .C
    OTHER = (|8.|)
  ;
  INVALUE N8P2F
    '-9999.99' = .
    '-8888.88' = .A
    '-6666.66' = .C
    OTHER = (|8.2|)
  ;
  INVALUE N8P4F
    '-99.9999' = .
    '-88.8888' = .A
    '-66.6666' = .C
    OTHER = (|8.4|)
  ;
  INVALUE N10PF
    '-999999999' = .
    '-888888888' = .A
    '-666666666' = .C
    OTHER = (|10.|)
  ;
  INVALUE N10P4F
    '-9999.9999' = .
    '-8888.8888' = .A
    '-6666.6666' = .C
    OTHER = (|10.4|)
  ;
  INVALUE N10P5F
    '-999.99999' = .
    '-888.88888' = .A
    '-666.66666' = .C
    OTHER = (|10.5|)
  ;
  INVALUE DATE10F
    '-999999999' = .
    '-888888888' = .A
    '-666666666' = .C
    OTHER = (|MMDDYY10.|)
  ;
  INVALUE N11P7F
    '-99.9999999' = .
    '-88.8888888' = .A
    '-66.6666666' = .C
    OTHER = (|11.7|)
  ;
  INVALUE N12P2F
    '-99999999.99' = .
    '-88888888.88' = .A
    '-66666666.66' = .C
    OTHER = (|12.2|)
  ;
  INVALUE N12P5F
    '-99999.99999' = .
    '-88888.88888' = .A
    '-66666.66666' = .C
    OTHER = (|12.5|)
  ;
  INVALUE N13PF
    '-999999999999' = .
    '-888888888888' = .A
    '-666666666666' = .C
    OTHER = (|13.|)
  ;
  INVALUE N15P2F
    '-99999999999.99' = .
    '-88888888888.88' = .A
    '-66666666666.66' = .C
    OTHER = (|15.2|)
  ;
RUN;

*** Data Step to load the file ***;
DATA NIS_2015_Hospital; 
INFILE 'NIS_2015_Hospital.ASC' LRECL = 64;

*** Define data element attributes ***;
ATTRIB 
  DISCWT                     LENGTH=8
  LABEL="NIS discharge weight"

  HOSP_BEDSIZE               LENGTH=3            FORMAT=2.
  LABEL="Bed size of hospital (STRATA)"

  HOSP_DIVISION              LENGTH=3            FORMAT=2.
  LABEL="Census Division of hospital (STRATA)"

  HOSP_LOCTEACH              LENGTH=3            FORMAT=2.
  LABEL="Location/teaching status of hospital (STRATA)"

  HOSP_NIS                   LENGTH=4            FORMAT=5.
  LABEL="NIS hospital number"

  HOSP_REGION                LENGTH=3            FORMAT=2.
  LABEL="Region of hospital"

  H_CONTRL                   LENGTH=3            FORMAT=2.
  LABEL="Control/ownership of hospital (STRATA)"

  NIS_STRATUM                LENGTH=4            FORMAT=4.
  LABEL="NIS hospital stratum"

  N_DISC_U                   LENGTH=5
  LABEL="Number of universe discharges in the stratum"

  N_HOSP_U                   LENGTH=3
  LABEL="Number of universe hospitals in the stratum"

  S_DISC_U                   LENGTH=4
  LABEL="Number of sample discharges in the stratum"

  S_HOSP_U                   LENGTH=3
  LABEL="Number of sample hospitals in the stratum"

  TOTAL_DISC                 LENGTH=4
  LABEL="Total number of discharges from this hospital in the NIS"

  YEAR                       LENGTH=3
  LABEL="Calendar year"
  ;

*** Read data elements from the ASCII file ***;
INPUT 
      @1      DISCWT                   N11P7F.
      @12     HOSP_BEDSIZE             N2PF.
      @14     HOSP_DIVISION            N2PF.
      @16     HOSP_LOCTEACH            N2PF.
      @18     HOSP_NIS                 N5PF.
      @23     HOSP_REGION              N2PF.
      @25     H_CONTRL                 N2PF.
      @27     NIS_STRATUM              N4PF.
      @31     N_DISC_U                 N8PF.
      @39     N_HOSP_U                 N4PF.
      @43     S_DISC_U                 N8PF.
      @51     S_HOSP_U                 N4PF.
      @55     TOTAL_DISC               N6PF.
      @61     YEAR                     N4PF.
      ;
RUN;
